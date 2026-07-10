import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak,
    Table, TableStyle, KeepTogether
)
from datetime import date

OUTPUT = r"C:\Prj_Ias\prj_rh\Manual_Sistema_RH.pdf"
SHOTS  = r"C:\Prj_Ias\prj_rh\screenshots"

BG_COLOR = HexColor("#f5f7fa")
HEADER_COLOR = HexColor("#2c3e50")
SUBHEADER_COLOR = HexColor("#34495e")
ACCENT_COLOR = HexColor("#3498db")
TIP_COLOR = HexColor("#16a085")
TEXT_COLOR = HexColor("#2c3e50")
MUTED_COLOR = HexColor("#7f8c8d")
LIGHT_BG = HexColor("#ecf0f1")

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=1.5*cm, rightMargin=1.5*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm
)

A4_W, A4_H = A4
USABLE_W = A4_W - 3*cm
USABLE_H = A4_H - 3*cm

styles = getSampleStyleSheet()

cover_title = ParagraphStyle('CoverTitle', fontSize=42, leading=48,
    textColor=HEADER_COLOR, alignment=TA_CENTER, spaceAfter=16, fontName='Helvetica-Bold')
cover_subtitle = ParagraphStyle('CoverSubtitle', fontSize=20, leading=24,
    textColor=SUBHEADER_COLOR, alignment=TA_CENTER, spaceAfter=12, fontName='Helvetica')
cover_info = ParagraphStyle('CoverInfo', fontSize=11,
    textColor=MUTED_COLOR, alignment=TA_CENTER, leading=14)

toc_title = ParagraphStyle('TocTitle', fontSize=22, leading=28,
    textColor=HEADER_COLOR, fontName='Helvetica-Bold', spaceAfter=16)
toc_item = ParagraphStyle('TocItem', fontSize=11, leading=16,
    textColor=TEXT_COLOR)

chapter_title = ParagraphStyle('ChapterTitle', fontSize=18, leading=22,
    textColor=white, fontName='Helvetica-Bold',
    borderPadding=8, leftIndent=0, rightIndent=0,
    backColor=HEADER_COLOR)
screen_title = ParagraphStyle('ScreenTitle', fontSize=14, leading=18,
    textColor=HEADER_COLOR, fontName='Helvetica-Bold',
    spaceAfter=8, spaceBefore=4)
section_label = ParagraphStyle('SectionLabel', fontSize=11, leading=14,
    textColor=white, fontName='Helvetica-Bold',
    backColor=ACCENT_COLOR, borderPadding=3, leftIndent=2, rightIndent=2,
    spaceAfter=6, spaceBefore=4)
body = ParagraphStyle('Body', fontSize=10.5, leading=14,
    textColor=TEXT_COLOR, alignment=TA_JUSTIFY, spaceAfter=6)
bullet = ParagraphStyle('Bullet', fontSize=10.5, leading=14,
    textColor=TEXT_COLOR, leftIndent=14, spaceAfter=3,
    bulletIndent=4)
tip = ParagraphStyle('Tip', fontSize=10.5, leading=14,
    textColor=TIP_COLOR, leftIndent=14, spaceAfter=6,
    fontName='Helvetica-Bold')
warn = ParagraphStyle('Warn', fontSize=10.5, leading=14,
    textColor=HexColor("#c0392b"), leftIndent=14, spaceAfter=6,
    fontName='Helvetica-Bold')

elements = []

def page_break():
    elements.append(PageBreak())

def title(text, style=screen_title):
    elements.append(Paragraph(text, style))

def label(text):
    elements.append(Paragraph(text, section_label))

def p(text, s=body):
    elements.append(Paragraph(text, s))

def bullets(items, s=bullet):
    for it in items:
        elements.append(Paragraph(it, s))

def spacer(pts):
    elements.append(Spacer(1, pts))

def img(path, w=USABLE_W, fixed_h=None):
    """Insere imagem com largura util padrao; opcional: altura fixa em cm."""
    if fixed_h:
        return Image(path, width=w, height=fixed_h*cm)
    return Image(path, width=w, height=USABLE_W*0.55)

# ============================================================
# CAPA
# ============================================================
elements.append(Spacer(1, 5*cm))
title("Sistema de Recursos Humanos", cover_title)
title("Manual do Usuario", cover_subtitle)
p("Guia completo de todas as telas e funcionalidades", cover_info)
spacer(3*cm)
p("Versao 1.0", cover_info)
p(date.today().strftime("Gerado em %d/%m/%Y"), cover_info)
page_break()

