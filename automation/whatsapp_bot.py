# ==========================================
# BOT PLAYWRIGHT - ENVIO AUTOMÁTICO VIA WA.ME
# ==========================================

import re
import urllib.parse

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from config import SESSION_FOLDER


# Seletor da caixa de digitação do chat aberto no WhatsApp Web.
# Pode precisar de ajuste caso o WhatsApp altere o HTML da página.
SELETOR_CAIXA_MENSAGEM = 'footer div[contenteditable="true"]'

# Texto do botão intermediário que o wa.me exibe antes de abrir o chat.
TEXTO_BOTAO_CONTINUAR = re.compile(
    r"Continue to Chat|Continuar para o chat|Continuar",
    re.IGNORECASE
)


class WhatsAppBot:
    """
    Controla um navegador (via Playwright) logado no WhatsApp Web
    para enviar mensagens automaticamente através de links wa.me.
    """

    def __init__(self, headless=False):
        self.headless = headless
        self._playwright = None
        self._context = None
        self._page = None

    def iniciar(self):
        """
        Abre o navegador com uma sessão persistente (pasta SESSION_FOLDER).
        Na primeira execução é necessário escanear o QR Code manualmente;
        nas próximas, a sessão já estará logada.
        """

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

        # Espera a lista de conversas (ou o QR Code) carregar.
        self._page.wait_for_selector(
            '#pane-side, canvas[aria-label]',
            timeout=120_000,
        )

    def enviar_mensagem(self, telefone, mensagem, timeout=30_000):
        """
        Abre o link wa.me do contato e envia a mensagem.
        Retorna (sucesso: bool, erro: str | None).
        """

        if self._page is None:
            raise RuntimeError("Chame iniciar() antes de enviar mensagens.")

        try:
            mensagem_codificada = urllib.parse.quote(mensagem)
            link = f"https://wa.me/{telefone}?text={mensagem_codificada}"

            self._page.goto(link)

            try:
                self._page.get_by_role(
                    "link", name=TEXTO_BOTAO_CONTINUAR
                ).click(timeout=5_000)
            except PlaywrightTimeoutError:
                pass

            caixa_mensagem = self._page.locator(SELETOR_CAIXA_MENSAGEM).last
            caixa_mensagem.wait_for(timeout=timeout)

            caixa_mensagem.press("Enter")

            self._page.wait_for_timeout(1500)

            return True, None

        except Exception as erro:
            return False, str(erro)

    def fechar(self):
        if self._context:
            self._context.close()

        if self._playwright:
            self._playwright.stop()
