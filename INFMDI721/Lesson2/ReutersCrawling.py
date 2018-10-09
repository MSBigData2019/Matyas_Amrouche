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

def financial_performances(data):
    indexOfValues = {}
    indexOfValues["Sales estimates (in M) Quarter Ending Dec-18"] = 0
    indexOfValues["Divide Yield of company"] = 67
    indexOfValues["Divide Yield of sector"] = 69
    indexOfValues["Divide Yield of industry"] = 68

    for i in indexOfValues.keys():
        print(i, " : ", data[indexOfValues.get(i)])


def main() :
    link = web_prefix+companies[0]+exchange_places[0]
    print("Data for ", companies[0], " on the ", exchange_places[0], " exchange place")

    financial_performances(get_data(link))

if __name__ == '__main__':
    main()