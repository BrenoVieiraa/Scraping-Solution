import re
import asyncio
import nest_asyncio
from requests_html import HTMLSession
from typing import Dict, Any, List

# Ajustar loop e aplicar nest_asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
nest_asyncio.apply()

# Funções auxiliares (sem alteração)
def clear_list(items: List[str]) -> List[str]:
    return [i for i in items if not any(x in i for x in ['posts', 'photos', 'pulse', 'tweet', 'share'])]

def clear_email(emails: List[str]) -> List[str]:
    return [e for e in emails if '@' in e and 'wix' not in e and 'png' not in e]

def clear_cnpj(cnpjs: List[str]) -> List[str]:
    return [c.replace('.', '').replace('-', '').replace('/', '') for c in cnpjs]


# --- MUDANÇA RADICAL: A função agora processa UMA URL e retorna UM DICIONÁRIO ---
def scrape_data_from_url(url: str) -> Dict[str, Any]:
    try:
        session = HTMLSession()
        response = session.get(url, timeout=(5, 10)) # Timeout aumentado
        response.html.render(wait=2, timeout=20, scrolldown=0)

        html = response.html.text
        
        # Expressões Regulares (sem alteração na lógica)
        whatsapp = re.findall(r'\b\d{10,15}\b', " ".join([l for l in response.html.links if "whatsapp" in l]))
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', html)
        cnpjs = re.findall(r'\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b', html)
        phones = re.findall(r'(?:\(?\d{2}\)?\s?)?\d{4,5}[-\s]?\d{4}', html)
        ceps = re.findall(r'\b\d{5}-\d{3}\b', html)
        addresses = re.findall(r'(Rua|Avenida|Av\.|Travessa|Praça|Alameda)[^,]+', html)

        social = lambda rgx: [l for l in response.html.links if re.search(rgx, l, re.I)]
        instagram = [x for x in social(r'instagram\.com/(?!p/)') if 'reel' not in x]
        facebook = social(r'facebook\.com/(?!p/)')
        
        data = {
            "domain": url,
            "cnpjs": clear_cnpj(cnpjs),
            "whatsapps": list(set(whatsapp)),
            "emails": clear_email(list(set(emails))),
            "phones": list(set(phones)),
            "ceps": list(set(ceps)),
            "addresses": list(set(addresses)),
            "instagrams": clear_list(list(set(instagram))),
            "facebooks": clear_list(list(set(facebook))),
        }
        
        # --- MUDANÇA: Em vez de salvar em arquivo, retorna o dicionário de dados ---
        print(f"✔ Dados extraídos de {url}")
        return data

    except Exception as e:
        print(f"Erro ao processar {url}: {e}")
        # Retorna um dicionário de erro para sabermos o que falhou
        return {"domain": url, "error": str(e)}