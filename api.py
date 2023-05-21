from datetime import datetime
import keys
from moralis import evm_api
import nfts
from pycoingecko import CoinGeckoAPI
import random
import requests
import tweepy

def get_abi(contract, chain):
    url = ""
    if chain == "eth":
        url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address=" + contract + keys.ether
    if chain == "bsc":
        url = f"https://api.bscscan.com/api?module=contract&action=getsourcecode&address=" + contract + keys.bsc
    response = requests.get(url)
    data = response.json()
    result = data["result"][0]["ABI"]
    return result

def get_ath(token):
    url = f"https://api.coingecko.com/api/v3/coins/{token}?localization=false&tickers=false&market_data=" \
          "true&community_data=false&developer_data=false&sparkline=false"
    response = requests.get(url)
    data = response.json()
    value = data["market_data"]
    ath = value["ath"]["usd"]
    change = value["ath_change_percentage"]["usd"]
    date = value["ath_date"]["usd"]
    return ath, change, date

def get_cg_price(token):
    coingecko = CoinGeckoAPI()
    cg = coingecko.get_price(ids=token, vs_currencies='usd',
                             include_24hr_change='true', include_24hr_vol='true', include_market_cap='true')
    return cg

def get_cg_search(token):
    url = 'https://api.coingecko.com/api/v3/search?query=' + token
    response = requests.get(url)
    result = response.json()
    return result

def get_gas(chain):
    if chain == "eth":
        url = 'https://api.etherscan.io/api?module=gastracker&action=gasoracle' + keys.ether
        response = requests.get(url)
        data = response.json()
        return data
    if chain == "poly":
        url = 'https://api.polygonscan.com/api?module=gastracker&action=gasoracle' + keys.poly
        response = requests.get(url)
        data = response.json()
        return data
    if chain == "bsc":
        url = 'https://api.bscscan.com/api?module=gastracker&action=gasoracle' + keys.bsc
        response = requests.get(url)
        data = response.json()
        return data

def get_holders(token):
    url = 'https://api.ethplorer.io/getTokenInfo/' + token + keys.ethplorer
    response = requests.get(url)
    data = response.json()
    amount = data["holdersCount"]
    return amount

def get_liquidity(pair, chain):
    amount = evm_api.defi.get_pair_reserves(api_key=keys.moralis, params={"chain": chain, "pair_address": pair})
    return amount

def get_native_balance(wallet, chain):
    if chain == "opti":
        key = keys.opti
        link = 'https://api-optimistic.etherscan.io/' \
               'api?module=account&action=balancemulti&address='
        response = requests.get(link + wallet + '&tag=latest' + key)
        data = response.json()
        amount_raw = float(data["result"][0]["balance"])
        amount = str(amount_raw / 10 ** 18)
        return amount
    if chain == "eth":
        key = keys.ether
        link = 'https://api.etherscan.io/' \
               'api?module=account&action=balancemulti&address='
        response = requests.get(link + wallet + '&tag=latest' + key)
        data = response.json()
        amount_raw = float(data["result"][0]["balance"])
        amount = str(amount_raw / 10 ** 18)
        return amount
    if chain == "arb":
        key = keys.arb
        link = 'https://api.arbiscan.io/' \
               'api?module=account&action=balancemulti&address='
        response = requests.get(link + wallet + '&tag=latest' + key)
        data = response.json()
        amount_raw = float(data["result"][0]["balance"])
        amount = str(amount_raw / 10 ** 18)
        return amount
    if chain == "bsc":
        key = keys.bsc
        link = "https://api.bscscan.com/" \
               "api?module=account&action=balancemulti&address="
        response = requests.get(link + wallet + '&tag=latest' + key)
        data = response.json()
        amount_raw = float(data["result"][0]["balance"])
        amount = str(amount_raw / 10 ** 18)
        return amount
    if chain == "poly":
        key = keys.poly
        link = "https://api.polygonscan.com/" \
               "api?module=account&action=balancemulti&address="
        response = requests.get(link + wallet + '&tag=latest' + key)
        data = response.json()
        amount_raw = float(data["result"][0]["balance"])
        amount = str(amount_raw / 10 ** 18)
        return amount

