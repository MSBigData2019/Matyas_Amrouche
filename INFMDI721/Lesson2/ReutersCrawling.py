# coding: utf-8
import datetime
import requests
import unittest
from bs4 import BeautifulSoup

# Scraping of Reuters to gather financial information about companies

web_prefix = 'https://www.reuters.com/finance/stocks/financial-highlights/'
companies = ['LVMH', 'DANO', 'AIR']
exchange_places = ['.PA']
now = datetime.datetime.now()

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
def get_sales_dividend_holders(data):
    indexOfValues = {}
    result = {}
    indexOfValues["Sales estimates (in M) Quarter Ending Dec-18"] = 0
    indexOfValues["Dividend Yield of company"] = 67
    indexOfValues["Dividend Yield of sector"] = 69
    indexOfValues["Dividend Yield of industry"] = 68
    indexOfValues["% of shares owned by instutional holders"] = 213

    for i in indexOfValues.keys():
        result[i] = data[indexOfValues.get(i)]
    return result

# Récupère le prix de l'action
def get_share_price(link):
    page_content = recup_source_code(link)
    data = page_content.findAll('span', {'style' : 'font-size: 23px;'})
    return  data[0].text.split("\t")[len(data[0].text.split("\t"))-1]


def get_share_percentage(link):
    page_content = recup_source_code(link)
    # Variation peut pos ou neg => 2 différentes balises à prendre en compte
    if len(page_content.findAll('span', {'class' : 'pos'})) == 0:
        data = page_content.findAll('span', {'class': 'neg'})
    else:
        data = page_content.findAll('span', {'class' : 'pos'})
    return data[1].text.strip(" \n").strip(" \t")




def main() :
    for i in range(0,len(companies)):
        link = web_prefix + companies[i] + exchange_places[0]
        print("Fiancial performaces data for", companies[i], "on the", exchange_places[0], "exchange place")
        for s in get_sales_dividend_holders(get_data1(link)).keys():
            print(s + " : " + get_sales_dividend_holders(get_data1(link)).get(s))
        print("Share price on the " + now.strftime("%Y-%m-%d %H:%M") + " : " + get_share_price(link) + " €")
        print("Share change % on the " + now.strftime("%Y-%m-%d %H:%M") + " : " +get_share_percentage(link))

if __name__ == '__main__':
    main()