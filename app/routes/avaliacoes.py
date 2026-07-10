from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Avaliacao, Funcionario

avaliacoes_bp = Blueprint("avaliacoes", __name__)


@avaliacoes_bp.route("/")
def listar():
    avaliacoes = Avaliacao.query.order_by(Avaliacao.data_avaliacao.desc()).all()
    return render_template("avaliacoes/listar.html", avaliacoes=avaliacoes)


@avaliacoes_bp.route("/nova", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        funcionario_id = request.form.get("funcionario_id", type=int)
        avaliador_id = request.form.get("avaliador_id", type=int)
        periodo = request.form.get("periodo", "").strip()
        nota = request.form.get("nota_geral", 0, type=float)
        competencias = request.form.get("competencias", "").strip()
        observacoes = request.form.get("observacoes", "").strip()

        if not periodo:
            flash("Periodo e obrigatorio!", "danger")
            return redirect(url_for("avaliacoes.cadastrar"))

        a = Avaliacao(
            funcionario_id=funcionario_id, avaliador_id=avaliador_id,
            periodo=periodo, nota_geral=nota,
            competencias=competencias, observacoes=observacoes
        )
        db.session.add(a)
        db.session.commit()
        flash("Avaliacao registrada!", "success")
        return redirect(url_for("avaliacoes.listar"))

    funcionarios = Funcionario.query.filter_by(status="Ativo").all()
    return render_template("avaliacoes/cadastrar.html", funcionarios=funcionarios)


@avaliacoes_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    a = Avaliacao.query.get_or_404(id)
    if request.method == "POST":
        a.nota_geral = request.form.get("nota_geral", a.nota_geral, type=float)
        a.competencias = request.form.get("competencias", a.competencias).strip()
        a.observacoes = request.form.get("observacoes", a.observacoes).strip()
        a.status = request.form.get("status", a.status)
        db.session.commit()
        flash("Avaliacao atualizada!", "success")
        return redirect(url_for("avaliacoes.listar"))

    funcionarios = Funcionario.query.filter_by(status="Ativo").all()
    return render_template("avaliacoes/cadastrar.html", avaliacao=a, funcionarios=funcionarios)


@avaliacoes_bp.route("/<int:id>/excluir", methods=["POST"])
def excluir(id):
    a = Avaliacao.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    flash("Avaliacao excluida!", "success")
    return redirect(url_for("avaliacoes.listar"))


@avaliacoes_bp.route("/<int:id>")
def detalhes(id):
    a = Avaliacao.query.get_or_404(id)
    return render_template("avaliacoes/detalhes.html", avaliacao=a)
