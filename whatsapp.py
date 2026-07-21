# ==========================================
# WHATSAPP - ABRIR CONVERSA
# ==========================================

import urllib.parse
import webbrowser
from datetime import datetime



class WhatsAppService:


    def __init__(self):

        self.historico = []



    def limpar_numero(
        self,
        telefone
    ):

        telefone = str(telefone)


        caracteres = [
            " ",
            "-",
            "(",
            ")",
            "+"
        ]


        for caractere in caracteres:

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


        mensagem = urllib.parse.quote(
            mensagem
        )


        link = (
            f"https://wa.me/{telefone}"
            f"?text={mensagem}"
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


        webbrowser.open(
            link
        )


        registro = {

            "telefone": telefone,

            "mensagem": mensagem,

            "data": datetime.now(),

            "status": "aberto"

        }


        self.historico.append(
            registro
        )


        return link



    def obter_historico(self):

        return self.historico