def get_native_price(token):
    if token == "eth":
        url = 'https://api.etherscan.io/api?module=stats&action=ethprice&' + keys.ether
        response = requests.get(url)
        data = response.json()
        value = float(data["result"]["ethusd"])
        return value
    if token == "bnb":
        url = 'https://api.bscscan.com/api?module=stats&action=bnbprice&' + keys.bsc
        response = requests.get(url)
        data = response.json()
        value = float(data["result"]["ethusd"])
        return value
    if token == "matic":
        url = 'https://api.polygonscan.com/api?module=stats&action=maticprice&' + keys.poly
        response = requests.get(url)
        data = response.json()
        value = float(data["result"]["maticusd"])
        return value

def get_nft_holder_list(nft, chain):
    result = evm_api.nft.get_nft_owners(
        api_key=keys.moralis, params={"chain": chain, "format": "decimal", "address": nft})
    return result

def get_nft_holder_count(nft, chain):
    url = 'https://api.blockspan.com/v1/collections/contract/' + nft + chain
    response = requests.get(url, headers={"accept": "application/json", "X-API-KEY": keys.blockspan})
    data = response.json()
    amount = data["total_tokens"]
    return amount

def get_nft_floor(nft, chain):
    url = 'https://api.blockspan.com/v1/collections/contract/' + nft + chain
    response = requests.get(url, headers={"accept": "application/json", "X-API-KEY": keys.blockspan})
    data = response.json()
    amount = data
    return amount["exchange_data"][0]["stats"]["floor_price"]

def get_nft_price(nft, chain):
    if chain == "eth":
        return nfts.eco_price_eth, nfts.liq_price_eth, nfts.borrow_price_eth, nfts.dex_price_eth, \
            nfts.magister_price_eth
    if chain == "bsc":
        return nfts.eco_price_bsc, nfts.liq_price_bsc, nfts.borrow_price_bsc, nfts.dex_price_bsc, \
            nfts.magister_price_bsc
    if chain == "poly":
        return nfts.eco_price_poly, nfts.liq_price_poly, nfts.borrow_price_poly, nfts.dex_price_poly, \
            nfts.magister_price_poly
    if chain == "opti":
        return nfts.eco_price_opti, nfts.liq_price_opti, nfts.borrow_price_opti, nfts.dex_price_opti, \
            nfts.magister_price_opti
    if chain == "arb":
        return nfts.eco_price_arb, nfts.liq_price_arb, nfts.borrow_price_arb, nfts.dex_price_arb, \
            nfts.magister_price_arb

def get_os_nft(slug):
    slug = slug
    headers = {"X-API-KEY": keys.os}
    url = "https://api.opensea.io/api/v1/collection/" + slug
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def get_pool_liq_balance(wallet, token, chain):
    if chain == "eth":
        url = f'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress='
        response = requests.get(url + token + '&address=' + wallet + '&tag=latest' + keys.ether)
        data = response.json()
        return int(data["result"])
    if chain == "bsc":
        url = f'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress='
        response = requests.get(url + token + '&address=' + wallet + '&tag=latest' + keys.bsc)
        data = response.json()
        return int(data["result"])
    if chain == "arb":
        url = f'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress='
        response = requests.get(url + token + '&address=' + wallet + '&tag=latest' + keys.arb)
        data = response.json()
        return int(data["result"])
    if chain == "poly":
        url = f'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress='
        response = requests.get(url + token + '&address=' + wallet + '&tag=latest' + keys.poly)
        data = response.json()
        return int(data["result"])
    if chain == "opti":
        url = f'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress='
        response = requests.get(url + token + '&address=' + wallet + '&tag=latest' + keys.opti)
        data = response.json()
        return int(data["result"])

def get_quote():
    response = requests.get('https://type.fit/api/quotes')
    data = response.json()
    quote_raw = (random.choice(data))
    quote = quote_raw["text"] + quote_raw["author"]
    quote = f'`"{quote_raw["text"]}"\n\n-{quote_raw["author"]}`'
    return quote

def get_scan(token, chain):
    chain_number = ""
    if chain == "eth":
        chain_number = 1
    if chain == "bsc":
        chain_number = 56
    url = f"https://api.gopluslabs.io/api/v1/token_security/{chain_number}?contract_addresses={token}"
    response = requests.get(url)
    data = response.json()
    return data["result"]

def get_signers(wallet):
    url = f'https://safe-transaction-mainnet.safe.global/api/v1/safes/{wallet}/'
    response = requests.get(url)
    result = response.json()
    return result

def get_snapshot():
    url = 'https://hub.snapshot.org/graphql'
    query = {"query": "query { proposals ( first: 1, skip: 0, where: { space_in: [\"X7COMMUNITY.eth\"]}, "
                      "orderBy: \"created\", orderDirection: desc ) { id title start end snapshot state choices "
                      "scores scores_total author }}"}
    response = requests.get(url, query)
    data = response.json()
    return data

