from pycoingecko import CoinGeckoAPI
from moralis import evm_api
import keys
import items
import requests
import random


# CG
coingecko = CoinGeckoAPI()
cg = coingecko.get_price(ids=',x7r,x7dao,x7101,x7102,x7103,x7104,x7105', vs_currencies='usd',
                         include_24hr_change='true', include_24hr_vol='true')


# MORALIS
# noinspection PyTypeChecker
x7rliq = evm_api.defi.get_pair_reserves(api_key=keys.moralis,
                                        params={"chain": "eth", "pair_address": items.x7rpaireth})
# noinspection PyTypeChecker
x7daoliq = evm_api.defi.get_pair_reserves(api_key=keys.moralis,
                                          params={"chain": "eth", "pair_address": items.x7daopaireth})
# noinspection PyTypeChecker
x7101liq = evm_api.defi.get_pair_reserves(api_key=keys.moralis,
                                          params={"chain": "eth", "pair_address": items.x7101paireth})
# noinspection PyTypeChecker
x7102liq = evm_api.defi.get_pair_reserves(api_key=keys.moralis,
                                          params={"chain": "eth", "pair_address": items.x7102paireth})
# noinspection PyTypeChecker
x7103liq = evm_api.defi.get_pair_reserves(api_key=keys.moralis,
                                          params={"chain": "eth", "pair_address": items.x7103paireth})
# noinspection PyTypeChecker
x7104liq = evm_api.defi.get_pair_reserves(api_key=keys.moralis,
                                          params={"chain": "eth", "pair_address": items.x7104paireth})
# noinspection PyTypeChecker
x7105liq = evm_api.defi.get_pair_reserves(api_key=keys.moralis,
                                          params={"chain": "eth", "pair_address": items.x7105paireth})


# ETH
ethprice = 'https://api.etherscan.io/api?module=stats&action=ethprice&'
tokenbalanceeth = 'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress='
ethbalanceeth = 'https://api.etherscan.io/api?module=account&action=balancemulti&address='
ethgas = 'https://api.etherscan.io/api?module=gastracker&action=gasoracle'

# BSC
bnbprice = 'https://api.bscscan.com/api?module=stats&action=bnbprice&'
tokenbalancebsc = 'https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress='
bnbbalance = 'https://api.bscscan.com/api?module=account&action=balancemulti&address='
bscgas = 'https://api.bscscan.com/api?module=gastracker&action=gasoracle'

# POLY
maticprice = 'https://api.polygonscan.com/api?module=stats&action=maticprice&'
tokenbalancepoly = 'https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress='
maticbalance = 'https://api.polygonscan.com/api?module=account&action=balancemulti&address='
polygas = 'https://api.polygonscan.com/api?module=gastracker&action=gasoracle'

# ARB
tokenbalancearb = 'https://api.arbiscan.io/api?module=account&action=tokenbalance&contractaddress='
ethbalancearb = 'https://api.arbiscan.io/api?module=account&action=balancemulti&address='

# OPTI
tokenbalanceopti = 'https://api-optimistic.etherscan.io/api?module=account&action=tokenbalance&contractaddress='
ethbalanceopti = 'https://api-optimistic.etherscan.io/api?module=account&action=balancemulti&address='

ethplorer = 'https://api.ethplorer.io/getTokenInfo/'
os = "https://api.opensea.io/api/v1/collection/"
fear = 'https://api.alternative.me/fng/?limit=0'
today = 'http://history.muffinlabs.com/date/'
joke = 'https://v2.jokeapi.dev/joke/Any?safe-mode'

def get_quote():
    quoteresponse = requests.get('https://type.fit/api/quotes')
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = quoteraw["text"] + quoteraw["author"]
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    return quote

def get_dexholderseth():
    dexholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.dexca + '?chain=eth-main'
    dexholdersresponse = requests.get(dexholdersurl, headers={"accept": "application/json",
                                                              "X-API-KEY": keys.blockspan})
    dexholdersdata = dexholdersresponse.json()
    dexholders = dexholdersdata["total_tokens"]
    return dexholders

def get_liqholderseth():
    liqholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.liqca + '?chain=eth-main'
    liqholdersresponse = requests.get(liqholdersurl, headers={"accept": "application/json",
                                                              "X-API-KEY": keys.blockspan})
    liqholdersdata = liqholdersresponse.json()
    liqholders = liqholdersdata["total_tokens"]
    return liqholders

def get_borrowholderseth():
    borrowholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.borrowca + '?chain=eth-main'
    borrowholdersresponse = requests.get(borrowholdersurl, headers={"accept": "application/json",
                                                                    "X-API-KEY": keys.blockspan})
    borrowholdersdata = borrowholdersresponse.json()
    borrowholders = borrowholdersdata["total_tokens"]
    return borrowholders

