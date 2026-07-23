# ==========================================
# PERSONALIZAÇÃO DE MENSAGENS
# ==========================================


def personalizar_mensagem(template, contato):
    """
    Substitui {coluna} no template pelos valores do contato.
    """

    texto = template

    for coluna in contato.index:
        texto = texto.replace("{" + coluna + "}", str(contato[coluna]))

    return texto
