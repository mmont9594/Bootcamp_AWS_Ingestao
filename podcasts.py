#%%
import requests
from bs4 import BeautifulSoup as bs
import logging

#%%
url='https://portalcafebrasil.com.br/todos/podcasts/page/'

#%%
ret = requests.get(url)

#%%
soup = bs(ret.text)
# %%
soup.find('h5').text

# %%
soup.find('h5').a['href']
# %%

lst_podcast = soup.find_all('h5')

for item in lst_podcast:
    print(f"EP: {item.text} - Link: {item.a['href']}")

#%%
url='https://portalcafebrasil.com.br/todos/podcasts/page/{}/'

def get_podcast(url:str):
    ret = requests.get(url)
    soup = bs(ret.text)
    return soup.find_all('h5')

#%%
get_podcast(url.format(5))
# %%
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

#%%

i=1
lst_podcast=[]
lst_get=get_podcast(url.format(i))
log.debug(f"Coletado {len(lst_get)} episódios do link: {url.format(i)}")
while len(lst_get) > 0:
    lst_podcast = lst_podcast + lst_get
    i += 1
    lst_get=get_podcast(url.format(i))    
# %%
import pandas as pd

#%%
df = pd.DataFrame(columns = ['nome', 'link'])

#%%
for item in lst_podcast:
    df.loc[df.shape[0]] = [item.text, item.a['href']]


# %%
df.to_csv('Banco_de_podcasts.csv', sep=',', index=False)