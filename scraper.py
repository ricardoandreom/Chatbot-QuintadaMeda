import requests
from bs4 import BeautifulSoup
import re
from openai import OpenAI
import os
from config import api_key, urls_website, url_booking

client = OpenAI(api_key=api_key)

def limpar_linhas_irrelevantes(texto: str) -> str:
    # Frases/palavras exatas a remover
    frases_remover = {
        "[email protected]",
        "/pt/booking/room",
        "/pt",
        "bem-vindo",
        "descobrir"
    }

    # Lista de meses
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
        # Ignorar se for um número ex: "123", "2023"
        if re.fullmatch(r"\d+", linha_strip):
            continue
        # Ignorar se for apenas um mês
        if linha_strip in meses:
            continue
        # Ignorar se a linha estiver vazia
        if not linha_strip:
            continue
        # Caso contrário manter a linha
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

    # Limpa e guarda
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
    
    A tua tarefa é:
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

# Extrai info do website oficial do alojamento e limpa info
for output_file, urls in urls_website.items():
    all_text = []
    for url in urls:
        print(f"🔍 A processar: {url}")
        content = scrape_and_save_website(url)
        if content:
            all_text.append(content)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n---\n\n".join(all_text))
    print(f"✅ Guardado em {output_file}")

# Extrai info do website do alojamento no Booking e limpa informação e remove info de comentários com preprocessamento usando LLM
for output_file, urls in url_booking.items():
    all_text = []
    for url in urls:
        print(f"🔍 A processar: {url}")
        content = scrape_and_save_booking(url)
        final_content = remover_comentarios_clientes(final_content)
        if final_content:
            all_text.append(final_content)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n---\n\n".join(all_text))
    print(f"✅ Guardado em {output_file}")

