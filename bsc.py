from telegram.ext import *
from telegram import *
import api
import asyncio
import ca
import logging
import media
from PIL import Image, ImageDraw, ImageFont
import random
import time
import url
from web3 import Web3
from web3.exceptions import Web3Exception
from eth_utils import to_checksum_address
from datetime import datetime
import os
from dotenv import load_dotenv

# Load all environment variables
load_dotenv()

# Get the tokens, split by comma
tokens = os.getenv("TOKENS").split(",")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

getblock_url = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(getblock_url))

factory = web3.eth.contract(address=ca.factory, abi=api.get_abi(ca.factory, "bsc"))
ill001 = web3.eth.contract(address=ca.ill001, abi=api.get_abi(ca.ill001, "bsc"))
ill002 = web3.eth.contract(address=ca.ill002, abi=api.get_abi(ca.ill002, "bsc"))
ill003 = web3.eth.contract(address=ca.ill003, abi=api.get_abi(ca.ill003, "bsc"))


async def new_pair(event):
    print("Pair found")
    tx = api.get_tx_from_hash(event["transactionHash"].hex(), "bsc")
    liq = {"reserve0": 0, "reserve1": 0}
    try:
        liq = api.get_liquidity(event["args"]["pair"], "bsc")
    except (Exception, TimeoutError, ValueError, StopAsyncIteration):
        print("Liquidity Error")
    if event["args"]["token0"] == ca.wbnb:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token_name = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = int(weth) * 2 * api.get_native_price("bnb") / 10**18
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
        dollar = int(weth) * 2 * api.get_native_price("eth") / 10**18
    elif event["args"]["token1"] in ca.bscethpairs:
        native = api.get_token_name(event["args"]["token1"], "bsc")
        token_name = api.get_token_name(event["args"]["token0"], "bsc")
        token_address = event["args"]["token0"]
        weth = liq["reserve1"]
        token = liq["reserve0"]
        dollar = int(weth) * 2 * api.get_native_price("eth") / 10**18
    elif event["args"]["token0"] in ca.stables:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token_name = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = int(weth) * 2 / 10**18
    elif event["args"]["token1"] in ca.stables:
        native = api.get_token_name(event["args"]["token1"], "bsc")
        token_name = api.get_token_name(event["args"]["token0"], "bsc")
        token_address = event["args"]["token0"]
        weth = liq["reserve1"]
        token = liq["reserve0"]
        dollar = int(weth) * 2 / 10**18
    else:
        native = api.get_token_name(event["args"]["token1"], "bsc")
        token_name = api.get_token_name(event["args"]["token0"], "bsc")
        token_address = event["args"]["token0"]
        weth = liq["reserve1"]
        token = liq["reserve0"]
        dollar = int(weth) * 2 * api.get_native_price("bnb") / 10**18
    verified_check = api.get_verified(token_address, "eth")
    if dollar == 0 or dollar == "" or not dollar:
        liquidity_text = "Total Liquidity: Unavailable"
    else:
        liquidity_text = f'Total Liquidity: ${"{:0,.0f}".format(dollar)}'
    info = api.get_token_data(token_address, "bsc")
    if (
        info[0]["decimals"] == ""
        or info[0]["decimals"] == "0"
        or not info[0]["decimals"]
    ):
        supply = int(api.get_supply(token_address, "bsc"))
    else:
        supply = int(api.get_supply(token_address, "bsc")) / 10 ** int(
            info[0]["decimals"]
        )
    status = ""
    renounced = ""
    lock = ""
    tax = ""
    tax_warning = ""
    verified = ""
    if verified_check == "No":
        verified = "⚠️ Contract Unverified"
    if verified_check == "Yes":
        contract = web3.eth.contract(
            address=token_address, abi=api.get_abi(token_address, "bsc")
        )
        verified = "✅ Contract Verified"
        try:
            owner = contract.functions.owner().call()
            if owner == "0x0000000000000000000000000000000000000000":
                renounced = "✅ Contract Renounced"
            else:
                renounced = "⚠️ Contract Not Renounced"
        except (Exception, TimeoutError, ValueError, StopAsyncIteration):
            print("Owner Error")
    time.sleep(10)
    try:
        scan = api.get_scan(token_address, "bsc")
        if scan[f"{str(token_address).lower()}"]["is_open_source"] == "1":
            try:
                if scan[f"{str(token_address).lower()}"]["slippage_modifiable"] == "1":
                    tax_warning = "(Changeable)"
                else:
                    tax_warning = ""
                if scan[f"{str(token_address).lower()}"]["is_honeypot"] == "1":
                    print("Skip - Honey Pot")
                    return
                if scan[f"{str(token_address).lower()}"]["is_mintable"] == "1":
                    print("Skip - Mintable")
                    return
            except (Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
                print(f"Initial Error: {e}")
        if scan[f"{str(token_address).lower()}"]["is_in_dex"] == "1":
            try:
                if (
                    scan[f"{str(token_address).lower()}"]["sell_tax"] == "1"
                    or scan[f"{str(token_address).lower()}"]["buy_tax"] == "1"
                ):
                    print("Skip - Cannot Buy")
                    return
                buy_tax_raw = (
                    float(scan[f"{str(token_address).lower()}"]["buy_tax"]) * 100
                )
                sell_tax_raw = (
                    float(scan[f"{str(token_address).lower()}"]["sell_tax"]) * 100
                )
                buy_tax = int(buy_tax_raw)
                sell_tax = int(sell_tax_raw)
                if sell_tax > 10 or buy_tax > 10:
                    tax = f"⚠️ Tax: {buy_tax}/{sell_tax} {tax_warning}"
                else:
                    tax = f"✅️ Tax: {buy_tax}/{sell_tax} {tax_warning}"
            except (Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
                print(f"Tax Error: {e}")
                tax = f"⚠️ Tax: Unavailable {tax_warning}"
            if "lp_holders" in scan[f"{str(token_address).lower()}"]:
                lp_holders = scan[f"{str(token_address).lower()}"]["lp_holders"]
            try:
                if "lp_holder_count" in scan[f"{str(token_address).lower()}"]:
                    locked_lp_list = [
                        lp
                        for lp in scan[f"{str(token_address).lower()}"]["lp_holders"]
                        if lp["is_locked"] == 1
                        and lp["address"]
                        != "0x0000000000000000000000000000000000000000"
                    ]
                    if locked_lp_list:
                        lp_with_locked_detail = [
                            lp for lp in locked_lp_list if "locked_detail" in lp
                        ]
                        if lp_with_locked_detail:
                            lock = (
                                f"✅ Liquidity Locked\n{locked_lp_list[0]['tag']} - "
                                f"{locked_lp_list[0]['percent'][:6]}%\n"
                                f"Unlock - {locked_lp_list[0]['locked_detail'][0]['end_time']}"
                            )
                        else:
                            lock = (
                                f"✅ Liquidity Locked\n{locked_lp_list[0]['tag']} - "
                                f"{locked_lp_list[0]['percent'][:6]}%\n"
                            )
                else:
                    lock = ""
            except (Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
                print(f"Liquidity Error: {e}")
        else:
            tax = f"⚠️ Tax: Unavailable {tax_warning}"
        status = f"{verified}\n{tax}\n{renounced}\n{lock}"
    except (Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
        print(f"Scan Error: {e}")
        status = "⚠️ Scan Unavailable"
    pool = int(tx["result"]["value"], 0) / 10**18
    if pool == 0 or pool == "" or not pool:
        pool_text = "Launched Pool Amount: Unavailable"
    else:
        pool_dollar = float(pool) * float(api.get_native_price("bnb")) / 1**18
        pool_text = (
            f'Launched Pool Amount: {pool} BNB (${"{:0,.0f}".format(pool_dollar)})'
        )
    im1 = Image.open((random.choice(media.blackhole)))
    im2 = Image.open(media.bsc_logo)
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (26, 30),
        f"New Pair Created (BSC)\n\n"
        f"{token_name[0]} ({token_name[1]}/{native[1]})\n\n"
        f'Supply: {"{:0,.0f}".format(supply)} ({info[0]["decimals"]} Decimals)\n\n'
        f"{pool_text}\n\n"
        f"{liquidity_text}\n\n"
        f"SCAN:\n"
        f"{status}\n",
        font=myfont,
        fill=(255, 255, 255),
    )
    im1.save(r"media\blackhole.png")
    await application.bot.send_photo(
        os.getenv("ALERTS_TELEGRAM_CHANNEL_ID"),
        photo=open(r"media\blackhole.png", "rb"),
        caption=f"*New Pair Created (BSC)*\n\n"
        f"{token_name[0]} ({token_name[1]}/{native[1]})\n\n"
        f"Token Address:\n`{token_address}`\n\n"
        f'Supply: {"{:0,.0f}".format(supply)} ({info[0]["decimals"]} Decimals)\n\n'
        f"{pool_text}\n\n"
        f"SCAN:\n"
        f"{liquidity_text}\n\n"
        f"{status}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=f"Buy On Xchange", url=f"{url.xchange_buy_bsc}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Chart", url=f'{url.dex_tools_bsc}{event["args"]["pair"]}'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Token Contract", url=f"{url.bsc_address}{token_address}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Deployer TX",
                        url=f'{url.bsc_tx}{event["transactionHash"].hex()}',
                    )
                ],
            ]
        ),
    )
    print(f"Pair sent: ({token_name[1]}/{native[1]})")


