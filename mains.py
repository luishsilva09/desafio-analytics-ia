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


def chamada_busca_historico(dias=None, moeda=None):
    """Trazer o response do busca historico"""

    response = json.loads(requests.get(
        f"""{url_api}coins/markets?vs_currency=usd&ids={moeda}&price_change_percentage={dias}""",
        headers=headers).text)

    return response


def historico_bitcoin():
    """Historico valor Bitcoin 24h"""
    dados = {
        'hora': [],
        'valor': []
    }

    # Buscar dados
    response = json.loads(requests.get(
        f"{url_api}coins/bitcoin/market_chart?vs_currency=usd&days=1",
        headers=headers).text)

    # Formatar dados
    for valor in response['prices']:
        dados['hora'].append(datetime.fromtimestamp(valor[0] / 1000))
        dados['valor'].append(valor[1])

    # Montar grafico
    fig, ax = plt.subplots(figsize=(10, 5))

    # Adicionar dados ao grafico
    ax.plot(dados['hora'], dados['valor'],
            label='Bitcoin')

    # Ajustar eixo x para ter escala de 1h
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # Deixar mais legivel e adicionar labels
    plt.gcf().autofmt_xdate()
    plt.xlabel('Hora')
    plt.ylabel('Valor U$')
    plt.title('Valores Bitcoin 24h')

    plt.show()
    df = pd.DataFrame({'Hora': dados['hora'][::12],
                       'Valor': dados['valor'][::12]})
    print(df)


def tabela_valores_top():
    """Comparar valores e crecimento atual entre Bitcoin, Ethereum e Solana"""
    dados = {}
    # Buscar dados
    response = json.loads(requests.get(
        f"{url_api}coins/markets?vs_currency=usd&ids=bitcoin%2Cethereum%2Csolana",
        headers=headers).text)

    for valores in response:
        dados[valores['name']] = {
            'valor_atual': f"U$ {valores['current_price']}",
            'maior_valor_24h': f"U$ {valores['high_24h']}",
            'menor_valor_24h': f"U$ {valores['low_24h']}",
            'porcentagem mudanca_preco':
            f"{formatar_cores(valores['price_change_percentage_24h'])}\
            {valores['price_change_percentage_24h']}%{formatar_cores()}",
            'valor_mudanca': f"{formatar_cores(valores['price_change_24h'])}\
                {valores['price_change_24h']:.2f}{formatar_cores()}"
        }
    df = pd.DataFrame(data=dados).T

    # Renomear as colunas
    df.columns = [
        'Preço Atual',
        'Maior Preço 24h',
        'Menor Preço 24h',
        'Porcentagem de Mudança (%)',
        'Valor da Mudança'
    ]

    print(df)


def crecimento_bitcoin():
    """Valorizacao bitcoin 1d, 7d, 30d, 1 ano"""
    busca = ['1h', '24h', '7d', '30d', '1y']
    dados = {}
    # Buscar dados
    for qtd in busca:
        response = chamada_busca_historico(dias=qtd, moeda='bitcoin')

        # Formatar dados
        valor = response[0][f"price_change_percentage_{qtd}_in_currency"]
        dados[qtd] = {
            'porcentagem_crecimento':
            f"{formatar_cores(valor)}{valor:.2f}%{formatar_cores()}"

        }
    # Exibir tabela
    df = pd.DataFrame(data=dados)

    print(df)

print('Criptomoedas mais buscadas')
buscar_top_buscados()

print('Valores Bitcoin, Ethereum e Solana')
tabela_valores_top()

print('Crecimento bitcoin')
crecimento_bitcoin()

print('Historico valor bitcoin 24h')
historico_bitcoin()
