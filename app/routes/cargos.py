from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Cargo, Departamento

cargos_bp = Blueprint("cargos", __name__)


@cargos_bp.route("/")
def listar():
    cargos = Cargo.query.order_by(Cargo.nome).all()
    departamentos = Departamento.query.order_by(Departamento.nome).all()
    return render_template("cargos/listar.html", cargos=cargos, departamentos=departamentos)


@cargos_bp.route("/novo", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        c = Cargo(
            nome=request.form["nome"],
            descricao=request.form.get("descricao", ""),
            salario_base=float(request.form.get("salario_base", 0)),
            departamento_id=int(request.form["departamento_id"]),
        )
        db.session.add(c)
        db.session.commit()
        flash("Cargo cadastrado com sucesso!", "success")
        return redirect(url_for("cargos.listar"))
    departamentos = Departamento.query.order_by(Departamento.nome).all()
    return render_template("cargos/cadastrar.html", departamentos=departamentos)


@cargos_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    c = Cargo.query.get_or_404(id)
    if request.method == "POST":
        c.nome = request.form["nome"]
        c.descricao = request.form.get("descricao", "")
        c.salario_base = float(request.form.get("salario_base", 0))
        c.departamento_id = int(request.form["departamento_id"])
        db.session.commit()
        flash("Cargo atualizado com sucesso!", "success")
        return redirect(url_for("cargos.listar"))
    departamentos = Departamento.query.order_by(Departamento.nome).all()
    return render_template("cargos/cadastrar.html", cargo=c, departamentos=departamentos)


@cargos_bp.route("/<int:id>/excluir", methods=["POST"])
def excluir(id):
    c = Cargo.query.get_or_404(id)
    if c.funcionarios:
        flash("Nao e possivel excluir cargo com funcionarios vinculados.", "danger")
        return redirect(url_for("cargos.listar"))
    db.session.delete(c)
    db.session.commit()
    flash("Cargo excluido com sucesso!", "success")
    return redirect(url_for("cargos.listar"))