async def new_loan(event):
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    print("Loan Originated")
    tx = api.get_tx_from_hash(event["transactionHash"].hex(), "arb")
    try:
        address = to_checksum_address(ca.lpool)
        contract = web3.eth.contract(address=address, abi=api.get_abi(ca.lpool, "bsc"))
        amount = (
            contract.functions.getRemainingLiability(
                int(event["args"]["loanID"])
            ).call()
            / 10**18
        )
        schedule1 = contract.functions.getPremiumPaymentSchedule(
            int(event["args"]["loanID"])
        ).call()
        schedule2 = contract.functions.getPrincipalPaymentSchedule(
            int(event["args"]["loanID"])
        ).call()
        schedule_list = []
        if len(schedule1[0]) > 0 and len(schedule1[1]) > 0:
            if len(schedule2[0]) == len(schedule1[0]) and len(schedule2[1]) == len(
                schedule1[1]
            ):
                for date1, value1, value2 in zip(
                    schedule1[0], schedule1[1], schedule2[1]
                ):
                    formatted_date = datetime.fromtimestamp(date1).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    combined_value = (value1 + value2) / 10**18
                    sch = f"{formatted_date} - {combined_value} BNB"
                    schedule_list.append(sch)
            else:
                for date, value in zip(schedule1[0], schedule1[1]):
                    formatted_date = datetime.fromtimestamp(date).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    formatted_value = value / 10**18
                    sch = f"{formatted_date} - {formatted_value} BNB"
                    schedule_list.append(sch)
        else:
            for date, value in zip(schedule2[0], schedule2[1]):
                formatted_date = datetime.fromtimestamp(date).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                formatted_value = value / 10**18
                sch = f"{formatted_date} - {formatted_value} BNB"
                schedule_list.append(sch)
        schedule_str = "\n".join(schedule_list)
    except (Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
        print(f" Scan Error:{e}")
        schedule_str = ""
        amount = ""
    cost = int(tx["result"]["value"], 0) / 10**18
    im1 = Image.open((random.choice(media.blackhole)))
    im2 = Image.open(media.bsc_logo)
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (26, 30),
        f"*New Loan Originated (BSC)*\n\n"
        f'Loan ID: {event["args"]["loanID"]}\n'
        f'Initial Cost: {int(tx["result"]["value"], 0) / 10 ** 18} BNB '
        f'(${"{:0,.0f}".format(api.get_native_price("bnb") * cost)})\n\n'
        f"Payment Schedule:\n{schedule_str}\n\n"
        f'Total: {amount} BNB (${"{:0,.0f}".format(api.get_native_price("bnb") * amount)}',
        font=myfont,
        fill=(255, 255, 255),
    )
    im1.save(r"media\blackhole.png")
    await application.bot.send_photo(
        os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        photo=open(r"media\blackhole.png", "rb"),
        caption=f"*New Loan Originated (BSC)*\n\n"
        f'Loan ID: {event["args"]["loanID"]}\n'
        f'Initial Cost: {int(tx["result"]["value"], 0) / 10 ** 18} BNB '
        f'(${"{:0,.0f}".format(api.get_native_price("bnb") * cost)})\n\n'
        f"Payment Schedule:\n{schedule_str}\n\n"
        f'Total: {amount} BNB (${"{:0,.0f}".format(api.get_native_price("bnb") * amount)}',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=f"Loan TX",
                        url=f'{url.bsc_tx}{event["transactionHash"].hex()}',
                    )
                ],
            ]
        ),
    )
    print(f'Loan {event["args"]["loanID"]} sent')


