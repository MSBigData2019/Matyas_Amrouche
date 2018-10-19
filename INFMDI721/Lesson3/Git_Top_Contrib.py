# coding: utf-8
import requests
import unittest
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Pool
import time


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
git_token = pd.read_csv('/Users/matyasamrouche/Documents/Master Telecom Big Data/Token/git_token.txt', header=None).ix[0, 0]

# Récupère les données du contibuteur souhaité
def get_json_data_all_repos(contributor, i):
    url_test = 'https://api.github.com/users/'+contributor+'/repos?page='+str(i)+'&per_page=100'
    while True:
        res = requests.get(url_test, headers={"Authorization": 'token %s' % git_token})
        if res.status_code == 200:
            break
        time.sleep(1)
    repos = res.json()
    return repos

# Compte le nombre d'étoiles 
def get_stars_contributor(contributor_repos):
    stars = pd.DataFrame(columns=['Stars'])
    i = 0
    for repo in contributor_repos:
        stars.loc[i] = repo['stargazers_count']
        i += 1
    return stars

def average_stars(contributor):
    i = 1
    stars = pd.DataFrame(columns=['Stars'])
    while len(get_json_data_all_repos(contributor, i)) > 0:
        contributor_repos = get_json_data_all_repos(contributor, i)
        stars = stars.append(get_stars_contributor(contributor_repos))
        i += 1
    return round(stars['Stars'].mean(), 1)


# Nombre de stars moyen pour chaque contributeur
def get_average_stars_contributor(list_contributors):
    rated_contributors = pd.DataFrame(columns=['Contributors', 'Average Stars'])
    pool = Pool(5)
    average_list = list(pool.map(average_stars, list_contributors['Contributors']))
    rated_contributors['Contributors'] = list_contributors['Contributors']
    rated_contributors['Average Stars'] = average_list
    return rated_contributors.sort_values(['Average Stars'], ascending=False)



def main() :
    start_time = time.time()

    headers = {'Authorization': 'token {}'.format(git_token)}
    requests.get("https://api.github.com/rate_limit", headers=headers).content
    r1 = requests.get("https://api.github.com/rate_limit", headers=headers).json()["rate"]["remaining"]

    list_contributors = get_list_contributors(link)[0:30]
    rated_contributors = get_average_stars_contributor(list_contributors)
    print(rated_contributors)
    r2 = requests.get("https://api.github.com/rate_limit", headers=headers).json()["rate"]["remaining"]
    print("Requêtes utilisés :", r1-r2)
    print("--- %s seconds ---" % round((time.time() - start_time), 2))

if __name__ == '__main__':
    main()

