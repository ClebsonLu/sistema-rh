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
        from app.models import (
            User, Departamento, Cargo, Funcionario, Ferias, RegistroPonto,
            Beneficio, FuncionarioBeneficio, FolhaPagamento,
            Vaga, Candidato, Treinamento, Capacitacao, Avaliacao, Documento,
        )
        try:
            db.create_all()
        except Exception:
            db.session.rollback()

        try:
            if not User.query.first():
                users = [
                    User(username="admin", nome_completo="Administrador", is_admin=True),
                    User(username="rh", nome_completo="Usuario RH", is_admin=False),
                ]
                for u in users:
                    u.set_password("123456")
                    db.session.add(u)
                db.session.commit()
        except Exception:
            db.session.rollback()

        try:
            if not Departamento.query.first():
                _seed_sample_data()
        except Exception:
            db.session.rollback()

    from app.routes.auth import auth_bp, check_login
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


def _seed_sample_data():
    from app.models import (
        Departamento, Cargo, Funcionario, Ferias, RegistroPonto,
        Beneficio, FuncionarioBeneficio, FolhaPagamento,
        Vaga, Candidato, Treinamento
    )
    from datetime import date, datetime, timedelta

    today = date.today()

    deps = [
        Departamento(nome="Recursos Humanos", descricao="Gestao de pessoas"),
        Departamento(nome="Tecnologia da Informacao", descricao="TI e Desenvolvimento"),
        Departamento(nome="Financeiro", descricao="Contabilidade e financas"),
        Departamento(nome="Comercial", descricao="Vendas e relacoes"),
        Departamento(nome="Administrativo", descricao="Administracao geral"),
    ]
    for d in deps:
        db.session.add(d)
    db.session.commit()

    cargos_dados = [
        ("Analista de RH", 4500, "Recursos Humanos"),
        ("Desenvolvedor Python", 8500, "Tecnologia da Informacao"),
        ("Desenvolvedor Frontend", 7500, "Tecnologia da Informacao"),
        ("Contador", 6000, "Financeiro"),
        ("Analista Financeiro", 5000, "Financeiro"),
        ("Vendedor", 3500, "Comercial"),
        ("Gerente Comercial", 8500, "Comercial"),
        ("Assistente Administrativo", 3200, "Administrativo"),
    ]
    for nome, sal, dept_nome in cargos_dados:
        dept = Departamento.query.filter_by(nome=dept_nome).first()
        if dept:
            db.session.add(Cargo(nome=nome, salario_base=sal, departamento_id=dept.id))
    db.session.commit()

    funcs = [
        ("Ana Silva Santos", "111.222.333-44", "1985-03-15", "2018-06-01", 5200, "Analista de RH", "Recursos Humanos"),
        ("Bruno Costa Lima", "222.333.444-55", "1990-07-22", "2019-02-15", 9200, "Desenvolvedor Python", "Tecnologia da Informacao"),
        ("Carla Oliveira Souza", "333.444.555-66", "1988-12-08", "2017-09-20", 8000, "Desenvolvedor Frontend", "Tecnologia da Informacao"),
        ("Diego Pereira Alves", "444.555.666-77", "1992-04-10", "2020-01-10", 6500, "Contador", "Financeiro"),
        ("Elena Ferreira Dias", "555.666.777-88", "1986-09-18", "2019-07-01", 5500, "Analista Financeiro", "Financeiro"),
        ("Felipe Rocha Mendes", "666.777.888-99", "1991-11-25", "2021-03-15", 3800, "Vendedor", "Comercial"),
        ("Gabriela Nunes Castro", "777.888.999-00", "1983-07-30", "2016-05-10", 9000, "Gerente Comercial", "Comercial"),
        ("Hugo Barbosa Reis", "888.999.000-11", "1995-02-12", "2022-04-01", 3500, "Assistente Administrativo", "Administrativo"),
        ("Isabela Cardoso Lima", "999.000.111-22", "1993-08-05", "2020-10-20", 9500, "Desenvolvedor Python", "Tecnologia da Informacao"),
        ("Joao Santos Vieira", "000.111.222-33", "1980-12-20", "2010-08-01", 11000, "Desenvolvedor Frontend", "Tecnologia da Informacao"),
    ]
    for nome, cpf, nasc, adm, sal, cargo_nome, dept_nome in funcs:
        cargo = Cargo.query.filter_by(nome=cargo_nome).first()
        dept = Departamento.query.filter_by(nome=dept_nome).first()
        if cargo and dept:
            db.session.add(Funcionario(
                nome=nome, cpf=cpf,
                data_nascimento=date.fromisoformat(nasc),
                data_admissao=date.fromisoformat(adm),
                cargo_id=cargo.id, departamento_id=dept.id,
                salario=sal, status="Ativo"
            ))
    db.session.commit()

    funcs_at = Funcionario.query.filter_by(status="Ativo").all()
    if len(funcs_at) >= 5:
        for f in funcs_at[:5]:
            for i in range(5):
                d = today - timedelta(days=i)
                entrada = datetime.combine(d, datetime.min.time()) + timedelta(hours=8)
                saida = datetime.combine(d, datetime.min.time()) + timedelta(hours=17)
                db.session.add(RegistroPonto(funcionario_id=f.id, data=d, entrada=entrada, saida=saida))
        db.session.commit()

    bens = [
        Beneficio(nome="Vale Refeicao", tipo="VR", valor_padrao=600),
        Beneficio(nome="Vale Transporte", tipo="VT", valor_padrao=300),
        Beneficio(nome="Plano de Saude", tipo="Saude", valor_padrao=450),
    ]
    for b in bens:
        db.session.add(b)
    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)