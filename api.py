from datetime import datetime
from moralis import evm_api

# import nfts
from pycoingecko import CoinGeckoAPI
import random
import tweepy
import requests
from typing import Tuple
import os
from dotenv import load_dotenv

# Load all environment variables
load_dotenv()


alchemy_arb = os.getenv("ALCHEMY_ARB")
alchemy_poly = os.getenv("ALCHEMY_POLY")
alchemy_opti = os.getenv("ALCHEMY_OPTI")
bsc = os.getenv("BSC")
ether = os.getenv("ETHER")
poly = os.getenv("POLY")
opti = os.getenv("OPTI")
arb = os.getenv("ARB")


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


COINGECKO_URL = "https://api.coingecko.com/api/v3"


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
    chains_info = {
        "eth": {"url": "https://api.etherscan.io/api", "key": ether},
        "poly": {"url": "https://api.polygonscan.com/api", "key": poly},
        "bsc": {"url": "https://api.bscscan.com/api", "key": bsc},
    }

    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")

    url = f'{chains_info[chain]["url"]}?module=gastracker&action=gasoracle{chains_info[chain]["key"]}'
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
    chains_info = {
        "opti": {"url": "https://api-optimistic.etherscan.io/api", "key": opti},
        "eth": {"url": "https://api.etherscan.io/api", "key": ether},
        "arb": {"url": "https://api.arbiscan.io/api", "key": arb},
        "bsc": {"url": "https://api.bscscan.com/api", "key": bsc},
        "poly": {"url": "https://api.polygonscan.com/api", "key": poly},
    }

    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")

    url = f'{chains_info[chain]["url"]}?module=account&action=balancemulti&address={wallet}&tag=latest{chains_info[chain]["key"]}'
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
    return data.get("total_tokens")


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


CHAIN_KEYS = {
    "eth": ether,
    "bsc": bsc,
    "arb": arb,
    "poly": poly,
    "opti": opti,
}

BASE_API_URL = "https://api.etherscan.io/api"


def get_pool_liq_balance(wallet, token, chain):
    url = f"{BASE_API_URL}?module=account&action=tokenbalance&contractaddress={token}&address={wallet}&tag=latest{CHAIN_KEYS.get(chain)}"
    response = requests.Session().get(url)
    data = response.json()
    return int(data["result"] or 0)


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
    # dictionary that maps chain name to chain number
    chains = {"eth": 1, "bsc": 56, "arb": 42161, "opti": 10, "poly": 137}

    # get the chain number corresponding to the input chain name
    chain_number = chains.get(chain)

    # raise a ValueError if the input chain name is not valid
    if not chain_number:
        raise ValueError(f"{chain} is not a valid chain")

    # create the URL for the API call using the chain number and token address
    url = f"https://api.gopluslabs.io/api/v1/token_security/{chain_number}?contract_addresses={token}"

    # make the API call and return the results as json
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
    url = ""
    if chain == "eth":
        url = f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={token}{ether}"
    if chain == "bsc":
        url = f"https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress={token}{bsc}"
    if chain == "arb":
        url = f"https://api.arbiscan.io/api?module=stats&action=tokensupply&contractaddress={token}{arb}"
    if chain == "opti":
        url = (
            f"https://api.optimistic-etherscan.io/api?module=stats&action=tokensupply&contractaddress={token}"
            f"{opti}"
        )
    if chain == "poly":
        url = f"https://api.polygonscan.com/api?module=stats&action=tokensupply&contractaddress={token}{poly}"
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
    if chain == "eth":
        url = (
            "https://api.etherscan.io/"
            "api?module=account&action=tokenbalance&contractaddress="
        )
        key = ether
        response = requests.get(
            url + token + "&address=" + wallet + "&tag=latest" + key
        )
        data = response.json()
        amount = int(data["result"][:-18])
        return amount
    if chain == "bsc":
        url = (
            "https://api.bscscan.com/"
            "api?module=account&action=tokenbalance&contractaddress="
        )
        key = bsc
        response = requests.get(
            url + token + "&address=" + wallet + "&tag=latest" + key
        )
        data = response.json()
        amount = int(data["result"][:-18])
        return amount
    if chain == "opti":
        url = (
            "https://api-optimistic.etherscan.io/"
            "api?module=account&action=tokenbalance&contractaddress="
        )
        key = opti
        response = requests.get(
            url + token + "&address=" + wallet + "&tag=latest" + key
        )
        data = response.json()
        amount = int(data["result"][:-18])
        return amount
    if chain == "poly":
        url = (
            "https://api.polygonscan.com/"
            "api?module=account&action=tokenbalance&contractaddress="
        )
        key = poly
        response = requests.get(
            url + token + "&address=" + wallet + "&tag=latest" + key
        )
        data = response.json()
        amount = int(data["result"][:-18])
        return amount
    if chain == "arb":
        url = (
            "https://api.arbiscan.io/"
            "api?module=account&action=tokenbalance&contractaddress="
        )
        key = arb
        response = requests.get(
            url + token + "&address=" + wallet + "&tag=latest" + key
        )
        data = response.json()
        amount = int(data["result"][:-18])
        return amount


