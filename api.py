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

os = "https://api.opensea.io/api/v1/collection/"
fear = 'https://api.alternative.me/fng/?limit=0'
today = 'http://history.muffinlabs.com/date/'
joke = 'https://v2.jokeapi.dev/joke/Any?safe-mode'

def get_x7r_holders():
    x7rholdersurl = 'https://api.ethplorer.io/getTokenInfo/' + items.x7rca + keys.ethplorer
    x7rholdersresponse = requests.get(x7rholdersurl)
    x7rholdersdata = x7rholdersresponse.json()
    x7rholders = x7rholdersdata["holdersCount"]
    return x7rholders

def get_x7dao_holders():
    x7daoholdersurl = 'https://api.ethplorer.io/getTokenInfo/' + items.x7daoca + keys.ethplorer
    x7daoholdersresponse = requests.get(x7daoholdersurl)
    x7daoholdersdata = x7daoholdersresponse.json()
    x7daoholders = x7daoholdersdata["holdersCount"]
    return x7daoholders

def get_x7d_holders():
    x7dholdersurl = 'https://api.ethplorer.io/getTokenInfo/' + items.x7dca + keys.ethplorer
    x7dholdersresponse = requests.get(x7dholdersurl)
    x7dholdersdata = x7dholdersresponse.json()
    x7dholders = x7dholdersdata["holdersCount"]
    return x7dholders

def get_x7101_holders():
    x7101holdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.x7101ca + keys.ethplorer
    x7101holdersresponse = requests.get(x7101holdersurl)
    x7101holdersdata = x7101holdersresponse.json()
    x7101holders = x7101holdersdata["holdersCount"]
    return x7101holders

def get_x7102_holders():
    x7102holdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.x7102ca + keys.ethplorer
    x7102holdersresponse = requests.get(x7102holdersurl)
    x7102holdersdata = x7102holdersresponse.json()
    x7102holders = x7102holdersdata["holdersCount"]
    return x7102holders

def get_x7103_holders():
    x7103holdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.x7103ca + keys.ethplorer
    x7103holdersresponse = requests.get(x7103holdersurl)
    x7103holdersdata = x7103holdersresponse.json()
    x7103holders = x7103holdersdata["holdersCount"]
    return x7103holders

def get_x7104_holders():
    x7104holdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.x7104ca + keys.ethplorer
    x7104holdersresponse = requests.get(x7104holdersurl)
    x7104holdersdata = x7104holdersresponse.json()
    x7104holders = x7104holdersdata["holdersCount"]
    return x7104holders

def get_x7105_holders():
    x7105holdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.x7105ca + keys.ethplorer
    x7105holdersresponse = requests.get(x7105holdersurl)
    x7105holdersdata = x7105holdersresponse.json()
    x7105holders = x7105holdersdata["holdersCount"]
    return x7105holders

def get_quote():
    quoteresponse = requests.get('https://type.fit/api/quotes')
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = quoteraw["text"] + quoteraw["author"]
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    return quote

def get_dex_holders_eth():
    dexholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.dexca + '?chain=eth-main'
    dexholdersresponse = requests.get(dexholdersurl, headers={"accept": "application/json",
                                                              "X-API-KEY": keys.blockspan})
    dexholdersdata = dexholdersresponse.json()
    dexholders = dexholdersdata["total_tokens"]
    return dexholders

def get_liq_holders_eth():
    liqholdersurl = 'https://api.blockspan.com/v1/collections/contract/' + items.liqca + '?chain=eth-main'
    liqholdersresponse = requests.get(liqholdersurl, headers={"accept": "application/json",
                                                              "X-API-KEY": keys.blockspan})
    liqholdersdata = liqholdersresponse.json()
    liqholders = liqholdersdata["total_tokens"]
    return liqholders

def get_borrow_holders_eth():
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
