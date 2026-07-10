from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Vaga, Candidato, Departamento, Cargo

recrutamento_bp = Blueprint("recrutamento", __name__)


@recrutamento_bp.route("/")
def listar_vagas():
    vagas = Vaga.query.order_by(Vaga.data_abertura.desc()).all()
    total_candidatos = sum(len(v.candidatos) for v in vagas)
    return render_template("recrutamento/listar_vagas.html", vagas=vagas, total_candidatos=total_candidatos)


@recrutamento_bp.route("/vaga/nova", methods=["GET", "POST"])
def cadastrar_vaga():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        departamento_id = request.form.get("departamento_id", type=int)
        cargo_id = request.form.get("cargo_id", type=int)
        salario = request.form.get("salario_oferecido", 0, type=float)

        if not titulo:
            flash("Titulo e obrigatorio!", "danger")
            return redirect(url_for("recrutamento.cadastrar_vaga"))

        v = Vaga(
            titulo=titulo, descricao=descricao,
            departamento_id=departamento_id, cargo_id=cargo_id,
            salario_oferecido=salario
        )
        db.session.add(v)
        db.session.commit()
        flash("Vaga criada com sucesso!", "success")
        return redirect(url_for("recrutamento.listar_vagas"))

    departamentos = Departamento.query.all()
    cargos = Cargo.query.all()
    return render_template("recrutamento/cadastrar_vaga.html", departamentos=departamentos, cargos=cargos)


@recrutamento_bp.route("/vaga/<int:id>")
def detalhes_vaga(id):
    vaga = Vaga.query.get_or_404(id)
    return render_template("recrutamento/detalhes_vaga.html", vaga=vaga)


@recrutamento_bp.route("/vaga/<int:id>/fechar", methods=["POST"])
def fechar_vaga(id):
    vaga = Vaga.query.get_or_404(id)
    vaga.status = "Fechada"
    db.session.commit()
    flash("Vaga fechada!", "success")
    return redirect(url_for("recrutamento.listar_vagas"))


@recrutamento_bp.route("/candidato/novo", methods=["GET", "POST"])
def cadastrar_candidato():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()
        vaga_id = request.form.get("vaga_id", type=int)
        observacoes = request.form.get("observacoes", "").strip()

        if not nome:
            flash("Nome e obrigatorio!", "danger")
            return redirect(url_for("recrutamento.cadastrar_candidato"))

        c = Candidato(
            nome=nome, email=email, telefone=telefone,
            vaga_id=vaga_id, observacoes=observacoes
        )
        db.session.add(c)
        db.session.commit()
        flash("Candidato cadastrado!", "success")
        return redirect(url_for("recrutamento.listar_candidatos"))

    vagas = Vaga.query.filter_by(status="Aberta").all()
    return render_template("recrutamento/cadastrar_candidato.html", vagas=vagas)


@recrutamento_bp.route("/candidatos")
def listar_candidatos():
    candidatos = Candidato.query.order_by(Candidato.data_candidatura.desc()).all()
    return render_template("recrutamento/listar_candidatos.html", candidatos=candidatos)


@recrutamento_bp.route("/candidato/<int:id>/status", methods=["POST"])
def status_candidato(id):
    candidato = Candidato.query.get_or_404(id)
    novo_status = request.form.get("status", candidato.status)
    candidato.status = novo_status
    db.session.commit()
    flash(f"Candidato atualizado para: {novo_status}", "success")
    return redirect(url_for("recrutamento.listar_candidatos"))
