import os
from extract_links_using_duckduckgo import extract_links_using_duckduckgo_regex
from extract_data_from_any_site_using_regex import extract_data_from_any_site_using_regex

def run_pipeline():
    text_to_find = "moda feminina sao paulo"
    pages = 5

    print("[1] Extraindo links com DuckDuckGo...")
    extract_links_using_duckduckgo_regex(text_to_find, pages)

    print("[2] Extraindo dados dos sites...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_data_path = os.path.join("data", "processed", f"{text_to_find.replace(' ', '_')}.csv")
    processed_data_dir = os.path.join("data", "processed")

    extract_data_from_any_site_using_regex(raw_data=raw_data_path, processed_data_dir=processed_data_dir)
    print("[3] Pipeline finalizado com sucesso!")

if __name__ == "__main__":
    run_pipeline()
