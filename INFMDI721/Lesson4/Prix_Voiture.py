# coding: utf-8
import requests
import unittest
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Pool
import time


####################### Crawling LaCentrale ################################

# Lien de la liste des voitures d'occasion en ile de France / PACA / Aquitaine
link = 'https://www.lacentrale.fr/listing?makesModelsCommercialNames=RENAULT%3AZOE&regions=FR-PAC%2CFR-IDF%2CFR-NAQ'


# Récupère le contenu HTML du site cible
def recup_source_code(link):
    page_response = requests.get(link, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    return page_content

# Get price of cars
def get_prix(page_content):
    page_content = recup_source_code(link)
    #data = page_content.findAll('nobr')
    #data = page_content.findAll('div', {'class': 'fieldPrice.sizeC'})
    data = page_content.findAll('div', {'class': 'adContainer'})

    result = data.find('span')

    #list_prix = pd.DataFrame(result, columns=['C sontributors'])
    return result

# Get year of cars
def get_year(page_content):
    page_content = recup_source_code(link)
    data = page_content.findAll('tr')
    result = list(map(lambda x: x.find('a').text, data[1:257]))
    list_year = pd.DataFrame(result, columns=['Contributors'])
    return list_year

# Get km done by cars
def get_km(page_content):
    page_content = recup_source_code(link)
    data = page_content.findAll('tr')
    result = list(map(lambda x: x.find('a').text, data[1:257]))
    list_km = pd.DataFrame(result, columns=['Contributors'])
    return list_km

def main() :
    start_time = time.time()

    soup = recup_source_code(link)
    print(get_prix(soup))
    print("--- %s seconds ---" % round((time.time() - start_time), 2))

if __name__ == '__main__':
    main()
