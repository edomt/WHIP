from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import sys


RUN_MODE = sys.argv[1]


def get_vote_list(mode='create'):
    url = 'http://www2.assemblee-nationale.fr/scrutins/liste/(legislature)/15'
    all_votes = []

    while True:
        r  = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, features="lxml")
        all_links_elements = soup.find(id='listeScrutins').find_all('a')
        all_links = [link['href'] for link in all_links_elements]
        votes = ['http://www2.assemblee-nationale.fr' + link for link in all_links if 'scrutin' in link]
        all_votes += votes
        
        if mode == 'update':
            return all_votes

        nxt_page = soup.find("div", {"class": "pagination-bootstrap"}).find_all('li')
        link_to_next = nxt_page[-1].find('a')
        if link_to_next is None:
            break
        else:
            url = 'http://www2.assemblee-nationale.fr' + link_to_next['href']
            
    return all_votes


def get_vote(url):
    print(url)
    r  = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, features="lxml")
    
    scrutin_id = re.compile('\d+$').search(url).group(0)
    
    date = soup.find('h1').get_text()
    date = re.compile('\d\d/\d\d/\d{4}').search(date).group(0)
    
    groups = soup.find_all("div", {"class": "TTgroupe"})
    df = []
    
    for group in groups:
        name = group.find("p", {"class": "nomgroupe"}).get_text()
        
        # Pour
        pour = group.find("div", {"class": "Pour"})
        if pour is not None:
            pour = pour.find('b').get_text()
        else:
            pour = 0
        
        # Contre
        contre = group.find("div", {"class": "Contre"})
        if contre is not None:
            contre = contre.find('b').get_text()
        else:
            contre = 0
        
        # Abstention
        abstention = group.find("div", {"class": "Abstention"})
        if abstention is not None:
            abstention = abstention.find('b').get_text()
        else:
            abstention = 0
        
        df.append(pd.DataFrame({'scrutin_id': scrutin_id, 'date': date, 'group': [name],
                                'pour': [pour], 'contre': [contre], 'abstention': [abstention]}))
    
    df = pd.concat(df)
    df['group'] = df['group'].str.replace(' \(.*', '')
    df['date'] = pd.to_datetime(df.date, format='%d/%m/%Y').astype('str')
    
    return df


def update_dataset(new_data):
    
    min_new_id = new_data.scrutin_id.astype('int').min()
    
    old_data = pd.read_csv('scrapped.csv', parse_dates=False)
    old_data = old_data[old_data.scrutin_id < min_new_id]
    
    updated_data = pd.concat([new_data, old_data])
    
    return updated_data


vote_list = get_vote_list(mode=RUN_MODE)
vote_data = pd.concat([get_vote(v) for v in vote_list])

if RUN_MODE == 'update':
    vote_data = update_dataset(vote_data)

vote_data.to_csv('scrapped.csv', index=False)

