# ==========================================
# SISTEMA DE LOGS E RELATÓRIOS
# ==========================================

import os
import pandas as pd
from datetime import datetime

from config import LOG_FOLDER


# Arquivo onde os logs serão salvos
ARQUIVO_LOG = os.path.join(
    LOG_FOLDER,
    "historico_envios.xlsx"
)



def registrar_envio(
    telefone,
    mensagem,
    status,
    erro=None
):
    """
    Registra uma tentativa de envio.
    """

    novo_registro = {

        "data_hora": datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        ),

        "telefone": telefone,

        "mensagem": mensagem,

        "status": status,

        "erro": erro if erro else ""

    }


    # Se já existe histórico, adiciona
    if os.path.exists(ARQUIVO_LOG):

        df = pd.read_excel(
            ARQUIVO_LOG
        )

        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    [novo_registro]
                )
            ],
            ignore_index=True
        )


    else:

        df = pd.DataFrame(
            [novo_registro]
        )


    # Salva novamente
    df.to_excel(
        ARQUIVO_LOG,
        index=False
    )



def carregar_logs():
    """
    Retorna o histórico completo.
    """

    if os.path.exists(ARQUIVO_LOG):

        return pd.read_excel(
            ARQUIVO_LOG
        )


    return pd.DataFrame(
        columns=[
            "data_hora",
            "telefone",
            "mensagem",
            "status",
            "erro"
        ]
    )



def limpar_logs():
    """
    Apaga todo histórico.
    """

    if os.path.exists(ARQUIVO_LOG):

        os.remove(
            ARQUIVO_LOG
        )



def resumo_envios():
    """
    Retorna um resumo dos envios.
    """

    df = carregar_logs()


    if df.empty:

        return {
            "total": 0,
            "sucesso": 0,
            "erro": 0
        }


    total = len(df)


    sucesso = len(
        df[
            df["status"] == "sucesso"
        ]
    )


    erro = len(
        df[
            df["status"] == "erro"
        ]
    )


    return {

        "total": total,

        "sucesso": sucesso,

        "erro": erro

    }
