import api
from web3 import Web3
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

infura_url = f'https://mainnet.infura.io/v3/{keys.infura}'
web3 = Web3(Web3.HTTPProvider(infura_url))

factory = web3.eth.contract(address=ca.uniswap, abi=api.get_abi(ca.uniswap, "eth"))
ill001 = web3.eth.contract(address=ca.ill001, abi=api.get_abi(ca.ill001, "eth"))
ill002 = web3.eth.contract(address=ca.ill002, abi=api.get_abi(ca.ill002, "eth"))
ill003 = web3.eth.contract(address=ca.ill003, abi=api.get_abi(ca.ill003, "eth"))
time_lock = web3.eth.contract(address=ca.time_lock, abi=api.get_abi(ca.time_lock, "eth"))

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
    tx = api.get_tx(event["transactionHash"].hex(), "eth")
    pool = int(tx["result"]["value"], 0) / 10 ** 18
    liq = api.get_liquidity(event["args"]["pair"], "eth")
    if pool == 0 or pool == "" or not pool:
        pool_text = "Launched Pool Amount: Unavailable"
    else:
        pool_dollar = float(pool) * float(api.get_native_price("eth")) / 1 ** 18
        pool_text = f'Launched Pool Amount: {pool} ETH (${"{:0,.0f}".format(pool_dollar)})'
    if event["args"]["token0"] == ca.weth:
        native = api.get_token_name(event["args"]["token0"], "eth")
        token_name = api.get_token_name(event["args"]["token1"], "eth")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = int(weth) * 2 * api.get_native_price("eth") / 10 ** 18
        return
    if event["args"]["token0"] == ca.usdt:
        native = api.get_token_name(event["args"]["token0"], "eth")
        token_name = api.get_token_name(event["args"]["token1"], "eth")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = int(weth) * 2
        return
    else:
        native = api.get_token_name(event["args"]["token1"], "eth")
        token_name = api.get_token_name(event["args"]["token0"], "eth")
        token_address = event["args"]["token0"]
        weth = liq["reserve1"]
        token = liq["reserve0"]
        dollar = int(weth) * 2 * api.get_native_price("eth") / 10 ** 18
    if dollar == 0:
        liquidity_text = 'Total Liquidity: Unavailable'
    else:
        liquidity_text = f'Total Liquidity: ${"{:0,.0f}".format(dollar)}'
    verified = api.get_verified(token_address, "eth")
    im1 = Image.open((random.choice(media.blackhole)))
    im2 = Image.open(media.eth_logo)
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
    i1 = ImageDraw.Draw(im1)
    i1.text((26, 30),
            f'New Pair Created (ETH)\n\n'
            f'{token_name[0]}\n({token_name[1]}/{native[1]})\n\n'
            f'{pool_text}\n\n'
            f'{liquidity_text}\n\n'
            f'Contract Verified: {verified}\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await application.bot.send_photo(
        ca.alerts_id,
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'*New Pair Created (ETH)*\n\n'
                f'{token_name[0]}\n({token_name[1]}/{native[1]})\n\n'
                f'Token Address:\n`{token_address}`\n\n'
                f'{pool_text}\n\n'
                f'{liquidity_text}\n\n'
                f'Contract Verified: {verified}', parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=f'Buy On Xchange', url=f'{url.xchange_buy_eth}{token_address}')],
             [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_eth}{event["args"]["pair"]}')],
             [InlineKeyboardButton(text='Token Contract', url=f'{url.ether_token}{token_address}')],
             [InlineKeyboardButton(text='Factory TX', url=f'{url.ether_tx}{event["transactionHash"].hex()}')], ]))

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
    print("Scanning Eth Network")
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
    finally:
        loop.close()


if __name__ == "__main__":
    application = ApplicationBuilder().token(keys.token).build()
    asyncio.run(main())
