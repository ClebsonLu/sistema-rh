import os
from flask import Flask, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app():
    env = os.environ.get("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config.get(env, config["default"]))

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from app.routes.auth import auth_bp, login_required, check_login
    from app.routes.dashboard import dashboard_bp
    from app.routes.funcionarios import funcionarios_bp
    from app.routes.departamentos import departamentos_bp
    from app.routes.ferias import ferias_bp
    from app.routes.ponto import ponto_bp
    from app.routes.relatorios import relatorios_bp
    from app.routes.cargos import cargos_bp
    from app.routes.beneficios import beneficios_bp
    from app.routes.folha import folha_bp
    from app.routes.recrutamento import recrutamento_bp
    from app.routes.treinamentos import treinamentos_bp
    from app.routes.avaliacoes import avaliacoes_bp
    from app.routes.documentos import documentos_bp
    from app.routes.bi import bi_bp

    app.register_blueprint(auth_bp)

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(funcionarios_bp, url_prefix="/funcionarios")
    app.register_blueprint(departamentos_bp, url_prefix="/departamentos")
    app.register_blueprint(ferias_bp, url_prefix="/ferias")
    app.register_blueprint(ponto_bp, url_prefix="/ponto")
    app.register_blueprint(relatorios_bp, url_prefix="/relatorios")
    app.register_blueprint(cargos_bp, url_prefix="/cargos")
    app.register_blueprint(beneficios_bp, url_prefix="/beneficios")
    app.register_blueprint(folha_bp, url_prefix="/folha")
    app.register_blueprint(recrutamento_bp, url_prefix="/recrutamento")
    app.register_blueprint(treinamentos_bp, url_prefix="/treinamentos")
    app.register_blueprint(avaliacoes_bp, url_prefix="/avaliacoes")
    app.register_blueprint(documentos_bp, url_prefix="/documentos")
    app.register_blueprint(bi_bp, url_prefix="/bi")

    @app.before_request
    def before_request_handler():
        return check_login()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)