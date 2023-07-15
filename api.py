from datetime import datetime
from moralis import evm_api
import csv
from pycoingecko import CoinGeckoAPI
import random
import tweepy
import requests
from typing import Tuple
import os
import ca
from dotenv import load_dotenv
load_dotenv()


alchemy_arb = os.getenv("ALCHEMY_ARB")
alchemy_poly = os.getenv("ALCHEMY_POLY")
alchemy_opti = os.getenv("ALCHEMY_OPTI")
bsc = os.getenv("BSC")
ether = os.getenv("ETHER")
poly = os.getenv("POLY")
opti = os.getenv("OPTI")
arb = os.getenv("ARB")
COINGECKO_URL = "https://api.coingecko.com/api/v3"


class ChainInfo:
    def __init__(self, url: str, key: str):
        self.url = url
        self.key = key


chains_info = {
    "eth": ChainInfo("https://api.etherscan.io/api", ether),
    "bsc": ChainInfo("https://api.bscscan.com/api", bsc),
    "arb": ChainInfo("https://api.arbiscan.io/api", arb),
    "opti": ChainInfo("https://api-optimistic.etherscan.io/api", opti),
    "poly": ChainInfo("https://api.polygonscan.com/api", poly),
}


def get_abi(contract: str, chain: str) -> str:
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=contract&action=getsourcecode&address={contract}{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    result = data["result"][0]["ABI"]
    return result


def get_ath(token):
    url = (
        f"https://api.coingecko.com/api/v3/coins/{token}?localization=false&tickers=false&market_data="
        "true&community_data=false&developer_data=false&sparkline=false"
    )
    response = requests.get(url)
    data = response.json()
    value = data["market_data"]
    ath = value["ath"]["usd"]
    change = value["ath_change_percentage"]["usd"]
    date = value["ath_date"]["usd"]
    return ath, change, date


def get_cg_price(token):
    coingecko = CoinGeckoAPI()
    cg = coingecko.get_price(
        ids=token,
        vs_currencies="usd",
        include_24hr_change="true",
        include_24hr_vol="true",
        include_market_cap="true",
    )
    return cg


def get_cg_search(token):
    url = "https://api.coingecko.com/api/v3/search?query=" + token
    response = requests.get(url)
    result = response.json()
    return result


def get_gas(chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f'{chain_info.url}?module=gastracker&action=gasoracle{chain_info.key}'
    response = requests.get(url)
    data = response.json()
    return data


def get_holders(token):
    base_url = "https://api.ethplorer.io/getTokenInfo"
    url = f"{base_url}/{token}{os.getenv('ETHPLORER_API_KEY')}"
    response = requests.get(url)
    data = response.json()
    return data.get("holdersCount")


def get_liquidity(pair, chain):
    return evm_api.defi.get_pair_reserves(
        api_key=os.getenv("MORALIS_API_KEY"),
        params={"chain": chain, "pair_address": pair},
    )


def get_native_balance(wallet, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f'{chain_info.url}?module=account&action=balancemulti&address={wallet}&tag=latest{chain_info.key}'
    response = requests.get(url)
    data = response.json()
    amount_raw = float(data["result"][0]["balance"])
    amount = str(amount_raw / 10**18)

    return amount


def get_native_price(token):
    tokens_info = {
        "eth": {
            "url": "https://api.etherscan.io/api?module=stats&action=ethprice",
            "key": ether,
            "field": "ethusd",
        },
        "bnb": {
            "url": "https://api.bscscan.com/api?module=stats&action=bnbprice",
            "key": bsc,
            "field": "ethusd",
        },
        "matic": {
            "url": "https://api.polygonscan.com/api?module=stats&action=maticprice",
            "key": poly,
            "field": "maticusd",
        },
    }

    if token not in tokens_info:
        raise ValueError(f"Invalid token: {token}")

    url = f"{tokens_info[token]['url']}&{tokens_info[token]['key']}"
    response = requests.get(url)
    data = response.json()
    value = float(data["result"][tokens_info[token]["field"]])

    return value


def get_nft_holder_list(nft, chain):
    return evm_api.nft.get_nft_owners(
        api_key=os.getenv("MORALIS_API_KEY"),
        params={"chain": chain, "format": "decimal", "address": nft},
    )


def get_nft_holder_count(nft, chain):
    url = f"https://api.blockspan.com/v1/collections/contract/{nft}{chain}"
    response = requests.get(
        url,
        headers={
            "accept": "application/json",
            "X-API-KEY": os.getenv("BLOCKSPAN_API_KEY"),
        },
    )
    data = response.json()
    return data.get("total_tokens", "0")


def get_nft_floor(nft, chain):
    url = f"https://api.blockspan.com/v1/collections/contract/{nft}{chain}"
    response = requests.get(
        url,
        headers={
            "accept": "application/json",
            "X-API-KEY": os.getenv("BLOCKSPAN_API_KEY"),
        },
    )
    data = response.json()
    return data["exchange_data"][0]["stats"].get("floor_price")


def get_nft_prices(nft):
    nft_prices = {
        "eth": [
            nft.eco_price_eth,
            nft.liq_price_eth,
            nft.borrow_price_eth,
            nft.dex_price_eth,
            nft.magister_price_eth,
        ],
        "bsc": [
            nft.eco_price_bsc,
            nft.liq_price_bsc,
            nft.borrow_price_bsc,
            nft.dex_price_bsc,
            nft.magister_price_bsc,
        ],
        "poly": [
            nft.eco_price_poly,
            nft.liq_price_poly,
            nft.borrow_price_poly,
            nft.dex_price_poly,
            nft.magister_price_poly,
        ],
        "opti": [
            nft.eco_price_opti,
            nft.liq_price_opti,
            nft.borrow_price_opti,
            nft.dex_price_opti,
            nft.magister_price_opti,
        ],
        "arb": [
            nft.eco_price_arb,
            nft.liq_price_arb,
            nft.borrow_price_arb,
            nft.dex_price_arb,
            nft.magister_price_arb,
        ],
    }
    return nft_prices


def get_os_nft(slug):
    url = f"https://api.opensea.io/api/v1/collection/{slug}"
    response = requests.get(url, headers={"X-API-KEY": os.getenv("OPENSEA_API_KEY")})
    return response.json()


def get_pool_liq_balance(wallet, token, chain):
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=account&action=tokenbalance&contractaddress={token}&address={wallet}&tag=latest{chain_info.key}"
    response = requests.Session().get(url)
    data = response.json()
    return int(data["result"] or 0)


def get_price(token, chain):
    api_key = os.getenv("MORALIS_API_KEY")
    params = {
        "address": token,
        "chain": "eth"
    }

    result = evm_api.token.get_token_price(
        api_key=api_key,
        params=params,
    )
    return result["usdPrice"]


def get_quote():
    response = requests.get("https://type.fit/api/quotes")
    data = response.json()
    quote_raw = random.choice(data)
    quote = quote_raw["text"] + quote_raw["author"]
    quote = f'`"{quote_raw["text"]}"\n\n-{quote_raw["author"]}`'
    return quote


def get_random_pioneer_number():
    min_num = 1
    max_num = 4480
    number = random.randint(min_num, max_num)
    return str(number).zfill(4)


def get_scan(token: str, chain: str) -> dict:
    chains = {"eth": 1, "bsc": 56, "arb": 42161, "opti": 10, "poly": 137}
    chain_number = chains.get(chain)
    if not chain_number:
        raise ValueError(f"{chain} is not a valid chain")
    url = f"https://api.gopluslabs.io/api/v1/token_security/{chain_number}?contract_addresses={token}"
    response = requests.get(url)
    return response.json()["result"]


def get_signers(wallet):
    url = f"https://safe-transaction-mainnet.safe.global/api/v1/safes/{wallet}/"
    response = requests.get(url)
    result = response.json()
    return result


def get_snapshot():
    url = "https://hub.snapshot.org/graphql"
    query = {
        "query": 'query { proposals ( first: 1, skip: 0, where: { space_in: ["X7COMMUNITY.eth"]}, '
        'orderBy: "created", orderDirection: desc ) { id title start end snapshot state choices '
        "scores scores_total author }}"
    }
    response = requests.get(url, query)
    data = response.json()
    return data


def get_supply(token, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f'{chain_info.url}?module=stats&action=tokensupply&contractaddress={token}{chain_info.key}'
    response = requests.get(url)
    data = response.json()
    result = data["result"]
    return result


def get_today():
    current_day = str(datetime.now().day)
    current_month = str(datetime.now().month)
    url = f"http://history.muffinlabs.com/date/{current_month}/{current_day}"
    response = requests.get(url)
    data = response.json()
    return data


def get_token_balance(wallet, token, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f'{chain_info.url}?module=account&action=tokenbalance&contractaddress={token}&address={wallet}&tag=latest{chain_info.key}'
    response = requests.get(url)
    data = response.json()
    amount = int(data["result"][:-18])
    return amount


def get_token_data(token: str, chain: str) -> dict:
    chain_names = {"poly": "polygon", "arb": "arbitrum"}
    if chain not in {"eth", "bsc", "opti", "poly", "arb"}:
        raise ValueError("Invalid chain name")

    chain = chain_names.get(chain, chain)
    result = evm_api.token.get_token_metadata(
        api_key=os.getenv("MORALIS_API_KEY"),
        params={"addresses": [f"{token}"], "chain": chain},
    )
    return result


def get_token_name(token: str, chain: str) -> Tuple[str, str]:
    result = get_token_data(token, chain)
    return result[0]["name"], result[0]["symbol"]


def get_tx_from_hash(tx, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f'{chain_info.url}?module=proxy&action=eth_getTransactionByHash&txhash={tx}{chain_info.key}'
    response = requests.get(url)
    data = response.json()
    return data


def get_tx(address, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f'{chain_info.url}?module=account&action=txlist&sort=desc&address={address}{chain_info.key}'
    response = requests.get(url)
    data = response.json()
    return data


def get_internal_tx(address, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f'{chain_info.url}?module=account&action=txlistinternal&sort=desc&address={address}{chain_info.key}'
    response = requests.get(url)
    data = response.json()
    return data


def get_verified(contract, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f'{chain_info.url}?module=contract&action=getsourcecode&address={contract}{chain_info.key}'
    response = requests.get(url)
    data = response.json()
    if "SourceCode" in data["result"][0]:
        return "Yes"
    else:
        return "No"


def read_csv_column(filename, column_index):
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        column_data = []
        for row in csv_reader:
            if len(row) > column_index and row[column_index] != '':
                column_data.append(row[column_index])
    return column_data


# TWITTER
auth = tweepy.OAuthHandler(os.getenv("TWITTER_API"), os.getenv("TWITTER_API_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS"), os.getenv("TWITTER_ACCESS_SECRET"))
twitter = tweepy.API(auth)
twitter_v2 = tweepy.Client(os.getenv("TWITTER_BEARER"))
