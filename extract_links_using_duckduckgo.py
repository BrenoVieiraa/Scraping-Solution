import os
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

# --- MUDANÇA: A função agora retorna a lista de links ---
def extract_links_using_duckduckgo_regex(text_to_find: str, pages: int) -> List[str]:
    query = urllib.parse.quote_plus(text_to_find)
    base_url = f"https://duckduckgo.com/?q={query}&t=h_&ia=web"

    with SB(uc=True, headless=True) as sb:
        print("Opening browser...")
        sb.open(base_url)
        sb.sleep(3)

        for page in range(pages):
            print(f"Loading more results... {page + 1}")
            sb.scroll_to_bottom()
            sb.sleep(2)
            if sb.is_element_visible("#more-results"):
                sb.click("#more-results")
                sb.sleep(2)
            else:
                break

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

        # --- MUDANÇA: Remove a parte que salva em CSV e retorna a lista ---
        print(f"Extração de links finalizada. {len(results)} links únicos encontrados.")
        return results