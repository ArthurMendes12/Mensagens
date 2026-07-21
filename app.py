import streamlit as st
import os


from excel import carregar_planilha
from whatsapp import WhatsAppService
from logs import registrar_envio, carregar_logs, resumo_envios
from config import UPLOAD_FOLDER



st.set_page_config(
    page_title="Disparador WhatsApp",
    page_icon="📱",
    layout="wide"
)



# ==============================
# SESSÃO
# ==============================


if "whatsapp" not in st.session_state:

    st.session_state.whatsapp = WhatsAppService()



if "df" not in st.session_state:

    st.session_state.df = None



# ==============================
# TÍTULO
# ==============================


st.title(
    "📱 Disparador WhatsApp"
)


st.write(
    "Envio manual com mensagens personalizadas."
)



# ==============================
# UPLOAD
# ==============================


st.header(
    "1️⃣ Carregar Excel"
)



arquivo = st.file_uploader(
    "Escolha sua planilha",
    type=["xlsx"]
)



if arquivo:


    caminho = os.path.join(
        UPLOAD_FOLDER,
        arquivo.name
    )


    with open(
        caminho,
        "wb"
    ) as f:

        f.write(
            arquivo.getbuffer()
        )



    st.session_state.df = carregar_planilha(
        caminho
    )


    st.success(
        "Planilha carregada!"
    )



# ==============================
# CONTATOS
# ==============================


if st.session_state.df is not None:


    st.subheader(
        "Contatos"
    )


    st.dataframe(
        st.session_state.df,
        use_container_width=True
    )



# ==============================
# MENSAGEM
# ==============================


st.header(
    "2️⃣ Criar mensagem"
)



mensagem = st.text_area(
    "Digite a mensagem",
    height=150
)



# ==============================
# VARIÁVEIS
# ==============================


if st.session_state.df is not None:


    st.write(
        "Variáveis disponíveis:"
    )


    for coluna in st.session_state.df.columns:

        st.code(
            "{" + coluna + "}"
        )



# ==============================
# ENVIO
# ==============================


st.header(
    "3️⃣ Enviar mensagens"
)



if (
    st.session_state.df is not None
    and mensagem
):


    for indice, contato in st.session_state.df.iterrows():


        texto = mensagem



        for coluna in contato.index:

            texto = texto.replace(
                "{" + coluna + "}",
                str(contato[coluna])
            )



        nome = contato["nome"]

        telefone = contato["telefone"]



        col1, col2 = st.columns(
            [3,1]
        )


        with col1:

            st.write(
                f"📱 {nome} - {telefone}"
            )



        with col2:


            if st.button(
                "Enviar",
                key=indice
            ):


                link = (
    st.session_state.whatsapp.abrir_whatsapp(
        telefone,
        texto
    )
)


st.markdown(
    f"""
    <a href="{link}" target="_blank">
        📲 Abrir WhatsApp
    </a>
    """,
    unsafe_allow_html=True
)


                registrar_envio(
                    telefone,
                    texto,
                    "aberto"
                )


                st.success(
                    f"WhatsApp aberto para {nome}"
                )



# ==============================
# LOGS
# ==============================


st.header(
    "📊 Histórico"
)



logs = carregar_logs()



if not logs.empty:

    st.dataframe(
        logs,
        use_container_width=True
    )
