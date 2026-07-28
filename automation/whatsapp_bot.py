# ==========================================
# BOT PLAYWRIGHT - ENVIO AUTOMATICO VIA WHATSAPP WEB
# ==========================================

import re
import time
import urllib.parse

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from config import SESSION_FOLDER


SELETOR_CAIXA_MENSAGEM = 'footer div[contenteditable="true"]'
SELETOR_QR_CODE = 'canvas[aria-label]'
TEXTO_BOTAO_CONTINUAR = re.compile(
    r"Continue to Chat|Continuar para o chat|Continuar",
    re.IGNORECASE,
)


class WhatsAppBot:
    """Controla uma sessao local e persistente do WhatsApp Web."""

    def __init__(self, headless=False):
        self.headless = headless
        self._playwright = None
        self._context = None
        self._page = None

    def iniciar(self):
        """Abre o WhatsApp Web e espera a sessao existente ou o QR Code."""
        self._playwright = sync_playwright().start()
        self._context = self._playwright.chromium.launch_persistent_context(
            SESSION_FOLDER,
            headless=self.headless,
        )
        self._page = (
            self._context.pages[0]
            if self._context.pages
            else self._context.new_page()
        )
        self._page.goto("https://web.whatsapp.com")
        self._page.wait_for_selector(
            f"#pane-side, {SELETOR_QR_CODE}",
            timeout=120_000,
        )

    def esta_conectado(self):
        """Retorna True quando a lista de conversas esta disponivel."""
        return bool(
            self._page
            and self._page.locator("#pane-side").is_visible(timeout=1_000)
        )

    def obter_qr_code(self):
        """Captura o QR Code atual como imagem em bytes.

        Retorna None quando a conta ja esta conectada ou o QR ainda nao foi
        carregado. A interface pode entregar esses bytes diretamente a
        ``st.image()`` no Streamlit.
        """
        if not self._page or self.esta_conectado():
            return None

        qr_code = self._page.locator(SELETOR_QR_CODE)

        if not qr_code.is_visible(timeout=1_000):
            return None

        return qr_code.screenshot()

    def aguardar_conexao(self, callback_qr=None, timeout=120):
        """Aguarda o escaneamento do QR Code.

        O WhatsApp renova o QR Code periodicamente. Quando informado,
        ``callback_qr`` recebe cada imagem atualizada para a tela exibi-la.
        """
        limite = time.time() + timeout

        while time.time() < limite:
            if self.esta_conectado():
                return True

            qr_code = self.obter_qr_code()

            if qr_code and callback_qr:
                callback_qr(qr_code)

            self._page.wait_for_timeout(2_000)

        return self.esta_conectado()

    def enviar_mensagem(self, telefone, mensagem, timeout=30_000):
        """Abre o chat do contato e envia a mensagem pre-preenchida."""
        if self._page is None:
            raise RuntimeError("Chame iniciar() antes de enviar mensagens.")

        if not self.esta_conectado():
            return False, "WhatsApp nao esta conectado."

        try:
            telefone_limpo = re.sub(r"\D", "", str(telefone))
            mensagem_codificada = urllib.parse.quote(mensagem)
            link = f"https://wa.me/{telefone_limpo}?text={mensagem_codificada}"

            self._page.goto(link)

            try:
                self._page.get_by_role(
                    "link",
                    name=TEXTO_BOTAO_CONTINUAR,
                ).click(timeout=5_000)
            except PlaywrightTimeoutError:
                pass

            caixa_mensagem = self._page.locator(SELETOR_CAIXA_MENSAGEM).last
            caixa_mensagem.wait_for(timeout=timeout)
            caixa_mensagem.press("Enter")
            self._page.wait_for_timeout(1_500)

            return True, None

        except Exception as erro:
            return False, str(erro)

    def fechar(self):
        if self._context:
            self._context.close()
            self._context = None

        if self._playwright:
            self._playwright.stop()
            self._playwright = None

        self._page = None
