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




def main() :
    print(recup_source_code(web_prefix+companies[0]+exchange_places[0]))
    #print(recup_source_code(web_prefix+companies[0]+exchange_places[0]))

if __name__ == '__main__':
    main()