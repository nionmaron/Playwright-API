import random
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
import logging

# Configurar logging para registrar erros e informações
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lista de User-Agents para rotacionar
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/112.0.0.0 Safari/537.36",
    # Adicione mais user-agents conforme necessário
]

def get_text_markdown(url):
    with sync_playwright() as p:
        # Selecionar um User-Agent aleatório
        user_agent = random.choice(USER_AGENTS)
        
        # Usar um navegador Chromium com configurações mais realistas
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=user_agent,
            viewport={"width": 1280, "height": 720},
            locale="pt-BR",
            java_script_enabled=True
        )
        page = context.new_page()
        try:
            logger.info(f"Acessando URL: {url} com User-Agent: {user_agent}")
            response = page.goto(url, timeout=60000, wait_until='networkidle')
            
            # Verificar se houve um redirecionamento
            final_url = page.url
            if final_url != url:
                logger.info(f"Redirecionado para: {final_url}")
                url = final_url

            # Verificar o status da resposta
            if response and response.status >= 400:
                logger.error(f"Erro HTTP {response.status} ao acessar {url}")
                return f"Erro HTTP {response.status} ao acessar {url}"

            # Verificar se a página solicitou ativar o JavaScript
            content = page.content()
            if "ativa o JavaScript" in content or "activate JavaScript" in content:
                logger.warning(f"JavaScript não está funcionando corretamente em {url}")
                return f"Erro: A página {url} solicita a ativação do JavaScript."

            # Extraindo apenas as tags h1, h2, h3 e p
            selected_html = page.evaluate("""
                () => {
                    const elements = document.querySelectorAll('h1, h2, h3, p');
                    let content = '';
                    elements.forEach(el => {
                        content += el.outerHTML + '\\n';
                    });
                    return content;
                }
            """)
            
            if not selected_html.strip():
                logger.warning(f"Nenhum conteúdo encontrado nas tags h1, h2, h3 e p em {url}")
                return f"Erro: Nenhum conteúdo encontrado nas tags h1, h2, h3 e p em {url}."

            # Parsear o HTML selecionado com BeautifulSoup
            soup = BeautifulSoup(selected_html, 'html.parser')

            # Construir o Markdown manualmente
            markdown_lines = []
            for tag in soup.find_all(['h1', 'h2', 'h3', 'p']):
                if tag.name == 'h1':
                    markdown_lines.append(f"# {tag.get_text(strip=True)}\n")
                elif tag.name == 'h2':
                    markdown_lines.append(f"## {tag.get_text(strip=True)}\n")
                elif tag.name == 'h3':
                    markdown_lines.append(f"### {tag.get_text(strip=True)}\n")
                elif tag.name == 'p':
                    paragraph = tag.get_text(strip=True)
                    if paragraph:
                        markdown_lines.append(f"{paragraph}\n")
            
            # Juntar todas as linhas de Markdown
            markdown = "\n".join(markdown_lines).strip()
            
            # Introduzir um atraso aleatório entre 2 a 5 segundos para simular comportamento humano
            delay = random.uniform(2, 5)
            logger.info(f"Esperando {delay:.2f} segundos antes da próxima requisição.")
            time.sleep(delay)
            
            return markdown

        except PlaywrightTimeoutError:
            logger.error(f"Timeout ao tentar acessar {url}")
            return f"Erro: Timeout ao tentar acessar {url}."
        except Exception as e:
            logger.exception(f"Erro ao processar a URL {url}: {str(e)}")
            return f"Erro ao processar a URL {url}: {str(e)}"
        finally:
            context.close()
            browser.close()