# ============================================================
# SUMARIO
# ============================================================
title("Sumario", toc_title)

toc_data = [
    ["1. Introducao",          "3"],
    ["2. Dashboard",           "4"],
    ["3. Funcionarios",        "5"],
    ["    3.1 Listar",         "5"],
    ["    3.2 Cadastrar",      "6"],
    ["4. Departamentos",       "7"],
    ["    4.1 Listar",         "7"],
    ["    4.2 Cadastrar",      "8"],
    ["5. Cargos",              "9"],
    ["    5.1 Listar",         "9"],
    ["    5.2 Cadastrar",     "10"],
    ["6. Ferias",             "11"],
    ["    6.1 Consulta",      "11"],
    ["    6.2 Solicitar",     "12"],
    ["7. Ponto Eletronico",   "13"],
    ["    7.1 Historico",     "13"],
    ["    7.2 Registrar",     "14"],
    ["8. Relatorios",         "15"],
    ["9. Informacoes Tecnicas","16"],
]
toc_rows = [[Paragraph(d[0], toc_item), Paragraph(d[1], ParagraphStyle('P', parent=toc_item, alignment=TA_CENTER))] for d in toc_data]
toc_table = Table(toc_rows, colWidths=[16*cm, 1.5*cm])
toc_table.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('LINEBELOW', (0,0), (-1,-1), 0.25, HexColor('#bdc3c7')),
]))
elements.append(toc_table)
page_break()

# ============================================================
# 1. INTRODUCAO
# ============================================================
title("1. Introducao", chapter_title)
spacer(8)

p("O Sistema de Recursos Humanos (RH) e uma aplicacao web desenvolvida em Python/Flask "
  "que permite o gerenciamento completo de funcionarios, departamentos, cargos, "
  "ferias, registros de ponto e geracao de relatorios.")

spacer(8)
label("Funcionalidades principais")
bullets([
    "<b>Funcionarios</b>: cadastro, edicao, consulta e desativacao",
    "<b>Departamentos</b>: organizacao da estrutura organizacional",
    "<b>Cargos</b>: definicao de posicoes e salarios base",
    "<b>Ferias</b>: solicitacao, aprovacao e rejeicao de periodos",
    "<b>Ponto</b>: registro de entrada/saida e consulta de historico",
    "<b>Relatorios</b>: exportacao automatica em PDF e Excel",
])

spacer(8)
label("Como navegar")
p("O acesso as funcionalidades e feito pelo <b>menu lateral esquerdo</b>. "
  "A pagina inicial e o <b>Dashboard</b>, com indicadores gerais do sistema.")

page_break()

# ============================================================
# 2. DASHBOARD
# ============================================================
title("2. Dashboard", chapter_title)
spacer(8)
p("Tela inicial do sistema. Apresenta os principais indicadores e "
  "permite uma visao geral rapida do estado atual da empresa.")
spacer(8)

elements.append(img(os.path.join(SHOTS, "01-dashboard.png"), w=USABLE_W))
spacer(8)

label("Indicadores Principais")
bullets([
    "<b>Funcionarios Ativos (azul)</b>: total de funcionarios com status Ativo",
    "<b>Ferias Pendentes (amarelo)</b>: solicitacoes aguardando aprovacao",
    "<b>Horas no Mes (verde)</b>: soma total de horas trabalhadas no mes",
    "<b>Aniversariantes (azul claro)</b>: funcionarios que fazem aniversario no mes",
])

spacer(8)
label("Aniversariantes do Mes")
p("Abaixo dos indicadores, quando houver aniversariantes no mes corrente, "
  "sera exibida uma lista com nome e dia do aniversario.")

spacer(8)
title("Dica de uso", screen_title)
p("Use o Dashboard para uma visao geral rapida do status da empresa antes de "
  "entrar em modulos especificos.", tip)

page_break()

# ============================================================
# 3. FUNCIONARIOS
# ============================================================
title("3. Funcionarios", chapter_title)
spacer(8)
p("Gerencia todo o cadastro de funcionarios da empresa. Permite buscar, "
  "visualizar, cadastrar, editar e desativar funcionarios.")
spacer(8)
label("Daqui em diante voce aprendera:")
bullets([
    "<b>3.1 Listar</b>: tela principal de consulta de funcionarios",
    "<b>3.2 Cadastrar / Editar</b>: formulario completo de cadastro",
])
spacer(8)

