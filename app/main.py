from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from scraper import get_text_markdown
import logging

# Configurar logging para registrar erros e informações
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API de Scraping com Playwright")

class URLs(BaseModel):
    urls: List[str]

@app.post("/scrape")
def scrape(urls: URLs):
    resultados = {}
    for url in urls.urls:
        try:
            markdown = get_text_markdown(url)
            resultados[url] = markdown
        except Exception as e:
            logger.exception(f"Erro ao processar a URL {url}: {str(e)}")
            resultados[url] = f"Erro: {str(e)}"
    return resultados
