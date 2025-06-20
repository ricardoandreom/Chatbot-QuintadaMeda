import os
import streamlit as st

api_key = st.secrets["openai"]["api_key"]

logo_url = "https://raw.githubusercontent.com/ricardoandreom/Data/main/LOGOTIPO-1-SEM_FUNDO.png"

urls_website = {
    "data/info_main_page.txt": ["https://www.quintadameda.com/pt/"],
    "data/info_contact.txt": ["https://www.quintadameda.com/pt/contato"],
    "data/info_region.txt": ["https://www.quintadameda.com/pt/pagina/regiao"],
    "data/info_rooms.txt": ["https://www.quintadameda.com/pt/quarto/casa-com-2-quartos"]
}

url_booking = {
    "data/info_booking.txt": ["https://www.booking.com/hotel/pt/quinta-da-meda.pt-pt.html?label=gen173bo-1DCAsouwFCDnF1aW50YS1kYS1tZWRhSDNYA2i7AYgBAZgBH7gBGMgBDNgBA-gBAYgCAZgCBqgCBLgCx__AwgbAAgHSAiRkY2U2ZDRmMy0xZTRiLTQzZjktOTBmOS04OTQzOTUzMGNlMzPYAgTgAgE&sid=d730f21376c4573d2e231b4d4420e383&dist=0&keep_landing=1&sb_price_type=total&type=total&"],
}