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


ankr_url = f'https://bsc.getblock.io/{keys.getblock}'
web3 = Web3(Web3.HTTPProvider(ankr_url))

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
    if pool == 0:
        pool_text = "Not Available"
    else:
        pool_dollar = float(pool) * float(api.get_native_price("bnb")) / 1 ** 18
        pool_text = f'{pool} BNB (${"{:0,.0f}".format(pool_dollar)})'
    if event["args"]["token0"] == ca.wbnb:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
    else:
        native = api.get_token_name(event["args"]["token1"], "bsc")
        token = api.get_token_name(event["args"]["token0"], "bsc")
        token_address = event["args"]["token0"]
    verified = api.get_verified(token_address, "bsc")
    im1 = Image.open((random.choice(media.blackhole)))
    im2 = Image.open(media.bsc_logo)
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
    i1 = ImageDraw.Draw(im1)
    i1.text((26, 30),
            f'New Pair Created (BSC)\n\n'
            f'{token[0]}\n({token[1]}/{native[1]})\n\n'
            f'Launched Pool Amount:\n'
            f'{pool_text}\n\n'
            f'Contract Verified: {verified}\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await application.bot.send_photo(
        f'{ca.alerts_id}',
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'*New Pair Created (BSC)*\n\n'
                f''f'{token[0]}\n({token[1]}/{native[1]})\n\n'
                f'Token Address:\n`{token_address}`\n\n'
                f'Launched Pool Amount:\n'
                f'{pool_text}\n\n'
                f'Contract Verified: {verified}', parse_mode='Markdown',
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
    finally:
        loop.close()


if __name__ == "__main__":
    application = ApplicationBuilder().token(keys.token).build()
    asyncio.run(main())
