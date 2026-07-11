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

        from app.models import User
        if not User.query.first():
            users = [
                User(username="admin", nome_completo="Administrador", is_admin=True),
                User(username="rh", nome_completo="Usuario RH", is_admin=False),
            ]
            for u in users:
                u.set_password("123456")
                db.session.add(u)
            db.session.commit()

            from app.models import Departamento, Cargo, Funcionario, Ferias, RegistroPonto
            from app.models import Beneficio, FuncionarioBeneficio, FolhaPagamento
            from app.models import Vaga, Candidato, Treinamento, Capacitacao, Avaliacao
            from datetime import date, datetime, timedelta

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
                ("Analista de RH", "Departamento de suporte", 4500, "Recursos Humanos"),
                ("Desenvolvedor Python", "Backend Python/Flask", 8500, "Tecnologia da Informacao"),
                ("Desenvolvedor Frontend", "React/Bootstrap", 7500, "Tecnologia da Informacao"),
                ("Contador", "Escrituracao fiscal", 6000, "Financeiro"),
                ("Analista Financeiro", "Contas a pagar/receber", 5000, "Financeiro"),
                ("Vendedor", "Vendas internas", 3500, "Comercial"),
                ("Gerente Comercial", "Gestao equipe vendas", 8500, "Comercial"),
                ("Assistente Administrativo", "Apoio geral", 3200, "Administrativo"),
            ]
            for nome, desc, sal, dept_nome in cargos_dados:
                dept = Departamento.query.filter_by(nome=dept_nome).first()
                if dept:
                    db.session.add(Cargo(nome=nome, descricao=desc, salario_base=sal, departamento_id=dept.id))
            db.session.commit()

            funcs = [
                ("Ana Silva Santos", "111.222.333-44", "ana.silva@empresa.com", "(11) 98765-1111", "1985-03-15", "2018-06-01", 5200, "Analista de RH", "Recursos Humanos"),
                ("Bruno Costa Lima", "222.333.444-55", "bruno.costa@empresa.com", "(11) 98765-2222", "1990-07-22", "2019-02-15", 9200, "Desenvolvedor Python", "Tecnologia da Informacao"),
                ("Carla Oliveira Souza", "333.444.555-66", "carla.oliveira@empresa.com", "(11) 98765-3333", "1988-12-08", "2017-09-20", 8000, "Desenvolvedor Frontend", "Tecnologia da Informacao"),
                ("Diego Pereira Alves", "444.555.666-77", "diego.pereira@empresa.com", "(11) 98765-4444", "1992-04-10", "2020-01-10", 6500, "Contador", "Financeiro"),
                ("Elena Ferreira Dias", "555.666.777-88", "elena.ferreira@empresa.com", "(11) 98765-5555", "1986-09-18", "2019-07-01", 5500, "Analista Financeiro", "Financeiro"),
                ("Felipe Rocha Mendes", "666.777.888-99", "felipe.rocha@empresa.com", "(11) 98765-6666", "1991-11-25", "2021-03-15", 3800, "Vendedor", "Comercial"),
                ("Gabriela Nunes Castro", "777.888.999-00", "gabriela.nunes@empresa.com", "(11) 98765-7777", "1983-07-30", "2016-05-10", 9000, "Gerente Comercial", "Comercial"),
                ("Hugo Barbosa Reis", "888.999.000-11", "hugo.barbosa@empresa.com", "(11) 98765-8888", "1995-02-12", "2022-04-01", 3500, "Assistente Administrativo", "Administrativo"),
                ("Isabela Cardoso Lima", "999.000.111-22", "isabela.cardoso@empresa.com", "(11) 98765-9999", "1993-08-05", "2020-10-20", 9500, "Desenvolvedor Python", "Tecnologia da Informacao"),
                ("Joao Santos Vieira", "000.111.222-33", "joao.santos@empresa.com", "(11) 98765-0000", "1980-12-20", "2010-08-01", 11000, "Desenvolvedor Frontend", "Tecnologia da Informacao"),
            ]
            for nome, cpf, email, tel, nasc, adm, sal, cargo_nome, dept_nome in funcs:
                cargo = Cargo.query.filter_by(nome=cargo_nome).first()
                dept = Departamento.query.filter_by(nome=dept_nome).first()
                if cargo and dept:
                    db.session.add(Funcionario(
                        nome=nome, cpf=cpf, email=email, telefone=tel,
                        data_nascimento=date.fromisoformat(nasc),
                        data_admissao=date.fromisoformat(adm),
                        cargo_id=cargo.id, departamento_id=dept.id,
                        salario=sal, status="Ativo"
                    ))
            db.session.commit()

            funcs_at = Funcionario.query.filter_by(status="Ativo").all()
            today = date.today()
            if len(funcs_at) >= 3:
                f_dados = [
                    (funcs_at[0], today + timedelta(days=10), today + timedelta(days=24), "Aprovada", "Viagem em familia"),
                    (funcs_at[2], today + timedelta(days=30), today + timedelta(days=44), "Pendente", "Ferias programadas"),
                    (funcs_at[4], today + timedelta(days=45), today + timedelta(days=59), "Pendente", "Descanso"),
                ]
                for f, ini, fim, st, mot in f_dados:
                    db.session.add(Ferias(
                        funcionario_id=f.id, data_inicio=ini, data_fim=fim,
                        dias=(fim-ini).days + 1, status=st, motivo=mot
                    ))
                db.session.commit()

            if len(funcs_at) >= 5:
                for f in funcs_at[:5]:
                    for i in range(5):
                        d = today - timedelta(days=i)
                        entrada = datetime.combine(d, datetime.min.time()) + timedelta(hours=8, minutes=30+i*5)
                        saida = datetime.combine(d, datetime.min.time()) + timedelta(hours=17, minutes=45+i*3)
                        db.session.add(RegistroPonto(
                            funcionario_id=f.id, data=d, entrada=entrada, saida=saida
                        ))
                db.session.commit()

            bens = [
                Beneficio(nome="Vale Refeicao", tipo="VR", valor_padrao=600, descricao="Alimentacao diaria"),
                Beneficio(nome="Vale Transporte", tipo="VT", valor_padrao=300, descricao="Deslocamento"),
                Beneficio(nome="Plano de Saude", tipo="Saude", valor_padrao=450, descricao="Plano medico"),
                Beneficio(nome="Plano Odontologico", tipo="Odontologico", valor_padrao=150, descricao="Plano dental"),
                Beneficio(nome="Seguro de Vida", tipo="Seguro", valor_padrao=80, descricao="Seguro em grupo"),
            ]
            for b in bens:
                db.session.add(b)
            db.session.commit()

            if len(funcs_at) >= 6:
                bens = Beneficio.query.all()
                for f in funcs_at[:6]:
                    for b in bens[:3]:
                        db.session.add(FuncionarioBeneficio(
                            funcionario_id=f.id, beneficio_id=b.id, valor=b.valor_padrao
                        ))
                db.session.commit()

            if len(funcs_at) >= 1:
                for f in funcs_at:
                    beneficios = FuncionarioBeneficio.query.filter_by(funcionario_id=f.id, status="Ativo").all()
                    total_benef = sum(b.valor for b in beneficios)
                    descontos = f.salario * 0.11
                    liquido = f.salario + total_benef - descontos
                    db.session.add(FolhaPagamento(
                        funcionario_id=f.id, mes=today.month, ano=today.year,
                        salario_bruto=f.salario, total_beneficios=total_benef,
                        total_descontos=descontos, salario_liquido=liquido,
                        status="Pago", data_pagamento=today
                    ))
                db.session.commit()

            dept = Departamento.query.first()
            cargo = Cargo.query.first()
            if dept and cargo:
                vagas = [
                    Vaga(titulo="Desenvolvedor Python Senior", descricao="Vaga para dev Python com 5+ anos", departamento_id=dept.id, cargo_id=cargo.id, salario_oferecido=12000, status="Aberta"),
                    Vaga(titulo="Analista de RH", descricao="Analista para setor de RH", departamento_id=dept.id, cargo_id=cargo.id, salario_oferecido=5000, status="Aberta"),
                ]
                for v in vagas:
                    db.session.add(v)
                db.session.commit()

                vaga = Vaga.query.first()
                if vaga:
                    db.session.add(Candidato(nome="Pedro Almeida", email="pedro@email.com", vaga_id=vaga.id, status="Em_Analise"))
                    db.session.add(Candidato(nome="Mariana Costa", email="mariana@email.com", vaga_id=vaga.id, status="Novo"))
                    db.session.commit()

            treinamentos = [
                Treinamento(titulo="Python Avancado", descricao="Curso de Python para devs", carga_horaria=40, data_inicio=today + timedelta(days=5), local="Sala de Treinamento", vagas_max=15, status="Aberto"),
                Treinamento(titulo="Lideranca", descricao="Desenvolvimento de lideres", carga_horaria=16, data_inicio=today - timedelta(days=10), local="Online", vagas_max=20, status="Em_Andamento"),
                Treinamento(titulo="Seguranca do Trabalho", descricao="NR-10 e NR-35", carga_horaria=8, data_inicio=today - timedelta(days=30), vagas_max=30, status="Concluido"),
            ]
            for t in treinamentos:
                db.session.add(t)
            db.session.commit()

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