from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Beneficio, FuncionarioBeneficio, Funcionario

beneficios_bp = Blueprint("beneficios", __name__)


@beneficios_bp.route("/")
def listar():
    beneficios = Beneficio.query.all()
    vinculados = FuncionarioBeneficio.query.filter_by(status="Ativo").all()
    return render_template("beneficios/listar.html", beneficios=beneficios, vinculados=vinculados)


@beneficios_bp.route("/novo", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        tipo = request.form.get("tipo", "Outro")
        valor = request.form.get("valor_padrao", 0, type=float)
        descricao = request.form.get("descricao", "").strip()

        if not nome:
            flash("Nome e obrigatorio.", "danger")
            return redirect(url_for("beneficios.cadastrar"))

        b = Beneficio(nome=nome, tipo=tipo, valor_padrao=valor, descricao=descricao)
        db.session.add(b)
        db.session.commit()
        flash("Beneficio cadastrado com sucesso!", "success")
        return redirect(url_for("beneficios.listar"))

    return render_template("beneficios/cadastrar.html")


@beneficios_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    b = Beneficio.query.get_or_404(id)
    if request.method == "POST":
        b.nome = request.form.get("nome", b.nome).strip()
        b.tipo = request.form.get("tipo", b.tipo)
        b.valor_padrao = request.form.get("valor_padrao", b.valor_padrao, type=float)
        b.descricao = request.form.get("descricao", b.descricao).strip()
        db.session.commit()
        flash("Beneficio atualizado!", "success")
        return redirect(url_for("beneficios.listar"))

    return render_template("beneficios/cadastrar.html", beneficio=b)


@beneficios_bp.route("/<int:id>/excluir", methods=["POST"])
def excluir(id):
    b = Beneficio.query.get_or_404(id)
    db.session.delete(b)
    db.session.commit()
    flash("Beneficio excluido!", "success")
    return redirect(url_for("beneficios.listar"))


@beneficios_bp.route("/vincular", methods=["GET", "POST"])
def vincular():
    if request.method == "POST":
        funcionario_id = request.form.get("funcionario_id", type=int)
        beneficio_id = request.form.get("beneficio_id", type=int)
        valor = request.form.get("valor", 0, type=float)

        v = FuncionarioBeneficio(
            funcionario_id=funcionario_id,
            beneficio_id=beneficio_id,
            valor=valor
        )
        db.session.add(v)
        db.session.commit()
        flash("Beneficio vinculado ao funcionario!", "success")
        return redirect(url_for("beneficios.listar"))

    funcionarios = Funcionario.query.filter_by(status="Ativo").all()
    beneficios = Beneficio.query.all()
    return render_template("beneficios/vincular.html", funcionarios=funcionarios, beneficios=beneficios)


@beneficios_bp.route("/desvincular/<int:id>", methods=["POST"])
def desvincular(id):
    v = FuncionarioBeneficio.query.get_or_404(id)
    v.status = "Inativo"
    db.session.commit()
    flash("Vinculo removido!", "success")
    return redirect(url_for("beneficios.listar"))
