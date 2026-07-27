Instale o Python se ainda não tiver
No VS Code, abra o terminal com Ctrl + ' e rode:
py --version

Se não aparecer uma versão, instale o Python e marque a opção para adicioná-lo ao PATH. O Streamlit atual suporta Python 3.10 a 3.14. Documentação
Abra a pasta do projeto no VS Code
Abra a pasta:
C:\Users\Arthur.Buegare\Downloads\Mensagens-main\Mensagens-main

No terminal do VS Code, execute uma vez:
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py -m playwright install chromium

O último comando baixa o navegador usado pelo sistema para abrir o WhatsApp Web. Documentação do Playwright

Se o PowerShell bloquear a ativação, execute antes:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Para iniciar o sistema:
py -m streamlit run app.py
O navegador abrirá em http://localhost:8501. O Streamlit inicia um servidor local e abre a aplicação no navegador. Documentação

Dentro do sistema:
Clique em “Gerar QR Code do WhatsApp”.
No celular: WhatsApp → Configurações → Dispositivos conectados → Conectar dispositivo.
Escaneie o QR.
Envie uma planilha .xlsx com as colunas nome e telefone.
Escreva a mensagem e teste primeiro com apenas um contato.

Mantenha o terminal do VS Code aberto enquanto estiver usando o sistema. Para parar, pressione Ctrl + C no terminal.
