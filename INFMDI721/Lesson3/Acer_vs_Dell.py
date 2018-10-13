# coding: utf-8
import datetime
import requests
import unittest
from bs4 import BeautifulSoup

# Scraping of Reuters to gather financial information about companies

web_prefix = 'https://www.fnac.com/SearchResult/ResultList.aspx?SCat=0%211&Search=acer'
web_suffix = '&sft=1&sa=0'
marques = ['acer', 'dell']


# Récupère le contenu HTML du site cible
def recup_source_code(link):
    page_response = requests.get(link, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    return page_content


# Récupère l'ensemble des données chiffrées sur le site
def get_data(link):
    page_content = recup_source_code(link)
    data = page_content.findAll('span', {'class' : 'oldPrice'})

    return data






def main() :
    #print(web_prefix + marques[0] + web_suffix)
    #print(recup_source_code(web_prefix + marques[0] + web_suffix))
    print(get_data(web_prefix + marques[0] + web_suffix))

if __name__ == '__main__':
    main()