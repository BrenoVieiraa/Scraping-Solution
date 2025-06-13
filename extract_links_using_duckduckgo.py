import os
import urllib.parse
from urllib.parse import urlparse
from seleniumbase import SB
from bs4 import BeautifulSoup

def is_valid_url(url):
    exclusions = [
        "https://duckduckgo.com",
        "https://www.duckduckgo.com",
        "https://www.instagram.com",
        "https://www.facebook.com"
    ]
    return url not in exclusions

def extract_links_using_duckduckgo_regex(text_to_find, pages):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data", "processed")
    os.makedirs(data_dir, exist_ok=True)

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

        csv_output = "\n".join(results)
        output_file = os.path.join(data_dir, f"{text_to_find.replace(' ', '_')}.csv")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(csv_output)

        print(f"Extracted data saved to {output_file}")

if __name__ == "__main__":
    extract_links_using_duckduckgo_regex("moda feminina sao paulo", 5)
