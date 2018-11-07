# coding: utf-8
import requests
import unittest
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Pool
import time


####################### API Open Medicaments ###############################

# Lien de la liste des top contributeurs de GitHub
paracetamol_id = 'https://www.open-medicaments.fr/api/v1/medicaments?query=paracetamol&limit=100'
info_id = 'https://www.open-medicaments.fr/api/v1/medicaments/67445776'

# Récupère le contenu JSON du paracétamol
def recup_list_medocs(link):
    res = requests.get(link, timeout=5)
    medocs = res.json()
    return medocs







def main() :
    start_time = time.time()
    json = recup_json_medocs(link)
    print(json)
    print("--- %s seconds ---" % round((time.time() - start_time), 2))

if __name__ == '__main__':
    main()