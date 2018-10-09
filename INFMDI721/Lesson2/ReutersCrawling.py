# coding: utf-8
import requests
import unittest
from bs4 import BeautifulSoup

# Scraping of Reuters to gather financial information about companies

web_prefix = 'https://www.reuters.com/finance/stocks/financial-highlights/'
companies = ['LVMH', 'DANONE', 'AIR']
exchange_places = ['.PA']

# Récupère le contenu HTML du site cible
def recup_source_code(link):
    page_response = requests.get(link, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    return page_content


# Récupère l'ensemble des données chiffrées sur le site
def get_data1(link):
    page_content = recup_source_code(link)
    data = page_content.findAll('td', {'class' : 'data'})

    data_value = []
    for d in data:
        data_value += [d.text]

    return data_value

# Les balises 'data' ne sont pas identifiables les unes des autres
# Créer un dictionnaire des valeurs recherchées et de leur index dans la page (extrait manuellement)
def get_sales_and_dividend(data):
    indexOfValues = {}
    indexOfValues["Sales estimates (in M) Quarter Ending Dec-18"] = 0
    indexOfValues["Dividend Yield of company"] = 67
    indexOfValues["Dividend Yield of sector"] = 69
    indexOfValues["Dividend Yield of industry"] = 68

    for i in indexOfValues.keys():
        print(i, ":", data[indexOfValues.get(i)])


def get_shares_prices_and_percentage(link):
    page_content = recup_source_code(link)
    data_value = []

    data = page_content.findAll('span', {'style' : 'font-size: 23px;'})
    print(data[0].text)

    data = page_content.findAll('span', {'class' : 'pos'})
    print(data[1].text)

    return data_value


def main() :
    link = web_prefix+companies[0]+exchange_places[0]
    #print("Data for", companies[0], "on the", exchange_places[0], "exchange place")

    #get_sales_and_dividend(get_data1(link))
    print(get_shares_prices_and_percentage(link))

if __name__ == '__main__':
    main()