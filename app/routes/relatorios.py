from flask import Blueprint, render_template, request, send_file
from app import db
from app.models import Funcionario, Ferias, RegistroPonto
from datetime import date
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from openpyxl import Workbook

relatorios_bp = Blueprint("relatorios", __name__)


@relatorios_bp.route("/")
def index():
    return render_template("relatorios/index.html")


@relatorios_bp.route("/funcionarios")
def funcionarios_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Relacao de Funcionarios", styles["Title"]))
    elements.append(Spacer(1, 20))

    dados = [["Nome", "CPF", "Departamento", "Cargo", "Salario", "Status"]]
    for f in Funcionario.query.order_by(Funcionario.nome).all():
        dados.append([
            f.nome, f.cpf,
            f.departamento.nome if f.departamento else "-",
            f.cargo.nome if f.cargo else "-",
            f"R$ {f.salario:,.2f}", f.status,
        ])

    t = Table(dados, colWidths=[100, 80, 90, 80, 70, 50])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#ecf0f1")]),
    ]))
    elements.append(t)
    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, mimetype="application/pdf", as_attachment=True, download_name="funcionarios.pdf")


@relatorios_bp.route("/folha")
def folha_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Folha de Pagamento"
    ws.append(["Nome", "CPF", "Departamento", "Cargo", "Salario"])
    for f in Funcionario.query.filter_by(status="Ativo").order_by(Funcionario.nome).all():
        ws.append([
            f.nome, f.cpf,
            f.departamento.nome if f.departamento else "-",
            f.cargo.nome if f.cargo else "-",
            f.salario,
        ])
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return send_file(buffer, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                     as_attachment=True, download_name="folha_pagamento.xlsx")


@relatorios_bp.route("/ponto")
def ponto_pdf():
    func_id = request.args.get("funcionario_id", 0, type=int)
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Relatorio de Ponto", styles["Title"]))
    elements.append(Spacer(1, 20))

    query = RegistroPonto.query
    if func_id:
        func = Funcionario.query.get_or_404(func_id)
        query = query.filter_by(funcionario_id=func_id)
        elements.append(Paragraph(f"Funcionario: {func.nome}", styles["Heading2"]))

    registros = query.order_by(RegistroPonto.data.desc()).limit(100).all()

    dados = [["Data", "Entrada", "Saida", "Observacao"]]
    for r in registros:
        entrada = r.entrada.strftime("%H:%M") if r.entrada else "-"
        saida = r.saida.strftime("%H:%M") if r.saida else "-"
        dados.append([str(r.data), entrada, saida, r.observacao or "-"])

    t = Table(dados, colWidths=[80, 70, 70, 150])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#ecf0f1")]),
    ]))
    elements.append(t)
    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, mimetype="application/pdf", as_attachment=True, download_name="ponto.pdf")
