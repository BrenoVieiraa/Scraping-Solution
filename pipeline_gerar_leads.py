from extract_links_using_duckduckgo import extract_links_using_duckduckgo_regex
from extract_data_from_any_site_using_regex import scrape_data_from_url
from typing import List, Dict

# --- MUDANÇA: A função agora aceita parâmetros e retorna dados ---
def run_pipeline(text_to_find: str, pages: int) -> List[Dict]:
    
    print("[1] Extraindo links com DuckDuckGo...")
    # --- MUDANÇA: Recebe a lista de links em vez de salvar em arquivo ---
    links_encontrados = extract_links_using_duckduckgo_regex(text_to_find, pages)
    
    if not links_encontrados:
        print("Nenhum link encontrado pelo DuckDuckGo.")
        return []

    print(f"[2] {len(links_encontrados)} links encontrados. Extraindo dados dos sites...")
    
    todos_os_leads = []
    for link in links_encontrados:
        print(f"Processando: {link}")
        # --- MUDANÇA: Chama o scraper para cada link e recebe os dados ---
        dados_do_site = scrape_data_from_url(link)
        if dados_do_site:
            todos_os_leads.append(dados_do_site)

    print(f"[3] Pipeline finalizado! {len(todos_os_leads)} leads encontrados.")
    # --- MUDANÇA: Retorna a lista completa de leads ---
    return todos_os_leads