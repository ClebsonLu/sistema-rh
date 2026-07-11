from flask import Blueprint, render_template
from app import db
from app.models import (
    Funcionario, Ferias, RegistroPonto, Departamento,
    Beneficio, Vaga, Treinamento, Capacitacao, Avaliacao, Documento,
    FolhaPagamento
)
from datetime import date
from sqlalchemy import func, extract

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    total_funcionarios = Funcionario.query.filter_by(status="Ativo").count()
    total_inativos = Funcionario.query.filter_by(status="Inativo").count()
    ferias_pendentes = Ferias.query.filter_by(status="Pendente").count()
    ferias_aprovadas = Ferias.query.filter_by(status="Aprovada").count()

    hoje = date.today()
    primeiro_dia_mes = hoje.replace(day=1)

    is_pg = db.engine.dialect.name == 'postgresql'
    if is_pg:
        horas_mes = db.session.query(
            func.sum(
                extract('epoch', RegistroPonto.saida - RegistroPonto.entrada) / 3600.0
            )
        ).filter(
            RegistroPonto.data >= primeiro_dia_mes,
            RegistroPonto.data <= hoje,
            RegistroPonto.saida.isnot(None)
        ).scalar() or 0
    else:
        horas_mes = db.session.query(
            func.sum(
                func.julianday(RegistroPonto.saida) - func.julianday(RegistroPonto.entrada)
            )
        ).filter(
            RegistroPonto.data >= primeiro_dia_mes,
            RegistroPonto.data <= hoje,
            RegistroPonto.saida.isnot(None)
        ).scalar() or 0
        horas_mes = horas_mes * 24

    departamentos = Departamento.query.join(Funcionario, Funcionario.departamento_id == Departamento.id
    ).filter(Funcionario.status == "Ativo"
    ).group_by(Departamento.id).all()

    aniversariantes = Funcionario.query.filter(
        Funcionario.status == "Ativo",
        func.extract("month", Funcionario.data_nascimento) == hoje.month
    ).all()

    vagas_abertas = Vaga.query.filter_by(status="Aberta").count()
    treinamentos_ativos = Treinamento.query.filter_by(status="Aberto").count()
    documentos_total = Documento.query.count()
    avaliacoes_pendentes = Avaliacao.query.filter_by(status="Pendente").count()

    funcionarios_por_dept = db.session.query(
        Departamento.nome, func.count(Funcionario.id)
    ).join(Funcionario, Funcionario.departamento_id == Departamento.id
    ).filter(Funcionario.status == "Ativo"
    ).group_by(Departamento.nome).all()

    folha_mes = db.session.query(
        func.sum(FolhaPagamento.salario_liquido)
    ).filter(
        FolhaPagamento.mes == hoje.month,
        FolhaPagamento.ano == hoje.year,
        FolhaPagamento.status == "Pago"
    ).scalar() or 0

    return render_template(
        "dashboard.html",
        total_funcionarios=total_funcionarios,
        total_inativos=total_inativos,
        ferias_pendentes=ferias_pendentes,
        ferias_aprovadas=ferias_aprovadas,
        horas_mes=round(horas_mes, 1),
        departamentos=departamentos,
        aniversariantes=aniversariantes,
        vagas_abertas=vagas_abertas,
        treinamentos_ativos=treinamentos_ativos,
        documentos_total=documentos_total,
        avaliacoes_pendentes=avaliacoes_pendentes,
        funcionarios_por_dept=funcionarios_por_dept,
        folha_mes=round(folha_mes, 2),
    )
