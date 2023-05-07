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
    tx = api.get_tx(event["transactionHash"].hex(), "bsc")
    pool = int(tx["result"]["value"], 0) / 10 ** 18
    liq = api.get_liquidity(event["args"]["pair"], "bsc")
    if pool == 0 or pool == "" or not pool:
        pool_text = "Launched Pool Amount: Unavailable"
    else:
        pool_dollar = float(pool) * float(api.get_native_price("bnb")) / 1 ** 18
        pool_text = f'Launched Pool Amount: {pool} BNB (${"{:0,.0f}".format(pool_dollar)})'
    if event["args"]["token0"] == ca.wbnb:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token_name = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = int(weth) * 2 * api.get_native_price("bnb") / 10 ** 18
        return
    if event["args"]["token0"] == ca.cake or event["args"]["token0"] == ca.matic:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token_name = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = 0
        return
    if event["args"]["token0"] == ca.beth or event["args"]["token0"] == ca.bweth:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token_name = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = dollar = int(weth) * 2 * api.get_native_price("eth") / 10 ** 18
        return
    if event["args"]["token0"] == ca.bep20usdt or event["args"]["token0"] == ca.busd:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token_name = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = int(weth) * 2
        return
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
        return
    else:
        supply = int(api.get_supply(token_address, "bsc")) / 10 ** int(info[0]["decimals"])
    if dollar == 0:
        liquidity_text = 'Total Liquidity: Unavailable'
    else:
        liquidity_text = f'Total Liquidity: ${"{:0,.0f}".format(dollar)}'
    verified = api.get_verified(token_address, "bsc")
    status = ""
    if verified == "Yes":
        status = 'Contract Verified: Yes'
        contract = web3.eth.contract(address=token_address, abi=api.get_abi(token_address, "bsc"))
        try:
            owner = contract.functions.owner().call()
            if owner == "0x0000000000000000000000000000000000000000":
                status = 'Contract Verified ✅\nContract Renounced ✅'
            else:
                status = 'Contract Verified ✅'
        except Web3Exception:
            status = 'Contract Verified ✅'
    if verified == "No":
        status = ''
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
            f'{status}\n\n',
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
                f'{liquidity_text}\n\n'
                f'{status}', parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=f'Buy On Xchange (COMING SOON)', url=f'{url.xchange_buy_bsc}')],
             [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_bsc}{event["args"]["pair"]}')],
             [InlineKeyboardButton(text='Token Contract', url=f'{url.bsc_token}{token_address}')],
             [InlineKeyboardButton(text='Factory TX', url=f'{url.bsc_tx}{event["transactionHash"].hex()}')], ]))

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
        pair_filter, ill001_filter, ill002_filter, ill003_filter, time_lock_filter, poll_interval):
    while True:
        for PairCreated in pair_filter.get_new_entries():
            await new_pair(PairCreated)
        await asyncio.sleep(poll_interval)
        for TokenUnlockTimeExtended in time_lock_filter.get_new_entries():
            await time_lock_extend(TokenUnlockTimeExtended)
        await asyncio.sleep(poll_interval)
        for LoanOriginated in \
                ill001_filter.get_new_entries() or ill002_filter.get_new_entries() or ill003_filter.get_new_entries():
            await new_loan(LoanOriginated)
        await asyncio.sleep(poll_interval)

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
    except Exception as e:
        print(f' Error: {e}')
        print(f'Trying Restart of BSC Network Scan')
        asyncio.run(main())


if __name__ == "__main__":
    application = ApplicationBuilder().token(keys.token).build()
    asyncio.run(main())
