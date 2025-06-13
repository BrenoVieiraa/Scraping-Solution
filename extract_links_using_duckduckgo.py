import urllib.parse
from urllib.parse import urlparse
from seleniumbase import SB
from bs4 import BeautifulSoup
from typing import List

def is_valid_url(url):
    exclusions = [
        "https://duckduckgo.com",
        "https://www.duckduckgo.com",
        "https://www.instagram.com",
        "https://www.facebook.com"
    ]
    return url not in exclusions

def extract_links_using_duckduckgo_regex(text_to_find: str, pages: int) -> List[str]:
    query = urllib.parse.quote_plus(text_to_find)
    base_url = f"https://duckduckgo.com/?q={query}&t=h_&ia=web"

    print("--> [SELENIUM] Inicializando o navegador...")
    # --- MUDANÇA PRINCIPAL: Adicionado no_sandbox=True ---
    with SB(uc=True, headless=True, no_sandbox=True) as sb:
        print("--> [SELENIUM] Navegador iniciado. Abrindo URL do DuckDuckGo...")
        sb.open(base_url)
        sb.sleep(3)
        print("--> [SELENIUM] Página aberta. Procurando mais resultados...")

        for page in range(pages):
            print(f"--> [SELENIUM] Carregando mais resultados... {page + 1}")
            sb.scroll_to_bottom()
            sb.sleep(2)
            if sb.is_element_visible("#more-results"):
                sb.click("#more-results")
                sb.sleep(2)
            else:
                print("--> [SELENIUM] Não há mais botão de 'mais resultados'.")
                break
        
        print("--> [SELENIUM] Buscando o código fonte da página...")
        soup = BeautifulSoup(sb.get_page_source(), "html.parser")
        article_elements = soup.find_all("article")
        results = []

        for article in article_elements:
            title_span = article.select_one("div:nth-of-type(3) h2 a span")
            href = title_span.find_parent("a")["href"] if title_span else ''
            parsed = urlparse(href)
            base_link = f"{parsed.scheme}://{parsed.netloc}"

            if base_link and is_valid_url(base_link) and base_link not in results:
                results.append(base_link)

        print(f"--> [SELENIUM] Extração de links finalizada. {len(results)} links únicos encontrados.")
        return results