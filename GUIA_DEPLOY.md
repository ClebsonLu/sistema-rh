# Deploy Sistema RH no Railway

## Arquivos ja configurados

- `Procfile` - comando para iniciar o app com gunicorn
- `railway.json` - configuracao do Railway
- `requirements.txt` - dependencias atualizadas
- `config.py` - suporte a SQLite (dev) e PostgreSQL (prod)
- `.gitignore` - exclui arquivos sensiveis

## Passos para Deploy

### 1. Preparar o projeto no GitHub

```bash
# Dentro da pasta do projeto
cd C:\Prj_Ias\prj_rh

# Inicializar git (se ainda nao fez)
git init
git add .
git commit -m "Initial commit"

# Criar repositorio no GitHub e subir
git remote add origin https://github.com/SEU_USUARIO/sistema-rh.git
git branch -M main
git push -u origin main
```

### 2. Deploy no Railway

1. Acesse [railway.app](https://railway.app)
2. Faca login com GitHub
3. Clique em **"New Project"** → **"Deploy from GitHub repo"**
4. Selecione o repositorio `sistema-rh`
5. O Railway detecta automaticamente o Python
6. Clique em **"Deploy"**

### 3. Configurar variaveis de ambiente (opcional)

No Railway Dashboard:
1. Va para o projeto
2. Clique em **"Variables"**
3. Adicione:
   - `SECRET_KEY` = uma-chave-secreta-forte-aqui
   - `FLASK_ENV` = production

### 4. Adicionar PostgreSQL (recomendado)

1. No Railway, clique em **"New"** → **"Database"** → **"PostgreSQL"**
2. O Railway cria e fornece a `DATABASE_URL` automaticamente
3. Va em **"Variables"** do seu projeto e verifique se `DATABASE_URL` esta definida

### 5. Acessar o deploy

Apos o deploy terminar, clique no dominio fornecido pelo Railway.

## Comandos Uteis

### Ver logs
```bash
railway logs
```

### Abrir shell
```bash
railway run python
```

### Restart
```bash
railway restart
```

## Resolver problemas

### "Module not found"
Verifique se todas dependencias estao no `requirements.txt`

### "Database connection error"
Verifique se a `DATABASE_URL` esta correta no Railway

### "Static files not loading"
O Gunicorn nao serve arquivos estaticos bem. Para producao, adicione Nginx ou use WhiteNoise.

## Desenvolvimento Local

```bash
# Clonar
git clone https://github.com/SEU_USUARIO/sistema-rh.git
cd sistema-rh

# Criar venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Rodar localmente
python run.py
```

## Atualizar deploy

```bash
git add .
git commit -m "Sua mensagem"
git push origin main
# O Railway faz deploy automaticamente!
```