from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    nome_completo = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Departamento(db.Model):
    __tablename__ = "departamentos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.Text)
    cargos = db.relationship("Cargo", backref="departamento", lazy=True)
    funcionarios = db.relationship("Funcionario", backref="departamento", lazy=True)


class Cargo(db.Model):
    __tablename__ = "cargos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    salario_base = db.Column(db.Float, nullable=False, default=0.0)
    departamento_id = db.Column(db.Integer, db.ForeignKey("departamentos.id"), nullable=False)
    funcionarios = db.relationship("Funcionario", backref="cargo", lazy=True)


class Funcionario(db.Model):
    __tablename__ = "funcionarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    email = db.Column(db.String(150))
    telefone = db.Column(db.String(20))
    data_nascimento = db.Column(db.Date)
    data_admissao = db.Column(db.Date, nullable=False, default=date.today)
    cargo_id = db.Column(db.Integer, db.ForeignKey("cargos.id"), nullable=False)
    departamento_id = db.Column(db.Integer, db.ForeignKey("departamentos.id"), nullable=False)
    salario = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(20), nullable=False, default="Ativo")
    ferias = db.relationship("Ferias", backref="funcionario", lazy=True)
    registros_ponto = db.relationship("RegistroPonto", backref="funcionario", lazy=True)
    beneficios = db.relationship("FuncionarioBeneficio", backref="funcionario", lazy=True)
    folhas = db.relationship("FolhaPagamento", backref="funcionario", lazy=True)
    capacitacoes = db.relationship("Capacitacao", backref="funcionario", lazy=True)
    avaliacoes = db.relationship("Avaliacao", backref="funcionario", lazy=True, foreign_keys="Avaliacao.funcionario_id")
    documentos = db.relationship("Documento", backref="funcionario", lazy=True)


class Ferias(db.Model):
    __tablename__ = "ferias"
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    dias = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pendente")
    motivo = db.Column(db.Text)
    data_solicitacao = db.Column(db.DateTime, nullable=False, default=datetime.now)


class RegistroPonto(db.Model):
    __tablename__ = "registros_ponto"
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"), nullable=False)
    data = db.Column(db.Date, nullable=False, default=date.today)
    entrada = db.Column(db.DateTime, nullable=False)
    saida = db.Column(db.DateTime)
    observacao = db.Column(db.Text)


class Beneficio(db.Model):
    __tablename__ = "beneficios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False, default="Outro")
    valor_padrao = db.Column(db.Float, nullable=False, default=0.0)
    descricao = db.Column(db.Text)
    vinculados = db.relationship("FuncionarioBeneficio", backref="beneficio", lazy=True)


class FuncionarioBeneficio(db.Model):
    __tablename__ = "funcionarios_beneficios"
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"), nullable=False)
    beneficio_id = db.Column(db.Integer, db.ForeignKey("beneficios.id"), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_inicio = db.Column(db.Date, nullable=False, default=date.today)
    data_fim = db.Column(db.Date)
    status = db.Column(db.String(20), nullable=False, default="Ativo")


class FolhaPagamento(db.Model):
    __tablename__ = "folha_pagamento"
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"), nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    salario_bruto = db.Column(db.Float, nullable=False, default=0.0)
    total_beneficios = db.Column(db.Float, nullable=False, default=0.0)
    total_descontos = db.Column(db.Float, nullable=False, default=0.0)
    salario_liquido = db.Column(db.Float, nullable=False, default=0.0)
    data_pagamento = db.Column(db.Date)
    status = db.Column(db.String(20), nullable=False, default="Pendente")


class Vaga(db.Model):
    __tablename__ = "vagas"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    departamento_id = db.Column(db.Integer, db.ForeignKey("departamentos.id"), nullable=False)
    cargo_id = db.Column(db.Integer, db.ForeignKey("cargos.id"), nullable=False)
    salario_oferecido = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(20), nullable=False, default="Aberta")
    data_abertura = db.Column(db.Date, nullable=False, default=date.today)
    data_encerramento = db.Column(db.Date)
    departamento = db.relationship("Departamento", backref="vagas")
    cargo = db.relationship("Cargo", backref="vagas")
    candidatos = db.relationship("Candidato", backref="vaga", lazy=True)


class Candidato(db.Model):
    __tablename__ = "candidatos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150))
    telefone = db.Column(db.String(20))
    vaga_id = db.Column(db.Integer, db.ForeignKey("vagas.id"), nullable=False)
    curriculo_path = db.Column(db.String(300))
    status = db.Column(db.String(30), nullable=False, default="Novo")
    data_candidatura = db.Column(db.Date, nullable=False, default=date.today)
    observacoes = db.Column(db.Text)


class Treinamento(db.Model):
    __tablename__ = "treinamentos"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    carga_horaria = db.Column(db.Integer, nullable=False, default=0)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date)
    local = db.Column(db.String(150))
    vagas_max = db.Column(db.Integer, nullable=False, default=30)
    status = db.Column(db.String(20), nullable=False, default="Aberto")
    capacitacoes = db.relationship("Capacitacao", backref="treinamento", lazy=True)


class Capacitacao(db.Model):
    __tablename__ = "capacitacoes"
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"), nullable=False)
    treinamento_id = db.Column(db.Integer, db.ForeignKey("treinamentos.id"), nullable=False)
    data_inscricao = db.Column(db.Date, nullable=False, default=date.today)
    nota_final = db.Column(db.Float)
    certificado = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.String(20), nullable=False, default="Inscrito")


class Avaliacao(db.Model):
    __tablename__ = "avaliacoes"
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"), nullable=False)
    avaliador_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"), nullable=False)
    periodo = db.Column(db.String(20), nullable=False)
    nota_geral = db.Column(db.Float, nullable=False, default=0.0)
    competencias = db.Column(db.Text)
    observacoes = db.Column(db.Text)
    data_avaliacao = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(20), nullable=False, default="Pendente")
    avaliador = db.relationship("Funcionario", foreign_keys=[avaliador_id], backref="avaliacoes_realizadas")


class Documento(db.Model):
    __tablename__ = "documentos"
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"), nullable=False)
    titulo = db.Column(db.String(150), nullable=False)
    categoria = db.Column(db.String(50), nullable=False, default="Geral")
    arquivo_path = db.Column(db.String(300))
    data_upload = db.Column(db.Date, nullable=False, default=date.today)
    descricao = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default="Ativo")
