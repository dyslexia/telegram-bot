from telegram.ext import *
from telegram import *
import api
import asyncio
import ca
import keys
import logging
import media
from PIL import Image, ImageDraw, ImageFont
import random
import time
import url
from web3 import Web3
from web3.exceptions import Web3Exception

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

alchemy_arb_url = f'https://arb-mainnet.g.alchemy.com/v2/{keys.alchemy_arb}'
web3 = Web3(Web3.HTTPProvider(alchemy_arb_url))

factory = web3.eth.contract(address=ca.factory, abi=api.get_abi(ca.factory, "arb"))
ill001 = web3.eth.contract(address=ca.ill001, abi=api.get_abi(ca.ill001, "arb"))
ill002 = web3.eth.contract(address=ca.ill002, abi=api.get_abi(ca.ill002, "arb"))
ill003 = web3.eth.contract(address=ca.ill003, abi=api.get_abi(ca.ill003, "arb"))

async def new_pair(event):
    print("Pair found")
    print(event)
    tx = api.get_tx_from_hash(event["transactionHash"].hex(), "arb")
    liq = {"reserve0": 0, "reserve1": 0}
    try:
        liq = api.get_liquidity(event["args"]["pair"], "arbitrum")
    except (Exception, TimeoutError, ValueError, StopAsyncIteration):
        print('Liquidity Error')
    if event["args"]["token0"] == ca.weth:
        native = api.get_token_name(event["args"]["token0"], "arb")
        token_name = api.get_token_name(event["args"]["token1"], "arb")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = int(weth) * 2 * api.get_native_price("eth") / 10 ** 18
    elif event["args"]["token0"] in ca.stables:
        native = api.get_token_name(event["args"]["token0"], "arb")
        token_name = api.get_token_name(event["args"]["token1"], "arb")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = int(weth) * 2 / 10 ** 18
    elif event["args"]["token1"] in ca.stables:
        native = api.get_token_name(event["args"]["token1"], "arb")
        token_name = api.get_token_name(event["args"]["token0"], "arb")
        token_address = event["args"]["token0"]
        weth = liq["reserve1"]
        token = liq["reserve0"]
        dollar = int(weth) * 2 / 10 ** 18
    else:
        native = api.get_token_name(event["args"]["token1"], "arb")
        token_name = api.get_token_name(event["args"]["token0"], "arb")
        token_address = event["args"]["token0"]
        weth = liq["reserve1"]
        token = liq["reserve0"]
        dollar = int(weth) * 2 * api.get_native_price("eth") / 10 ** 18
    verified_check = api.get_verified(token_address, "arb")
    if dollar == 0 or dollar == "" or not dollar:
        liquidity_text = 'Total Liquidity: Unavailable'
    else:
        liquidity_text = f'Total Liquidity: ${"{:0,.0f}".format(dollar)}'
    info = api.get_token_data(token_address, "arb")
    if info[0]["decimals"] == "" or info[0]["decimals"] == "0" or not info[0]["decimals"]:
        supply = int(api.get_supply(token_address, "arb"))
    else:
        supply = int(api.get_supply(token_address, "arb")) / 10 ** int(info[0]["decimals"])
    status = ""
    renounced = ""
    lock = ""
    tax = ""
    tax_warning = ""
    verified = ""
    if verified_check == "No":
        verified = '⚠️ Contract Unverified'
    if verified_check == "Yes":
        contract = web3.eth.contract(address=token_address, abi=api.get_abi(token_address, "arb"))
        verified = '✅ Contract Verified'
        try:
            owner = contract.functions.owner().call()
            if owner == "0x0000000000000000000000000000000000000000":
                renounced = '✅ Contract Renounced'
            else:
                renounced = '⚠️ Contract Not Renounced'
        except (Exception, TimeoutError, ValueError, StopAsyncIteration):
            print('Owner Error')
    time.sleep(10)
    try:
        scan = api.get_scan(token_address, "arb")
        if scan[f'{str(token_address).lower()}']["is_open_source"] == "1":
            try:
                if scan[f'{str(token_address).lower()}']["slippage_modifiable"] == "1":
                    tax_warning = "(Changeable)"
                else:
                    tax_warning = ""
                if scan[f'{str(token_address).lower()}']["is_honeypot"] == "1":
                    print('Skip - Honey Pot')
                    return
                if scan[f'{str(token_address).lower()}']["is_mintable"] == "1":
                    print('Skip - Mintable')
                    return
            except (Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
                print(f'Initial Scan Error: {e}')
        if scan[f'{str(token_address).lower()}']["is_in_dex"] == "1":
            try:
                if scan[f'{str(token_address).lower()}']["sell_tax"] == "1"\
                        or scan[f'{str(token_address).lower()}']["buy_tax"] == "1":
                    print('Skip - Cannot Buy')
                    return
                buy_tax_raw = float(scan[f'{str(token_address).lower()}']["buy_tax"]) * 100
                sell_tax_raw = float(scan[f'{str(token_address).lower()}']["sell_tax"]) * 100
                buy_tax = int(buy_tax_raw)
                sell_tax = int(sell_tax_raw)
                if sell_tax > 10 or buy_tax > 10:
                    tax = f'⚠️ Tax: {buy_tax}/{sell_tax} {tax_warning}'
                else:
                    tax = f'✅️ Tax: {buy_tax}/{sell_tax} {tax_warning}'
            except (Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
                print(f'Tax Error: {e}')
                tax = f'⚠️ Tax: Unavailable {tax_warning}'
            if "lp_holders" in scan[f'{str(token_address).lower()}']:
                lp_holders = scan[f'{str(token_address).lower()}']["lp_holders"]
            try:
                if "lp_holder_count" in scan[f'{str(token_address).lower()}']:
                    locked_lp_list = [
                        lp for lp in scan[f'{str(token_address).lower()}']["lp_holders"]
                        if lp["is_locked"] == 1 and lp["address"] != "0x0000000000000000000000000000000000000000"]
                    if locked_lp_list:
                        lp_with_locked_detail = [lp for lp in locked_lp_list if "locked_detail" in lp]
                        if lp_with_locked_detail:
                            lock =\
                                f"✅ Liquidity Locked\n{locked_lp_list[0]['tag']} - " \
                                f"{locked_lp_list[0]['percent'][:6]}%\n" \
                                f"Unlock - {locked_lp_list[0]['locked_detail'][0]['end_time']}"
                        else:
                            lock = f"✅ Liquidity Locked\n{locked_lp_list[0]['tag']} - " \
                                   f"{locked_lp_list[0]['percent'][:6]}%\n"
                else:
                    lock = ""
            except (Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
                print(f'Liquidity Error: {e}')
        else:
            tax = f'⚠️ Tax: Unavailable {tax_warning}'
        status = f'{verified}\n{tax}\n{renounced}\n{lock}'
    except (Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
        print(f'Scan Error: {e}')
        status = '⚠️ Scan Unavailable'
    pool = int(tx["result"]["value"], 0) / 10 ** 18
    if pool == 0 or pool == "" or not pool:
        pool_text = "Launched Pool Amount: Unavailable"
    else:
        pool_dollar = float(pool) * float(api.get_native_price("eth")) / 1 ** 18
        pool_text = f'Launched Pool Amount: {pool} ETH (${"{:0,.0f}".format(pool_dollar)})'
    im1 = Image.open((random.choice(media.blackhole)))
    im2 = Image.open(media.arb_logo)
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
    i1 = ImageDraw.Draw(im1)
    i1.text((26, 30),
            f'New Pair Created (ARB) \n\n'
            f'{token_name[0]} ({token_name[1]}/{native[1]})\n\n'
            f'Supply: {"{:0,.0f}".format(supply)} ({info[0]["decimals"]} Decimals)\n\n'
            f'{pool_text}\n\n'
            f'{liquidity_text}\n\n'
            f'SCAN:\n'
            f'{status}\n',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await application.bot.send_photo(
        keys.alerts_id,
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'*New Pair Created (ARB)*\n\n'
                f'{token_name[0]} ({token_name[1]}/{native[1]})\n\n'
                f'Token Address:\n`{token_address}`\n\n'
                f'Supply: {"{:0,.0f}".format(supply)} ({info[0]["decimals"]} Decimals)\n\n'
                f'{pool_text}\n\n'
                f'{liquidity_text}\n\n'
                f'SCAN:\n'
                f'{status}\n', parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=f'Buy On Xchange', url=f'{url.xchange_buy_eth}{token_address}')],
             [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_arb}{event["args"]["pair"]}')],
             [InlineKeyboardButton(text='Token Contract', url=f'{url.arb_address}{token_address}')],
             [InlineKeyboardButton(text='Deployer TX', url=f'{url.arb_tx}{event["transactionHash"].hex()}')], ]))
    print(f'Pair sent: ({token_name[1]}/{native[1]})')

async def new_loan(event):
    im1 = Image.open((random.choice(media.blackhole)))
    im2 = Image.open(media.arb_logo)
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
    i1 = ImageDraw.Draw(im1)
    i1.text((26, 30),
            f'New Loan Originated (ARB)\n\n'
            f'Loan ID: {event["args"]["loanID"]}\n\n'
            f'{url.arb_tx}{event["transactionHash"].hex()}',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await application.bot.send_photo(
        keys.alerts_id,
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'*New Loan Originated (ETH)*\n\n'
                f'Loan ID: {event["args"]["loanID"]}\n\n'
                f'{url.arb_tx}{event["transactionHash"].hex()}', parse_mode='Markdown')

async def log_loop(pair_filter, ill001_filter, ill002_filter, ill003_filter, poll_interval):
    while True:
        try:
            for PairCreated in pair_filter.get_new_entries():
                await new_pair(PairCreated)
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
            print(f'Error: {e}')

async def main():
    print("Scanning ARB Network")
    pair_filter = factory.events.PairCreated.create_filter(fromBlock='latest')
    ill001_filter = ill001.events.LoanOriginated.create_filter(fromBlock='latest')
    ill002_filter = ill002.events.LoanOriginated.create_filter(fromBlock='latest')
    ill003_filter = ill003.events.LoanOriginated.create_filter(fromBlock='latest')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        try:
            tasks = [log_loop(pair_filter, ill001_filter, ill002_filter, ill003_filter, 2)]
            await asyncio.gather(*tasks)
        except (Web3Exception, Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
            print(f'Main Error: {e}')
            break


if __name__ == "__main__":
    application = ApplicationBuilder().token(random.choice(keys.tokens)).connection_pool_size(512).build()
    asyncio.run(main())
