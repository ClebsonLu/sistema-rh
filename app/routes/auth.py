from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User


auth_bp = Blueprint("auth", __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Acesse sua conta para continuar.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


def check_login():
    if "user_id" not in session:
        from flask import request as req
        if req.endpoint and req.endpoint.startswith("auth."):
            return None
        if req.endpoint and req.endpoint.startswith("static"):
            return None
        return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["nome_completo"] = user.nome_completo
            session["is_admin"] = user.is_admin
            flash(f"Bem-vindo, {user.nome_completo or user.username}!", "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash("Usuario ou senha invalidos.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/change-password", methods=["GET", "POST"])
def change_password():
    user = User.query.get(session["user_id"])
    
    if request.method == "POST":
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not current_password or not new_password:
            flash("Preencha todos os campos.", "danger")
            return redirect(url_for("auth.change_password"))

        if not user.check_password(current_password):
            flash("Senha atual incorreta.", "danger")
            return redirect(url_for("auth.change_password"))

        if new_password != confirm_password:
            flash("As novas senhas nao coincidem.", "danger")
            return redirect(url_for("auth.change_password"))

        if len(new_password) < 6:
            flash("A nova senha deve ter pelo menos 6 caracteres.", "warning")
            return redirect(url_for("auth.change_password"))

        user.set_password(new_password)
        db.session.commit()
        flash("Senha alterada com sucesso!", "success")
        return redirect(url_for("dashboard.index"))

    return render_template("auth/change_password.html")