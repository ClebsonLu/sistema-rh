from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Funcionario, Cargo, Departamento

funcionarios_bp = Blueprint("funcionarios", __name__)


@funcionarios_bp.route("/")
def listar():
    busca = request.args.get("busca", "")
    page = request.args.get("page", 1, type=int)
    query = Funcionario.query
    if busca:
        query = query.filter(Funcionario.nome.ilike(f"%{busca}%"))
    pagination = query.order_by(Funcionario.nome).paginate(page=page, per_page=10)
    return render_template("funcionarios/listar.html", funcionarios=pagination.items, pagination=pagination, busca=busca)


@funcionarios_bp.route("/novo", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        cpf = request.form.get("cpf", "").strip()
        if not request.form.get("nome", "").strip():
            flash("Nome e obrigatorio.", "danger")
            return redirect(url_for("funcionarios.cadastrar"))
        if not cpf:
            flash("CPF e obrigatorio.", "danger")
            return redirect(url_for("funcionarios.cadastrar"))
        existing = Funcionario.query.filter_by(cpf=cpf).first()
        if existing:
            flash("CPF ja cadastrado para outro funcionario.", "danger")
            return redirect(url_for("funcionarios.cadastrar"))
        func = Funcionario(
            nome=request.form["nome"].strip(),
            cpf=cpf,
            email=request.form.get("email", "").strip(),
            telefone=request.form.get("telefone", "").strip(),
            data_nascimento=request.form.get("data_nascimento") or None,
            data_admissao=request.form["data_admissao"],
            cargo_id=int(request.form["cargo_id"]),
            departamento_id=int(request.form["departamento_id"]),
            salario=float(request.form.get("salario", 0)),
            status=request.form.get("status", "Ativo"),
        )
        db.session.add(func)
        db.session.commit()
        flash("Funcionario cadastrado com sucesso!", "success")
        return redirect(url_for("funcionarios.listar"))
    cargos = Cargo.query.all()
    departamentos = Departamento.query.all()
    return render_template("funcionarios/cadastrar.html", cargos=cargos, departamentos=departamentos)


@funcionarios_bp.route("/<int:id>")
def detalhes(id):
    func = Funcionario.query.get_or_404(id)
    return render_template("funcionarios/detalhes.html", funcionario=func)


@funcionarios_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    func = Funcionario.query.get_or_404(id)
    if request.method == "POST":
        cpf = request.form.get("cpf", "").strip()
        existing = Funcionario.query.filter(Funcionario.cpf == cpf, Funcionario.id != id).first()
        if existing:
            flash("CPF ja cadastrado para outro funcionario.", "danger")
            return redirect(url_for("funcionarios.editar", id=id))
        func.nome = request.form["nome"].strip()
        func.cpf = cpf
        func.email = request.form.get("email", "")
        func.telefone = request.form.get("telefone", "")
        func.data_nascimento = request.form.get("data_nascimento") or None
        func.data_admissao = request.form["data_admissao"]
        func.cargo_id = int(request.form["cargo_id"])
        func.departamento_id = int(request.form["departamento_id"])
        func.salario = float(request.form.get("salario", 0))
        func.status = request.form.get("status", "Ativo")
        db.session.commit()
        flash("Funcionario atualizado com sucesso!", "success")
        return redirect(url_for("funcionarios.detalhes", id=func.id))
    cargos = Cargo.query.all()
    departamentos = Departamento.query.all()
    return render_template("funcionarios/editar.html", funcionario=func, cargos=cargos, departamentos=departamentos)


@funcionarios_bp.route("/<int:id>/excluir", methods=["POST"])
def excluir(id):
    func = Funcionario.query.get_or_404(id)
    func.status = "Inativo"
    db.session.commit()
    flash("Funcionario desativado com sucesso!", "success")
    return redirect(url_for("funcionarios.listar"))
