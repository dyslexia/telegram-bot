import logging
import api
from web3 import Web3
from web3.exceptions import Web3Exception
import asyncio
import keys
import ca
from datetime import datetime, timezone
import random
from PIL import Image, ImageDraw, ImageFont
import media
import url
from telegram.ext import *
from telegram import *

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

getblock_url = f'https://bsc.getblock.io/{keys.getblock}'
web3 = Web3(Web3.HTTPProvider(getblock_url))

factory = web3.eth.contract(address=ca.pancake, abi=api.get_abi(ca.pancake, "bsc"))
ill001 = web3.eth.contract(address=ca.ill001, abi=api.get_abi(ca.ill001, "bsc"))
ill002 = web3.eth.contract(address=ca.ill002, abi=api.get_abi(ca.ill002, "bsc"))
ill003 = web3.eth.contract(address=ca.ill003, abi=api.get_abi(ca.ill003, "bsc"))
time_lock = web3.eth.contract(address=ca.time_lock, abi=api.get_abi(ca.time_lock, "bsc"))

async def new_loan(event):
    im1 = Image.open((random.choice(media.blackhole)))
    im2 = Image.open(media.eth_logo)
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
    i1 = ImageDraw.Draw(im1)
    i1.text((26, 30),
            f'New Loan Originated (ETH)\n\n{event["loanID"]}\n\n'
            f'https://etherscan.io/tx/{event["transactionHash"].hex()}',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await application.bot.send_photo(
        "-1001780235511",
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'*New Loan Originated (ETH)*\n\n{event["loanID"]}\n\n'
                f'https://etherscan.io/tx/{event["transactionHash"].hex()}', parse_mode='Markdown')

async def new_pair(event):
    print("Pair found")
    tx = api.get_tx(event["transactionHash"].hex(), "bsc")
    liq = api.get_liquidity(event["args"]["pair"], "bsc")
    if event["args"]["token0"] == ca.wbnb:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token_name = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = int(weth) * 2 * api.get_native_price("bnb") / 10 ** 18
    elif event["args"]["token0"] in ca.bscpairs:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token_name = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = 0
    elif event["args"]["token1"] in ca.bscpairs:
        native = api.get_token_name(event["args"]["token1"], "bsc")
        token_name = api.get_token_name(event["args"]["token0"], "bsc")
        token_address = event["args"]["token0"]
        weth = liq["reserve1"]
        token = liq["reserve0"]
        dollar = 0
    elif event["args"]["token0"] in ca.bscethpairs:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token_name = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = dollar = int(weth) * 2 * api.get_native_price("eth") / 10 ** 18
    elif event["args"]["token1"] in ca.bscethpairs:
        native = api.get_token_name(event["args"]["token1"], "bsc")
        token_name = api.get_token_name(event["args"]["token0"], "bsc")
        token_address = event["args"]["token0"]
        weth = liq["reserve1"]
        token = liq["reserve0"]
        dollar = dollar = int(weth) * 2 * api.get_native_price("eth") / 10 ** 18
    elif event["args"]["token0"] in ca.bscethpairs:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token_name = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = int(weth) * 2 / 10 ** 18
    elif event["args"]["token1"] in ca.bscethpairs:
        native = api.get_token_name(event["args"]["token1"], "bsc")
        token_name = api.get_token_name(event["args"]["token0"], "bsc")
        token_address = event["args"]["token0"]
        weth = liq["reserve1"]
        token = liq["reserve0"]
        dollar = int(weth) * 2 / 10 ** 18
    else:
        native = api.get_token_name(event["args"]["token1"], "bsc")
        token_name = api.get_token_name(event["args"]["token0"], "bsc")
        token_address = event["args"]["token0"]
        weth = liq["reserve1"]
        token = liq["reserve0"]
        dollar = int(weth) * 2 * api.get_native_price("bnb") / 10 ** 18
    info = api.get_token_data(token_address, "bsc")
    if info[0]["decimals"] == "" or info[0]["decimals"] == "0" or not info[0]["decimals"]:
        supply = int(api.get_supply(token_address, "bsc"))
    else:
        supply = int(api.get_supply(token_address, "bsc")) / 10 ** int(info[0]["decimals"])
    if dollar == 0:
        liquidity_text = 'Total Liquidity: Unavailable'
    else:
        liquidity_text = f'Total Liquidity: ${"{:0,.0f}".format(dollar)}'
    verified = api.get_verified(token_address, "bsc")
    status = ""
    renounced = ""
    lock = ""
    if verified == "No":
        return
    if verified == "Yes":
        contract = web3.eth.contract(address=token_address, abi=api.get_abi(token_address, "eth"))
        verified = '✅ Contract Verified'
        scan = api.get_scan(token_address, "bsc")
        try:
            if (scan[f'{token_address.lower()}']["is_honeypot"]) == 1:
                print('Skip - Honey Pot')
                return
        except (Web3Exception, Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
            print(f'Error: {e}')
        try:
            if (scan[f'{token_address.lower()}']["is_mintable"]) == 1:
                print('Skip - Mintable')
                return
        except (Web3Exception, Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
            print(f'Error: {e}')
        try:
            if (scan[f'{token_address.lower()}']["is_in_dex"]) == 1:
                if (scan[f'{token_address.lower()}']["cannot_sell_all"]) == 1:
                    print('Skip - Cannot Sell')
                    return
                if scan[f'{str(token_address).lower()}']["lp_holders"][0]["is_locked"] == 1:
                    lock = f'✅ Liquidity Locked ({scan[str(token_address).lower()]["lp_holders"][0]["percent"][:4]}%)'
        except (Web3Exception, Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
            print(f'Error: {e}')
        try:
            if (scan[f'{token_address.lower()}']["honeypot_with_same_creator"]) == 1:
                print('Skip - Honey Pot')
                return
        except (Web3Exception, Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
            print(f'Error: {e}')
        try:
            owner = contract.functions.owner().call()
            if owner == "0x0000000000000000000000000000000000000000":
                renounced = '✅ Contract Renounced'
        except (Web3Exception, Exception, TimeoutError, ValueError, StopAsyncIteration):
            status = verified
    pool = int(tx["result"]["value"], 0) / 10 ** 18
    deployer = tx["result"]["from"]
    if pool == 0 or pool == "" or not pool:
        pool_text = "Launched Pool Amount: Unavailable"
    else:
        pool_dollar = float(pool) * float(api.get_native_price("bnb")) / 1 ** 18
        pool_text = f'Launched Pool Amount: {pool} BNB (${"{:0,.0f}".format(pool_dollar)})'
    status = f'{verified}\n{renounced}\n{lock}\n'
    im1 = Image.open((random.choice(media.blackhole)))
    im2 = Image.open(media.bsc_logo)
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
    i1 = ImageDraw.Draw(im1)
    i1.text((26, 30),
            f'New Pair Created (BSC)\n\n'
            f'{token_name[0]} ({token_name[1]}/{native[1]})\n\n'
            f'Supply: {"{:0,.0f}".format(supply)} ({info[0]["decimals"]} Decimals)\n\n'
            f'{pool_text}\n\n'
            f'{liquidity_text}\n\n'
            f'SCAN:\n'
            f'{status}\n',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await application.bot.send_photo(
        ca.alerts_id,
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'*New Pair Created (BSC)*\n\n'
                f'{token_name[0]} ({token_name[1]}/{native[1]})\n\n'
                f'Token Address:\n`{token_address}`\n\n'
                f'Supply: {"{:0,.0f}".format(supply)} ({info[0]["decimals"]} Decimals)\n\n'
                f'{pool_text}\n\n'
                f'SCAN:\n'
                f'🖥️ [Deployer]({url.ether_address}{deployer})\n'
                f'{liquidity_text}\n\n'
                f'{status}', parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=f'Buy On Xchange (COMING SOON)', url=f'{url.xchange_buy_bsc}')],
             [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_bsc}{event["args"]["pair"]}')],
             [InlineKeyboardButton(text='Token Contract', url=f'{url.bsc_address}{token_address}')],
             [InlineKeyboardButton(text='Factory TX', url=f'{url.bsc_tx}{event["transactionHash"].hex()}')], ]))
    print(f'V2 Pair sent: ({token_name[1]}/{native[1]})')

async def time_lock_extend(event):
    token_name = api.get_token_name(event["args"]["tokenAddress"], "eth")
    time = datetime.fromtimestamp(event["tokenAddress"], timezone.utc)
    im1 = Image.open((random.choice(media.blackhole)))
    im2 = Image.open(media.eth_logo)
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
    i1 = ImageDraw.Draw(im1)
    i1.text((26, 30),
            f'Token Unlock Time Extended (ETH)\n\n*{token_name}*\n\n'
            f'{event["tokenAddress"]}\n'
            f'{time}\n\n'
            f'https://etherscan.io/tx/{event["transactionHash"].hex()}',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await application.bot.send_photo(
        "-1001780235511",
        photo=open(r"media\blackhole.png"),
        caption=f'*Token Unlock Time Extended (ETH)*\n\n*{token_name}*\n\n'
                f'{event["tokenAddress"]}\n'
                f'{time}\n\n'
                f'https://etherscan.io/tx/{event["transactionHash"].hex()}', parse_mode='Markdown')

async def log_loop(
        v2_pair_filter, ill001_filter, ill002_filter, ill003_filter, time_lock_filter, poll_interval):
    while True:
        try:
            for PairCreated in v2_pair_filter.get_new_entries():
                await new_pair(PairCreated)
                application = ApplicationBuilder().token(random.choice(keys.tokens)).connection_pool_size(512).build()
            await asyncio.sleep(poll_interval)
            for TokenUnlockTimeExtended in time_lock_filter.get_new_entries():
                await time_lock_extend(TokenUnlockTimeExtended)
                application = ApplicationBuilder().token(random.choice(keys.tokens)).connection_pool_size(512).build()
            await asyncio.sleep(poll_interval)
            for LoanOriginated in ill001_filter.get_new_entries():
                await new_loan(LoanOriginated)
                application = ApplicationBuilder().token(random.choice(keys.tokens)).connection_pool_size(512).build()
            await asyncio.sleep(poll_interval)
            for LoanOriginated in ill002_filter.get_new_entries():
                await new_loan(LoanOriginated)
                application = ApplicationBuilder().token(random.choice(keys.tokens)).connection_pool_size(512).build()
            await asyncio.sleep(poll_interval)
            for LoanOriginated in ill003_filter.get_new_entries():
                await new_loan(LoanOriginated)
                application = ApplicationBuilder().token(random.choice(keys.tokens)).connection_pool_size(512).build()
            await asyncio.sleep(poll_interval)
        except (Web3Exception, Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
            print(f'Loop Error: {e}')
            break
        break

def main():
    print("Scanning BSC Network")
    pair_filter = factory.events.PairCreated.create_filter(fromBlock='latest')
    ill001_filter = ill001.events.LoanOriginated.create_filter(fromBlock='latest')
    ill002_filter = ill002.events.LoanOriginated.create_filter(fromBlock='latest')
    ill003_filter = ill003.events.LoanOriginated.create_filter(fromBlock='latest')
    time_lock_filter = ill003.events.LoanOriginated.create_filter(fromBlock='latest')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(asyncio.gather(log_loop(
            pair_filter, ill001_filter, ill002_filter, ill003_filter, time_lock_filter, 2)))
    except (Web3Exception, Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
        print(f'Error: {e}')
        loop.close()
        asyncio.run(main())
    finally:
        loop.close()


if __name__ == "__main__":
    application = ApplicationBuilder().token(random.choice(keys.tokens)).connection_pool_size(512).build()
    asyncio.run(main())
