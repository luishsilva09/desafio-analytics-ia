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


