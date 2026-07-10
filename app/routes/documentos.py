import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import Documento, Funcionario
from datetime import date

documentos_bp = Blueprint("documentos", __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "doc", "docx", "xls", "xlsx"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@documentos_bp.route("/")
def listar():
    documentos = Documento.query.order_by(Documento.data_upload.desc()).all()
    return render_template("documentos/listar.html", documentos=documentos)


@documentos_bp.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        funcionario_id = request.form.get("funcionario_id", type=int)
        titulo = request.form.get("titulo", "").strip()
        categoria = request.form.get("categoria", "Geral")
        descricao = request.form.get("descricao", "").strip()
        arquivo = request.files.get("arquivo")

        if not titulo:
            flash("Titulo e obrigatorio!", "danger")
            return redirect(url_for("documentos.upload"))

        filename = None
        if arquivo and arquivo.filename and allowed_file(arquivo.filename):
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = secure_filename(f"{date.today().strftime('%Y%m%d')}_{arquivo.filename}")
            arquivo.save(os.path.join(UPLOAD_FOLDER, filename))

        d = Documento(
            funcionario_id=funcionario_id, titulo=titulo,
            categoria=categoria, arquivo_path=filename,
            descricao=descricao
        )
        db.session.add(d)
        db.session.commit()
        flash("Documento enviado!", "success")
        return redirect(url_for("documentos.listar"))

    funcionarios = Funcionario.query.filter_by(status="Ativo").all()
    return render_template("documentos/upload.html", funcionarios=funcionarios)


@documentos_bp.route("/download/<int:id>")
def download(id):
    d = Documento.query.get_or_404(id)
    if d.arquivo_path and os.path.exists(os.path.join(UPLOAD_FOLDER, d.arquivo_path)):
        return send_from_directory(UPLOAD_FOLDER, d.arquivo_path, as_attachment=True)
    flash("Arquivo nao encontrado!", "danger")
    return redirect(url_for("documentos.listar"))


@documentos_bp.route("/<int:id>/excluir", methods=["POST"])
def excluir(id):
    d = Documento.query.get_or_404(id)
    if d.arquivo_path:
        path = os.path.join(UPLOAD_FOLDER, d.arquivo_path)
        if os.path.exists(path):
            os.remove(path)
    db.session.delete(d)
    db.session.commit()
    flash("Documento excluido!", "success")
    return redirect(url_for("documentos.listar"))
