# ==========================================
# GERENCIADOR DE FILA DE MENSAGENS
# ==========================================

from datetime import datetime


class FilaMensagens:


    def __init__(self):

        self.fila = []



    def adicionar(
        self,
        telefone,
        nome,
        mensagem
    ):

        item = {

            "telefone": telefone,

            "nome": nome,

            "mensagem": mensagem,

            "status": "pendente",

            "criado_em": datetime.now()

        }


        self.fila.append(item)



    def listar(self):

        return self.fila



    def pendentes(self):

        return [

            item

            for item in self.fila

            if item["status"] == "pendente"

        ]



    def atualizar_status(
        self,
        telefone,
        status
    ):

        for item in self.fila:


            if item["telefone"] == telefone:

                item["status"] = status



    def limpar(self):

        self.fila = []
