from datetime import datetime
import keys
from moralis import evm_api
import nfts
from pycoingecko import CoinGeckoAPI
import random
import tweepy
import requests


def get_abi(contract, chain):
    chains_info = {
        "eth": {"url": "https://api.etherscan.io/api", "key": keys.ether},
        "bsc": {"url": "https://api.bscscan.com/api", "key": keys.bsc},
        "arb": {"url": "https://api.arbiscan.io/api", "key": keys.arb},
        "opti": {"url": "https://api-optimistic.etherscan.io/api", "key": keys.opti},
        "poly": {"url": "https://api.polygonscan.com/api", "key": keys.poly},
    }

    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")

    url = f'{chains_info[chain]["url"]}?module=contract&action=getsourcecode&address={contract}{chains_info[chain]["key"]}'

    response = requests.get(url)
    data = response.json()
    result = data["result"][0]["ABI"]
    return result


def get_ath(token):
    base_url = "https://api.coingecko.com/api/v3/coins"
    url = (
        f"{base_url}/{token}"
        "?localization=false"
        "&tickers=false"
        "&market_data=true"
        "&community_data=false"
        "&developer_data=false"
        "&sparkline=false"
    )

    response = requests.get(url)
    data = response.json()
    market_data = data["market_data"]

    ath = market_data["ath"]["usd"]
    change = market_data["ath_change_percentage"]["usd"]
    date = market_data["ath_date"]["usd"]

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
    base_url = "https://api.coingecko.com/api/v3/search"
    url = f"{base_url}?query={token}"
    response = requests.get(url)
    result = response.json()
    return result


def get_gas(chain):
    chains_info = {
        "eth": {"url": "https://api.etherscan.io/api", "key": keys.ether},
        "poly": {"url": "https://api.polygonscan.com/api", "key": keys.poly},
        "bsc": {"url": "https://api.bscscan.com/api", "key": keys.bsc},
    }

    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")

    url = f'{chains_info[chain]["url"]}?module=gastracker&action=gasoracle{chains_info[chain]["key"]}'
    response = requests.get(url)
    data = response.json()

    return data


def get_holders(token):
    base_url = "https://api.ethplorer.io/getTokenInfo"
    url = f"{base_url}/{token}{keys.ethplorer}"
    response = requests.get(url)
    data = response.json()
    return data.get("holdersCount")


def get_liquidity(pair, chain):
    return evm_api.defi.get_pair_reserves(
        api_key=keys.moralis, params={"chain": chain, "pair_address": pair}
    )


def get_native_balance(wallet, chain):
    chains_info = {
        "opti": {"url": "https://api-optimistic.etherscan.io/api", "key": keys.opti},
        "eth": {"url": "https://api.etherscan.io/api", "key": keys.ether},
        "arb": {"url": "https://api.arbiscan.io/api", "key": keys.arb},
        "bsc": {"url": "https://api.bscscan.com/api", "key": keys.bsc},
        "poly": {"url": "https://api.polygonscan.com/api", "key": keys.poly},
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
            "key": keys.ether,
            "field": "ethusd",
        },
        "bnb": {
            "url": "https://api.bscscan.com/api?module=stats&action=bnbprice",
            "key": keys.bsc,
            "field": "ethusd",
        },
        "matic": {
            "url": "https://api.polygonscan.com/api?module=stats&action=maticprice",
            "key": keys.poly,
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
        api_key=keys.moralis,
        params={"chain": chain, "format": "decimal", "address": nft},
    )


def get_nft_holder_count(nft, chain):
    url = f"https://api.blockspan.com/v1/collections/contract/{nft}{chain}"
    response = requests.get(
        url, headers={"accept": "application/json", "X-API-KEY": keys.blockspan}
    )
    data = response.json()
    return data.get("total_tokens")


def get_nft_floor(nft, chain):
    url = f"https://api.blockspan.com/v1/collections/contract/{nft}{chain}"
    response = requests.get(
        url, headers={"accept": "application/json", "X-API-KEY": keys.blockspan}
    )
    data = response.json()
    return data["exchange_data"][0]["stats"].get("floor_price")


def get_nft_price(nft, chain):
    nft_prices = {
        "eth": (
            nfts.eco_price_eth,
            nfts.liq_price_eth,
            nfts.borrow_price_eth,
            nfts.dex_price_eth,
            nfts.magister_price_eth,
        ),
        "bsc": (
            nfts.eco_price_bsc,
            nfts.liq_price_bsc,
            nfts.borrow_price_bsc,
            nfts.dex_price_bsc,
            nfts.magister_price_bsc,
        ),
        "poly": (
            nfts.eco_price_poly,
            nfts.liq_price_poly,
            nfts.borrow_price_poly,
            nfts.dex_price_poly,
            nfts.magister_price_poly,
        ),
        "opti": (
            nfts.eco_price_opti,
            nfts.liq_price_opti,
            nfts.borrow_price_opti,
            nfts.dex_price_opti,
            nfts.magister_price_opti,
        ),
        "arb": (
            nfts.eco_price_arb,
            nfts.liq_price_arb,
            nfts.borrow_price_arb,
            nfts.dex_price_arb,
            nfts.magister_price_arb,
        ),
    }
    return nft_prices.get(chain)


