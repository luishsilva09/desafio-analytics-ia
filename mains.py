from datetime import datetime
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dotenv import load_dotenv
import os

#  Configurar env
load_dotenv()

# Configurar chamadas para api coingecko
headers = {
    "x-cg-demo-api-key": os.getenv('API_KEY')
}
url_api = "https://api.coingecko.com/api/v3/"


def formatar_cores(valor=0):
    """Mudar cor dos texto"""
    RED = "\033[31m"
    GREEN = "\033[32m"

    color = "\033[0m"
    if valor < 0:
        color = RED
    elif valor > 0:
        color = GREEN
    return color


def buscar_top_buscados():
    """Buscar as tops moedas mais buscadas pelos usuarios"""
    dados = {}
    # Buscar dados e transformar para json
    response = json.loads(requests.get(
        url_api + 'search/trending', headers=headers).text)

    # Formatar dados
    for dado in response['coins']:
        porcentagem = \
            dado['item']['data']['price_change_percentage_24h']['usd']

        dados[dado['item']['name']] = {
            'Preço': f"U${dado['item']['data']['price']:.6f}",
            'Crecimento':
            f"{formatar_cores(porcentagem)}{porcentagem:.2f}%{formatar_cores()}"
        }

    df = pd.DataFrame(data=dados).T
    df_styled = df.style.set_properties(**{'text-align': 'center'})

    # Centralizando os rótulos das colunas
    df_styled = df_styled.set_table_styles(
        [{'selector': 'th', 'props': [('text-align', 'center')]}])

    # display(df_styled)

    print(df)


