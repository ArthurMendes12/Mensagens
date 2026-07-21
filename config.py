# ==========================================
# CONFIGURAÇÕES DO SISTEMA
# ==========================================

import os


UPLOAD_FOLDER = "uploads"


PHONE_COLUMN = "telefone"

NAME_COLUMN = "nome"



if not os.path.exists(UPLOAD_FOLDER):

    os.makedirs(UPLOAD_FOLDER)

# Pasta para salvar logs
LOG_FOLDER = "logs"

# Pasta onde o Playwright armazenará a sessão do WhatsApp
SESSION_FOLDER = "session"

# Tempo mínimo entre mensagens (segundos)
MIN_DELAY = 8

# Tempo máximo entre mensagens (segundos)
MAX_DELAY = 15

# Nome da coluna que contém os telefones
PHONE_COLUMN = "telefone"

# Nome da coluna que contém o nome do contato
NAME_COLUMN = "nome"

# Cria as pastas automaticamente caso não existam
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)
os.makedirs(SESSION_FOLDER, exist_ok=True)
