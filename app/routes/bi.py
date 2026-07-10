from flask import Blueprint, render_template
from app import db
from app.models import (
    Funcionario, Departamento, Ferias, RegistroPonto,
    FolhaPagamento, Vaga, Candidato, Treinamento, Capacitacao, Avaliacao
)
from datetime import date
from sqlalchemy import func

bi_bp = Blueprint("bi", __name__)


@bi_bp.route("/")
def index():
    hoje = date.today()

    funcionarios_por_dept = db.session.query(
        Departamento.nome, func.count(Funcionario.id)
    ).join(Funcionario, Funcionario.departamento_id == Departamento.id
    ).filter(Funcionario.status == "Ativo"
    ).group_by(Departamento.nome).all()

    ferias_por_mes = db.session.query(
        func.strftime("%m", Ferias.data_inicio), func.count(Ferias.id)
    ).filter(
        Ferias.data_inicio >= f"{hoje.year}-01-01"
    ).group_by(func.strftime("%m", Ferias.data_inicio)).all()

    vagas_por_status = db.session.query(
        Vaga.status, func.count(Vaga.id)
    ).group_by(Vaga.status).all()

    treinamentos_por_status = db.session.query(
        Treinamento.status, func.count(Treinamento.id)
    ).group_by(Treinamento.status).all()

    notas_avaliacao = db.session.query(
        func.avg(Avaliacao.nota_geral)
    ).filter(Avaliacao.status != "Pendente").scalar() or 0

    folha_por_mes = db.session.query(
        func.strftime("%m-%Y", db.func.concat(FolhaPagamento.ano, "-", FolhaPagamento.mes, "-01")),
        func.sum(FolhaPagamento.salario_liquido)
    ).filter(
        FolhaPagamento.status == "Pago"
    ).group_by(func.strftime("%m-%Y", db.func.concat(FolhaPagamento.ano, "-", FolhaPagamento.mes, "-01"))).all()

    return render_template("bi/index.html",
        funcionarios_por_dept=funcionarios_por_dept,
        ferias_por_mes=ferias_por_mes,
        vagas_por_status=vagas_por_status,
        treinamentos_por_status=treinamentos_por_status,
        notas_avaliacao=round(notas_avaliacao, 1),
        folha_por_mes=folha_por_mes
    )
