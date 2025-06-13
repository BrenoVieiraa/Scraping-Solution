from extract_links_using_duckduckgo import extract_links_using_duckduckgo_regex
from extract_data_from_any_site_using_regex import scrape_data_from_url
from typing import List, Dict

def run_pipeline(text_to_find: str, pages: int) -> List[Dict]:
    
    print("--- INÍCIO DO PIPELINE ---")
    print(f"[1] Extraindo links para o termo: '{text_to_find}'...")
    
    links_encontrados = extract_links_using_duckduckgo_regex(text_to_find, pages)
    
    if not links_encontrados:
        print("Nenhum link encontrado pelo DuckDuckGo. Finalizando.")
        return []

    print(f"--- Links extraídos com sucesso: {len(links_encontrados)} links ---")
    print("[2] Iniciando extração de dados dos sites...")
    
    todos_os_leads = []
    for i, link in enumerate(links_encontrados):
        print(f"--> Processando link {i+1}/{len(links_encontrados)}: {link}")
        dados_do_site = scrape_data_from_url(link)
        if dados_do_site:
            todos_os_leads.append(dados_do_site)

    print(f"--- Extração de dados finalizada ---")
    print(f"[3] Pipeline finalizado! {len(todos_os_leads)} leads encontrados.")
    return todos_os_leads