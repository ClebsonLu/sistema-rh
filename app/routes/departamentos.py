from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Departamento

departamentos_bp = Blueprint("departamentos", __name__)


@departamentos_bp.route("/")
def listar():
    departamentos = Departamento.query.order_by(Departamento.nome).all()
    return render_template("departamentos/listar.html", departamentos=departamentos)


@departamentos_bp.route("/novo", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        dept = Departamento(
            nome=request.form["nome"],
            descricao=request.form.get("descricao", ""),
        )
        db.session.add(dept)
        db.session.commit()
        flash("Departamento cadastrado com sucesso!", "success")
        return redirect(url_for("departamentos.listar"))
    return render_template("departamentos/cadastrar.html")


@departamentos_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    dept = Departamento.query.get_or_404(id)
    if request.method == "POST":
        dept.nome = request.form["nome"]
        dept.descricao = request.form.get("descricao", "")
        db.session.commit()
        flash("Departamento atualizado com sucesso!", "success")
        return redirect(url_for("departamentos.listar"))
    return render_template("departamentos/cadastrar.html", departamento=dept)


@departamentos_bp.route("/<int:id>/excluir", methods=["POST"])
def excluir(id):
    dept = Departamento.query.get_or_404(id)
    if dept.funcionarios or dept.cargos:
        flash("Nao e possivel excluir departamento com funcionarios ou cargos vinculados.", "danger")
        return redirect(url_for("departamentos.listar"))
    db.session.delete(dept)
    db.session.commit()
    flash("Departamento excluido com sucesso!", "success")
    return redirect(url_for("departamentos.listar"))
