import os
import csv
import random
from typing import Tuple
from datetime import datetime

import tweepy
import requests
from moralis import evm_api
from dotenv import load_dotenv
from pycoingecko import CoinGeckoAPI

load_dotenv()

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
    "eth": ChainInfo(
        "https://api.etherscan.io/api",
        ether,
    ),
    "bsc": ChainInfo("https://api.bscscan.com/api", bsc),
    "arb": ChainInfo("https://api.arbiscan.io/api", arb),
    "opti": ChainInfo("https://api-optimistic.etherscan.io/api", opti),
    "poly": ChainInfo("https://api.polygonscan.com/api", poly),
}


# SCAN


def get_abi(contract: str, chain: str) -> str:
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=contract&action=getsourcecode&address={contract}{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    return data["result"][0]["ABI"]


def get_gas(chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=gastracker&action=gasoracle{chain_info.key}"
    response = requests.get(url)
    return response.json()


def get_native_balance(wallet, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=account&action=balancemulti&address={wallet}&tag=latest{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    amount_raw = float(data["result"][0]["balance"])
    return f"{amount_raw / 10 ** 18}"


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
    return float(data["result"][tokens_info[token]["field"]])


def get_pool_liq_balance(wallet, token, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=account&action=tokenbalance&contractaddress={token}&address={wallet}&tag=latest{chain_info.key}"
    response = requests.Session().get(url)
    data = response.json()
    return int(data["result"] or 0)


def get_supply(token, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=stats&action=tokensupply&contractaddress={token}{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    return data["result"]


def get_token_balance(wallet, token, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=account&action=tokenbalance&contractaddress={token}&address={wallet}&tag=latest{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    return int(data["result"][:-18])


def get_tx_from_hash(tx, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=proxy&action=eth_getTransactionByHash&txhash={tx}{chain_info.key}"
    response = requests.get(url)
    return response.json()


def get_tx(address, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=account&action=txlist&sort=desc&address={address}{chain_info.key}"
    response = requests.get(url)
    return response.json()


def get_internal_tx(address, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=account&action=txlistinternal&sort=desc&address={address}{chain_info.key}"
    response = requests.get(url)
    return response.json()


def get_verified(contract, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=contract&action=getsourcecode&address={contract}{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    return "Yes" if "SourceCode" in data["result"][0] else "No"


# CG


def get_ath(token):
    url = (
        f"https://api.coingecko.com/api/v3/coins/{token}?localization=false&tickers=false&market_data="
        "true&community_data=false&developer_data=false&sparkline=false"
    )
    response = requests.get(url)
    data = response.json()
    value = data["market_data"]
    return (
        value["ath"]["usd"],
        value["ath_change_percentage"]["usd"],
        value["ath_date"]["usd"],
    )


def get_cg_price(token):
    coingecko = CoinGeckoAPI()
    return coingecko.get_price(
        ids=token,
        vs_currencies="usd",
        include_24hr_change="true",
        include_24hr_vol="true",
        include_market_cap="true",
    )


def get_cg_search(token):
    url = "https://api.coingecko.com/api/v3/search?query=" + token
    response = requests.get(url)
    return response.json()


def get_mcap(token):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token}&vs_currencies=usd&include_market_cap=true"
    response = requests.get(url)
    data = response.json()
    return data[token]["usd_market_cap"]


# MORALIS


def get_liquidity(pair, chain):
    chain_mappings = {
        "eth": "eth",
        "arb": "arbitrum",
        "poly": "polygon",
        "bsc": "bsc",
        "opti": "optimism",
    }
    if chain in chain_mappings:
        chain = chain_mappings[chain]
    return evm_api.defi.get_pair_reserves(
        api_key=os.getenv("MORALIS_API_KEY"),
        params={"chain": chain, "pair_address": pair},
    )


def get_nft_holder_list(nft, chain):
    chain_mappings = {
        "eth": "eth",
        "arb": "arbitrum",
        "poly": "polygon",
        "bsc": "bsc",
        "opti": "optimism",
    }
    if chain in chain_mappings:
        chain = chain_mappings[chain]
    return evm_api.nft.get_nft_owners(
        api_key=os.getenv("MORALIS_API_KEY"),
        params={"chain": chain, "format": "decimal", "address": nft},
    )


def get_price(token, chain):
    chain_mappings = {
        "eth": "eth",
        "arb": "arbitrum",
        "poly": "polygon",
        "bsc": "bsc",
        "opti": "optimism",
    }
    if chain in chain_mappings:
        chain = chain_mappings[chain]
    api_key = os.getenv("MORALIS_API_KEY")
    result = evm_api.token.get_token_price(
        api_key=api_key,
        params={"address": token, "chain": chain},
    )
    return result["usdPrice"]


def get_token_data(token: str, chain: str) -> dict:
    chain_mappings = {
        "eth": "eth",
        "arb": "arbitrum",
        "poly": "polygon",
        "bsc": "bsc",
        "opti": "optimism",
    }
    if chain in chain_mappings:
        chain = chain_mappings[chain]
    result = evm_api.token.get_token_metadata(
        api_key=os.getenv("MORALIS_API_KEY"),
        params={"addresses": [f"{token}"], "chain": chain},
    )
    return result


def get_token_name(token: str, chain: str) -> Tuple[str, str]:
    chain_mappings = {
        "eth": "eth",
        "arb": "arbitrum",
        "poly": "polygon",
        "bsc": "bsc",
        "opti": "optimism",
    }
    if chain in chain_mappings:
        chain = chain_mappings[chain]
    result = evm_api.token.get_token_metadata(
        api_key=os.getenv("MORALIS_API_KEY"),
        params={"addresses": [f"{token}"], "chain": chain},
    )
    return result[0]["name"], result[0]["symbol"]


# BLOCKSPAN


def get_nft_holder_count(nft, chain):
    chain_mappings = {
        "eth": "eth-main",
        "arb": "arbitrum-main",
        "poly": "poly-main",
        "bsc": "bsc-main",
        "opti": "optimism-main",
    }
    if chain in chain_mappings:
        chain = chain_mappings[chain]
    url = f"https://api.blockspan.com/v1/collections/contract/{nft}?chain={chain}"
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
    chain_mappings = {
        "eth": ("eth-main", "ETH"),
        "arb": ("arbitrum-main", "ETH"),
        "poly": ("poly-main", "MATIC"),
        "bsc": ("bsc-main", "BNB"),
        "opti": (
            "optimism-main",
            "ETH",
        ),
    }
    if chain in chain_mappings:
        chain, chain_native = chain_mappings[chain]
    url = f"https://api.blockspan.com/v1/collections/contract/{nft}?chain={chain}"
    response = requests.get(
        url,
        headers={
            "accept": "application/json",
            "X-API-KEY": os.getenv("BLOCKSPAN_API_KEY"),
        },
    )
    data = response.json()
    exchange_data = data.get("exchange_data")
    if exchange_data is not None:
        for item in exchange_data:
            stats = item.get("stats")
            if stats is not None:
                floor_price = stats.get("floor_price")
                if floor_price is not None:
                    return floor_price
        return "N/A"
    else:
        return "N/A"


# OTHER


def get_fact():
    response = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
    quote = response.json()
    return quote["text"]


def get_holders(token):
    base_url = "https://api.ethplorer.io/getTokenInfo"
    url = f"{base_url}/{token}{os.getenv('ETHPLORER_API_KEY')}"
    response = requests.get(url)
    data = response.json()
    return data.get("holdersCount")


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


def get_quote():
    response = requests.get("https://type.fit/api/quotes")
    data = response.json()
    quote = random.choice(data)
    quote_text = quote["text"]
    quote_author = quote["author"]
    if quote_author.endswith(", type.fit"):
        quote_author = quote_author[:-10].strip()

    return f'`"{quote_text}"\n\n-{quote_author}`'


def get_random_pioneer_number():
    return f"{random.randint(1, 4480)}".zfill(4)


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
    return response.json()


def get_snapshot():
    url = "https://hub.snapshot.org/graphql"
    query = {
        "query": 'query { proposals ( first: 1, skip: 0, where: { space_in: ["X7COMMUNITY.eth"]}, '
        'orderBy: "created", orderDirection: desc ) { id title start end snapshot state choices '
        "scores scores_total author }}"
    }
    response = requests.get(url, query)
    return response.json()


def get_split(eth_value):
    founding_dev_percentage = 0.07
    pioneer_reward_pool_percentage = 0.06
    community_multisig_percentage = 0.32
    developers_multisig_percentage = 0.13
    x7r_percentage = 0.10
    x7dao_percentage = 0.10
    x7_constellations_percentage = 0.10
    lending_pool_percentage = 0.20
    treasury_percentage = 0.50
    treasury_share = eth_value * treasury_percentage
    founding_dev_share = treasury_share * founding_dev_percentage * 7
    pioneer_reward_pool_share = treasury_share * pioneer_reward_pool_percentage
    community_multisig_share = treasury_share * community_multisig_percentage
    developers_multisig_share = treasury_share * developers_multisig_percentage
    x7r_share = eth_value * x7r_percentage
    x7dao_share = eth_value * x7dao_percentage
    x7_constellations_share = eth_value * x7_constellations_percentage
    lending_pool_share = eth_value * lending_pool_percentage

    return {
        "X7R": x7r_share,
        "X7DAO": x7dao_share,
        "X7 Constellations": x7_constellations_share,
        "Lending Pool": lending_pool_share,
        "Treasury": treasury_share,
        "Founding X7 Devs Total": founding_dev_share,
        "Pioneer Reward Pool": pioneer_reward_pool_share,
        "Community Multi Sig": community_multisig_share,
        "Developers Multi Sig": developers_multisig_share,
    }


def get_today():
    now = datetime.now()
    url = f"http://history.muffinlabs.com/date/{now.month}/{now.day}"
    response = requests.get(url)
    return response.json()


def read_csv_column(filename, column_index):
    with open(filename, "r") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        column_data = []
        for row in csv_reader:
            if len(row) > column_index and row[column_index] != "":
                column_data.append(row[column_index])
    return column_data


# TWITTER
auth = tweepy.OAuthHandler(os.getenv("TWITTER_API"), os.getenv("TWITTER_API_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS"), os.getenv("TWITTER_ACCESS_SECRET"))
twitter = tweepy.API(auth)
twitter_v2 = tweepy.Client(os.getenv("TWITTER_BEARER"))