def get_ecoholderseth():
    ecoholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.ecoca + '?chain=eth-main'
    ecoholdersresponse = requests.get(ecoholdersurl, headers={"accept": "application/json",
                                                              "X-API-KEY": keys.blockspan})
    ecoholdersdata = ecoholdersresponse.json()
    ecoholders = ecoholdersdata["total_tokens"]
    return ecoholders

def get_dexholdersarb():
    dexholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.dexca + '?chain=arbitrum'
    dexholdersresponse = requests.get(dexholdersurl, headers={"accept": "application/json",
                                                              "X-API-KEY": keys.blockspan})
    dexholdersdata = dexholdersresponse.json()
    dexholders = dexholdersdata["total_tokens"]
    return dexholders

def get_liqholdersarb():
    liqholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.liqca + '?chain=arbitrum'
    liqholdersresponse = requests.get(liqholdersurl, headers={"accept": "application/json",
                                                              "X-API-KEY": keys.blockspan})
    liqholdersdata = liqholdersresponse.json()
    liqholders = liqholdersdata["total_tokens"]
    return liqholders

def get_borrowholdersarb():
    borrowholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.borrowca + '?chain=arbitrum'
    borrowholdersresponse = requests.get(borrowholdersurl, headers={"accept": "application/json",
                                                                    "X-API-KEY": keys.blockspan})
    borrowholdersdata = borrowholdersresponse.json()
    borrowholders = borrowholdersdata["total_tokens"]
    return borrowholders

def get_ecoholdersarb():
    ecoholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.ecoca + '?chain=arbitrum'
    ecoholdersresponse = requests.get(ecoholdersurl, headers={"accept": "application/json",
                                                              "X-API-KEY": keys.blockspan})
    ecoholdersdata = ecoholdersresponse.json()
    ecoholders = ecoholdersdata["total_tokens"]
    return ecoholders

def get_dexholderspoly():
    dexholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.dexca + '?chain=poly-main'
    dexholdersresponse = requests.get(dexholdersurl, headers={"accept": "application/json",
                                                              "X-API-KEY": keys.blockspan})
    dexholdersdata = dexholdersresponse.json()
    dexholders = dexholdersdata["total_tokens"]
    return dexholders

def get_liqholderspoly():
    liqholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.liqca + '?chain=poly-main'
    liqholdersresponse = requests.get(liqholdersurl, headers={"accept": "application/json",
                                                              "X-API-KEY": keys.blockspan})
    liqholdersdata = liqholdersresponse.json()
    liqholders = liqholdersdata["total_tokens"]
    return liqholders

def get_borrowholderspoly():
    borrowholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.borrowca + '?chain=poly-main'
    borrowholdersresponse = requests.get(borrowholdersurl, headers={"accept": "application/json",
                                                                    "X-API-KEY": keys.blockspan})
    borrowholdersdata = borrowholdersresponse.json()
    borrowholders = borrowholdersdata["total_tokens"]
    return borrowholders

def get_ecoholderspoly():
    ecoholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.ecoca + '?chain=poly-main'
    ecoholdersresponse = requests.get(ecoholdersurl, headers={"accept": "application/json",
                                                              "X-API-KEY": keys.blockspan})
    ecoholdersdata = ecoholdersresponse.json()
    ecoholders = ecoholdersdata["total_tokens"]
    return ecoholders

def get_dexholdersopti():
    dexholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.dexca + '?chain=optimism-main'
    dexholdersresponse = requests.get(dexholdersurl, headers={"accept": "application/json",
                                                              "X-API-KEY": keys.blockspan})
    dexholdersdata = dexholdersresponse.json()
    dexholders = dexholdersdata["total_tokens"]
    return dexholders

def get_liqholdersopti():
    liqholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.liqca + '?chain=optimism-main'
    liqholdersresponse = requests.get(liqholdersurl, headers={"accept": "application/json",
                                                              "X-API-KEY": keys.blockspan})
    liqholdersdata = liqholdersresponse.json()
    liqholders = liqholdersdata["total_tokens"]
    return liqholders

def get_borrowholdersopti():
    borrowholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.borrowca + '?chain=optimism-main'
    borrowholdersresponse = requests.get(borrowholdersurl, headers={"accept": "application/json",
                                                                    "X-API-KEY": keys.blockspan})
    borrowholdersdata = borrowholdersresponse.json()
    borrowholders = borrowholdersdata["total_tokens"]
    return borrowholders

def get_ecoholdersopti():
    ecoholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.ecoca + '?chain=optimism-main'
    ecoholdersresponse = requests.get(ecoholdersurl, headers={"accept": "application/json",
                                                              "X-API-KEY": keys.blockspan})
    ecoholdersdata = ecoholdersresponse.json()
    ecoholders = ecoholdersdata["total_tokens"]
    return ecoholders
