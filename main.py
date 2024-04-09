#%%
import pandas as pd
import requests
import json

#%%

""" Return from request

        1XX - Informação
        2XX - Sucesso
        3XX - Redirecionar 
        4XX - Erro de Cliente (Você cometeu um erro)
        5XX - Erro de servidor (Eles cometeram um erro)
        
"""

#%%
url = 'https://economia.awesomeapi.com.br/last/USD-BRL'

ret = requests.get(url)

#%%
dolar = json.loads(ret.text)['USDBRL']

# %%
print(f"20 Dolares hoje custam {float(dolar['bid'])*20} reais")
# %%

def cotacao(valor:int, moeda:str):
    url = f'https://economia.awesomeapi.com.br/last/{moeda}'
    ret= requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-', '')]
    print(f"{valor} {moeda[:3]} hoje custam {float(dolar['bid'])*valor} {moeda[4:]}")

# %%
try:
    cotacao(20, 'Matheus')
except Exception as e: 
    print(e)
    
#%%
def error_check(func):
    def inner_func(*args, **kargs):
        try:
            func(*args, **kargs)
        except:
            print(f"{func.__name__} falhou")
    return inner_func

@error_check
def multi_moedas(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/last/{moeda}'
    ret= requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-', '')]
    print(f"{valor} {moeda[:3]} hoje custam {float(dolar['bid'])*valor} {moeda[4:]}")

#%%

multi_moedas(20, "USD-BRL")
multi_moedas(20, "EUR-BRL")
multi_moedas(20, "BTC-BRL")
multi_moedas(20, "JPY-BRL")
multi_moedas(20, "RPL-BRL")

# %%
import backoff
import random

@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=4)
def test_func(*args, **kargs):
    rnd = random.random()
    print(f"""
          RND: {rnd}
          args: {args if args else 'sem args'}
          kargs: {kargs if kargs else 'sem kargs'}
          """)
    if rnd < .2:
        raise ConnectionAbortedError('Conexão foi finalizada')
    elif rnd < .4:
        raise ConnectionRefusedError('Conexão foi recusada')
    elif rnd < .6:
        raise TimeoutError('Tempo de espera excedido')
    else:
        return 'Ok!'
    
#%%
test_func()

#%%
import logging

# %%
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

# %%
import backoff
import random

@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=4)
def test_func(*args, **kargs):
    rnd = random.random()
    log.debug(f"RND: {rnd}")
    log.info(f"args: {args if args else 'sem args'}")
    log.info(f"kargs: {kargs if kargs else 'sem kargs'}")

    if rnd < .2:
        log.error('Conexão foi finalizada')
        raise ConnectionAbortedError('Conexão foi finalizada')
    elif rnd < .4:
        log.error('Conexão foi recusada')
        raise ConnectionRefusedError('Conexão foi recusada')
    elif rnd < .6:
        log.error('Tempo de espera excedido')
        raise TimeoutError('Tempo de espera excedido')
    else:
        return 'Ok!'
# %%
test_func()
# %%
