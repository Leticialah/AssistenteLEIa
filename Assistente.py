import re
import threading
import time
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import ttk, messagebox
import urllib.parse
import time

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


@dataclass
class Config:
    user_name: str
    monitor_url: str
    selector_type: str          # "css" ou "xpath"
    selector_value: str
    check_interval: float
    page_timeout_ms: int
    gmail_recipient: str
    chrome_profile_dir: str = "./chrome_profile"


def validate_name(name: str) -> None:
    name = name.strip()
    if len(name) < 3:
        raise ValueError("O nome deve ter pelo menos 3 caracteres.")
    if not re.fullmatch(r"[A-Za-zÀ-ÿ]+(?:\s+[A-Za-zÀ-ÿ]+)*", name):
        raise ValueError("O nome deve conter apenas letras e espaços.")


def validate_config(cfg: Config) -> None:
    validate_name(cfg.user_name)

    if not cfg.monitor_url.startswith(("http://", "https://")):
        raise ValueError("URL inválida. Use http:// ou https://")

    if cfg.selector_type not in {"css", "xpath"}:
        raise ValueError("Tipo de seletor inválido. Use 'css' ou 'xpath'.")

    if not cfg.selector_value.strip():
        raise ValueError("O seletor não pode ser vazio.")

    if cfg.check_interval <= 0:
        raise ValueError("O intervalo deve ser maior que zero.")

    if cfg.page_timeout_ms <= 0:
        raise ValueError("O timeout deve ser maior que zero.")

    if "@" not in cfg.gmail_recipient or "." not in cfg.gmail_recipient:
        raise ValueError("E-mail de destino inválido.")


def build_locator(page, selector_type: str, selector_value: str):
    if selector_type == "css":
        return page.locator(selector_value)
    return page.locator(f"xpath={selector_value}")


def extract_number(text: str) -> float:
    raw = text.strip()
    if not raw:
        raise ValueError("Texto vazio no elemento monitorado.")

    cleaned = re.sub(r"[^\d,.\- ]+", " ", raw)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    candidates = re.findall(r"\d[\d.,]*", cleaned)
    if not candidates:
        raise ValueError(f"Nenhum número encontrado em: {raw!r}")

    best = max(candidates, key=len)

    if "," in best and "." in best:
        if best.rfind(",") > best.rfind("."):
            best = best.replace(".", "").replace(",", ".")
        else:
            best = best.replace(",", "")
    elif "," in best:
        if best.count(",") == 1:
            best = best.replace(".", "").replace(",", ".")
        else:
            best = best.replace(".", "").replace(",", "")
    else:
        best = best.replace(",", "")

    return float(best)


def read_value(page, selector_type: str, selector_value: str, timeout_ms: int, log=print) -> float:
    locator = build_locator(page, selector_type, selector_value)
    locator.first.wait_for(state="visible", timeout=timeout_ms)

    text = locator.first.text_content()
    if not text or not text.strip():
        text = locator.first.inner_text()

    if not text or not text.strip():
        raise ValueError("Elemento encontrado, mas o texto está vazio.")

    log(f"Valor monitorado: {text!r}")
    value = extract_number(text)
    return value

def send_gmail_message(context, recipient: str, new_value: float, timeout_ms: int, log=print) -> None:
    gmail_page = context.new_page()

    try:
        log("Informação confirmada. Abrindo Gmail...")

        assunto = urllib.parse.quote("Atenção!")
        mensagem = urllib.parse.quote(f"valor alterado para: {new_value}")
        destinatario = urllib.parse.quote(recipient)

        url = (
            f"https://mail.google.com/mail/?view=cm&fs=1"
            f"&to={destinatario}"
            f"&su={assunto}"
            f"&body={mensagem}"
        )

        gmail_page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)

        # espera carregar
        gmail_page.wait_for_timeout(5000)

        log("5 segundos para envio...")

        # botão enviar
        send_button = gmail_page.locator(
            'div[role="button"][data-tooltip*="Enviar"], '
            'div[role="button"][data-tooltip*="Send"]'
        ).first

        send_button.wait_for(state="visible", timeout=timeout_ms)

        log("Enviando informação...")
        send_button.click()

        # espera confirmar envio
        gmail_page.wait_for_timeout(5000)

        log("E-mail enviado com sucesso.")

    except Exception as e:
        log(f"Erro ao enviar email: {e}")

    finally:
        gmail_page.close()

class AuctionMonitorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Assistente LEIa")
        self.root.geometry("860x700")

        self.monitor_thread = None
        self.stop_event = threading.Event()

        self._build_ui()
        self.log(
            "Bem-vindo(a) ao Assistente LEIa!\n" 
            "Passos para usar:\n"
            "1) Faça login no Gmail (botão 'Abrir Gmail').\n"
            "2) Insira a URL da página.\n"
            "3) Informe o seletor (CSS ou XPath) do valor a ser monitorado.\n"
            "4) Verifique se o valor está sendo capturado corretamente.\n"
            "5) Adicione o e-mail que receberá o alerta.\n"
            "6) Clique em 'Iniciar Monitoramento'."
            )
        
    def _build_ui(self):
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill="both", expand=True)

        form = ttk.LabelFrame(main, text="Configuração", padding=12)
        form.pack(fill="x")

        ttk.Label(form, text="Nome do usuário").grid(row=0, column=0, sticky="w", pady=4)
        self.user_name_var = tk.StringVar(value="Lav")
        ttk.Entry(form, textvariable=self.user_name_var, width=50).grid(row=0, column=1, sticky="ew", pady=4)

        ttk.Label(form, text="URL da página a monitorar").grid(row=1, column=0, sticky="w", pady=4)
        self.url_var = tk.StringVar(value="https://br.tradingview.com/symbols/BTCUSD/")
        ttk.Entry(form, textvariable=self.url_var, width=50).grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(form, text="Timeout (segundos)").grid(row=2, column=0, sticky="w", pady=4)
        self.timeout_var = tk.StringVar(value="20")
        ttk.Entry(form, textvariable=self.timeout_var, width=20).grid(row=2, column=1, sticky="w", pady=4)

        ttk.Label(form, text="Intervalo (segundos)").grid(row=3, column=0, sticky="w", pady=4)
        self.interval_var = tk.StringVar(value="5")
        ttk.Entry(form, textvariable=self.interval_var, width=20).grid(row=3, column=1, sticky="w", pady=4)

        ttk.Label(form, text="Tipo de localização").grid(row=4, column=0, sticky="w", pady=4)
        self.selector_type_var = tk.StringVar(value="css")
        selector_type_combo = ttk.Combobox(
            form,
            textvariable=self.selector_type_var,
            values=["css", "xpath"],
            state="readonly",
            width=20
        )
        selector_type_combo.grid(row=4, column=1, sticky="w", pady=4)

        ttk.Label(form, text="Seletor").grid(row=5, column=0, sticky="w", pady=4)
        self.selector_value_var = tk.StringVar(value='span[data-qa-id="symbol-last-value"]')
        ttk.Entry(form, textvariable=self.selector_value_var, width=50).grid(row=5, column=1, sticky="ew", pady=4)

        ttk.Label(form, text="E-mail de destino").grid(row=6, column=0, sticky="w", pady=4)
        self.recipient_var = tk.StringVar(value="destinatario@gmail.com")
        ttk.Entry(form, textvariable=self.recipient_var, width=50).grid(row=6, column=1, sticky="ew", pady=4)

        form.columnconfigure(1, weight=1)

        buttons = ttk.Frame(main, padding=(0, 12))
        buttons.pack(fill="x")

        ttk.Button(buttons, text="Abrir Gmail / Fazer login", command=self.open_gmail_login).pack(side="left", padx=4)
        ttk.Button(buttons, text="Testar leitura do valor", command=self.test_read_value).pack(side="left", padx=4)
        ttk.Button(buttons, text="Iniciar monitoramento", command=self.start_monitoring).pack(side="left", padx=4)
        ttk.Button(buttons, text="Parar monitoramento", command=self.stop_monitoring).pack(side="left", padx=4)

        log_frame = ttk.LabelFrame(main, text="Log", padding=12)
        log_frame.pack(fill="both", expand=True)

        self.log_text = tk.Text(log_frame, wrap="word", height=22)
        self.log_text.pack(fill="both", expand=True)

    def log(self, message: str):
        timestamp = time.strftime("[%H:%M:%S]")
        full = f"{timestamp} {message}\n"
        self.log_text.insert("end", full)
        self.log_text.see("end")
        print(full, end="")

    def get_config(self) -> Config:
        try:
            timeout_s = float(self.timeout_var.get().strip())
            interval_s = float(self.interval_var.get().strip())
        except ValueError:
            raise ValueError("Timeout e intervalo devem ser numéricos.")

        cfg = Config(
            user_name=self.user_name_var.get().strip(),
            monitor_url=self.url_var.get().strip(),
            selector_type=self.selector_type_var.get().strip(),
            selector_value=self.selector_value_var.get().strip(),
            check_interval=interval_s,
            page_timeout_ms=int(timeout_s * 1000),
            gmail_recipient=self.recipient_var.get().strip(),
            chrome_profile_dir="./chrome_profile",
        )
        validate_config(cfg)
        return cfg

    def open_gmail_login(self):
        try:
            Path("./chrome_profile").mkdir(parents=True, exist_ok=True)

            self.log("Abrindo Gmail...")
            self.log("Faça login manualmente no Gmail nessa janela, depois feche o navegador.")

            with sync_playwright() as p:
                context = p.chromium.launch_persistent_context(
                    user_data_dir="./chrome_profile",
                    headless=False,
                    slow_mo=200,
                )
                page = context.new_page()
                page.goto("https://mail.google.com/mail/u/0/#inbox", wait_until="domcontentloaded", timeout=30000)

                try:
                    while True:
                        page.wait_for_timeout(1000)
                except Exception:
                    pass
                finally:
                    try:
                        context.close()
                    except Exception:
                        pass

            self.log("Janela do Gmail encerrada.")
        except Exception as e:
            self.log(f"Erro ao abrir Gmail: {e}")

    def test_read_value(self):
        try:
            cfg = self.get_config()
            self.log("Testando leitura do valor...")

            with sync_playwright() as p:
                context = p.chromium.launch_persistent_context(
                    user_data_dir=cfg.chrome_profile_dir,
                    headless=False,
                    slow_mo=100,
                )
                try:
                    page = context.new_page()
                    self.log("Abrindo site monitorado...")
                    page.goto(cfg.monitor_url, wait_until="domcontentloaded", timeout=cfg.page_timeout_ms)

                    value = read_value(
                        page,
                        cfg.selector_type,
                        cfg.selector_value,
                        cfg.page_timeout_ms,
                        log=self.log
                    )
                    self.log(f"Valor numérico identificado: {value}")
                finally:
                    context.close()

        except Exception as e:
            self.log(f"Erro no teste de leitura: {e}")
            messagebox.showerror("Erro", str(e))

    def start_monitoring(self):
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.log("O monitoramento já está em execução.")
            return

        try:
            cfg = self.get_config()

            self.log(f"{cfg.user_name} iniciou o monitoramento.")
            self.log(f"URL monitorada: {cfg.monitor_url}")
            self.log(f"Seletor usado: {cfg.selector_type} = {cfg.selector_value}")

        except Exception as e:
            self.log(f"Erro de validação: {e}")
            messagebox.showerror("Erro", str(e))
            return

        self.stop_event.clear()
        self.monitor_thread = threading.Thread(target=self.monitor_worker, args=(cfg,), daemon=True)
        self.monitor_thread.start()
        self.log("O monitoramento iniciado.")

    def stop_monitoring(self):
        self.stop_event.set()
        self.log("Solicitação de parada recebida.")

    def monitor_worker(self, cfg: Config):
        try:
            self.log("Configuração validada com sucesso.")
            Path(cfg.chrome_profile_dir).mkdir(parents=True, exist_ok=True)

            with sync_playwright() as p:
                context = p.chromium.launch_persistent_context(
                    user_data_dir=cfg.chrome_profile_dir,
                    headless=False,
                    slow_mo=100,
                )

                try:
                    page = context.new_page()
                    self.log("Abrindo página monitorada...")
                    page.goto(cfg.monitor_url, wait_until="domcontentloaded", timeout=cfg.page_timeout_ms)

                    current_value = read_value(
                        page,
                        cfg.selector_type,
                        cfg.selector_value,
                        cfg.page_timeout_ms,
                        log=self.log
                    )
                    self.log(f"Valor inicial: {current_value}")

                    while not self.stop_event.is_set():
                        time.sleep(cfg.check_interval)

                        try:
                            page.reload(wait_until="domcontentloaded", timeout=cfg.page_timeout_ms)

                            new_value = read_value(
                                page,
                                cfg.selector_type,
                                cfg.selector_value,
                                cfg.page_timeout_ms,
                                log=self.log
                            )

                            if new_value != current_value:
                                old_value = current_value
                                current_value = new_value

                                self.log(f"ALTERAÇÃO detectada: {old_value} -> {new_value}")

                                send_gmail_message(
                                    context=context,
                                    recipient=cfg.gmail_recipient,
                                    new_value=new_value,
                                    timeout_ms=cfg.page_timeout_ms,
                                    log=self.log
                                )
                            else:
                                self.log(f"Sem alteração. Valor atual: {current_value}")

                        except PlaywrightTimeoutError:
                            self.log("Timeout ao localizar elemento ou recarregar a página. Tentando novamente...")
                        except Exception as e:
                            self.log(f"Erro durante o monitoramento: {e}")

                finally:
                    context.close()

        except Exception as e:
            self.log(f"Falha crítica: {e}")
            messagebox.showerror("Erro crítico", str(e))
        finally:
            self.log("Monitoramento interrompido.")


def main():
    root = tk.Tk()
    app = AuctionMonitorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
