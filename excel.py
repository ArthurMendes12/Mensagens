# ==========================================
# LEITOR E TRATAMENTO DE PLANILHAS
# ==========================================

import pandas as pd
from config import PHONE_COLUMN, NAME_COLUMN


def carregar_planilha(caminho_arquivo):
    """
    Lê uma planilha XLSX e retorna os contatos tratados.
    """

    try:
        # Lê o arquivo Excel
        df = pd.read_excel(caminho_arquivo)

    except Exception as erro:
        raise Exception(f"Erro ao abrir a planilha: {erro}")


    # Verifica se as colunas existem
    colunas_obrigatorias = [
        PHONE_COLUMN,
        NAME_COLUMN
    ]

    for coluna in colunas_obrigatorias:
        if coluna not in df.columns:
            raise Exception(
                f"A coluna '{coluna}' não foi encontrada na planilha."
            )


    # Remove linhas sem telefone
    df = df.dropna(subset=[PHONE_COLUMN])


    # Remove espaços extras
    df[NAME_COLUMN] = (
        df[NAME_COLUMN]
        .fillna("")
        .astype(str)
        .str.strip()
    )


    # Trata os telefones
    df[PHONE_COLUMN] = (
        df[PHONE_COLUMN]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.replace(" ", "")
        .str.replace("-", "")
        .str.replace("(", "")
        .str.replace(")", "")
    )


    # Remove telefones duplicados
    df = df.drop_duplicates(
        subset=[PHONE_COLUMN]
    )


    # Reseta o índice
    df = df.reset_index(drop=True)


    return df



def quantidade_contatos(df):
    """
    Retorna a quantidade de contatos encontrados.
    """

    return len(df)
