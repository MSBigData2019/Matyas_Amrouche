# coding: utf-8
import requests
import unittest
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Pool


####################### Crawling Github ###############################

# Lien de la liste des top contributeurs de GitHub
link = 'https://gist.github.com/paulmillr/2657075'

# Récupère le contenu HTML du site cible
def recup_source_code(link):
    page_response = requests.get(link, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    return page_content

# Récupère l'ensemble des 256 top contributeurs Git
def get_list_contributors(link):
    page_content = recup_source_code(link)
    data = page_content.findAll('tr')
    result = list(map(lambda x: x.find('a').text, data[1:257]))
    list_contributors = pd.DataFrame(result, columns=['Contributors'])
    return list_contributors

############################ Git API ###############################

# Fichier contenant la token pour l'API Git
git_token = pd.read_csv('/tmp/git_token.txt', header=None).ix[0, 0]

# Récupère les données du contibuteur souhaité
def get_json_data(contributor):
    url = 'https://api.github.com/users/'+contributor+'/repos'
    res = requests.get(url, headers={"Authorization": 'token %s' % git_token})
    repos = res.json()
    return repos


# Nombre de stars moyen pour chaque contributeur
def get_average_stars(list_contributors):
    rated_contributors = pd.DataFrame(columns=['Contributors', 'Average Stars'])
    for i in range(0, list_contributors.count().values[0]):
        data = get_json_data(list_contributors.ix[i, 0])
        stars = 0
        for j in range(0, len(data)):
            stars += data[j]['stargazers_count']
        if len(data) == 0:
            moyenne = 0
        else:
            moyenne = round(stars/len(data), 2)
        rated_contributors.loc[i] = [list_contributors.ix[i, 0], moyenne]
    return rated_contributors.sort_values(['Average Stars'], ascending=False)


def main() :
    list_contributors = get_list_contributors(link)[0:3]
    rated_contributors = get_average_stars(list_contributors)
    print(rated_contributors)

if __name__ == '__main__':
    main()