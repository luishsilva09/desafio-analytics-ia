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