title("3.1 Listar Funcionarios", screen_title)
p("Tela principal de consulta. Exibe todos os funcionarios cadastrados em formato de tabela.")
spacer(6)
elements.append(img(os.path.join(SHOTS, "02-funcionarios.png"), w=USABLE_W))
spacer(8)

label("Componentes da Tela")
bullets([
    "<b>Botao Novo</b>: abre o formulario de cadastro",
    "<b>Campo de busca</b>: digite o nome para filtrar a lista",
    "<b>Tabela</b>: mostra Nome, CPF, Departamento, Cargo e Status",
    "<b>Botao olho</b>: ver detalhes completos do funcionario",
    "<b>Botao lapis</b>: editar dados do funcionario",
    "<b>Paginacao</b>: navegue entre paginas quando houver muitos registros",
])

spacer(6)
label("Status")
p("<b>Ativo</b> (verde): funcionario trabalha normalmente na empresa. "
  "<br/><b>Inativo</b> (cinza): funcionario desativado, nao aparece nas listas de selecao.")

page_break()

# 3.2 Cadastrar Funcionario
title("3.2 Cadastrar / Editar Funcionario", screen_title)
p("Formulario para incluir ou alterar um funcionario no sistema.")
spacer(6)
elements.append(img(os.path.join(SHOTS, "03-funcionario-cadastrar.png"), w=USABLE_W))
spacer(8)

label("Campos do Formulario")
bullets([
    "<b>Nome</b>*: nome completo do funcionario (obrigatorio)",
    "<b>CPF</b>*: 000.000.000-00 - obrigatorio e unico",
    "<b>Email</b>: email de contato",
    "<b>Telefone</b>: telefone de contato",
    "<b>Data Nascimento</b>: data de nascimento",
    "<b>Data Admissao</b>*: inicio na empresa (obrigatorio)",
    "<b>Departamento</b>*: selecao obrigatoria",
    "<b>Cargo</b>*: selecao obrigatoria",
    "<b>Salario</b>: remuneracao em R$",
    "<b>Status</b>: Ativo ou Inativo",
])

spacer(6)
title("Importante", screen_title)
p("Antes de cadastrar um funcionario, e necessario ter pelo menos um <b>Departamento</b> "
  "e um <b>Cargo</b> previamente cadastrados.", tip)

page_break()

# ============================================================
# 4. DEPARTAMENTOS
# ============================================================
title("4. Departamentos", chapter_title)
spacer(8)
p("Gerencia os departamentos da empresa. Cada departamento pode conter "
  "multiplos cargos e funcionarios.")
spacer(8)
label("Daqui em diante voce aprendera:")
bullets([
    "<b>4.1 Listar</b>: visualizar e gerenciar departamentos",
    "<b>4.2 Cadastrar</b>: formulario simples de cadastro",
])
spacer(8)

title("4.1 Listar Departamentos", screen_title)
p("Lista de todos os departamentos cadastrados.")
spacer(6)
elements.append(img(os.path.join(SHOTS, "04-departamentos.png"), w=USABLE_W))
spacer(8)

label("Acoes Disponiveis")
bullets([
    "<b>Botao Novo</b>: cadastrar novo departamento",
    "<b>Botao lapis</b>: editar departamento existente",
    "<b>Botao lixeira</b>: excluir departamento",
])

spacer(6)
title("Atencao", screen_title)
p("Nao e possivel excluir um departamento que possui cargos ou funcionarios "
  "vinculados. Remova os vinculos ou desative os funcionarios antes.", warn)

page_break()

# 4.2 Cadastrar
title("4.2 Cadastrar Departamento", screen_title)
p("Formulario simples com apenas dois campos: Nome e Descricao.")
spacer(6)
elements.append(img(os.path.join(SHOTS, "05-departamento-cadastrar.png"), w=USABLE_W))
spacer(8)

label("Campos")
bullets([
    "<b>Nome</b>*: nome do departamento (obrigatorio e unico)",
    "<b>Descricao</b>: texto livre sobre as atividades",
])

spacer(6)
label("Dica")
p("Use nomes claros como \"Tecnologia da Informacao\" ou \"Recursos Humanos\" "
  "para facilitar a identificacao.", tip)

page_break()

# ============================================================
# 5. CARGOS
# ============================================================
title("5. Cargos", chapter_title)
spacer(8)
p("Gerencia os cargos (posicoes funcionais) da empresa. Cada cargo pertence a "
  "um departamento e possui um salario base.")
