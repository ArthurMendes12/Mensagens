# ==========================================
# WHATSAPP - GERADOR DE LINK
# ==========================================

import urllib.parse
from datetime import datetime


class WhatsAppService:


    def __init__(self):

        self.historico = []



    def limpar_numero(
        self,
        telefone
    ):

        telefone = str(telefone)


        remover = [
            " ",
            "-",
            "(",
            ")",
            "+"
        ]


        for caractere in remover:

            telefone = telefone.replace(
                caractere,
                ""
            )


        return telefone



    def criar_link(
        self,
        telefone,
        mensagem
    ):

        telefone = self.limpar_numero(
            telefone
        )


        mensagem_codificada = urllib.parse.quote(
            mensagem
        )


        link = (
            f"https://wa.me/{telefone}"
            f"?text={mensagem_codificada}"
        )


        return link



    def abrir_whatsapp(
        self,
        telefone,
        mensagem
    ):


        link = self.criar_link(
            telefone,
            mensagem
        )


        self.historico.append({

            "telefone": telefone,

            "mensagem": mensagem,

            "data": datetime.now(),

            "status": "link criado"

        })


        return link



    def obter_historico(self):

        return self.historico