def get_os_nft(slug):
    url = f"https://api.opensea.io/api/v1/collection/{slug}"
    response = requests.get(url, headers={"X-API-KEY": keys.os})
    return response.json()


def get_pool_liq_balance(wallet, token, chain):
    chain_keys = {
        "eth": keys.ether,
        "bsc": keys.bsc,
        "arb": keys.arb,
        "poly": keys.poly,
        "opti": keys.opti,
    }
    url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={token}&address={wallet}&tag=latest{chain_keys.get(chain)}"
    response = requests.get(url)
    data = response.json()
    return int(data.get("result", 0))


def get_quote():
    response = requests.get("https://type.fit/api/quotes")
    data = response.json()
    quote_raw = random.choice(data)
    quote = quote_raw["text"] + quote_raw["author"]
    quote = f'`"{quote_raw["text"]}"\n\n-{quote_raw["author"]}`'
    return quote


def get_random_pioneer_number():
    min_num = 1
    max_num = 641
    number = random.randint(min_num, max_num)
    return str(number).zfill(4)


def get_scan(token, chain):
    chain_number = ""
    if chain == "eth":
        chain_number = 1
    if chain == "bsc":
        chain_number = 56
    if chain == "arb":
        chain_number = 42161
    if chain == "opti":
        chain_number = 10
    if chain == "poly":
        chain_number = 137
    url = f"https://api.gopluslabs.io/api/v1/token_security/{chain_number}?contract_addresses={token}"
    response = requests.get(url)
    data = response.json()
    return data["result"]


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
        url = f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={token}{keys.ether}"
    if chain == "bsc":
        url = f"https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress={token}{keys.bsc}"
    if chain == "arb":
        url = f"https://api.arbiscan.io/api?module=stats&action=tokensupply&contractaddress={token}{keys.arb}"
    if chain == "opti":
        url = (
            f"https://api.optimistic-etherscan.io/api?module=stats&action=tokensupply&contractaddress={token}"
            f"{keys.opti}"
        )
    if chain == "poly":
        url = f"https://api.polygonscan.com/api?module=stats&action=tokensupply&contractaddress={token}{keys.poly}"
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
        key = keys.ether
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
        key = keys.bsc
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
        key = keys.opti
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
        key = keys.poly
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
        key = keys.arb
        response = requests.get(
            url + token + "&address=" + wallet + "&tag=latest" + key
        )
        data = response.json()
        amount = int(data["result"][:-18])
        return amount


def get_token_data(token, chain):
    result = evm_api.token.get_token_metadata(
        api_key=keys.moralis, params={"addresses": [f"{token}"], "chain": chain}
    )
    return result


def get_token_name(token, chain):
    if chain == "poly":
        chain = "polygon"
    if chain == "arb":
        chain = "arbitrum"
    else:
        chain = chain
    result = evm_api.token.get_token_metadata(
        api_key=keys.moralis, params={"addresses": [f"{token}"], "chain": chain}
    )
    return result[0]["name"], result[0]["symbol"]


def get_tx_from_hash(tx, chain):
    url = ""
    if chain == "eth":
        url = f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={tx}{keys.ether}"
    if chain == "bsc":
        url = f"https://api.bscscan.com/api?module=proxy&action=eth_getTransactionByHash&txhash={tx}{keys.bsc}"
    if chain == "poly":
        url = f"https://api.polygonscan.com/api?module=proxy&action=eth_getTransactionByHash&txhash={tx}{keys.poly}"
    if chain == "arb":
        url = f"https://api.arbiscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={tx}{keys.arb}"
    if chain == "opti":
        url = (
            f"https://api.optimistic.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash="
            f"{tx}{keys.opti}"
        )
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
        url = (
            f"https://api.etherscan.io/api?module=account&action=txlistinternal&sort="
            f"desc&address={address}{keys.ether}"
        )
        response = requests.get(url)
        data = response.json()
        return data


def get_verified(contract, chain):
    url = ""
    if chain == "eth":
        url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={contract}{keys.ether}"
    if chain == "bsc":
        url = f"https://api.bscscan.com/api?module=contract&action=getsourcecode&address={contract}{keys.bsc}"
    if chain == "arb":
        url = f"https://api.arbican.io/api?module=contract&action=getsourcecode&address={contract}{keys.arb}"
    if chain == "poly":
        url = f"https://api.polygonscan.com/api?module=contract&action=getsourcecode&address={contract}{keys.poly}"
    if chain == "opti":
        url = f"https://api.optimistic-etherscan.com/api?module=contract&action=getsourcecode&address={contract}{keys.opti}"
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
twitter_v2 = tweepy.Client(keys.twitter_bearer)
