# coding: utf-8
import requests
import unittest
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Pool
import time

####################### Crawling Wikipedia ville de France ###############################

# Lien de la liste des top contributeurs de GitHub
link = 'https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es'

# Récupère le contenu HTML du site cible
def recup_source_code(link):
    page_response = requests.get(link, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    return page_content

# Récupère l'ensemble des 256 top contributeurs Git
def get_list_villes(link):
    page_content = recup_source_code(link)
    data = page_content.findAll('tr')
    result = list(map(lambda x: x.find('a').text, data))
    list_villes = pd.DataFrame(result, columns=['Villes'])
    return list_villes[1:50]


############################ Geoloc API ###############################

# Fichier contenant la token pour l'API Git




def main() :
    #start_time = time.time()
    list_villes = get_list_villes(link)
    print(list_villes)
    #print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()