def get_supply(token, chain):
    url = ""
    if chain == "eth":
        url = f'https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={token}{keys.ether}'
    if chain == "bsc":
        url = f'https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress={token}{keys.bsc}'
    response = requests.get(url)
    data = response.json()
    result = data["result"]
    return result

def get_today():
    current_day = str(datetime.now().day)
    current_month = str(datetime.now().month)
    url = f'http://history.muffinlabs.com/date/{current_month}/{current_day}'
    response = requests.get(url)
    data = response.json()
    return data

def get_token_balance(wallet, token, chain):
    if chain == "eth":
        url = 'https://api.etherscan.io/' \
              'api?module=account&action=tokenbalance&contractaddress='
        key = keys.ether
        response = requests.get(url + token + '&address=' + wallet + '&tag=latest' + key)
        data = response.json()
        amount = int(data["result"][:-18])
        return amount
    if chain == "bsc":
        url = 'https://api.bscscan.com/' \
              'api?module=account&action=tokenbalance&contractaddress='
        key = keys.bsc
        response = requests.get(url + token + '&address=' + wallet + '&tag=latest' + key)
        data = response.json()
        amount = int(data["result"][:-18])
        return amount
    if chain == "opti":
        url = 'https://api-optimistic.etherscan.io/' \
              'api?module=account&action=tokenbalance&contractaddress='
        key = keys.opti
        response = requests.get(url + token + '&address=' + wallet + '&tag=latest' + key)
        data = response.json()
        amount = int(data["result"][:-18])
        return amount
    if chain == "poly":
        url = 'https://api.polygonscan.com/' \
              'api?module=account&action=tokenbalance&contractaddress='
        key = keys.poly
        response = requests.get(url + token + '&address=' + wallet + '&tag=latest' + key)
        data = response.json()
        amount = int(data["result"][:-18])
        return amount
    if chain == "arb":
        url = 'https://api.arbiscan.io/' \
              'api?module=account&action=tokenbalance&contractaddress='
        key = keys.arb
        response = requests.get(url + token + '&address=' + wallet + '&tag=latest' + key)
        data = response.json()
        amount = int(data["result"][:-18])
        return amount

def get_token_data(token, chain):
    result = evm_api.token.get_token_metadata(
        api_key=keys.moralis, params={"addresses": [f"{token}"], "chain": chain})
    return result

def get_token_name(token, chain):
    result = evm_api.token.get_token_metadata(
        api_key=keys.moralis, params={"addresses": [f"{token}"], "chain": chain})
    return result[0]["name"], result[0]["symbol"]

def get_tx_from_hash(tx, chain):
    url = ""
    if chain == "eth":
        url = f'https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={tx}{keys.ether}'
    if chain == "bsc":
        url = f'https://api.bscscan.com/api?module=proxy&action=eth_getTransactionByHash&txhash={tx}{keys.bsc}'
    response = requests.get(url)
    data = response.json()
    return data

def get_tx(address, chain):
    if chain == "eth":
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc{keys.ether}"
        response = requests.get(url)
        data = response.json()
        return data

def get_tx_internal(address, chain):
    if chain == "eth":
        url = f"https://api.etherscan.io/api?module=account&action=txlistinternal&sort=" \
              f"desc&address={address}{keys.ether}"
        response = requests.get(url)
        data = response.json()
        return data

def get_verified(contract, chain):
    url = ""
    if chain == "eth":
        url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={contract}{keys.ether}"
    if chain == "bsc":
        url = f"https://api.bscscan.com/api?module=contract&action=getsourcecode&address={contract}{keys.bsc}"
    response = requests.get(url)
    data = response.json()
    for result in data["result"][0]["SourceCode"]:
        return "Yes"
    else:
        return "No"


# TWITTER
auth = tweepy.OAuthHandler(keys.twitter_api, keys.twitter_api_secret)
auth.set_access_token(keys.twitter_access, keys.twitter_access_secret)
twitter = tweepy.API(auth)
twitter_bearer = tweepy.Client(keys.twitter_bearer)

def get_space(space_id):
    url = f"https://api.twitter.com/2/spaces/{space_id}?space.fields=scheduled_start,title"
    headers = {"Authorization": "Bearer {}".format(keys.twitter_bearer), "User-Agent": "v2SpacesLookupPython"}
    response = requests.request("GET", url, headers=headers)
    result = response.json()
    return result["data"]
