import requests
from bs4 import BeautifulSoup
import re
from openai import OpenAI
import os
import streamlit as st

from dotenv import load_dotenv

# Load variables do .env
# load_dotenv()

# api_key from secrets
api_key = st.secrets["openai"]["api_key"] # os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def limpar_linhas_irrelevantes(texto: str) -> str:
    # Frases/palavras exatas a remover
    frases_remover = {
        "[email protected]",
        # "RNET 10407",
        # "EN",
        # "PT",
        # "Alimentado usando Amenitiz",
        # "Menu",
        # "Contacto",
        # "Livro de Reclamações",
        # "Informações Legais",
        "/pt/booking/room",
        "/pt",
        # "Quinta da Meda",
        # "Região",
        # "Início",
        "bem-vindo",
        "descobrir",
        # "Procurar",
        # "If you see this, leave this form field blank.",
        # "Eu concordo com a política de privacidade",
        # "Adultos", "Check-in", "Check-out", "Apenas no nosso site oficial"
    }

    # Lista de meses em português e inglês
    meses = {
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december"
    }

    linhas_filtradas = []

    for linha in texto.splitlines():
        linha_strip = linha.strip().lower()

        # Ignorar se estiver na lista exata de frases
        if linha_strip in {frase.lower() for frase in frases_remover}:
            continue

        # Ignorar se for um número puro (ex: "123", "2023")
        if re.fullmatch(r"\d+", linha_strip):
            continue

        # Ignorar se for apenas um mês
        if linha_strip in meses:
            continue

        # Ignorar se a linha estiver vazia
        if not linha_strip:
            continue

        # Caso contrário, manter a linha
        linhas_filtradas.append(linha)

    return "\n".join(linhas_filtradas)

def scrape_and_save_booking(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Erro ao acessar {url}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts e styles
    for tag in soup(
            ["script", "style", "noscript", "header", "nav", "footer", "aside", "form", "input", "select", "textarea"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    # Limpa e salva
    lines = [line.strip() for line in text.splitlines()]
    clean_text = "\n".join(line for line in lines if line)

    return clean_text

def scrape_and_save_website(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Erro ao acessar {url}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove elementos não relacionados ao conteúdo principal
    for tag in soup([
        "script", "style", "noscript", "header", "nav", "footer",
        "aside", "form", "input", "button", "select", "textarea"
    ]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    # Limpa linhas vazias e lixo
    lines = [line.strip() for line in text.splitlines()]
    raw_text = "\n".join(line for line in lines if line)
    clean_text = limpar_linhas_irrelevantes(raw_text)

    return clean_text

def remover_comentarios_clientes(texto):
    prompt = f"""
    O seguinte texto foi extraído de um website de uma unidade hoteleira. Ele mistura informações descritivas com comentários de clientes presentes no website.
    
    Tua tarefa é:
    - Remover quaisquer comentários, avaliações, opiniões, testemunhos ou frases que expressem experiências pessoais de clientes.
    
    Texto original:
    \"\"\"{texto}\"\"\"
    
    Texto limpo sem comentários de clientes:
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "És um assistente que limpa texto para um sistema de recuperação de informação."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()

urls_website = {
    "data/info_main_page.txt": ["https://www.quintadameda.com/pt/"],
    "data/info_contact.txt": ["https://www.quintadameda.com/pt/contato"],
    "data/info_region.txt": ["https://www.quintadameda.com/pt/pagina/regiao"],
    "data/info_rooms.txt": ["https://www.quintadameda.com/pt/quarto/casa-com-2-quartos"]
}

url_booking = {
    "data/info_booking.txt": ["https://www.booking.com/hotel/pt/quinta-da-meda.pt-pt.html?label=gen173bo-1DCAsouwFCDnF1aW50YS1kYS1tZWRhSDNYA2i7AYgBAZgBH7gBGMgBDNgBA-gBAYgCAZgCBqgCBLgCx__AwgbAAgHSAiRkY2U2ZDRmMy0xZTRiLTQzZjktOTBmOS04OTQzOTUzMGNlMzPYAgTgAgE&sid=d730f21376c4573d2e231b4d4420e383&dist=0&keep_landing=1&sb_price_type=total&type=total&"],
}


for output_file, urls in urls_website.items():
    all_text = []
    for url in urls:
        print(f"🔍 A processar: {url}")
        conteudo = scrape_and_save_website(url)
        if conteudo:
            all_text.append(conteudo)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n---\n\n".join(all_text))
    print(f"✅ Guardado em {output_file}")

for output_file, urls in url_booking.items():
    all_text = []
    for url in urls:
        print(f"🔍 A processar: {url}")
        conteudo = scrape_and_save_booking(url)
        conteudo_final = remover_comentarios_clientes(conteudo)
        if conteudo_final:
            all_text.append(conteudo_final)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n---\n\n".join(all_text))
    print(f"✅ Guardado em {output_file}")

