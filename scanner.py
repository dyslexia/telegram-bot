import api
from telegram.ext import *
from web3 import Web3
import asyncio
import keys
import ca

infura_url = f'https://mainnet.infura.io/v3/{keys.infura}'
web3 = Web3(Web3.HTTPProvider(infura_url))

xchange = web3.eth.contract(address=ca.factory, abi=api.get_abi(ca.uniswap))

async def new_pair(event):
    name_token0 = api.get_token_name(event["args"]["token0"])
    name_token1 = api.get_token_name(event["args"]["token1"])
    await application.bot.send_photo(
        "-1001780235511",
        photo=open('media/logo10.png', 'rb'),
        caption=f'*New Pair Created*\n\n{event["args"]["pair"]}\n\n'
                f'Token 0: {name_token0}\n'
                f'Token 1: {name_token1}\n\n'
                f'https://etherscan.io/tx/{event["transactionHash"].hex()}', parse_mode='Markdown')


async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            await new_pair(PairCreated)
        await asyncio.sleep(poll_interval)


def main():
    print("Scanning X7 Finance Ecosystem...")
    pair_filter = xchange.events.PairCreated.create_filter(fromBlock='latest')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(
            asyncio.gather(log_loop(pair_filter, 2)))
    finally:
        loop.close()


if __name__ == "__main__":
    application = ApplicationBuilder().token(keys.token).build()
    asyncio.run(main())
