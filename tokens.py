import keys
from web3 import Web3
import os
from dotenv import load_dotenv
load_dotenv()

alchemy_eth = os.getenv("ALCHEMY_ETH")
alchemy_arb = os.getenv("ALCHEMY_ARB")
alchemy_poly = os.getenv("ALCHEMY_POLY")
alchemy_opti = os.getenv("ALCHEMY_OPTI")
key_bsc = os.getenv("BSC")
key_ether = os.getenv("ETHER")
key_poly = os.getenv("POLY")
key_opti = os.getenv("OPTI")
key_arb = os.getenv("ARB")

pairs = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"hasMinimums","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"mintFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"gasAmount","type":"uint256"}],"name":"mustBurn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint112","name":"minimumAmount","type":"uint112"}],"name":"setMinimumBalance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"feeAmountOverride","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swapWithDiscount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"sync","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"gasAmountToken0","type":"uint256"},{"internalType":"uint256","name":"gasAmountToken1","type":"uint256"}],"name":"syncSafe","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"tokenMinimumBalance","outputs":[{"internalType":"uint112","name":"","type":"uint112"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint112","name":"amount","type":"uint112"}],"name":"withdrawTokensAgainstMinimumBalance","outputs":[{"internalType":"uint112","name":"","type":"uint112"}],"stateMutability":"nonpayable","type":"function"}]'


class TokensInfo:
    def __init__(self, ca: str, pair: str, decimals: int, chain: str, logo: str = ""):
        self.ca = ca
        self.pair = pair
        self.decimals = decimals
        self.chain = chain
        self.logo = logo


info = {
    "xinu": TokensInfo("0x117546D1467d80C6BdE13910412c724383260CF9",
                       "0xbb1599c41b15383c4063b1adad18923fee559b18",
                       18,
                       "eth",
                       "https://www.dextools.io/resources/tokens/logos/ether/0x117546d1467d80c6bde13910412c724383260cf9.png"),
    "lld": TokensInfo("0xA43d2860B53CeCA1fd0dfa5Bd80A89994A080171",
                      "0xc7cAfa645Ec4fA43D4EF8F32AD1121aD36c8A626",
                      18,
                      "eth",
                      ""),
    "xpepe": TokensInfo("0xDBc7945C5403c589Ec39A9Aa8C5AF234C706f6a2",
                        "0x24d10e222fbd113d72b9cf78d118f53ff9e1737d",
                        18,
                        "eth",
                        ""),
    "xniper": TokensInfo("0x65F8b641d031C2344d10D5f435D4776ec2ec1cB5",
                      "0x70f53da18df905e7d1aaf37d049c355298b4a0a2",
                      9,
                      "eth",
                      ""),
    "xswap": TokensInfo("0xdbDB16Be6408d0774B48df546D32D6bF589e0710",
                      "0xc521efbe7bb2dbf1909a7775a85c08d5e5c6fa22",
                      9,
                      "eth",
                      ""),
    "quixlink": TokensInfo("0xf524f2D3f8e492BbCb618BCe36e911Eb55e8b368",
                      "0x744fd0ff7dea32d8024509e13fc408572bab53a9",
                      18,
                      "eth"
                      ""),
}


class UrlInfo:
    def __init__(self, scan: str, dext: str, w3: str, api: str, key: str):
        self.scan = scan
        self.dext = dext
        self.w3 = w3
        self.api = api
        self.key = key


chains = {
    "eth": UrlInfo(
        "https://etherscan.io/token/",
        "https://www.dextools.io/app/en/ether/pair-explorer/",
        Web3(Web3.HTTPProvider(f"https://eth-mainnet.g.alchemy.com/v2/{alchemy_eth}")),
        "https://api.etherscan.io/api",
        key_ether
    ),
    "bsc": UrlInfo(
        "https://bscscan.com/token/",
        "https://www.dextools.io/app/en/bnb/pair-explorer/",
        Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/")),
        "https://api.bscscan.com/api",
        key_bsc
    ),
    "arb": UrlInfo(
        "https://arbiscan.io/token/",
        "https://www.dextools.io/app/arbitrum/pair-explorer/",
        Web3(Web3.HTTPProvider(f"https://arb-mainnet.g.alchemy.com/v2/{alchemy_arb}")),
        "https://api.arbiscan.io/api",
        key_arb
    ),
    "opti": UrlInfo(
        "https://optimistic.etherscan.io/token/",
        "https://www.dextools.io/app/optimism/pair-explorer/",
        Web3(Web3.HTTPProvider(f"https://opt-mainnet.g.alchemy.com/v2/{alchemy_opti}")),
        "https://api-optimistic.etherscan.io/api",
        key_opti
    ),
    "poly": UrlInfo(
        "https://polygonscan.com/token/",
        "https://www.dextools.io/app/polygon/pair-explorer/",
        Web3(Web3.HTTPProvider(f"https://polygon-mainnet.g.alchemy.com/v2/{alchemy_poly}")),
        "https://api.polygonscan.com/api",
        key_poly
    )
}

