# coding: utf-8
import requests
import unittest
from bs4 import BeautifulSoup

# Scraping of Le Bonbon to see which district of Paris is the "best", according to the number of Shares by article
page_link = 'https://www.lebonbon.fr'

def recup_source_code(link):
    page_response = requests.get(link, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    return page_content

def choose_place(ville, place):
    location = page_link + "/" + ville + "/" + "?s=" + place
    return location

def list_url_articles(link):
    page_content = recup_source_code(link)
    articles = page_content.findAll('div', attrs={'class': 'bloc one-two interne'})
    list_url = list(map(lambda x: page_link + x.find('a')['href'], articles))
    return list_url

# Site du bonbon en Ajax => impossible de lire les share count
def recup_number_of_shares(link):
    page_content = recup_source_code(link)
    #print(page_content)
    #shares = page_content.find_all('div', attrs={'class': 'single-title'})
    shares = page_content.find_all('div',)
    print(shares)
    return shares

def popularity(list_url):
    popularity = 0
    for i in range(0, len(list_url)):
        soup = recup_source_code(list_url[i])
    return


#print(recup_source_code(choose_place("paris", "mouffetard")))
print(list_url_articles(choose_place("paris", "mouffetard")))
print(len(list_url_articles(choose_place("paris", "mouffetard"))))
print(recup_number_of_shares(list_url_articles(choose_place("paris", "mouffetard"))[0]))