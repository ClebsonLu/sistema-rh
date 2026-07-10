from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Treinamento, Capacitacao, Funcionario

treinamentos_bp = Blueprint("treinamentos", __name__)


@treinamentos_bp.route("/")
def listar():
    treinamentos = Treinamento.query.order_by(Treinamento.data_inicio.desc()).all()
    total_inscritos = sum(len(t.capacitacoes) for t in treinamentos)
    return render_template("treinamentos/listar.html", treinamentos=treinamentos, total_inscritos=total_inscritos)


@treinamentos_bp.route("/novo", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        carga = request.form.get("carga_horaria", 0, type=int)
        data_inicio = request.form.get("data_inicio")
        data_fim = request.form.get("data_fim") or None
        local = request.form.get("local", "").strip()
        vagas = request.form.get("vagas_max", 30, type=int)

        if not titulo:
            flash("Titulo e obrigatorio!", "danger")
            return redirect(url_for("treinamentos.cadastrar"))

        from datetime import datetime
        t = Treinamento(
            titulo=titulo, descricao=descricao, carga_horaria=carga,
            data_inicio=datetime.strptime(data_inicio, "%Y-%m-%d").date(),
            data_fim=datetime.strptime(data_fim, "%Y-%m-%d").date() if data_fim else None,
            local=local, vagas_max=vagas
        )
        db.session.add(t)
        db.session.commit()
        flash("Treinamento cadastrado!", "success")
        return redirect(url_for("treinamentos.listar"))

    return render_template("treinamentos/cadastrar.html")


@treinamentos_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    t = Treinamento.query.get_or_404(id)
    if request.method == "POST":
        t.titulo = request.form.get("titulo", t.titulo).strip()
        t.descricao = request.form.get("descricao", t.descricao).strip()
        t.carga_horaria = request.form.get("carga_horaria", t.carga_horaria, type=int)
        t.local = request.form.get("local", t.local).strip()
        t.vagas_max = request.form.get("vagas_max", t.vagas_max, type=int)
        t.status = request.form.get("status", t.status)
        db.session.commit()
        flash("Treinamento atualizado!", "success")
        return redirect(url_for("treinamentos.listar"))

    return render_template("treinamentos/cadastrar.html", treinamento=t)


@treinamentos_bp.route("/<int:id>/excluir", methods=["POST"])
def excluir(id):
    t = Treinamento.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    flash("Treinamento excluido!", "success")
    return redirect(url_for("treinamentos.listar"))


@treinamentos_bp.route("/<int:id>/inscrever", methods=["GET", "POST"])
def inscrever(id):
    t = Treinamento.query.get_or_404(id)
    if request.method == "POST":
        funcionario_id = request.form.get("funcionario_id", type=int)
        existente = Capacitacao.query.filter_by(
            funcionario_id=funcionario_id, treinamento_id=id
        ).first()
        if existente:
            flash("Funcionario ja inscrito!", "warning")
            return redirect(url_for("treinamentos.inscrever", id=id))

        c = Capacitacao(funcionario_id=funcionario_id, treinamento_id=id)
        db.session.add(c)
        db.session.commit()
        flash("Inscricao realizada!", "success")
        return redirect(url_for("treinamentos.detalhes", id=id))

    inscritos = Capacitacao.query.filter_by(treinamento_id=id).all()
    ids_inscritos = [c.funcionario_id for c in inscritos]
    funcionarios = Funcionario.query.filter(
        Funcionario.status == "Ativo",
        ~Funcionario.id.in_(ids_inscritos)
    ).all()
    return render_template("treinamentos/inscrever.html", treinamento=t, funcionarios=funcionarios)


@treinamentos_bp.route("/<int:id>")
def detalhes(id):
    t = Treinamento.query.get_or_404(id)
    capacitacoes = Capacitacao.query.filter_by(treinamento_id=id).all()
    return render_template("treinamentos/detalhes.html", treinamento=t, capacitacoes=capacitacoes)


@treinamentos_bp.route("/<int:id>/nota", methods=["POST"])
def registrar_nota(id):
    c = Capacitacao.query.get_or_404(id)
    c.nota_final = request.form.get("nota", type=float)
    c.certificado = request.form.get("certificado") == "on"
    if c.nota_final and c.nota_final >= 7:
        c.status = "Aprovado"
    else:
        c.status = "Reprovado"
    db.session.commit()
    flash("Nota registrada!", "success")
    return redirect(url_for("treinamentos.detalhes", id=c.treinamento_id))
