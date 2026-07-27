import os

import streamlit as st

from automation.enviador import EnviadorAutomatico
from config import UPLOAD_FOLDER
from excel import carregar_planilha
from logs import carregar_logs, registrar_envio
from mensagens import personalizar_mensagem
from whatsapp import WhatsAppService


st.set_page_config(
    page_title="Disparador WhatsApp",
    page_icon="📱",
    layout="wide",
)


# ==============================
# SESSAO
# ==============================

if "whatsapp" not in st.session_state:
    st.session_state.whatsapp = WhatsAppService()

if "df" not in st.session_state:
    st.session_state.df = None

if "enviador" not in st.session_state:
    st.session_state.enviador = None

if "whatsapp_conectado" not in st.session_state:
    st.session_state.whatsapp_conectado = False


# ==============================
# TITULO
# ==============================

st.title("📱 Disparador WhatsApp")
st.write("Envio de mensagens personalizadas pelo seu WhatsApp Web.")


# ==============================
# CONEXAO WHATSAPP
# ==============================

st.header("0️⃣ Conectar WhatsApp")

if st.session_state.whatsapp_conectado:
    st.success("WhatsApp conectado. Os envios automaticos sairao desta conta.")

    if st.button("Encerrar navegador do WhatsApp"):
        st.session_state.enviador.fechar()
        st.session_state.enviador = None
        st.session_state.whatsapp_conectado = False
        st.rerun()

else:
    st.info(
        "Clique em Gerar QR Code. No celular, abra o WhatsApp e acesse "
        "Dispositivos conectados > Conectar dispositivo para escanear o codigo."
    )

    if st.button("Gerar QR Code do WhatsApp"):
        qr_placeholder = st.empty()
        status_placeholder = st.empty()
        enviador = None

        try:
            status_placeholder.info("Abrindo o WhatsApp Web...")
            enviador = EnviadorAutomatico(headless=False)
            enviador.iniciar()

            def atualizar_qr_code(imagem_qr):
                qr_placeholder.image(
                    imagem_qr,
                    caption="Escaneie este QR Code usando o WhatsApp no celular.",
                    width=300,
                )
                status_placeholder.info("Aguardando a leitura do QR Code...")

            conectado = enviador.bot.aguardar_conexao(
                callback_qr=atualizar_qr_code,
                timeout=120,
            )

            if conectado:
                st.session_state.enviador = enviador
                st.session_state.whatsapp_conectado = True
                qr_placeholder.empty()
                status_placeholder.success("WhatsApp conectado com sucesso.")
                st.rerun()

            enviador.fechar()
            status_placeholder.warning(
                "O QR Code expirou antes da conexao. Gere um novo codigo e tente novamente."
            )

        except Exception as erro:
            if enviador:
                enviador.fechar()
            st.error(f"Nao foi possivel iniciar o WhatsApp Web: {erro}")


# ==============================
# UPLOAD
# ==============================

st.header("1️⃣ Carregar Excel")

arquivo = st.file_uploader("Escolha sua planilha", type=["xlsx"])

if arquivo:
    caminho = os.path.join(UPLOAD_FOLDER, arquivo.name)

    with open(caminho, "wb") as arquivo_destino:
        arquivo_destino.write(arquivo.getbuffer())

    st.session_state.df = carregar_planilha(caminho)
    st.success("Planilha carregada!")


# ==============================
# CONTATOS
# ==============================

if st.session_state.df is not None:
    st.subheader("Contatos")
    st.dataframe(st.session_state.df, use_container_width=True)


# ==============================
# MENSAGEM
# ==============================

st.header("2️⃣ Criar mensagem")
mensagem = st.text_area("Digite a mensagem", height=150)

if st.session_state.df is not None:
    st.write("Variaveis disponiveis:")

    for coluna in st.session_state.df.columns:
        st.code("{" + coluna + "}")


# ==============================
# ENVIO MANUAL
# ==============================

st.header("3️⃣ Enviar mensagens manualmente")

if st.session_state.df is not None and mensagem:
    for indice, contato in st.session_state.df.iterrows():
        texto = personalizar_mensagem(mensagem, contato)
        nome = contato["nome"]
        telefone = contato["telefone"]

        col1, col2 = st.columns([3, 1])

        with col1:
            st.write(f"📱 {nome} - {telefone}")

        with col2:
            if st.button("Abrir WhatsApp", key=f"manual_{indice}"):
                link = st.session_state.whatsapp.abrir_whatsapp(telefone, texto)
                st.markdown(
                    f'<a href="{link}" target="_blank">📲 Abrir WhatsApp</a>',
                    unsafe_allow_html=True,
                )
                registrar_envio(telefone, texto, "link criado")
                st.success(f"Link criado para {nome}")


# ==============================
# ENVIO AUTOMATICO
# ==============================

st.header("4️⃣ Envio automatico")
st.caption(
    "As mensagens sao enviadas pelo WhatsApp conectado acima, com intervalo "
    "aleatorio entre cada envio."
)

if st.session_state.df is not None and mensagem:
    if not st.session_state.whatsapp_conectado:
        st.warning("Conecte seu WhatsApp pelo QR Code para habilitar o envio automatico.")

    elif st.button("🤖 Iniciar envio automatico"):
        total = len(st.session_state.df)
        barra = st.progress(0)
        status_placeholder = st.empty()

        def atualizar_progresso(posicao, total, nome, telefone, sucesso, erro):
            barra.progress((posicao + 1) / total)

            if sucesso:
                status_placeholder.write(f"✅ Enviado para {nome} ({telefone})")
            else:
                status_placeholder.write(
                    f"❌ Falha ao enviar para {nome} ({telefone}): {erro}"
                )

        resultados = st.session_state.enviador.enviar_para_todos(
            st.session_state.df,
            mensagem,
            callback=atualizar_progresso,
        )

        sucessos = len([resultado for resultado in resultados if resultado["sucesso"]])
        st.success(
            f"Envio automatico concluido: {sucessos}/{total} mensagens enviadas com sucesso."
        )

else:
    st.info("Carregue uma planilha e escreva uma mensagem para habilitar o envio automatico.")


# ==============================
# LOGS
# ==============================

st.header("📊 Historico")
logs = carregar_logs()

if not logs.empty:
    st.dataframe(logs, use_container_width=True)