def get_token_data(token: str, chain: str) -> dict:
    # Create a dictionary to map chain names to their verbose names
    chain_names = {"poly": "polygon", "arb": "arbitrum"}
    # Check if the chain name is valid
    if chain not in {"eth", "bsc", "opti", "poly", "arb"}:
        raise ValueError("Invalid chain name")

    # If chain name is present in chain_names then it must be updated to the verbose name
    chain = chain_names.get(chain, chain)
    # Get token metadata using Moralis API
    result = evm_api.token.get_token_metadata(
        api_key=os.getenv("MORALIS_API_KEY"),
        params={"addresses": [f"{token}"], "chain": chain},
    )
    return result


def get_token_name(token: str, chain: str) -> Tuple[str, str]:
    # Call get_token_data function to get the token metadata
    result = get_token_data(token, chain)
    # Extract the name and symbol from token metadata and return as a tuple
    return result[0]["name"], result[0]["symbol"]


API_ENDPOINTS = {
    "eth": "https://api.etherscan.io/api",
    "bsc": "https://api.bscscan.com/api",
    "poly": "https://api.polygonscan.com/api",
    "arb": "https://api.arbiscan.io/api",
    "opti": "https://api.optimistic.etherscan.io/api",
}


def get_tx_from_hash(tx, chain, api_key):
    api_endpoint = API_ENDPOINTS.get(chain)

    if api_endpoint is None:
        raise ValueError(f"Unsupported chain: {chain}")

    params = {
        "module": "proxy",
        "action": "eth_getTransactionByHash",
        "txhash": f"{tx}{api_key}",
    }

    response = requests.get(api_endpoint, params=params)
    response.raise_for_status()

    return response.json()


def get_tx(address: str, chain: str, internal: bool = False) -> dict:
    """
    Given an Ethereum address and chain name, retrieves the transactions for the address
    from Etherscan's API.

    address: str     - Ethereum address
    chain: str       - Blockchain name. Supported: "eth"
    internal: bool   - Flag to retrieve internal transactions as well (Default: False)

    Returns: dict    - Transaction data in JSON format
    """
    action = "txlistinternal" if internal else "txlist"
    url = f"https://api.etherscan.io/api?module=account&action={action}&sort=desc&address={address}{ether}"
    response = requests.get(url)
    data = response.json()
    return data


def get_verified(contract, chain):
    api_url = {
        "eth": f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={contract}{ether}",
        "bsc": f"https://api.bscscan.com/api?module=contract&action=getsourcecode&address={contract}{bsc}",
        "arb": f"https://api.arbican.io/api?module=contract&action=getsourcecode&address={contract}{arb}",
        "poly": f"https://api.polygonscan.com/api?module=contract&action=getsourcecode&address={contract}{poly}",
        "opti": f"https://api.optimistic-etherscan.com/api?module=contract&action=getsourcecode&address={contract}{opti}",
    }
    response = requests.get(api_url[chain])
    data = response.json()
    if "SourceCode" in data["result"][0]:
        return "Yes"
    else:
        return "No"


# TWITTER
auth = tweepy.OAuthHandler(os.getenv("TWITTER_API"), os.getenv("TWITTER_API_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS"), os.getenv("TWITTER_ACCESS_SECRET"))
twitter = tweepy.API(auth)
twitter_v2 = tweepy.Client(os.getenv("TWITTER_BEARER"))
