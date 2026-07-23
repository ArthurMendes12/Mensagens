import streamlit as st
import os


from excel import carregar_planilha
from whatsapp import WhatsAppService
from logs import registrar_envio, carregar_logs, resumo_envios
from config import UPLOAD_FOLDER
from mensagens import personalizar_mensagem
from automation.enviador import EnviadorAutomatico



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


        texto = personalizar_mensagem(
            mensagem,
            contato
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
                    "link criado"
                )


                st.success(
                    f"Link criado para {nome}"
                )



# ==============================
# ENVIO AUTOMÁTICO (PLAYWRIGHT)
# ==============================


st.header(
    "4️⃣ Envio automático (Playwright)"
)


st.caption(
    "Abre o WhatsApp Web em um navegador controlado e envia as mensagens "
    "automaticamente, respeitando um intervalo aleatório entre cada envio. "
    "Na primeira execução será necessário escanear o QR Code."
)


if (
    st.session_state.df is not None
    and mensagem
):

    if st.button("🤖 Iniciar envio automático"):

        total = len(st.session_state.df)

        barra = st.progress(0)

        status_placeholder = st.empty()

        enviador = EnviadorAutomatico(headless=False)

        with st.spinner("Abrindo WhatsApp Web..."):
            enviador.iniciar()

        def atualizar_progresso(posicao, total, nome, telefone, sucesso, erro):

            barra.progress((posicao + 1) / total)

            if sucesso:
                status_placeholder.write(f"✅ Enviado para {nome} ({telefone})")
            else:
                status_placeholder.write(f"❌ Falha ao enviar para {nome} ({telefone}): {erro}")

        resultados = enviador.enviar_para_todos(
            st.session_state.df,
            mensagem,
            callback=atualizar_progresso
        )

        enviador.fechar()

        sucessos = len([r for r in resultados if r["sucesso"]])

        st.success(
            f"Envio automático concluído: {sucessos}/{total} mensagens enviadas com sucesso."
        )

else:

    st.info(
        "Carregue uma planilha e escreva uma mensagem para habilitar o envio automático."
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