async def log_loop(poll_interval):
    filters = [pair_filter, ill001_filter, ill002_filter, ill003_filter]
    while True:
        try:
            for my_filter in filters:
                for entry in my_filter.get_new_entries():
                    await new_entry(entry)
            await asyncio.sleep(poll_interval)
        except (
            Web3Exception,
            Exception,
            TimeoutError,
            ValueError,
            StopAsyncIteration,
        ) as e:
            print(f"Error: {e}")


async def new_entry(entry):
    await new_loan(entry) if "LoanOriginated" in entry.event_name else await new_pair(
        entry
    )
    application = (
        ApplicationBuilder()
        .token(random.choice(tokens))
        .connection_pool_size(512)
        .build()
    )


async def main():
    print("Scanning BSC Network")
    pair_filter = factory.events.PairCreated.create_filter(fromBlock="latest")
    ill001_filter = ill001.events.LoanOriginated.create_filter(fromBlock="latest")
    ill002_filter = ill002.events.LoanOriginated.create_filter(fromBlock="latest")
    ill003_filter = ill003.events.LoanOriginated.create_filter(fromBlock="latest")
    await log_loop(pair_filter, ill001_filter, ill002_filter, ill003_filter, 2)


async def log_loop(
    pair_filter, ill001_filter, ill002_filter, ill003_filter, poll_interval
):
    while True:
        try:
            pair_events = await pair_filter.get_new_entries()
            ill001_events = await ill001_filter.get_new_entries()
            ill002_events = await ill002_filter.get_new_entries()
            ill003_events = await ill003_filter.get_new_entries()

            # process events

            await asyncio.sleep(poll_interval)
        except (
            Web3Exception,
            Exception,
            TimeoutError,
            ValueError,
            StopAsyncIteration,
        ) as e:
            print(f"Log Loop Error: {e}")
            break


if __name__ == "__main__":
    application = (
        ApplicationBuilder()
        .token(random.choice(tokens))
        .connection_pool_size(512)
        .build()
    )
    asyncio.run(main())