spacer(8)
label("Daqui em diante voce aprendera:")
bullets([
    "<b>5.1 Listar</b>: visualizar cargos por departamento",
    "<b>5.2 Cadastrar</b>: criar novo cargo vinculado a um departamento",
])
spacer(8)

title("5.1 Listar Cargos", screen_title)
p("Lista todos os cargos cadastrados com seu departamento e salario base.")
spacer(6)
elements.append(img(os.path.join(SHOTS, "06-cargos.png"), w=USABLE_W))
spacer(8)

label("Colunas")
bullets([
    "<b>Nome</b>: nome do cargo",
    "<b>Departamento</b>: departamento ao qual pertence",
    "<b>Salario Base</b>: remuneracao inicial de referencia em R$",
    "<b>Acoes</b>: botoes para editar ou excluir",
])

spacer(6)
title("Importante", screen_title)
p("Nao e possivel excluir um cargo que possui funcionarios vinculados. "
  "Desative ou mova os funcionarios antes.", warn)

page_break()

# 5.2 Cadastrar
title("5.2 Cadastrar Cargo", screen_title)
p("Formulario para criar um novo cargo. E necessario um departamento ja cadastrado.")
spacer(6)
elements.append(img(os.path.join(SHOTS, "07-cargo-cadastrar.png"), w=USABLE_W))
spacer(8)

label("Campos do Formulario")
bullets([
    "<b>Nome</b>*: nome do cargo (obrigatorio)",
    "<b>Departamento</b>*: departamento de vinculacao (obrigatorio)",
    "<b>Descricao</b>: atividades exercidas no cargo",
    "<b>Salario Base</b>: valor de referencia inicial em R$",
])

spacer(6)
label("Dica")
p("Mantenha o nome do cargo coerente com a funcao, como \"Analista de RH\" "
  "ou \"Desenvolvedor Python\".", tip)

page_break()

# ============================================================
# 6. FERIAS
# ============================================================
title("6. Ferias", chapter_title)
spacer(8)
p("Controle de solicitacoes de ferias dos funcionarios. Permite solicitar, "
  "aprovar e rejeitar periodos.")
spacer(8)
label("Daqui em diante voce aprendera:")
bullets([
    "<b>6.1 Consulta</b>: visualizar todas as solicitacoes com filtros",
    "<b>6.2 Solicitar</b>: registrar novo pedido de ferias",
])
spacer(8)

title("6.1 Consulta de Ferias", screen_title)
p("Exibe todas as solicitacoes de ferias com filtros por status.")
spacer(6)
elements.append(img(os.path.join(SHOTS, "08-ferias.png"), w=USABLE_W))
spacer(8)

label("Filtros")
bullets([
    "<b>Todos</b>: exibe todas as solicitacoes",
    "<b>Pendentes</b>: somente aguardando aprovacao",
    "<b>Aprovadas</b>: somente as ja aprovadas",
    "<b>Rejeitadas</b>: somente as rejeitadas",
])

spacer(6)
label("Acoes")
p("Para solicitacoes <b>Pendentes</b>, aparecem dois botoes: "
  "<b>check verde</b> (aprovar) e <b>X vermelho</b> (rejeitar).")

spacer(6)
title("Avisos", screen_title)
bullets([
    "Nao permite ferias sobrepostas (Pendente ou Aprovada)",
    "Data fim deve ser igual ou posterior a data inicio",
    "Periodos invalidos sao rejeitados automaticamente",
], tip)

page_break()

# 6.2 Solicitar
title("6.2 Solicitar Ferias", screen_title)
p("Formulario para registrar uma nova solicitacao de ferias.")
spacer(6)
elements.append(img(os.path.join(SHOTS, "09-ferias-solicitar.png"), w=USABLE_W))
spacer(8)

label("Campos")
bullets([
    "<b>Funcionario</b>*: selecao obrigatoria",
    "<b>Data Inicio</b>*: data inicial do periodo",
    "<b>Data Fim</b>*: data final do periodo",
    "<b>Motivo</b>: justificativa ou observacao",
])

spacer(6)
label("Fluxo")
p("Apos solicitar, o status inicial e <b>Pendente</b>. Um gestor pode aprovar "
  "ou rejeitar, e o estado e atualizado em tempo real.", tip)

page_break()

# ============================================================
# 7. PONTO ELETRONICO
# ============================================================
title("7. Ponto Eletronico", chapter_title)
spacer(8)
p("Registro de entrada e saida dos funcionarios. Funciona como ponto eletronico simplificado.")
spacer(8)
label("Daqui em diante voce aprendera:")
bullets([
    "<b>7.1 Historico</b>: consultar registros com filtros",
    "<b>7.2 Registrar</b>: marcar entrada e saida do dia",
])
spacer(8)

