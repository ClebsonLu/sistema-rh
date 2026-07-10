from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import RegistroPonto, Funcionario
from sqlalchemy import func
from datetime import datetime, date

ponto_bp = Blueprint("ponto", __name__)


@ponto_bp.route("/")
def historico():
    funcionario_id = request.args.get("funcionario_id", 0, type=int)
    mes = request.args.get("mes", date.today().month, type=int)
    ano = request.args.get("ano", date.today().year, type=int)
    query = RegistroPonto.query
    if funcionario_id:
        query = query.filter_by(funcionario_id=funcionario_id)
    registros = query.filter(
        func.extract("month", RegistroPonto.data) == mes,
        func.extract("year", RegistroPonto.data) == ano,
    ).order_by(RegistroPonto.data.desc()).all()
    funcionarios = Funcionario.query.filter_by(status="Ativo").order_by(Funcionario.nome).all()
    return render_template("ponto/historico.html", registros=registros, funcionarios=funcionarios, funcionario_id=funcionario_id, mes=mes, ano=ano)


@ponto_bp.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        func_id = int(request.form["funcionario_id"])
        hoje = date.today()
        registro = RegistroPonto.query.filter_by(funcionario_id=func_id, data=hoje).first()
        if registro and registro.saida is None:
            registro.saida = datetime.now()
            registro.observacao = request.form.get("observacao", "")
            db.session.commit()
            flash("Saida registrada!", "success")
        elif registro and registro.saida is not None:
            flash("Ponto ja registrado para hoje.", "warning")
        else:
            registro = RegistroPonto(
                funcionario_id=func_id,
                data=hoje,
                entrada=datetime.now(),
                observacao=request.form.get("observacao", ""),
            )
            db.session.add(registro)
            db.session.commit()
            flash("Entrada registrada!", "success")
        return redirect(url_for("ponto.registrar"))
    funcionarios = Funcionario.query.filter_by(status="Ativo").order_by(Funcionario.nome).all()
    return render_template("ponto/registrar.html", funcionarios=funcionarios)
