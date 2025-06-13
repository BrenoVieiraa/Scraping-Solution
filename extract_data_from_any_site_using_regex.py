import re
import os
import json
import asyncio
import nest_asyncio
from requests_html import HTMLSession

# Ajustar loop e aplicar nest_asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

nest_asyncio.apply()

def clear_list(items):
    return [i for i in items if not any(x in i for x in ['posts', 'photos', 'pulse', 'tweet', 'share'])]

def clear_email(emails):
    return [e for e in emails if '@' in e and 'wix' not in e and 'png' not in e]

def clear_cnpj(cnpjs):
    return [c.replace('.', '').replace('-', '').replace('/', '') for c in cnpjs]

def create_domain_filename(domain):
    return domain.replace('https://', '').replace('.', '_').replace('/', '_') + ".json"

def extract_data_from_any_site_using_regex(raw_data, processed_data_dir):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "..", raw_data)
    output_dir = os.path.join(base_dir, "..", processed_data_dir)
    os.makedirs(output_dir, exist_ok=True)

    with open(csv_path, "r", encoding="utf-8") as f:
        links = f.read().splitlines()

    for link in links:
        domain_file = os.path.join(output_dir, create_domain_filename(link))
        if os.path.isfile(domain_file):
            print(f"{domain_file} já existe. Pulando...")
            continue

        try:
            session = HTMLSession()
            response = session.get(link, timeout=(3, 5))
            response.html.render(wait=2, timeout=20, scrolldown=0)

            html = response.html.text
            whatsapp = re.findall(r'\b\d{10,15}\b', " ".join([l for l in response.html.links if "whatsapp" in l]))
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', html)
            cnpjs = re.findall(r'\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b', html)
            phones = re.findall(r'(?:\(?\d{2}\)?\s?)?\d{4,5}[-\s]?\d{4}', html)
            ceps = re.findall(r'\b\d{5}-\d{3}\b', html)
            addresses = re.findall(r'(Rua|Avenida|Av\.|Travessa|Praça|Alameda)[^,]+', html)

            social = lambda rgx: [l for l in response.html.links if re.search(rgx, l, re.I)]
            instagram = [x for x in social(r'instagram\.com/(?!p/)') if 'reel' not in x]
            facebook = social(r'facebook\.com/(?!p/)')
            pinterest = social(r'pinterest\.com/(?!p/)')
            linkedin = social(r'linkedin\.com/(?!p/)')
            twitter = social(r'twitter\.com/(?!p/)')

            if any([whatsapp, emails, cnpjs, phones, ceps, addresses, instagram, facebook]):
                data = {
                    "domain": link,
                    "cnpjs": clear_cnpj(cnpjs),
                    "whatsapps": list(set(whatsapp)),
                    "emails": clear_email(list(set(emails))),
                    "phones": list(set(phones)),
                    "ceps": list(set(ceps)),
                    "addresses": list(set(addresses)),
                    "instagrams": clear_list(instagram),
                    "facebooks": clear_list(facebook),
                    "pinterests": pinterest,
                    "linkedins": linkedin,
                    "twitters": twitter
                }
                with open(domain_file, "w", encoding="utf-8") as f_out:
                    json.dump(data, f_out, indent=4, ensure_ascii=False)
                print(f"✔ Dados salvos em {domain_file}")
            else:
                print(f"Nada encontrado em {link}")

        except Exception as e:
            print(f"Erro ao processar {link}: {e}")
            continue

if __name__ == "__main__":
    extract_data_from_any_site_using_regex(
        raw_data="data/processed/moda_feminina_sao_paulo.csv",
        processed_data_dir="data/processed"
    )