title("7.1 Historico de Ponto", screen_title)
p("Consulta todos os registros de ponto com filtros por funcionario, mes e ano.")
spacer(6)
elements.append(img(os.path.join(SHOTS, "10-ponto-historico.png"), w=USABLE_W))
spacer(8)

label("Filtros Disponiveis")
bullets([
    "<b>Funcionario</b>: lista ou selecao especifica",
    "<b>Mes</b>: filtra por mes (1 a 12)",
    "<b>Ano</b>: filtra por ano (2020 a 2030)",
])

spacer(6)
label("Tabela")
p("Colunas: Funcionario, Data, Hora Entrada, Hora Saida, Observacao.")

page_break()

# 7.2 Registrar
title("7.2 Registrar Ponto", screen_title)
p("Registra a entrada ou saida do funcionario com a data/hora atual do sistema.")
spacer(6)
elements.append(img(os.path.join(SHOTS, "11-ponto-registrar.png"), w=USABLE_W))
spacer(8)

label("Como Funciona")
bullets([
    "<b>1o registro do dia</b>: marca a entrada",
    "<b>2o registro do dia</b>: marca a saida",
    "<b>3o registro em diante</b>: sistema informa que ja existe registro",
])

spacer(6)
label("Dica")
p("Para registrar a saida, basta submeter o formulario novamente no mesmo dia.", tip)

page_break()

# ============================================================
# 8. RELATORIOS
# ============================================================
title("8. Relatorios", chapter_title)
spacer(8)
p("Centro de exportacao de relatorios em formatos PDF e Excel.")
spacer(6)
elements.append(img(os.path.join(SHOTS, "12-relatorios.png"), w=USABLE_W))
spacer(8)

label("Relatorios Disponiveis")
bullets([
    "<b>Funcionarios (PDF)</b>: lista com CPF, departamento, cargo, salario e status",
    "<b>Folha de Pagamento (Excel)</b>: planilha com funcionarios ativos e salarios",
    "<b>Ponto (PDF)</b>: historico dos ultimos 100 registros de ponto",
])

spacer(6)
label("Como Gerar")
p("Clique no botao <b>Baixar PDF</b> ou <b>Baixar Excel</b> do relatorio desejado. "
  "O arquivo sera baixado automaticamente.")

spacer(6)
label("Dica")
p("Para gerar PDF de um funcionario especifico, abra o Historico de Ponto, "
  "filtre por funcionario, e gere via menu.", tip)

page_break()

# ============================================================
# 9. INFORMACOES TECNICAS
# ============================================================
title("9. Informacoes Tecnicas", chapter_title)
spacer(8)

info = [
    ("Tecnologia", "Python 3.12 + Flask + SQLAlchemy"),
    ("Banco de Dados", "SQLite"),
    ("Frontend", "Bootstrap 5 + Bootstrap Icons"),
    ("Geracao de PDF", "ReportLab"),
    ("Geracao de Excel", "OpenPyXL"),
    ("Servidor", "http://127.0.0.1:5000"),
    ("Porta padrao", "5000"),
    ("Diretorio", "C:\\Prj_Ias\\prj_rh"),
]
info_rows = [[Paragraph(f"<b>{k}</b>", body), Paragraph(v, body)] for k, v in info]
info_table = Table(info_rows, colWidths=[5*cm, 12*cm])
info_table.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BACKGROUND', (0,0), (0,-1), HexColor('#ecf0f1')),
    ('LINEBELOW', (0,0), (-1,-1), 0.5, HexColor('#bdc3c7')),
]))
elements.append(info_table)

spacer(14)
label("Suporte")
p("Em caso de duvidas sobre o sistema, consulte esta documentacao ou "
  "entre em contato com o administrador do sistema.")

spacer(10)
label("Boa utilizacao!")
p("Este sistema foi desenvolvido para simplificar a gestao de pessoas. "
  "Mantenha os dados sempre atualizados.", tip)

# ============================================================
# Build
# ============================================================
def apply_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG_COLOR)
    canvas.rect(0, 0, A4_W, A4_H, fill=1, stroke=0)
    canvas.restoreState()

doc.build(elements, onFirstPage=apply_bg, onLaterPages=apply_bg)
print(f"PDF criado: {OUTPUT}")
print(f"Tamanho: {os.path.getsize(OUTPUT) / 1024:.1f} KB")
