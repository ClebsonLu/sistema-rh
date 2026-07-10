import os
from app import create_app, db
from app.models import (
    User, Departamento, Cargo, Funcionario, Ferias, RegistroPonto,
    Beneficio, FuncionarioBeneficio, FolhaPagamento,
    Vaga, Candidato, Treinamento, Capacitacao, Avaliacao, Documento
)
from datetime import date, datetime, timedelta

app = create_app()

with app.app_context():
    db.create_all()

    # Default users
    if not User.query.first():
        users = [
            User(username="admin", nome_completo="Administrador", is_admin=True),
            User(username="rh", nome_completo="Usuario RH", is_admin=False),
        ]
        for u in users:
            u.set_password("123456")
            db.session.add(u)
        db.session.commit()

    # Sample departments
    if not Departamento.query.first():
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

    # Sample cargos
    if not Cargo.query.first():
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
            db.session.add(Cargo(nome=nome, descricao=desc, salario_base=sal, departamento_id=dept.id))
        db.session.commit()

    # Sample funcionarios
    if not Funcionario.query.first():
        funcs = [
            ("Ana Silva Santos", "111.222.333-44", "ana.silva@empresa.com", "(11) 98765-1111", "1985-03-15", "2018-06-01", 5200, "Ativo", "Analista de RH", "Recursos Humanos"),
            ("Bruno Costa Lima", "222.333.444-55", "bruno.costa@empresa.com", "(11) 98765-2222", "1990-07-22", "2019-02-15", 9200, "Ativo", "Desenvolvedor Python", "Tecnologia da Informacao"),
            ("Carla Oliveira Souza", "333.444.555-66", "carla.oliveira@empresa.com", "(11) 98765-3333", "1988-12-08", "2017-09-20", 8000, "Ativo", "Desenvolvedor Frontend", "Tecnologia da Informacao"),
            ("Diego Pereira Alves", "444.555.666-77", "diego.pereira@empresa.com", "(11) 98765-4444", "1992-04-10", "2020-01-10", 6500, "Ativo", "Contador", "Financeiro"),
            ("Elena Ferreira Dias", "555.666.777-88", "elena.ferreira@empresa.com", "(11) 98765-5555", "1986-09-18", "2019-07-01", 5500, "Ativo", "Analista Financeiro", "Financeiro"),
            ("Felipe Rocha Mendes", "666.777.888-99", "felipe.rocha@empresa.com", "(11) 98765-6666", "1991-11-25", "2021-03-15", 3800, "Ativo", "Vendedor", "Comercial"),
            ("Gabriela Nunes Castro", "777.888.999-00", "gabriela.nunes@empresa.com", "(11) 98765-7777", "1983-07-30", "2016-05-10", 9000, "Ativo", "Gerente Comercial", "Comercial"),
            ("Hugo Barbosa Reis", "888.999.000-11", "hugo.barbosa@empresa.com", "(11) 98765-8888", "1995-02-12", "2022-04-01", 3500, "Ativo", "Assistente Administrativo", "Administrativo"),
            ("Isabela Cardoso Lima", "999.000.111-22", "isabela.cardoso@empresa.com", "(11) 98765-9999", "1993-08-05", "2020-10-20", 9500, "Ativo", "Desenvolvedor Python", "Tecnologia da Informacao"),
            ("Joao Santos Vieira", "000.111.222-33", "joao.santos@empresa.com", "(11) 98765-0000", "1980-12-20", "2010-08-01", 11000, "Ativo", "Desenvolvedor Frontend", "Tecnologia da Informacao"),
        ]
        for nome, cpf, email, tel, nasc, adm, sal, status, cargo_nome, dept_nome in funcs:
            cargo = Cargo.query.filter_by(nome=cargo_nome).first()
            dept = Departamento.query.filter_by(nome=dept_nome).first()
            db.session.add(Funcionario(
                nome=nome, cpf=cpf, email=email, telefone=tel,
                data_nascimento=date.fromisoformat(nasc),
                data_admissao=date.fromisoformat(adm),
                cargo_id=cargo.id, departamento_id=dept.id,
                salario=sal, status=status
            ))
        db.session.commit()

    # Sample ferias
    if not Ferias.query.first():
        funcs_at = Funcionario.query.filter_by(status="Ativo").all()
        today = date.today()
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

    # Sample registros de ponto
    if not RegistroPonto.query.first():
        funcs_at = [f for f in Funcionario.query.filter_by(status="Ativo").all()][:5]
        today = date.today()
        for f in funcs_at:
            for i in range(5):
                d = today - timedelta(days=i)
                entrada = datetime.combine(d, datetime.min.time()) + timedelta(hours=8, minutes=30+i*5)
                saida = datetime.combine(d, datetime.min.time()) + timedelta(hours=17, minutes=45+i*3)
                db.session.add(RegistroPonto(
                    funcionario_id=f.id, data=d, entrada=entrada, saida=saida,
                    observacao="Expediente normal" if i == 0 else ""
                ))
        db.session.commit()

    # Sample beneficios
    if not Beneficio.query.first():
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

    # Sample vinculos funcionario-beneficio
    if not FuncionarioBeneficio.query.first():
        funcs_at = Funcionario.query.filter_by(status="Ativo").all()
        bens = Beneficio.query.all()
        for f in funcs_at[:6]:
            for b in bens[:3]:
                db.session.add(FuncionarioBeneficio(
                    funcionario_id=f.id, beneficio_id=b.id, valor=b.valor_padrao
                ))
        db.session.commit()

    # Sample folha de pagamento
    if not FolhaPagamento.query.first():
        funcs_at = Funcionario.query.filter_by(status="Ativo").all()
        today = date.today()
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

    # Sample vagas
    if not Vaga.query.first():
        vagas = [
            Vaga(titulo="Desenvolvedor Python Senior", descricao="Vaga para dev Python com 5+ anos", departamento_id=2, cargo_id=2, salario_oferecido=12000, status="Aberta"),
            Vaga(titulo="Analista de RH", descricao="Analista para setor de RH", departamento_id=1, cargo_id=1, salario_oferecido=5000, status="Aberta"),
            Vaga(titulo="Vendedor Externo", descricao="Equipe comercial externa", departamento_id=4, cargo_id=6, salario_oferecido=4000, status="Em_Analise"),
        ]
        for v in vagas:
            db.session.add(v)
        db.session.commit()

    # Sample candidatos
    if not Candidato.query.first():
        candidatos = [
            Candidato(nome="Pedro Almeida", email="pedro@email.com", vaga_id=1, status="Em_Analise", observacoes="Experiencia em Flask"),
            Candidato(nome="Mariana Costa", email="mariana@email.com", vaga_id=1, status="Novo"),
            Candidato(nome="Lucas Oliveira", email="lucas@email.com", vaga_id=2, status="Aprovado"),
        ]
        for c in candidatos:
            db.session.add(c)
        db.session.commit()

    # Sample treinamentos
    if not Treinamento.query.first():
        today = date.today()
        treinamentos = [
            Treinamento(titulo="Python Avancado", descricao="Curso de Python para devs", carga_horaria=40, data_inicio=today + timedelta(days=5), local="Sala de Treinamento", vagas_max=15, status="Aberto"),
            Treinamento(titulo="Lideranca", descricao="Desenvolvimento de lideres", carga_horaria=16, data_inicio=today - timedelta(days=10), data_fim=today + timedelta(days=5), local="Online", vagas_max=20, status="Em_Andamento"),
            Treinamento(titulo="Seguranca do Trabalho", descricao="NR-10 e NR-35", carga_horaria=8, data_inicio=today - timedelta(days=30), data_fim=today - timedelta(days=30), vagas_max=30, status="Concluido"),
        ]
        for t in treinamentos:
            db.session.add(t)
        db.session.commit()

    # Sample capacitacoes
    if not Capacitacao.query.first():
        funcs_at = Funcionario.query.filter_by(status="Ativo").all()
        treins = Treinamento.query.all()
        capac = [
            Capacitacao(funcionario_id=funcs_at[1].id, treinamento_id=treins[0].id, nota_final=None, status="Inscrito"),
            Capacitacao(funcionario_id=funcs_at[2].id, treinamento_id=treins[0].id, nota_final=None, status="Inscrito"),
            Capacitacao(funcionario_id=funcs_at[0].id, treinamento_id=treins[1].id, nota_final=8.5, certificado=True, status="Aprovado"),
            Capacitacao(funcionario_id=funcs_at[3].id, treinamento_id=treins[2].id, nota_final=9.0, certificado=True, status="Aprovado"),
            Capacitacao(funcionario_id=funcs_at[4].id, treinamento_id=treins[2].id, nota_final=6.5, certificado=False, status="Reprovado"),
        ]
        for c in capac:
            db.session.add(c)
        db.session.commit()

    # Sample avaliacoes
    if not Avaliacao.query.first():
        funcs_at = Funcionario.query.filter_by(status="Ativo").all()
        avaliacoes = [
            Avaliacao(funcionario_id=funcs_at[1].id, avaliador_id=funcs_at[8].id, periodo="2024-T1", nota_geral=8.5, competencias="Lideranca: 9, Comunicacao: 8, Trabalho em Equipe: 8.5", observacoes="Excelente desempenho", status="Concluida"),
            Avaliacao(funcionario_id=funcs_at[3].id, avaliador_id=funcs_at[4].id, periodo="2024-T1", nota_geral=7.0, competencias="Atencao a detalhes: 8, Pontualidade: 7, Organizacao: 6", observacoes="Bom trabalho", status="Concluida"),
            Avaliacao(funcionario_id=funcs_at[5].id, avaliador_id=funcs_at[6].id, periodo="2024-T1", nota_geral=6.0, competencias="Proatividade: 5, Comunicacao: 6, Vendas: 7", observacoes="Pode melhorar", status="Pendente"),
        ]
        for a in avaliacoes:
            db.session.add(a)
        db.session.commit()

    print(f"Departamentos: {Departamento.query.count()}")
    print(f"Cargos: {Cargo.query.count()}")
    print(f"Funcionarios: {Funcionario.query.count()}")
    print(f"Ferias: {Ferias.query.count()}")
    print(f"Registros de Ponto: {RegistroPonto.query.count()}")
    print(f"Beneficios: {Beneficio.query.count()}")
    print(f"Vinculos: {FuncionarioBeneficio.query.count()}")
    print(f"Folha: {FolhaPagamento.query.count()}")
    print(f"Vagas: {Vaga.query.count()}")
    print(f"Candidatos: {Candidato.query.count()}")
    print(f"Treinamentos: {Treinamento.query.count()}")
    print(f"Capacitacoes: {Capacitacao.query.count()}")
    print(f"Avaliacoes: {Avaliacao.query.count()}")
