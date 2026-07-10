from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Ferias, Funcionario
from datetime import datetime

ferias_bp = Blueprint("ferias", __name__)


@ferias_bp.route("/")
def listar():
    status_filtro = request.args.get("status", "")
    query = Ferias.query
    if status_filtro:
        query = query.filter_by(status=status_filtro)
    ferias = query.order_by(Ferias.data_solicitacao.desc()).all()
    return render_template("ferias/listar.html", ferias=ferias, status_filtro=status_filtro)


@ferias_bp.route("/novo", methods=["GET", "POST"])
def solicitar():
    if request.method == "POST":
        func_id = int(request.form["funcionario_id"])
        data_inicio = datetime.strptime(request.form["data_inicio"], "%Y-%m-%d").date()
        data_fim = datetime.strptime(request.form["data_fim"], "%Y-%m-%d").date()
        if data_fim < data_inicio:
            flash("Data fim nao pode ser anterior a data inicio.", "danger")
            return redirect(url_for("ferias.solicitar"))
        dias = (data_fim - data_inicio).days + 1
        if dias <= 0:
            flash("Periodo de ferias invalido.", "danger")
            return redirect(url_for("ferias.solicitar"))
        overlap = Ferias.query.filter(
            Ferias.funcionario_id == func_id,
            Ferias.status.in_(["Pendente", "Aprovada"]),
            Ferias.data_inicio <= data_fim,
            Ferias.data_fim >= data_inicio,
        ).first()
        if overlap:
            flash("Ja existe ferias solicitadas/aprovadas para este periodo.", "danger")
            return redirect(url_for("ferias.solicitar"))
        f = Ferias(
            funcionario_id=func_id,
            data_inicio=data_inicio,
            data_fim=data_fim,
            dias=dias,
            motivo=request.form.get("motivo", ""),
        )
        db.session.add(f)
        db.session.commit()
        flash(f"Solicitacao de ferias registrada ({dias} dias).", "success")
        return redirect(url_for("ferias.listar"))
    funcionarios = Funcionario.query.filter_by(status="Ativo").order_by(Funcionario.nome).all()
    return render_template("ferias/solicitar.html", funcionarios=funcionarios)


@ferias_bp.route("/<int:id>/aprovar", methods=["POST"])
def aprovar(id):
    f = Ferias.query.get_or_404(id)
    if f.status != "Pendente":
        flash("Somente ferias pendentes podem ser aprovadas.", "warning")
        return redirect(url_for("ferias.listar"))
    f.status = "Aprovada"
    db.session.commit()
    flash("Ferias aprovadas!", "success")
    return redirect(url_for("ferias.listar"))


@ferias_bp.route("/<int:id>/rejeitar", methods=["POST"])
def rejeitar(id):
    f = Ferias.query.get_or_404(id)
    if f.status != "Pendente":
        flash("Somente ferias pendentes podem ser rejeitadas.", "warning")
        return redirect(url_for("ferias.listar"))
    f.status = "Rejeitada"
    db.session.commit()
    flash("Ferias rejeitadas.", "warning")
    return redirect(url_for("ferias.listar"))
