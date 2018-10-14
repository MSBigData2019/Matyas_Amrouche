# coding: utf-8
import requests
import unittest
from bs4 import BeautifulSoup
import pandas as pd


link = 'https://gist.github.com/paulmillr/2657075'


# Récupère le contenu HTML du site cible
def recup_source_code(link):
    page_response = requests.get(link, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    return page_content


# Récupère l'ensemble des contributeurs Git de lapage
def get_list_contributors(link):
    page_content = recup_source_code(link)
    data = page_content.findAll('td')

    contributors = []
    for i in range(0, len(data)):
      if data[i].find('a'):
           contributors.append(data[i].find('a').text)

    list_contributors = pd.DataFrame(contributors, columns=['Contributors'])
    filter = list_contributors["Contributors"] != ""
    list_contributors_bis = list_contributors[filter]
    return list_contributors_bis



def main() :
    result = get_list_contributors(link)
    print(result)
    #for i in range(0, 564):
      #  print(result[i])


if __name__ == '__main__':
    main()