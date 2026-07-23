# ==========================================
# ENVIADOR AUTOMÁTICO - ORQUESTRA FILA + BOT
# ==========================================

import random
import time

from config import MIN_DELAY, MAX_DELAY
from mensagens import personalizar_mensagem
from logs import registrar_envio
from automation.whatsapp_bot import WhatsAppBot


class EnviadorAutomatico:
    """
    Percorre os contatos de um DataFrame e envia as mensagens
    automaticamente via WhatsApp Web (Playwright), respeitando
    um intervalo aleatório entre envios para reduzir o risco de bloqueio.
    """

    def __init__(self, headless=False):
        self.bot = WhatsAppBot(headless=headless)

    def iniciar(self):
        self.bot.iniciar()

    def enviar_para_todos(self, df, mensagem_template, callback=None):
        """
        Envia a mensagem personalizada para cada contato do df.

        callback(posicao, total, nome, telefone, sucesso, erro) é chamado
        após cada tentativa, útil para atualizar a UI do Streamlit.
        """

        resultados = []

        total = len(df)

        for posicao, (indice, contato) in enumerate(df.iterrows()):

            texto = personalizar_mensagem(mensagem_template, contato)

            nome = contato["nome"]
            telefone = contato["telefone"]

            sucesso, erro = self.bot.enviar_mensagem(telefone, texto)

            status = "sucesso" if sucesso else "erro"

            registrar_envio(telefone, texto, status, erro)

            resultados.append({
                "indice": indice,
                "nome": nome,
                "telefone": telefone,
                "sucesso": sucesso,
                "erro": erro,
            })

            if callback:
                callback(posicao, total, nome, telefone, sucesso, erro)

            if posicao < total - 1:
                time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

        return resultados

    def fechar(self):
        self.bot.fechar()
