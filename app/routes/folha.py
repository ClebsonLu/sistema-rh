from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import FolhaPagamento, Funcionario, FuncionarioBeneficio
from datetime import date

folha_bp = Blueprint("folha", __name__)


@folha_bp.route("/")
def listar():
    mes = request.args.get("mes", date.today().month, type=int)
    ano = request.args.get("ano", date.today().year, type=int)
    registros = FolhaPagamento.query.filter_by(mes=mes, ano=ano).all()
    total_pago = sum(r.salario_liquido for r in registros if r.status == "Pago")
    return render_template("folha/listar.html", registros=registros, mes=mes, ano=ano, total_pago=total_pago)


@folha_bp.route("/gerar", methods=["POST"])
def gerar():
    mes = request.form.get("mes", date.today().month, type=int)
    ano = request.form.get("ano", date.today().year, type=int)

    existentes = FolhaPagamento.query.filter_by(mes=mes, ano=ano).count()
    if existentes > 0:
        flash("Folha ja gerada para este periodo!", "warning")
        return redirect(url_for("folha.listar", mes=mes, ano=ano))

    funcionarios = Funcionario.query.filter_by(status="Ativo").all()
    for func in funcionarios:
        beneficios = FuncionarioBeneficio.query.filter_by(
            funcionario_id=func.id, status="Ativo"
        ).all()
        total_beneficios = sum(b.valor for b in beneficios)
        descontos = func.salario * 0.11
        liquido = func.salario + total_beneficios - descontos

        f = FolhaPagamento(
            funcionario_id=func.id,
            mes=mes,
            ano=ano,
            salario_bruto=func.salario,
            total_beneficios=total_beneficios,
            total_descontos=descontos,
            salario_liquido=liquido,
            status="Pendente"
        )
        db.session.add(f)

    db.session.commit()
    flash(f"Folha de {len(funcionarios)} funcionarios gerada!", "success")
    return redirect(url_for("folha.listar", mes=mes, ano=ano))


@folha_bp.route("/<int:id>/pagar", methods=["POST"])
def pagar(id):
    f = FolhaPagamento.query.get_or_404(id)
    f.status = "Pago"
    f.data_pagamento = date.today()
    db.session.commit()
    flash("Pagamento registrado!", "success")
    return redirect(url_for("folha.listar", mes=f.mes, ano=f.ano))


@folha_bp.route("/<int:id>/cancelar", methods=["POST"])
def cancelar(id):
    f = FolhaPagamento.query.get_or_404(id)
    f.status = "Cancelado"
    db.session.commit()
    flash("Pagamento cancelado!", "success")
    return redirect(url_for("folha.listar", mes=f.mes, ano=f.ano))
