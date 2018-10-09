# coding: utf-8
import requests
import unittest
from bs4 import BeautifulSoup

# Scraping of Reuters to gather financial information about companies
web_prefix = 'https://www.reuters.com/finance/stocks/financial-highlights/'
companies = ['LVMH', 'DANONE' , 'AIR']
exchange_places = ['.PA']

def recup_source_code(link):
    page_response = requests.get(link, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    return page_content


def get_data(link):
    page_content = recup_source_code(link)
    data = page_content.findAll('td', {'class' : 'data'})

    data_value = []
    for d in data:
        data_value += [d.text]

    return data_value

#def financial_performances(data):

def main() :
    link = web_prefix+companies[0]+exchange_places[0]
    #print(recup_source_code(web_prefix+companies[0]+exchange_places[0]))

    print(get_data(link))

if __name__ == '__main__':
    main()