from telegram.ext import *
from telegram import *
from api import index as api
from data import ca as ca
from datetime import datetime, timedelta, timezone
from dateutil import parser
import pytz
from data import loans as loans
from media import index as media
from data import nfts as nfts
from PIL import Image, ImageDraw, ImageFont
import random
import requests
from data import tax as tax
from data import text as text
import textwrap
from data import times as times
from data import giveaway as giveaway
from translate import Translator
import pyttsx3
from data import url as url
import wikipediaapi
import re
from web3 import Web3
from web3.exceptions import Web3Exception
from eth_utils import to_checksum_address
import os
from dotenv import load_dotenv
from api import dune as dune
import time as t
from tokens import chains, pairs, all_tokens_info
import traceback
import sentry_sdk
load_dotenv()


sentry_sdk.init(
  dsn=os.getenv("SENTRY_DSN"),
  traces_sample_rate=1.0
)


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return


# COMMANDS
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"{text.about}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Xchange App", url=f"{url.xchange}")],
                [InlineKeyboardButton(text="Website", url=f"{url.dashboard}")],
            ]
        ),
    )


async def airdrop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_sticker(sticker=media.chains)
    await update.message.reply_text(
        f"{text.airdrop}\n\n"
        f"{api.get_quote()}",
        parse_mode="Markdown",
    )


async def alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"Check out the link below for the Xchange Alerts channel\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="XChange Alerts", url=f"{url.tg_alerts}"
                    )
                ],
            ]
        ),
    )


async def alumni(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Alumni*\n\n{text.alumni}\n\n{api.get_quote()}",
        parse_mode="Markdown",
    )


async def announcements(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption="Check out the link below for the announcement channel",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7 Announcement Channel",
                        url="https://t.me/X7announcements",
                    )
                ],
            ]
        ),
    )


async def ath(update: Update, context: ContextTypes.DEFAULT_TYPE):
    def get_ath_info(coin):
        ath, ath_change, date = api.get_ath(coin)
        ath_change_str = str(ath_change)
        return ath, ath_change_str[:3], date

    x7r_ath, x7r_ath_change, x7r_date = get_ath_info("x7r")
    x7dao_ath, x7dao_ath_change, x7dao_date = get_ath_info("x7dao")
    x7dao_date_object = datetime.fromisoformat(x7dao_date.replace("Z", "+00:00"))
    x7dao_readable_date = x7dao_date_object.strftime("%Y-%m-%d %H:%M:%S")
    x7r_date_object = datetime.fromisoformat(x7r.replace("Z", "+00:00"))
    x7r_readable_date = x7r_date_object.strftime("%Y-%m-%d %H:%M:%S")
    img = Image.open((random.choice(media.blackhole)))
    i1 = ImageDraw.Draw(img)
    myfont = ImageFont.truetype(R"media/FreeMonoBold.ttf", 26)
    i1.text(
        (28, 36),
        f"X7 Finance ATH Info\n\n"
        f'X7R   - ${x7r_ath} (${"{:0,.0f}".format(x7r_ath * ca.supply)}) {x7r_ath_change}%\n'
        f"{x7r_readable_date}\n\n"
        f'X7DAO - ${x7dao_ath} (${"{:0,.0f}".format(x7dao_ath * ca.supply)}) {x7dao_ath_change}%\n'
        f"{x7dao_readable_date}"
        f"\n\n\n\n\n\n\n"
        f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font=myfont,
        fill=(255, 255, 255),
    )
    img.save(r"media/blackhole.png")
    caption = (
        f"*X7 Finance ATH Info*\n\n"
        f'X7R - ${x7r_ath} (${"{:0,.0f}".format(x7r_ath * ca.supply)}) {x7r_ath_change}%\n'
        f"{x7r_date}\n\n"
        f'X7DAO - ${x7dao_ath} (${"{:0,.0f}".format(x7dao_ath * ca.supply)}) {x7dao_ath_change}%\n'
        f"{x7dao_date}\n\n"
        f"{api.get_quote()}"
    )
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"), caption=caption, parse_mode="Markdown"
    )


async def blog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Blog*\n\nCentralizing the best content on decentralized finance in one place.\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7 Finance Blog", url=f"{url.dashboard}blog"
                    )
                ],
            ]
        ),
    )


async def bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"{text.commands}")


async def burn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_url = ""
    chain_name = ""
    burn = ""
    im2 = ""
    burn_dollar = ""
    percent = ""
    native = ""
    if chain == "" or chain == "eth":
        chain_name = "(ETH)"
        chain_url = url.ether_token
        burn = api.get_token_balance(ca.dead, ca.x7r, "eth")
        percent = round(burn / ca.supply * 100, 2)
        burn_dollar = api.get_price(ca.x7r, "eth") * float(burn)
        im2 = Image.open(media.eth_logo)
        native = f'{str(burn_dollar / api.get_native_price("eth"))[:5]} ETH'
    if chain == "bsc" or chain == "bnb":
        chain_name = "(BSC)"
        chain_url = url.bsc_token
        burn = api.get_token_balance(ca.dead, ca.x7r, "bsc")
        percent = round(burn / ca.supply * 100, 2)
        burn_dollar = api.get_price(ca.x7r, "bsc") * float(burn)
        im2 = Image.open(media.bsc_logo)
        native = f'{str(burn_dollar / api.get_native_price("bnb"))[:7]} BNB'
    if chain == "polygon" or chain == "poly":
        chain_name = "(POLYGON)"
        chain_url = url.poly_token
        burn = api.get_token_balance(ca.dead, ca.x7r, "poly")
        burn_dollar = api.get_price(ca.x7r, "polygon") * float(burn)
        percent = round(burn / ca.supply * 100, 2)
        im2 = Image.open(media.poly_logo)
        native = f'{str(burn_dollar / api.get_native_price("matic"))[:7]} MATIC'
    if chain == "arbitrum" or chain == "arb":
        chain_name = "(ARB)"
        chain_url = url.arb_token
        burn = api.get_token_balance(ca.dead, ca.x7r, "arb")
        percent = round(burn / ca.supply * 100, 2)
        burn_dollar = api.get_price(ca.x7r, "arbitrum") * float(burn)
        im2 = Image.open(media.arb_logo)
        native = f'{str(burn_dollar / api.get_native_price("eth"))[:5]} ETH'
    if chain == "optimism" or chain == "arb":
        chain_name = "(OPTIMISM)"
        chain_url = url.opti_token
        burn = api.get_token_balance(ca.dead, ca.x7r, "opti")
        burn_dollar = api.get_price(ca.x7r, "optimism") * float(burn)
        percent = round(burn / ca.supply * 100, 2)
        im2 = Image.open(media.opti_logo)
        native = f'{str(burn_dollar / api.get_native_price("eth"))[:5]} ETH'
    im1 = Image.open((random.choice(media.blackhole)))
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 28)
    i1.text(
        (28, 36),
        f"X7R {chain_name} Tokens Burned:\n\n"
        f'{"{:0,.0f}".format(float(burn))} / {native} (${"{:0,.0f}".format(float(burn_dollar))})\n'
        f"{percent}% of Supply\n\n\n\n\n\n\n\n\n"
        f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font=myfont,
        fill=(255, 255, 255),
    )
    img_path = os.path.join("media", "blackhole.png")
    im1.save(img_path)
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=f"\n\nX7R {chain_name} Tokens Burned:\nUse `/burn [chain-name]` for other chains\n\n"
        f'{"{:0,.0f}".format(float(burn))} / {native} (${"{:0,.0f}".format(float(burn_dollar))})\n'
        f"{percent}% of Supply\n\n{api.get_quote()}",
        parse_mode="markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Burn Wallet",
                        url=f"{chain_url}{ca.x7r}?a={ca.dead}",
                    )
                ],
            ]
        ),
    )


async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context is None:
        context = ContextTypes.DEFAULT_TYPE()
    chain = " ".join(context.args).lower()
    chain_url = ""
    chain_name = ""
    chain_mappings = {
        "eth": ("(ETH)", url.xchange_buy_eth),
        "bsc": ("(BSC)", url.xchange_buy_bsc),
        "bnb": ("(BSC)", url.xchange_buy_bsc),
        "polygon": ("(POLYGON)", url.xchange_buy_poly),
        "poly": ("(POLYGON)", url.xchange_buy_poly),
        "optimism": ("(OPTIMISM)", url.xchange_buy_opti),
        "opti": ("(OPTIMISM)", url.xchange_buy_opti),
        "arbitrum": ("(ARB)", url.xchange_buy_arb),
        "arb": ("(ARB)", url.xchange_buy_arb),
    }
    if chain in chain_mappings:
        chain_name, chain_url = chain_mappings[chain]
    else:
        chain_name, chain_url = chain_mappings["eth"]
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Buy Links {chain_name}*\nUse `/buy [chain-name]` for other chains\n"
        f"Use `/constellations` for constellations\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7R - Rewards Token", url=f"{chain_url}{ca.x7r}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7DAO - Governance Token", url=f"{chain_url}{ca.x7dao}"
                    )
                ],
            ]
        ),
    )


async def buy_bots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Bobby Buy Bot Channels*\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Xchange Alerts", url="https://t.me/x7_alerts)"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Ethereum", url="https://t.me/X7constellation)"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Arbitrum", url="https://t.me/x7arbbuybots"
                    )
                ],
                [InlineKeyboardButton(text="BSC", url="https://t.me/x7bscbuybots")],
                [
                    InlineKeyboardButton(
                        text="Optimism", url="https://t.me/x7optibuybots"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Polygon", url="https://t.me/x7polygonbuybots"
                    )
                ],
            ]
        ),
    )


async def buy_evenly(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"{text.evenly}\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Via Dashboard", url="https://dapp.x7community.space/"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Via Etherscan",
                        url="https://etherscan.io/address/0x0419074afe1a"
                        "137dfa6afd5b6af5771c3ffbea49#code",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Epoch Convertor", url="https://www.epochconverter.com/"
                    )
                ],
            ]
        ),
    )


async def channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Community TG Channels*\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Community Chat", url="https://t.me/X7m105portal"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Announcements", url="https://t.me/X7announcements"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Xchange Alerts", url="https://t.me/x7_alerts)"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Media", url="https://t.me/X7MediaChannel"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Research Notes", url="https://t.me/X7m105_Research"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Chinese Community", url="https://t.me/X7CNPortal"
                    )
                ],
            ]
        ),
    )


async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE = None):
    if context is None:
        context = ContextTypes.DEFAULT_TYPE()
    chain = " ".join(context.args).lower()
    chain_url = ""
    chain_name = ""
    chain_mappings = {
        "eth": (url.dex_tools_eth, "(ETH)"),
        "bsc": (url.dex_tools_bsc, "(BSC)"),
        "bnb": (url.dex_tools_bsc, "(BSC)"),
        "polygon": (url.dex_tools_poly, "(POLYGON)"),
        "poly": (url.dex_tools_poly, "(POLYGON)"),
        "optimism": (url.dex_tools_opti, "(OPTI)"),
        "opti": (url.dex_tools_opti, "(OPTI)"),
        "arbitrum": (url.dex_tools_arb, "(ARB)"),
        "arb": (url.dex_tools_arb, "(ARB)"),
    }
    if chain in chain_mappings:
        chain_url, chain_name = chain_mappings[chain]
    else:
        chain_url, chain_name = chain_mappings["eth"]
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Chart Links* {chain_name}\nUse `/chart [chain-name]` for other chains\n"
        f"Use `/constellations` for constellations\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7R - Rewards Token", url=f"{chain_url}{ca.x7r}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7DAO - Governance Token",
                        url=f"{chain_url}{ca.x7dao}",
                    )
                ],
            ]
        ),
    )


async def compare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token_names = {
    "x7r": {
        "contract": ca.x7r,
        "image": media.x7r_logo
    },
    "x7dao": {
        "contract": ca.x7dao,
        "image": media.x7dao_logo
    },
    "x7101": {
        "contract": ca.x7101,
        "image": media.x7101_logo
    },
    "x7102": {
        "contract": ca.x7102,
        "image": media.x7102_logo
    },
    "x7103": {
        "symbol": ca.x7103,
        "image": media.x7103_logo
    },
    "x7104": {
        "contract": ca.x7104,
        "image": media.x7104_logo
    },
    "x7105": {
        "contract": ca.x7105,
        "image": media.x7105_logo
        }
    }

    x7token = context.args[0].lower()
    token2 = context.args[1].lower()
    search = api.get_cg_search(token2)
    token_id = search["coins"][0]["api_symbol"]
    thumb = search["coins"][0]["large"]

    if x7token in token_names:
        token_info = token_names[x7token]
        x7_price = api.get_price(token_info["contract"], "eth")
        image = token_info["image"]
        token_market_cap = api.get_mcap(token_id)
        if token_market_cap == 0:
            await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=
            f'*X7 Finance Market Cap Comparison*\n\n'
            f"No Market Cap data found for {token2.upper()}\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )
        if x7token == ca.x7r:
            x7_supply = ca.supply - api.get_token_balance(ca.dead, ca.x7r, "eth")
        else:
            x7_supply = ca.supply
        x7_market_cap = x7_price * x7_supply
        percent = ((token_market_cap - x7_market_cap) / x7_market_cap) * 100
        x = ((token_market_cap - x7_market_cap) / x7_market_cap)
        token_value = token_market_cap / x7_supply
        img = Image.open(requests.get(thumb, stream=True).raw)
        result = img.convert("RGBA")
        result.save(r"media/cgtokenlogo.png")
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(r"media/cgtokenlogo.png")
        im2_resized = im2.resize((200, 200))
        im3 = Image.open(image)
        im1.paste(im2_resized, (680, 20), im2_resized)
        im1.paste(im3, (680, 200), im3)
        myfont = ImageFont.truetype(R"media/FreeMonoBold.ttf", 28)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (28, 36),
            f'X7 Finance Market Cap Comparison\n\n'
            f"Token value of {context.args[0].upper()} at {context.args[1].upper()} Market Cap:\n"
            f'(${"{:,.2f}".format(token_market_cap)})\n\n'
            f'${"{:,.2f}".format(token_value)}\n'
            f'{"{:,.0f}%".format(percent)}\n'
            f'{"{:,.0f}x".format(x)}\n\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        im1.save(r"media/blackhole.png", quality=95)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=
                f'*X7 Finance Market Cap Comparison*\n\n'
                f"Token value of {context.args[0].upper()} at {context.args[1].upper()} Market Cap\n"
                f'(${"{:,.2f}".format(token_market_cap)})\n\n'
                f'${"{:,.2f}".format(token_value)}\n'
                f'{"{:,.0f}%".format(percent)}\n'
                f'{"{:,.0f}x".format(x)}\n\n{api.get_quote()}',
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=f"{context.args[1].upper()} Chart",
                            url=f"https://www.coingecko.com/en/coins/{token_id}",
                        )
                    ],
                ]
            ),
        )
    else:
        await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=
            f'*X7 Finance Market Cap Comparison*\n\n'
            f"Please enter X7 token first followed by token to compare\n\n"
            f"ie. `/compare x7r uni`\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )


async def constellations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    price = api.get_cg_price("x7101, x7102, x7103, x7104, x7105")
    x7101mc = price["x7101"]["usd"] * ca.supply
    x7102mc = price["x7102"]["usd"] * ca.supply
    x7103mc = price["x7103"]["usd"] * ca.supply
    x7104mc = price["x7104"]["usd"] * ca.supply
    x7105mc = price["x7105"]["usd"] * ca.supply
    const_mc = x7101mc + x7102mc + x7103mc + x7104mc + x7105mc
    if price["x7101"]["usd_24h_change"] is None:
        price["x7101"]["usd_24h_change"] = 0
    if price["x7102"]["usd_24h_change"] is None:
        price["x7102"]["usd_24h_change"] = 0
    if price["x7103"]["usd_24h_change"] is None:
        price["x7103"]["usd_24h_change"] = 0
    if price["x7104"]["usd_24h_change"] is None:
        price["x7104"]["usd_24h_change"] = 0
    if price["x7105"]["usd_24h_change"] is None:
        price["x7105"]["usd_24h_change"] = 0
    if chain == "":
        img = Image.open((random.choice(media.blackhole)))
        i1 = ImageDraw.Draw(img)
        myfont = ImageFont.truetype(R"media/FreeMonoBold.ttf", 20)
        i1.text(
            (28, 36),
            f"X7 Finance Constellation Token Prices (ETH)\n\n"
            f'X7101:      ${price["x7101"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7101"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(x7101mc)}\n\n'
            f'X7102:      ${price["x7102"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7102"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(x7102mc)}\n\n'
            f'X7103:      ${price["x7103"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7103"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(x7103mc)}\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        i1.text(
            (522, 90),
            f'X7104:      ${price["x7104"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7104"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(x7104mc)}\n\n'
            f'X7105:      ${price["x7105"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7105"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(x7105mc)}\n\n'
            f'Combined Market Cap:\n${"{:0,.0f}".format(const_mc)}\n',
            font=myfont,
            fill=(255, 255, 255),
        )
        img.save(r"media/blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f"*X7 Finance Constellation Token Prices (ETH)*\n\n"
            f"For more info use `/x7token-name`\n\n"
            f'X7101:      ${price["x7101"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7101"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(x7101mc)}\n'
            f"CA: `{ca.x7101}\n\n`"
            f'X7102:      ${price["x7102"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7102"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(x7102mc)}\n'
            f"CA: `{ca.x7102}\n\n`"
            f'X7103:      ${price["x7103"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7103"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(x7103mc)}\n'
            f"CA: `{ca.x7103}\n\n`"
            f'X7104:      ${price["x7104"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7104"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(x7104mc)}\n'
            f"CA: `{ca.x7104}\n\n`"
            f'X7105:      ${price["x7105"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7105"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(x7105mc)}\n'
            f"CA: `{ca.x7105}\n\n`"
            f'Combined Market Cap: ${"{:0,.0f}".format(const_mc)}\n\n'
            f"{api.get_quote()}",
            parse_mode="Markdown",
        )


async def contracts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Contract Addresses for all chains*\n\n"
        f"*X7R - Rewards Token *\n`{ca.x7r}`\n\n"
        f"*X7DAO - Governance Token*\n`{ca.x7dao}`\n\n"
        f"For advanced trading and arbitrage opportunities see `/constellations`\n\n"
        f"{api.get_quote()}",
        parse_mode="Markdown",
    )


async def deployer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tx = api.get_tx(ca.deployer, "eth")
    time = datetime.utcfromtimestamp(int(tx["result"][0]["timeStamp"]))
    now = datetime.utcnow()
    duration = now - time
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    if (
        str(tx["result"][0]["to"]).lower()
        == "0x000000000000000000000000000000000000dead"
    ):
        message = bytes.fromhex(tx["result"][0]["input"][2:]).decode("utf-8")
        await update.message.reply_text(
            f"*Last On Chain Message:*\n\n{time} (UTC)\n"
            f"{int(days[0])} days, {int(hours[0])} hours and {int(minutes[0])} minutes ago:\n\n"
            f"`{message}`\n",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="View on chain",
                            url=f'{url.ether_tx}{tx["result"][0]["hash"]}',
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="View all on chains", url=f"{url.dashboard}docs/onchains"
                        )
                    ],
                ]
            ),
        )
    else:
        await update.message.reply_photo(
            photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
            caption=f"*Deployer Wallet last TX*\n\n{time} (UTC)\n"
            f"{int(days[0])} days, {int(hours[0])} hours and {int(minutes[0])} minutes ago:\n\n"
            f'*{tx["result"][0]["functionName"]}*\n\n'
            f"This command will pull last TX on the X7 Finance deployer wallet."
            f" To view last on chain use `/on_chain`\n\n"
            f"{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="View on chain",
                            url=f'{url.ether_tx}{tx["result"][0]["hash"]}',
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="View all on chains", url=f"{url.dashboard}docs/onchains"
                        )
                    ],
                ]
            ),
        )


async def discount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"*X7 Finance Discount*\n\n{text.discount}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Discount Application", url=url.dac)],
                [
                    InlineKeyboardButton(
                        text="X7 Lending Discount Contract",
                        url=f"{url.ether_address}{ca.lending_discount}#code",
                    )
                ],
            ]
        ),
    )


async def docs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Documents*\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Get Started", url=f"{url.dashboard}getstarted/")
                ],
                [
                    InlineKeyboardButton(
                        text="Trader", url=f"{url.dashboard}docs/guides/trade/"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Project Launcher", url=f"{url.dashboard}docs/guides/launch/"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Project Engineer", url=f"{url.dashboard}docs/guides/integrate/",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Capital Allocator", url=f"{url.dashboard}docs/guides/lending/"
                    )
                ],
            ]
        ),
    )


async def ebb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "eth" or chain == "":
        chain_name = "(ETH)"
        chain_url = url.ether_address
        now = datetime.utcnow()

        def get_liquidity_data(hub_address):
            hub = api.get_internal_tx(hub_address, "eth")
            hub_filter = [
                d for d in hub["result"] if d["from"] in str(hub_address).lower()
            ]
            value_raw = int(hub_filter[0]["value"]) / 10**18
            value = str(value_raw)
            dollar = float(value) * float(api.get_native_price("eth")) / 1**18
            time = datetime.utcfromtimestamp(int(hub_filter[0]["timeStamp"]))
            duration = now - time
            duration_in_s = duration.total_seconds()
            days = divmod(duration_in_s, 86400)
            hours = divmod(days[1], 3600)
            minutes = divmod(hours[1], 60)
            return value, dollar, time, int(days[0]), int(hours[0]), int(minutes[0])

        (
            x7r_value,
            x7r_dollar,
            x7r_time,
            x7r_days,
            x7r_hours,
            x7r_minutes,
        ) = get_liquidity_data(ca.x7r_liq_hub)
        (
            x7dao_value,
            x7dao_dollar,
            x7dao_time,
            x7dao_days,
            x7dao_hours,
            x7dao_minutes,
        ) = get_liquidity_data(ca.x7dao_liq_hub)
        (
            x7100_value,
            x7100_dollar,
            x7100_time,
            x7100_days,
            x7100_hours,
            x7100_minutes,
        ) = get_liquidity_data(ca.x7100_liq_hub)
        await update.message.reply_photo(
            photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
            caption=f"*X7 Finance Liquidity Hubs {chain_name}*\nUse `/ebb [chain-name]` for other chains\n\n"
            f'Last X7R Buy Back: {x7r_time}\n{x7r_value[:5]} ETH (${"{:0,.0f}".format(x7r_dollar)})\n'
            f"{x7r_days} days, {x7r_hours} hours and {x7r_minutes} minutes ago\n\n"
            f'Last X7DAO Buy Back: {x7dao_time}\n{x7dao_value[:5]} ETH (${"{:0,.0f}".format(x7dao_dollar)})\n'
            f"{x7dao_days} days, {x7dao_hours} hours and {x7dao_minutes} minutes ago\n\n"
            f'Last X7100 Buy Back: {x7100_time}\n{x7100_value[:5]} ETH (${"{:0,.0f}".format(x7100_dollar)})\n'
            f"{x7100_days} days, {x7100_hours} hours and {x7100_minutes} minutes ago\n\n"
            f"{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="X7R Liquidity Hub", url=f"{chain_url}{ca.x7r_liq_hub}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="X7DAO Liquidity Hub",
                            url=f"{chain_url}{ca.x7dao_liq_hub}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="X7100 Liquidity Hub",
                            url=f"{chain_url}{ca.x7100_liq_hub}",
                        )
                    ],
                ]
            ),
        )


async def ecosystem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"{text.ecosystem}" f"\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Xchange App", url=f"{url.xchange}")],
                [InlineKeyboardButton(text="Website", url=f"{url.dashboard}")],
            ]
        ),
    )


async def endorse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"{text.endorse}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7 Xchange Alerts ", url=f"{url.tg_alerts}"
                    )
                ],
            ]
        ),
    )


async def fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*Fact!*\n\n{api.get_fact()}",
        parse_mode="Markdown"
    )


async def factory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Factories*\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="ETH", url=f"{url.ether_address}{ca.factory}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="BSC", url=f"{url.bsc_address}{ca.factory}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Polygon", url=f"{url.poly_address}{ca.factory}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Arbitrum", url=f"{url.arb_address}{ca.factory}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Optimism", url=f"{url.opti_address}{ca.factory}"
                    )
                ],
            ]
        ),
    )


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance FAQ*\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Airdrop Questions",
                        url="https://www.x7finance.org/docs/faq/airdrop",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Constellation Tokens",
                        url="https://www.x7finance.org/docs/faq/constellations",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Developer Questions",
                        url="https://www.x7finance.org/docs/faq/devs",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="General Questions",
                        url="https://www.x7finance.org/docs/faq/general",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Governance Questions",
                        url="https://www.x7finance.org/docs/faq/governance",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Investor Questions",
                        url="https://www.x7finance.org/faq/investors",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Liquidity Lending Questions",
                        url="https://www.x7finance.org/docs/faq/liquiditylending",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="NFT Questions",
                        url="https://www.x7finance.org/faq/nfts"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Snapshot.org Questions",
                        url="https://www.x7finance.org/docs/faq/daosnapshot",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Xchange Questions",
                        url="https://www.x7finance.org/faq/xchange",
                    )
                ],
            ]
        ),
    )


async def fg(update, context):
    fear_response = requests.get("https://api.alternative.me/fng/?limit=0")
    fear_data = fear_response.json()
    fear_values = []
    for i in range(7):
        timestamp = float(fear_data["data"][i]["timestamp"])
        localtime = datetime.fromtimestamp(timestamp)
        fear_values.append(
            (
                fear_data["data"][i]["value"],
                fear_data["data"][i]["value_classification"],
                localtime,
            )
        )
    duration_in_s = float(fear_data["data"][0]["time_until_update"])
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    caption = "*Market Fear and Greed Index*\n\n"
    caption += f'{fear_values[0][0]} - {fear_values[0][1]} - {fear_values[0][2].strftime("%A %B %d")}\n\n'
    caption += "Change:\n"
    for i in range(1, 7):
        caption += f'{fear_values[i][0]} - {fear_values[i][1]} - {fear_values[i][2].strftime("%A %B %d")}\n'
    caption += "\nNext Update:\n"
    caption += (
        f"{int(hours[0])} hours and {int(minutes[0])} minutes\n\n{api.get_quote()}"
    )
    await update.message.reply_photo(
        photo="https://alternative.me/crypto/fear-and-greed-index.png",
        caption=caption,
        parse_mode="Markdown",
    )


async def gas(update, context):
    chain = " ".join(context.args).lower()
    chain_name = ""
    chain_url = ""
    gas_data = ""
    im2 = None
    if chain == "" or chain == "eth":
        chain = "eth"
        gas_data = api.get_gas(chain)
        im2 = Image.open(media.eth_logo)
        chain_name = "(ETH)"
        chain_url = "https://etherscan.io/gastracker"
    elif chain == "bsc":
        gas_data = api.get_gas(chain)
        im2 = Image.open(media.bsc_logo)
        chain_name = "(BSC)"
        chain_url = "https://bscscan.com/gastracker"
    elif chain == "polygon" or chain == "poly":
        chain = "poly"
        gas_data = api.get_gas(chain)
        im2 = Image.open(media.poly_logo)
        chain_name = "(POLYGON)"
        chain_url = "https://polygon.com/gastracker"
    if im2 is None:
        await update.message.reply_text(
            "Invalid chain. Please provide a valid chain name.", parse_mode="Markdown"
        )
        return
    im1 = Image.open(random.choice(media.blackhole))
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (26, 30),
        f"{chain_name} Gas Prices:\n\n"
        f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n'
        f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n'
        f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n\n\n\n\n\n\n\n'
        f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font=myfont,
        fill=(255, 255, 255),
    )
    im1.save("media/blackhole.png")
    await update.message.reply_photo(
        photo=open("media/blackhole.png", "rb"),
        caption=f"*{chain_name} Gas Prices:*\n"
        f"For other chains use `/gas [chain-name]`\n\n"
        f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n'
        f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n'
        f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n'
        f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=f"{chain_name} Gas Tracker", url=chain_url)]]
        ),
    )


async def giveaway_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ext = " ".join(context.args)
    giveaway_time = giveaway.time
    def calculate_duration(giveaway_time):
        now = datetime.now(timezone.utc)
        duration = giveaway_time - now
        return duration
    giveaway_time = giveaway.time
    duration = calculate_duration(giveaway_time)
    if duration < timedelta(0):
        await update.message.reply_photo(
            photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
            caption=f"X7 Finance Giveaway is now closed\n\nPlease check back for more details"
            f"\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )
    else:
        if ext == "":
            await update.message.reply_photo(
                 photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
                 caption=f"*{giveaway.header}*\n\n{giveaway.text}\n\n{giveaway.countdown()}\n\n{api.get_quote()}",
                 parse_mode="Markdown",
             )
        if ext == "entries":
            await update.message.reply_photo(
                photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
                caption=f'*{giveaway.header}*\n\n{giveaway.entries()}\n\n'
                f"{api.get_quote()}",
                parse_mode="Markdown",
            )
        if ext == "run":
            chat_admins = await update.effective_chat.get_administrators()
            if update.effective_user in (admin.user for admin in chat_admins):
                await update.message.reply_photo(
                    photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
                    caption=f"*{giveaway.header}*\n\n{giveaway.run()}\n\n{api.get_quote()}",
                    parse_mode="Markdown",
                )
            else:
                await update.message.reply_text(f"{text.mods_only}")


async def holders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    x7dao_holders = api.get_holders(ca.x7dao)
    x7r_holders = api.get_holders(ca.x7r)
    img = Image.open((random.choice(media.blackhole)))
    i1 = ImageDraw.Draw(img)
    myfont = ImageFont.truetype(R"media/FreeMonoBold.ttf", 28)
    i1.text(
        (28, 36),
        f"X7 Finance Token Holders (ETH)\n\n"
        f"X7R Holders: {x7r_holders}\n"
        f"X7DAO Holders: {x7dao_holders}\n\n\n\n\n\n\n\n\n"
        f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font=myfont,
        fill=(255, 255, 255),
    )
    img.save(r"media/blackhole.png")
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=f"*X7 Finance Token Holders (ETH)*\n\n"
        f"X7R Holders: {x7r_holders}\n"
        f"X7DAO Holders: {x7dao_holders}\n\n"
        f"{api.get_quote()}",
        parse_mode="Markdown",
    )


async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    img = Image.open((random.choice(media.blackhole)))
    i1 = ImageDraw.Draw(img)
    myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 28)
    wrapper = textwrap.TextWrapper(width=50)
    word_list = wrapper.wrap(text=text)
    caption_new = ""
    for ii in word_list:
        caption_new = caption_new + ii + "\n"
    i1.text((50, img.size[1] / 8), caption_new, font=myfont, fill=(255, 255, 255))
    img.save(r"media/blackhole.png")
    i1.text(
        (50, 460),
        f"{update.message.from_user.username}\n"
        f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font=myfont,
        fill=(255, 255, 255),
    )
    img.save(r"media/blackhole.png")
    await update.message.reply_photo(photo=open(r"media/blackhole.png", "rb"))


async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joke_response = requests.get("https://v2.jokeapi.dev/joke/Any?safe-mode")
    joke = joke_response.json()
    if joke["type"] == "single":
        await update.message.reply_photo(
            photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
            caption=f'`{joke["joke"]}`',
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_photo(
            photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
            caption=f'`{joke["setup"]}\n\n{joke["delivery"]}`',
            parse_mode="Markdown",
        )


async def launch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    launch_raw = datetime(2022, 8, 13, 14, 10, 17)
    migration_raw = datetime(2022, 9, 25, 5, 0, 11)
    now = datetime.now()

    launch_duration = now - launch_raw
    launch_years = launch_duration.days // 365
    launch_months = (launch_duration.days % 365) // 30
    launch_weeks = ((launch_duration.days % 365) % 30) // 7
    launch_days = ((launch_duration.days % 365) % 30) % 7

    migration_duration = now - migration_raw
    migration_years = migration_duration.days // 365
    migration_months = (migration_duration.days % 365) // 30
    migration_weeks = ((migration_duration.days % 365) % 30) // 7
    migration_days = ((migration_duration.days % 365) % 30) % 7

    reply_message = f'*X7 Finance Launch Info*\n\nX7M105 Stealth Launch\n{launch_raw.strftime("%A %B %d %Y %I:%M %p")}\n'
    reply_message += f'{launch_years} years, {launch_months} months, {launch_weeks} weeks, and {launch_days} days ago\n\n'
    reply_message += f'V2 Migration\n{migration_raw.strftime("%A %B %d %Y %I:%M %p")}\n'
    reply_message += f'{migration_years} years, {migration_months} months, {migration_weeks} weeks, and {migration_days} days ago\n\n'
    reply_message += api.get_quote()

    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=reply_message,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7M105 Launch TX",
                        url=f"{url.ether_tx}0x11ff5b6a860170eaac5b33930680bf79dbf0656292cac039805dbcf34e8abdbf",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Migration Go Live TX",
                        url=f"{url.ether_tx}0x13e8ed59bcf97c5948837c8069f1d61e3b0f817d6912015427e468a77056fe41",
                    )
                ],
            ]
        ),
    )


async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance links*\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Xchange App", url=f"{url.xchange}")],
                [InlineKeyboardButton(text="Website", url=f"{url.dashboard}")],
                [InlineKeyboardButton(text="Snapshot", url=f"{url.snapshot}")],
                [InlineKeyboardButton(text="Twitter", url=f"{url.twitter}")],
                [InlineKeyboardButton(text="Discord", url=f"{url.discord}")],
                [InlineKeyboardButton(text="Reddit", url=f"{url.reddit}")],
                [InlineKeyboardButton(text="Youtube", url=f"{url.youtube}")],
                [InlineKeyboardButton(text="Github", url=f"{url.github}")],
                [InlineKeyboardButton(text="Dune", url=f"{url.dune}")],
            ]
        ),
    )


async def liquidate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "eth" or chain == "":
        web3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{os.getenv('INFURA_API_KEY')}",))
        link = url.ether_address
        chain = "eth"
    elif chain == "arb":
        web3 = Web3(Web3.HTTPProvider(f"https://arb-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_ARB')}",))
        link = url.arb_address
    elif chain == "bsc":
        web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/",))
        link = url.bsc_address
    elif chain == "opti":
        web3 = Web3(Web3.HTTPProvider(f"https://opt-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_OPTI')}",))
        link = url.opti_address
    elif chain == "poly":
        web3 = Web3(Web3.HTTPProvider(f"https://polygon-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_POLY')}",))
        link = url.poly_address

    contract = web3.eth.contract(address=Web3.to_checksum_address(ca.lpool), abi=api.get_abi(ca.lpool,chain))
    num_loans = contract.functions.nextLoanID().call()
    liquidatable_loans = 0
    results = []
    for loan_id in range(num_loans + 1):
        try:
            result = contract.functions.canLiquidate(int(loan_id)).call()
            if result == 1:
                liquidatable_loans += 1
                results.append(f"Loan ID {loan_id}")
        except Exception:
            continue
        
    liquidatable_loans_text = f"Total liquidatable loans: {liquidatable_loans}"
    output = "\n".join([liquidatable_loans_text] + results)
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Loan Liquidations ({chain.upper()})*\nfor other chains use `/liquidate [chain-name]`\n\n{output}\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Lending Pool Contract", url=f"{link}{ca.lpool}#writeContract")],
            ]
        ),
    )


async def liquidity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_name = ""
    chain_token_api = ""
    chain_token_name = ""
    chain_title = ""
    im2 = ""
    x7r_amount = ""
    x7dao_amount = ""
    cons_amount = ""
    x7dao_dollar = ""
    x7r_dollar = ""
    cons_dollar = ""
    chain_url = ""
    if chain == "" or chain == "eth":
        x7r_price = api.get_price(ca.x7r, "eth")
        x7dao_price = api.get_price(ca.x7r, "eth")
        x7101_price = api.get_price(ca.x7r, "eth")
        x7102_price = api.get_price(ca.x7r, "eth")
        x7103_price = api.get_price(ca.x7r, "eth")
        x7104_price = api.get_price(ca.x7r, "eth")
        x7105_price = api.get_price(ca.x7r, "eth")
        x7r = api.get_liquidity(ca.x7r_pair_eth, "eth")
        x7dao = api.get_liquidity(ca.x7dao_pair_eth, "eth")
        x7101 = api.get_liquidity(ca.x7101_pair_eth, "eth")
        x7102 = api.get_liquidity(ca.x7102_pair_eth, "eth")
        x7103 = api.get_liquidity(ca.x7103_pair_eth, "eth")
        x7104 = api.get_liquidity(ca.x7104_pair_eth, "eth")
        x7105 = api.get_liquidity(ca.x7105_pair_eth, "eth")
        x7r_token = float(x7r["reserve0"])
        x7r_weth = float(x7r["reserve1"]) / 10**18
        x7r_weth_dollar = float(x7r_weth) * float(api.get_native_price("eth"))
        x7r_token_dollar = float(x7r_price) * float(x7r_token) / 10**18
        x7dao_token = float(x7dao["reserve0"])
        x7dao_weth = float(x7dao["reserve1"]) / 10**18
        x7dao_weth_dollar = float(x7dao_weth) * float(api.get_native_price("eth"))
        x7dao_token_dollar = float(x7dao_price) * float(x7dao_token) / 10**18
        x7101_token = float(x7101["reserve0"])
        x7101_weth = float(x7101["reserve1"]) / 10**18
        x7101_weth_dollar = float(x7101_weth) * float(api.get_native_price("eth"))
        x7101_token_dollar = float(x7101_price) * float(x7101_token) / 10**18
        x7102_token = float(x7102["reserve0"])
        x7102_weth = float(x7102["reserve1"]) / 10**18
        x7102_weth_dollar = float(x7102_weth) * float(api.get_native_price("eth"))
        x7102_token_dollar = float(x7102_price) * float(x7102_token) / 10**18
        x7103_token = float(x7103["reserve0"])
        x7103_weth = float(x7103["reserve1"]) / 10**18
        x7103_weth_dollar = float(x7103_weth) * float(api.get_native_price("eth"))
        x7103_token_dollar = float(x7103_price) * float(x7103_token) / 10**18
        x7104_token = float(x7104["reserve0"])
        x7104_weth = float(x7104["reserve1"]) / 10**18
        x7104_weth_dollar = float(x7104_weth) * float(api.get_native_price("eth"))
        x7104_token_dollar = float(x7104_price) * float(x7104_token) / 10**18
        x7105_token = float(x7105["reserve0"])
        x7105_weth = float(x7105["reserve1"]) / 10**18
        x7105_weth_dollar = float(x7105_weth) * float(api.get_native_price("eth"))
        x7105_token_dollar = float(x7105_price) * float(x7105_token) / 10**18
        constellations_tokens = (
            x7101_token + x7102_token + x7103_token + x7104_token + x7105_token
        )
        constellations_weth = (
            x7101_weth + x7102_weth + x7103_weth + x7104_weth + x7105_weth
        )
        constellations_weth_dollar = (
            x7101_weth_dollar
            + x7102_weth_dollar
            + x7103_weth_dollar
            + x7104_weth_dollar
            + x7105_weth_dollar
        )
        constellations_token_dollar = (
            x7101_token_dollar
            + x7102_token_dollar
            + x7103_token_dollar
            + x7104_token_dollar
            + x7105_token_dollar
        )
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.eth_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 20)
        i1.text(
            (28, 36),
            f"X7 Finance Token Liquidity (ETH)\n\n"
            f"X7R\n"
            f'{"{:0,.0f}".format(x7r_token)[:4]}M X7R (${"{:0,.0f}".format(x7r_token_dollar)})\n'
            f'{"{:0,.0f}".format(x7r_weth)} WETH (${"{:0,.0f}".format(x7r_weth_dollar)})\n'
            f'Total Liquidity ${"{:0,.0f}".format(x7r_weth_dollar + x7r_token_dollar)}\n\n'
            f"X7DAO\n"
            f'{"{:0,.0f}".format(x7dao_token)[:4]}M X7DAO (${"{:0,.0f}".format(x7dao_token_dollar)})\n'
            f'{"{:0,.0f}".format(x7dao_weth)} WETH (${"{:0,.0f}".format(x7dao_weth_dollar)})\n'
            f'Total Liquidity ${"{:0,.0f}".format(x7dao_weth_dollar + x7dao_token_dollar)}\n\n'
            f"Constellations\n"
            f'{"{:0,.0f}".format(constellations_tokens)[:4]}M X7100 '
            f'(${"{:0,.0f}".format(constellations_token_dollar)})\n'
            f'{"{:0,.0f}".format(constellations_weth)} WETH '
            f'(${"{:0,.0f}".format(constellations_weth_dollar)})\n'
            f'Total Liquidity ${"{:0,.0f}".format(constellations_weth_dollar+constellations_token_dollar)}\n'
            f'\nUTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f"*X7 Finance Token Liquidity (ETH)*\n"
            f"To show initial liquidity for other chains, Use `/liquidity "
            f"[chain-name]`\n\n"
            f"*X7R*\n"
            f'{"{:0,.0f}".format(x7r_token)[:4]}M X7R (${"{:0,.0f}".format(x7r_token_dollar)})\n'
            f'{"{:0,.0f}".format(x7r_weth)} WETH (${"{:0,.0f}".format(x7r_weth_dollar)})\n'
            f'Total Liquidity ${"{:0,.0f}".format(x7r_weth_dollar + x7r_token_dollar)}\n\n'
            f"*X7DAO*\n"
            f'{"{:0,.0f}".format(x7dao_token)[:4]}M X7DAO (${"{:0,.0f}".format(x7dao_token_dollar)})\n'
            f'{"{:0,.0f}".format(x7dao_weth)} WETH (${"{:0,.0f}".format(x7dao_weth_dollar)})\n'
            f'Total Liquidity ${"{:0,.0f}".format(x7dao_weth_dollar + x7dao_token_dollar)}\n\n'
            f"*Constellations*\n"
            f'{"{:0,.0f}".format(constellations_tokens)[:4]}M X7100 '
            f'(${"{:0,.0f}".format(constellations_token_dollar)})\n'
            f'{"{:0,.0f}".format(constellations_weth)} WETH '
            f'(${"{:0,.0f}".format(constellations_weth_dollar)})\n'
            f'Total Liquidity ${"{:0,.0f}".format(constellations_weth_dollar+constellations_token_dollar)}\n\n'
            f"{api.get_quote()}",
            parse_mode="Markdown",
        )
        return
    if chain == "bsc" or chain == "bnb":
        chain_name = "bsc"
        chain_token_api = "bnb"
        chain_token_name = "BNB"
        chain_title = "(BSC)"
        chain_url = url.bsc_address
        im2 = Image.open(media.bsc_logo)
    if chain == "arbitrum" or chain == "arb":
        chain_name = "arb"
        chain_token_api = "eth"
        chain_token_name = "ETH"
        chain_title = "(ARB)"
        chain_url = url.arb_address
        im2 = Image.open(media.arb_logo)
    if chain == "optimism" or chain == "opti":
        chain_name = "opti"
        chain_token_api = "eth"
        chain_token_name = "ETH"
        chain_title = "(OPTI)"
        chain_url = url.opti_address
        im2 = Image.open(media.opti_logo)
    if chain == "polygon" or chain == "poly":
        chain_name = "poly"
        chain_token_api = "matic"
        chain_token_name = "MATIC"
        chain_title = "(POLYGON)"
        im2 = Image.open(media.poly_logo)
        chain_url = url.poly_address
    x7r_amount = api.get_native_balance(ca.x7r_liq_lock, chain_name)
    x7dao_amount = api.get_native_balance(ca.x7dao_liq_lock, chain_name)
    cons_amount = api.get_native_balance(ca.cons_liq_lock, chain_name)
    x7dao_dollar = (
        float(x7dao_amount) * float(api.get_native_price(chain_token_api)) / 1**18
    )
    x7r_dollar = (
        float(x7r_amount) * float(api.get_native_price(chain_token_api)) / 1**18
    )
    cons_dollar = (
        float(cons_amount) * float(api.get_native_price(chain_token_api)) / 1**18
    )
    im1 = Image.open((random.choice(media.blackhole)))
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
    i1.text(
        (28, 36),
        f"X7 Finance Initial Liquidity {chain_title}\n\n"
        f'X7R:\n{x7r_amount} {chain_token_name} (${"{:0,.0f}".format(x7r_dollar)})\n\n'
        f'X7DAO:\n{x7dao_amount} {chain_token_name} (${"{:0,.0f}".format(x7dao_dollar)})\n\n'
        f'X7100:\n{cons_amount} {chain_token_name} (${"{:0,.0f}".format(cons_dollar)})\n\n\n\n'
        f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font=myfont,
        fill=(255, 255, 255),
    )
    img_path = os.path.join("media", "blackhole.png")
    im1.save(img_path)
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=f"*X7 Finance Initial Liquidity {chain_title}*\nUse `/liquidity [chain-name]` for other chains\n\n"
        f'X7R:\n{x7r_amount} {chain_token_name} (${"{:0,.0f}".format(x7r_dollar)})\n\n'
        f'X7DAO:\n{x7dao_amount} {chain_token_name} (${"{:0,.0f}".format(x7dao_dollar)})\n\n'
        f'X7100:\n{cons_amount} {chain_token_name} (${"{:0,.0f}".format(cons_dollar)})\n\n{api.get_quote()}',
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7R Initial Liquidity",
                        url=f"{chain_url}{ca.x7r_liq_lock}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7DAO Initial Liquidity",
                        url=f"{chain_url}{ca.x7dao_liq_lock}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7100 Initial Liquidity",
                        url=f"{chain_url}{ca.cons_liq_lock}",
                    )
                ],
            ]
        ),
    )


async def loan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loan_id = ""
    chain = ""
    web_url = ""
    token = ""
    scan_address = ""
    scan_token = ""
    price = ""
    if len(context.args) >= 2:
        chain = context.args[0].lower()
        loan_id = context.args[1]
    else:
        await update.message.reply_text(
            f"Please use `/loan chain_name loan_id` to see details",
            parse_mode="Markdown",
        )
        return
    if chain == "eth":
        web_url = f"https://eth-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_ETH')}"
        token = "ETH"
        scan_address = url.ether_address
        scan_token = url.ether_token
        price = api.get_native_price("eth")
    elif chain == "arb":
        web_url = f"https://arb-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_ARB')}"
        token = "ETH"
        scan_address = url.arb_address
        scan_token = url.arb_token
        price = api.get_native_price("eth")
    elif chain == "bsc":
        web_url = "https://bsc-dataseed.binance.org/"
        token = "BNB"
        scan_address = url.bsc_address
        scan_token = url.bsc_token
        price = api.get_native_price("bnb")
    elif chain == "poly":
        web_url = f"https://polygon-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_POLY')}"
        token = "MATIC"
        scan_address = url.poly_address
        scan_token = url.poly_token
        price = api.get_native_price("matic")
    elif chain == "opti":
        web_url = f"https://opt-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_OPTI')}"
        token = "ETH"
        scan_address = url.opti_address
        scan_token = url.opti_token
        price = api.get_native_price("eth")
    else:
        await update.message.reply_text(
            f"Please use `/loan chain_name loan_id` to see details",
            parse_mode="Markdown",
        )
        return
    web3 = Web3(Web3.HTTPProvider(web_url))
    address = to_checksum_address(ca.lpool)
    contract = web3.eth.contract(address=address, abi=api.get_abi(ca.lpool, chain))
    liquidation_status = ""
    try:
        liquidation = contract.functions.canLiquidate(int(loan_id)).call()
        if liquidation != 0:
            reward = contract.functions.liquidationReward().call() / 10**18
            liquidation_status = (
                f"\n\n*Eligible For Liquidation*\n"
                f"Cost: {liquidation / 10 ** 18} {token} "
                f'(${"{:0,.0f}".format(price*liquidation / 10 ** 18)})\n'
                f'Reward: {reward} {token} (${"{:0,.0f}".format(price*reward)})'
            )
    except (Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
        pass
    liability = contract.functions.getRemainingLiability(int(loan_id)).call() / 10**18
    remaining = f'Remaining Liability {liability} {token} (${"{:0,.0f}".format(price*liability)})'
    schedule1 = contract.functions.getPremiumPaymentSchedule(int(loan_id)).call()
    schedule2 = contract.functions.getPrincipalPaymentSchedule(int(loan_id)).call()
    schedule_list = []
    if len(schedule1[0]) > 0 and len(schedule1[1]) > 0:
        if len(schedule2[0]) == len(schedule1[0]) and len(schedule2[1]) == len(
            schedule1[1]
        ):
            for date1, value1, value2 in zip(schedule1[0], schedule1[1], schedule2[1]):
                formatted_date = datetime.fromtimestamp(date1).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                combined_value = (value1 + value2) / 10**18
                sch = f"{formatted_date} - {combined_value} {token}"
                schedule_list.append(sch)
        else:
            for date, value in zip(schedule1[0], schedule1[1]):
                formatted_date = datetime.fromtimestamp(date).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                formatted_value = value / 10**18
                sch = f"{formatted_date} - {formatted_value} {token}"
                schedule_list.append(sch)
    else:
        for date, value in zip(schedule2[0], schedule2[1]):
            formatted_date = datetime.fromtimestamp(date).strftime("%Y-%m-%d %H:%M:%S")
            formatted_value = value / 10**18
            sch = f"{formatted_date} - {formatted_value} {token}"
            schedule_list.append(sch)
    schedule_str = "\n".join(schedule_list)
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Initial Liquidity Loan - {loan_id} ({chain.upper()})*\n\n"
        f"Payment Schedule (UTC):\n{schedule_str}\n\n"
        f"{remaining}"
        f"{liquidation_status}\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=f"Token Contract",
                        url=f"{scan_token}{contract.functions.loanToken(int(loan_id)).call()}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"Borrower",
                        url=f"{scan_address}{contract.functions.loanBorrower(int(loan_id)).call()}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"X7 Lending Pool Contract",
                        url=f"{scan_address}{ca.lpool}#code",
                    )
                ],
            ]
        ),
    )


async def loans_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loan_type = " ".join(context.args).lower()
    loan_name = ""
    loan_terms = ""
    loan_ca = ""
    if loan_type == "":
        await update.message.reply_text(
            f"{loans.overview}\n\n{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="X7 Finance Whitepaper", url=f"{url.wp_link}"
                        )
                    ],
                ]
            ),
        )
        return
    else:
        loan_types = {
            "ill001": (loans.ill001_name, loans.ill001_terms, ca.ill001),
            "ill002": (loans.ill002_name, loans.ill002_terms, ca.ill002),
            "ill003": (loans.ill003_name, loans.ill003_terms, ca.ill003),
        }
        if loan_type in loan_types:
            loan_name, loan_terms, loan_ca = loan_types[loan_type]
            await update.message.reply_photo(
                photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
                caption=f"{loan_name}\n\n{loan_terms.generate_terms()}\n\n",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=f"Ethereum", url=f"{url.ether_address}{loan_ca}"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text=f"BSC", url=f"{url.bsc_address}{loan_ca}"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text=f"Polygon", url=f"{url.poly_address}{loan_ca}"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text=f"Arbitrum", url=f"{url.arb_address}{loan_ca}"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text=f"Optimism", url=f"{url.opti_address}{loan_ca}"
                            )
                        ],
                    ]
                ),
            )
    if loan_type == "count":
        networks = {
            "ETH": f"https://eth-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_ETH')}",
            "ARB": f"https://arb-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_ARB')}",
            "BSC": "https://bsc-dataseed.binance.org/",
            "POLY": f"https://polygon-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_POLY')}",
            "OPTI": f"https://opt-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_OPTI')}",
        }
        contract_networks = {
            "ETH": "eth",
            "ARB": "arb",
            "BSC": "bsc",
            "POLY": "poly",
            "OPTI": "opti",
        }
        contract_instances = {}
        for network, web3_url in networks.items():
            web3 = Web3(Web3.HTTPProvider(web3_url))
            contract = web3.eth.contract(
                address=to_checksum_address(ca.lpool),
                abi=api.get_abi(ca.lpool, contract_networks[network]),
            )
            amount = contract.functions.nextLoanID().call() - 1
            contract_instances[network] = amount
        await update.message.reply_photo(
            photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
            caption=f"*X7 Finance Loan Count*\n\n"
            f'`ETH:`       {contract_instances["ETH"]}\n'
            f'`BSC:`       {contract_instances["BSC"]}\n'
            f'`ARB:`       {contract_instances["ARB"]}\n'
            f'`POLY:`     {contract_instances["POLY"]}\n'
            f'`OPTI:`     {contract_instances["OPTI"]}\n\n'
            f"`TOTAL:`   {sum(contract_instances.values())}\n\n"
            f"{api.get_quote()}",
            parse_mode="Markdown",
        )


async def magisters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_name = ""
    chain_url = ""
    holders = ""
    if chain in ["eth", ""]:
        chain = "eth"
        chain_name = "(ETH)"
        chain_url = url.ether_token
        holders = api.get_nft_holder_count(ca.magister, "?chain=eth-main")
    elif chain == "bsc" or chain == "bnb":
        chain = "bsc"
        chain_name = "(BSC)"
        chain_url = url.bsc_token
    elif chain == "polygon" or chain == "poly":
        chain = "polygon"
        chain_name = "(POLYGON)"
        chain_url = url.poly_token
        holders = api.get_nft_holder_count(ca.magister, "?chain=poly-main")
    elif chain == "optimism" or chain == "opti":
        chain = "optimism"
        chain_name = "(OPTIMISM)"
        chain_url = url.opti_token
        holders = api.get_nft_holder_count(ca.magister, "?chain=optimism-main")
    elif chain == "arbitrum" or chain == "arb":
        chain = "arbitrum"
        chain_name = "(ARB)"
        chain_url = url.arb_token
        holders = api.get_nft_holder_count(ca.magister, "?chain=arbitrum-main")
    else:
        await update.message.reply_text("Invalid chain. Please specify a valid chain.")
        return
    response = api.get_nft_holder_list(ca.magister, chain)
    magisters = [holder["owner_of"] for holder in response["result"]]
    address = "\n\n".join(map(str, magisters))
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Magister Holders {chain_name}*\n"
        f"Use `/magisters [chain-name]` or other chains\n\n"
        f"Holders - {holders}\n\n"
        f"`{address}`\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Magister Holder List",
                        url=f"{chain_url}{ca.magister}#balances",
                    )
                ],
            ]
        ),
    )


async def mcap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain in ["eth", ""]:
        chain = "eth"
        chain_name = "(ETH)"
    elif chain == "bsc" or chain == "bnb":
        chain = "bsc"
        chain_name = "(BSC)"
    elif chain == "polygon" or chain == "poly":
        chain = "polygon"
        chain_name = "(POLYGON)"
    elif chain == "optimism" or chain == "opti":
        chain = "optimism"
        chain_name = "(OPTIMISM)"
    elif chain == "arbitrum" or chain == "arb":
        chain = "arbitrum"
        chain_name = "(ARB)"
    price = {}
    token_names = {
    ca.x7r: "X7R",
    ca.x7dao: "X7DAO",
    ca.x7101: "X7101",
    ca.x7102: "X7102",
    ca.x7103: "X7103",
    ca.x7104: "X7104",
    ca.x7105: "X7105",
}
    for token in ca.tokens:
        token_name = token_names.get(token, "Unknown Token")
        price[token] = api.get_price(token, chain)

    x7r_supply = ca.supply - api.get_token_balance(ca.dead, ca.x7r, chain)

    caps = {}
    for token in ca.tokens:
        if token == ca.x7r:
            caps[token] = price[token] * x7r_supply
        else:
            caps[token] = price[token] * ca.supply
    cons_cap = sum(caps.values()) - caps[ca.x7r] - caps[ca.x7dao]
    total_cap = sum(caps.values())
    im1 = Image.open(random.choice(media.blackhole))
    im2 = Image.open(media.eth_logo)
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 22)
    i1 = ImageDraw.Draw(im1)
    market_cap_info = f"X7 Finance Market Cap Info {chain_name}\n\n"
    market_cap_info += f'X7R:     ${"{:0,.0f}".format(caps[ca.x7r])}\n'
    for token in ca.tokens:
        if token == ca.x7r:
            continue
        market_cap_info += f'{token_name}:   ${"{:0,.0f}".format(caps[token])}\n'
    market_cap_info += f'\nConstellations Combined:\n${"{:0,.0f}".format(cons_cap)}\n\n'
    market_cap_info += f'Total Token Market Cap:\n${"{:0,.0f}".format(total_cap)}\n\n'
    market_cap_info += (
        f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}'
    )
    i1.text((28, 36), market_cap_info, font=myfont, fill=(255, 255, 255))
    im1.save(r"media/blackhole.png")
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=f"*X7 Finance Market Cap Info {chain_name}*\n\n"
        f'`X7R: `            ${"{:0,.0f}".format(caps[ca.x7r])}\n'
        f'`X7DAO:`         ${"{:0,.0f}".format(caps[ca.x7dao])}\n'
        f'`X7101:`         ${"{:0,.0f}".format(caps[ca.x7101])}\n'
        f'`X7102:`         ${"{:0,.0f}".format(caps[ca.x7102])}\n'
        f'`X7103:`         ${"{:0,.0f}".format(caps[ca.x7103])}\n'
        f'`X7104:`         ${"{:0,.0f}".format(caps[ca.x7104])}\n'
        f'`X7105:`         ${"{:0,.0f}".format(caps[ca.x7105])}\n\n'
        f"`Constellations Combined:`\n"
        f'${"{:0,.0f}".format(cons_cap)}\n\n'
        f"`Total Token Market Cap:`\n"
        f'${"{:0,.0f}".format(total_cap)}'
        f"\n\n{api.get_quote()}",
        parse_mode="Markdown",
    )


async def media_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Media Links*\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7 Official Images", 
                        url="https://imgur.com/a/WEszZTa"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 Official Token Logos Pack 1",
                        url="https://t.me/X7announcements/58",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 Official Token Logos Pack 2",
                        url="https://t.me/X7announcements/141",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 TG Sticker Pack 1",
                        url="https://t.me/addstickers/x7financestickers",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 TG Sticker Pack 2",
                        url="https://t.me/addstickers/X7finance",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 TG Sticker Pack 3",
                        url="https://t.me/addstickers/x7financ",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 TG Sticker Pack 4",
                        url="https://t.me/addstickers/GavalarsX7",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 Emojis Pack",
                        url="https://t.me/addemoji/x7FinanceEmojis",
                    )
                ],
            ]
        ),
    )


async def nft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower().strip()
    if chain == "" or chain == "eth":
        chain = "eth"
    elif chain == "poly" or chain == "polygon":
        chain = "poly"
    elif chain == "arb" or chain == "arbitrum":
        chain = "arb"
    elif chain == "opti" or chain == "optimism":
        chain = "opti"
    elif chain == "bsc" or chain == "binance" or chain == "binance smart chain":
        chain = "bsc"
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Invalid chain. Please provide a valid chain name."
        )
        return

    chain_prices = nfts.prices.get(chain)
    chain_counts = nfts.counts.get(chain)

    if chain_prices is None or chain_counts is None:
        if chain == "eth":
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text="Chain information not found."
            )
            return
        else:
            chain_prices = nfts.prices.get("eth")
            chain_counts = nfts.counts.get("eth")

            if chain_prices is None or chain_counts is None:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, text="Chain information not found."
                )
                return
            
    eco_price = chain_prices.get("eco")
    liq_price = chain_prices.get("liq")
    dex_price = chain_prices.get("dex")
    borrow_price = chain_prices.get("borrow")
    magister_price = chain_prices.get("magister")

    eco_count = chain_counts.get("eco", 0)
    liq_count = chain_counts.get("liq", 0)
    dex_count = chain_counts.get("dex", 0)
    borrow_count = chain_counts.get("borrow", 0)
    magister_count = chain_counts.get("magister", 0)

    eco_discount = nfts.discount.get("eco", {})
    liq_discount = nfts.discount.get("liq", {})
    dex_discount = nfts.discount.get("dex", {})
    borrow_discount = nfts.discount.get("borrow", {})
    magister_discount = nfts.discount.get("magister", {})

    eco_discount_text = "\n".join([f"> {discount}% discount on {token}" for token, discount in eco_discount.items()])
    liq_discount_text = "\n".join([f"> {discount}% discount on {token}" for token, discount in liq_discount.items()])
    dex_discount_text = "\n".join([f"> {discount}" for discount in dex_discount])
    borrow_discount_text = "\n".join([f"> {discount}" for discount in borrow_discount])
    magister_discount_text = "\n".join([f"> {discount}% discount on {token}" for token, discount in magister_discount.items()])

    await update.message.reply_photo(
    photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
    caption=f"*NFT Info ({chain.upper()})*\nUse `/nft [chain-name]` for other chains\n\n"
         f"*Ecosystem Maxi*\n{eco_price}\n"
         f"Available - {500 - eco_count}\n"
         f"{eco_discount_text}\n\n"
         f"*Liquidity Maxi*\n{liq_price}\n"
         f"Available - {250 - liq_count}\n"
         f"{liq_discount_text}\n\n"
         f"*Dex Maxi*\n{dex_price}\n"
         f"Available - {150 - dex_count}\n"
         f"{dex_discount_text}\n\n"
         f"*Borrow Maxi*\n{borrow_price}\n"
         f"Available - {100 - borrow_count}\n"
         f"{borrow_discount_text}\n\n"
         f"*Magister*\n{magister_price}\n"
         f"Available - {49 - magister_count}\n"
         f"{magister_discount_text}\n",
    parse_mode="Markdown",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Mint Here",
                        url=f'https://x7.finance/x/nft/mint',
                    )
                ],
            ]
        ),
    )


async def on_chain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.utcnow()
    tx = api.get_tx(ca.deployer, "eth")
    tx_filter = [d for d in tx["result"] if d["to"] in str(ca.dead).lower()]
    message = bytes.fromhex(tx_filter[0]["input"][2:]).decode("utf-8")
    time = datetime.utcfromtimestamp(int(tx_filter[0]["timeStamp"]))
    duration = now - time
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    await update.message.reply_text(
        f"*Last On Chain Message:*\n\n{time} (UTC)\n"
        f"{int(days[0])} days, {int(hours[0])} hours and {int(minutes[0])} minutes ago\n\n"
        f"`{message}`",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="View on chain",
                        url=f'{url.ether_tx}{tx_filter[0]["hash"]}',
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="View all on chains", url=f"{url.dashboard}docs/onchains"
                    )
                ],
            ]
        ),
    )


async def opensea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_url = ""
    chain_name = ""
    if chain == "" or chain == "eth":
        chain_name = "(ETH)"
        chain_url = ""
    if chain == "arb" or chain == "arbitrum":
        chain_name = "(ARB)"
        chain_url = "-arbitrum"
    if chain == "optimism" or chain == "opti":
        chain_name = "(OPTI)"
        chain_url = "-optimism"
    if chain == "bnb" or chain == "bsc" or chain == "binance":
        chain_name = "(BSC)"
        chain_url = "-binance"
    if chain == "poly" or chain == "polygon":
        chain_name = "(POLYGON)"
        chain_url = "-polygon"
    await update.message.reply_photo(
        photo=open(media.opensea_logo, "rb"),
        caption=f"*X7 Finance Opensea Links {chain_name}*\nUse `/nft [chain-name]` "
        f"for other chains\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Ecosystem Maxi", url=f"{url.os_eco}{chain_url}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Liquidity Maxi", url=f"{url.os_liq}{chain_url}"
                    )
                ],
                [   InlineKeyboardButton(
                        text="DEX Maxi", url=f"{url.os_dex}{chain_url}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Borrowing Maxi", url=f"{url.os_borrow}{chain_url}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Magister", url=f"{url.os_magister}{chain_url}"
                    )
                ],
            ]
        ),
    )


async def pair(update: Update, context: CallbackContext):
    networks = {
        "ETH": f"https://eth-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_ETH')}",
        "ARB": f"https://arb-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_ARB')}",
        "BSC": "https://bsc-dataseed.binance.org/",
        "POLY": f"https://polygon-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_POLY')}",
        "OPTI": f"https://opt-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_OPTI')}",
    }
    contract_networks = {
        "ETH": "eth",
        "ARB": "arb",
        "BSC": "bsc",
        "POLY": "poly",
        "OPTI": "opti",
    }
    contract_instances = {}
    for network, web3_url in networks.items():
        web3 = Web3(Web3.HTTPProvider(web3_url))
        contract = web3.eth.contract(
            address=to_checksum_address(ca.factory),
            abi=api.get_abi(ca.factory, contract_networks[network]),
        )
        amount = contract.functions.allPairsLength().call()
        contract_instances[network] = amount
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Pair Count*\n\n"
                f'`ETH:`       {contract_instances["ETH"]}\n'
                f'`BSC:`       {contract_instances["BSC"]}\n'
                f'`ARB:`       {contract_instances["ARB"]}\n'
                f'`POLY:`     {contract_instances["POLY"]}\n'
                f'`OPTI:`     {contract_instances["OPTI"]}\n\n'
                f"`TOTAL:`   {sum(contract_instances.values())}\n\n"
                f"{api.get_quote()}",
        parse_mode="Markdown",
    )


async def pioneer(update: Update, context: ContextTypes.DEFAULT_TYPE = None):
    pioneer_id = " ".join(context.args)
    data = api.get_os_nft("/x7-pioneer")
    floor = api.get_nft_floor(ca.pioneer, "?chain=eth-main")
    floor_dollar = floor * float(api.get_native_price("eth")) / 1**18
    traits = data["collection"]["traits"]["Transfer Lock Status"]["unlocked"]
    cap = round(data["collection"]["stats"]["market_cap"], 2)
    cap_dollar = cap * float(api.get_native_price("eth")) / 1**18
    sales = data["collection"]["stats"]["total_sales"]
    owners = data["collection"]["stats"]["num_owners"]
    price = round(data["collection"]["stats"]["average_price"], 2)
    price_dollar = price * float(api.get_native_price("eth")) / 1**18
    volume = round(data["collection"]["stats"]["total_volume"], 2)
    volume_dollar = volume * float(api.get_native_price("eth")) / 1**18
    pioneer_pool = api.get_native_balance(ca.pioneer, "eth")
    total_dollar = float(pioneer_pool) * float(api.get_native_price("eth")) / 1**18
    if pioneer_id == "":
        img = Image.open(random.choice(media.blackhole))
        i1 = ImageDraw.Draw(img)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 28)
        i1.text(
            (28, 36),
            f"X7 Pioneer NFT Info\n\n"
            f"LooksRare Floor Price: {floor} ETH (${'{:0,.0f}'.format(floor_dollar)})\n"
            f"Average Price: {price} ETH (${'{:0,.0f}'.format(price_dollar)})\n"
            f"Market Cap: {cap} ETH (${'{:0,.0f}'.format(cap_dollar)})\n"
            f"Total Volume: {volume} ETH (${'{:0,.0f}'.format(volume_dollar)})\n"
            f"Total Sales: {sales}\n"
            f"Number of Owners: {owners}\n"
            f"Pioneers Unlocked: {traits}\n\n\n"
            f"Pioneer Pool: {pioneer_pool[:3]} ETH (${'{:0,.0f}'.format(total_dollar)})\n\n"
            f"UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}",
            font=myfont,
            fill=(255, 255, 255),
        )
        img.save(r"media/blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f"*X7 Pioneer NFT Info*\n\n"
            f"LooksRare Floor Price: {floor} ETH (${'{:0,.0f}'.format(floor_dollar)})\n"
            f"Average Price: {price} ETH (${'{:0,.0f}'.format(price_dollar)})\n"
            f"Market Cap: {cap} ETH (${'{:0,.0f}'.format(cap_dollar)})\n"
            f"Total Volume: {volume} ETH (${'{:0,.0f}'.format(volume_dollar)})\n"
            f"Number of Owners: {owners}\n"
            f"Pioneers Unlocked: {traits}\n\n"
            f"Pioneer Pool: {pioneer_pool[:3]} ETH (${'{:0,.0f}'.format(total_dollar)})\n\n"
            f"{api.get_quote()}",
            parse_mode="markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="X7 Pioneer Dashboard",
                            url="https://x7.finance/x/nft/pioneer",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="LooksRare",
                            url=f"{url.lr_pioneer}"
                            "?filters=%7B%22attributes"
                            f"%22%3A%5B%7B%22traitType%22%3A%22Transfer+Lock+Status%22%2C%22values"
                            f"%22%3A%5B%22Unlocked%22%5D%7D%5D%7D",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Blur.io",
                            url=f"{url.blur_pioneer}"
                            "?traits=%7B%22Transfer%20Lock%20Status%22%3A%5B%22Unlocked%22%5D%7D",
                        )
                    ],
                ]
            ),
        )
    else:
        base_url = "https://api.opensea.io/api/v1/asset/"
        slug = ca.pioneer + "/"
        headers = {"X-API-KEY": os.getenv("OPENSEA_API_KEY")}
        single_url = base_url + slug + pioneer_id + "/"
        single_response = requests.get(single_url, headers=headers)
        single_data = single_response.json()
        status = single_data["traits"][0]["value"]
        await update.message.reply_text(
            f"*X7 Pioneer {pioneer_id} NFT Info*\n\n"
            f"Transfer Lock Status: {status}\n\n"
            f"{url.lr_pioneer}/{pioneer_id}\n\n"
            f"{api.get_quote()}",
            parse_mode="markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="X7 Pioneer Dashboard",
                            url="https://x7.finance/x/nft/pioneer",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="LooksRare",
                            url=f"https://looksrare.org/collections/{ca.pioneer}/{pioneer_id}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Blur.io",
                            url=f"https://blur.io/asset/{ca.pioneer}/{pioneer_id}",
                        )
                    ],
                ]
            ),
        )


async def pool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    eth_lpool_reserve = api.get_native_balance(ca.lpool_reserve, "eth")
    eth_lpool_reserve_dollar = (
        float(eth_lpool_reserve) * float(api.get_native_price("eth")) / 1**18
    )
    eth_lpool = api.get_native_balance(ca.lpool, "eth")
    eth_lpool_dollar = float(eth_lpool) * float(api.get_native_price("eth")) / 1**18
    eth_pool = round(float(eth_lpool_reserve) + float(eth_lpool), 2)
    eth_dollar = eth_lpool_reserve_dollar + eth_lpool_dollar
    bsc_lpool_reserve = api.get_native_balance(ca.lpool_reserve, "bsc")
    bsc_lpool_reserve_dollar = (
        float(bsc_lpool_reserve) * float(api.get_native_price("bnb")) / 1**18
    )
    bsc_lpool = api.get_native_balance(ca.lpool, "bsc")
    bsc_lpool_dollar = float(bsc_lpool) * float(api.get_native_price("bnb")) / 1**18
    bsc_pool = round(float(bsc_lpool_reserve) + float(bsc_lpool), 2)
    bsc_dollar = bsc_lpool_reserve_dollar + bsc_lpool_dollar
    poly_lpool_reserve = api.get_native_balance(ca.lpool_reserve, "poly")
    poly_lpool_reserve_dollar = (
        float(poly_lpool_reserve) * float(api.get_native_price("matic")) / 1**18
    )
    poly_lpool = api.get_native_balance(ca.lpool, "poly")
    poly_lpool_dollar = (
        float(poly_lpool) * float(api.get_native_price("matic")) / 1**18
    )
    poly_pool = round(float(poly_lpool_reserve) + float(poly_lpool), 2)
    poly_dollar = poly_lpool_reserve_dollar + poly_lpool_dollar
    arb_lpool_reserve = api.get_native_balance(ca.lpool_reserve, "arb")
    arb_lpool_reserve_dollar = (
        float(arb_lpool_reserve) * float(api.get_native_price("eth")) / 1**18
    )
    arb_lpool = api.get_native_balance(ca.lpool, "arb")
    arb_lpool_dollar = float(arb_lpool) * float(api.get_native_price("eth")) / 1**18
    arb_pool = round(float(arb_lpool_reserve) + float(arb_lpool), 2)
    arb_dollar = arb_lpool_reserve_dollar + arb_lpool_dollar
    opti_lpool_reserve = api.get_native_balance(ca.lpool_reserve, "opti")
    opti_lpool_reserve_dollar = (
        float(opti_lpool_reserve) * float(api.get_native_price("eth")) / 1**18
    )
    opti_lpool = api.get_native_balance(ca.lpool, "opti")
    opti_lpool_dollar = float(opti_lpool) * float(api.get_native_price("eth")) / 1**18
    opti_pool = round(float(opti_lpool_reserve) + float(opti_lpool), 2)
    opti_dollar = opti_lpool_reserve_dollar + opti_lpool_dollar
    total_dollar = poly_dollar + bsc_dollar + opti_dollar + arb_dollar + eth_dollar
    if chain == "":
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7d_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 28)
        i1.text(
            (28, 36),
            f"X7 Finance Lending Pool Info\n\n"
            f'ETH:   {eth_pool} ETH (${"{:0,.0f}".format(eth_dollar)})\n'
            f'ARB:   {arb_pool} ETH (${"{:0,.0f}".format(arb_dollar)})\n'
            f'OPTI: {opti_pool} ETH (${"{:0,.0f}".format(opti_dollar)})\n'
            f'BSC:   {bsc_pool} BNB (${"{:0,.0f}".format(bsc_dollar)})\n'
            f'POLY:  {poly_pool} MATIC (${"{:0,.0f}".format(poly_dollar)})\n\n'
            f'TOTAL: ${"{:0,.0f}".format(total_dollar)}\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f"*X7 Finance Lending Pool Info *\nUse `/pool [chain-name]` for individual chains\n\n"
            f'`ETH:`   {eth_pool} ETH (${"{:0,.0f}".format(eth_dollar)})\n'
            f'`ARB:`   {arb_pool} ETH (${"{:0,.0f}".format(arb_dollar)})\n'
            f'`OPTI:` {opti_pool} ETH (${"{:0,.0f}".format(opti_dollar)})\n'
            f'`BSC:`   {bsc_pool} BNB (${"{:0,.0f}".format(bsc_dollar)})\n'
            f'`POLY:`  {poly_pool} MATIC (${"{:0,.0f}".format(poly_dollar)})\n\n'
            f'TOTAL: ${"{:0,.0f}".format(total_dollar)}\n\n'
            f"{api.get_quote()}",
            parse_mode="Markdown",
        )
        return
    if chain == "eth":
        chain_name = "(ETH)"
        chain_token = "ETH"
        pool = eth_pool[:4]
        chain_url = url.ether_address
        pool_dollar = float(pool) * float(api.get_native_price("eth")) / 1**18
        im2 = Image.open(media.eth_logo)
    if chain == "bsc" or chain == "bnb":
        chain_name = "(BSC)"
        chain_token = "BNB"
        pool = bsc_pool
        chain_url = url.bsc_address
        pool_dollar = float(pool) * float(api.get_native_price("bnb")) / 1**18
        im2 = Image.open(media.bsc_logo)
    if chain == "arbitrum" or chain == "arb":
        chain_name = "(ARB)"
        chain_token = "ETH"
        pool = arb_pool
        chain_url = url.arb_address
        pool_dollar = float(pool) * float(api.get_native_price("eth")) / 1**18
        im2 = Image.open(media.arb_logo)
    if chain == "optimism" or chain == "opti":
        chain_name = "(OPTI)"
        chain_token = "ETH"
        pool = opti_pool
        chain_url = url.opti_address
        pool_dollar = float(pool) * float(api.get_native_price("eth")) / 1**18
        im2 = Image.open(media.opti_logo)
    if chain == "polygon" or chain == "poly":
        chain_name = "(POLYGON)"
        chain_token = "MATIC"
        pool = poly_pool
        chain_url = url.poly_address
        pool_dollar = float(pool) * float(api.get_native_price("matic")) / 1**18
        im2 = Image.open(media.poly_logo)
    im1 = Image.open((random.choice(media.blackhole)))
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 28)
    i1.text(
        (28, 36),
        f"X7 Finance Lending Pool Info {chain_name}\n\n"
        f'{pool} {chain_token} (${"{:0,.0f}".format(pool_dollar)})\n\n\n\n\n\n\n\n\n\n'
        f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font=myfont,
        fill=(255, 255, 255),
    )
    img_path = os.path.join("media", "blackhole.png")
    im1.save(img_path)
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=f"*X7 Finance Lending Pool Info {chain_name}*\nUse `/pool [chain-name]` for other chains\n\n"
        f'{pool} {chain_token} (${"{:0,.0f}".format(pool_dollar)})\n\n'
        f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Lending Pool Contract",
                        url=f"{chain_url}{ca.lpool}",
                    )
                ],
            ]
        ),
    )


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    search = " ".join(context.args).lower()
    token_info = None
    for token_instance in all_tokens_info:
        if token_instance.name.lower() == search:
            token_info = token_instance
            break

    if not token_info:
        token = api.get_cg_search(search)
        token_id = token["coins"][0]["api_symbol"]
        symbol = token["coins"][0]["symbol"]
        thumb = token["coins"][0]["large"]
        price = api.get_cg_price("x7r, x7dao")
        x7r_change = price["x7r"]["usd_24h_change"]
        if x7r_change is None:
            x7r_change = 0
        x7dao_change = price["x7dao"]["usd_24h_change"]
        if x7dao_change is None:
            x7dao_change = 0
        token_price = api.get_cg_price(token_id)
        if search == "":
            im1 = Image.open((random.choice(media.blackhole)))
            im2 = Image.open(r"media/logo11.png")
            im1.paste(im2, (740, 20), im2)
            i1 = ImageDraw.Draw(im1)
            myfont = ImageFont.truetype(R"media/FreeMonoBold.ttf", 28)
            i1.text(
                (28, 36),
                f"X7 Finance Token Price Info (ETH)\n\n"
                f'X7R:    ${price["x7r"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7r"]["usd_24h_change"], 1)}%\n\n'
                f'X7DAO:  ${price["x7dao"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7dao"]["usd_24h_change"], 0)}%\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont,
                fill=(255, 255, 255),
            )
            img_path = os.path.join("media", "blackhole.png")
            im1.save(img_path)
            await update.message.reply_photo(
                photo=open(r"media/blackhole.png", "rb"),
                caption=f"*X7 Finance Token Price Info (ETH)*\n"
                f"Use `/x7r [chain]` or `/x7dao [chain]` for all other details\n"
                f"Use `/constellations` for constellations\n\n"
                f'X7R:    ${price["x7r"]["usd"]}\n'
                f'24 Hour Change: {round(x7r_change, 1)}%\n\n'
                f'X7DAO:  ${price["x7dao"]["usd"]}\n'
                f'24 Hour Change: {round(x7dao_change, 0)}%\n\n'
                f"{api.get_quote()}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="X7R Chart - Rewards Token",
                                url=f"{url.dex_tools_eth}{ca.x7r_pair_eth}",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text="X7DAO Chart - Governance Token",
                                url=f"{url.dex_tools_eth}{ca.x7dao_pair_eth}",
                            )
                        ],
                    ]
                ),
            )
            return
        if (
            search == "eth"
            or search == "bnb"
            or search == "matic"
            or search == "poly"
            or search == "polygon"
        ):
            if search == "eth":
                cg_name = "ethereum"
                price = api.get_cg_price("ethereum")
                gas_data = api.get_gas("eth")
                im2 = Image.open(requests.get(thumb, stream=True).raw)
            if search == "bnb":
                cg_name = "binancecoin"
                price = api.get_cg_price("binancecoin")
                gas_data = api.get_gas("bsc")
                im2 = Image.open(requests.get(thumb, stream=True).raw)
            if search == "matic" or search == "poly" or search == "polygon":
                cg_name = "matic-network"
                price = api.get_cg_price("matic-network")
                gas_data = api.get_gas("poly")
                im2 = Image.open(requests.get(thumb, stream=True).raw)
            price_change = token_price[cg_name]["usd_24h_change"]
            if price_change is None:
                price_change = 0
            im1 = Image.open((random.choice(media.blackhole)))
            im1.paste(im2, (680, 20), im2)
            i1 = ImageDraw.Draw(im1)
            myfont = ImageFont.truetype(R"media/FreeMonoBold.ttf", 28)
            i1.text(
                (28, 36),
                f"{symbol} price\n\n"
                f'Price: ${price[cg_name]["usd"]}\n'
                f'24 Hour Change: {round(price_change, 1)}%\n\n'
                f"Gas Prices:\n"
                f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n'
                f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n'
                f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont,
                fill=(255, 255, 255),
            )
            img_path = os.path.join("media", "blackhole.png")
            im1.save(img_path)
            await update.message.reply_photo(
                photo=open(r"media/blackhole.png", "rb"),
                caption=f"*{symbol} price*\n\n"
                f'Price: ${price[cg_name]["usd"]}\n'
                f'24 Hour Change: {round(price[cg_name]["usd_24h_change"], 1)}%\n\n'
                f"Gas Prices:\n"
                f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n'
                f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n'
                f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n'
                f"{api.get_quote()}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(text="Chart",
                                              url=f"https://www.coingecko.com/en/coins/{cg_name}",
                                            )
                        ],
                        [InlineKeyboardButton(text="Buy", 
                                              url=f"{url.xchange}/#/swap?outputCurrency={token_id}"
                                            )
                        ],
                        [InlineKeyboardButton(text="List a token", 
                                              url=f"https://github.com/x7finance/telegram-bot/blob/main/tokens/README.md"
                                            )
                        ]
                    ]
                ),
            )
            return
        else:
            price_change = token_price[token_id]["usd_24h_change"]
            if price_change is None:
                price_change = 0
            img = Image.open(requests.get(thumb, stream=True).raw)
            result = img.convert("RGBA")
            result.save(r"media/cgtokenlogo.png")
            im1 = Image.open((random.choice(media.blackhole)))
            im2 = Image.open(r"media/cgtokenlogo.png")
            im1.paste(im2, (680, 20), im2)
            myfont = ImageFont.truetype(R"media/FreeMonoBold.ttf", 28)
            i1 = ImageDraw.Draw(im1)
            i1.text(
                (28, 36),
                f"{symbol} price\n\n"
                f'Price: ${"{:.8f}".format(token_price[token_id]["usd"])}\n'
                f'24 Hour Change: {round(price_change, 1)}%\n'
                f'Market Cap: ${"{:0,.0f}".format(token_price[token_id]["usd_market_cap"])}\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont,
                fill=(255, 255, 255),
            )
            im1.save(r"media/blackhole.png", quality=95)
            await update.message.reply_photo(
                photo=open(r"media/blackhole.png", "rb"),
                caption=f"*{symbol} price*\n\n"
                f'Price: ${"{:.8f}".format(token_price[token_id]["usd"])}\n'
                f'24 Hour Change: {round(token_price[token_id]["usd_24h_change"], 1)}%\n'
                f'Market Cap: ${"{:0,.0f}".format(token_price[token_id]["usd_market_cap"])}\n\n'
                f"{api.get_quote()}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(text="Chart",
                                              url=f"https://www.coingecko.com/en/coins/{token_id}",
                                            )
                        ],
                        [InlineKeyboardButton(text="Buy", url=f"{url.xchange}/#/swap?outputCurrency={token_id}"
                                            )
                        ],
                        [InlineKeyboardButton(text="List a token", 
                                              url=f"https://github.com/x7finance/telegram-bot/blob/main/tokens/README.md")
                        ]
                    ]
                ),
            )
    else:
        if token_info.chain == "eth":
            holders = api.get_holders(token_info.ca)
        else:
            holders = "N/A"
        scan = chains[token_info.chain].scan
        dext = chains[token_info.chain].dext
        w3 = chains[token_info.chain].w3
        contract = w3.eth.contract(address=Web3.to_checksum_address(token_info.pair), abi=pairs)
        token0_address = contract.functions.token0().call()
        token1_address = contract.functions.token1().call()
        supply = contract.functions.totalSupply().call()
        is_reserve_token0 = token_info.ca.lower() == token0_address.lower()
        is_reserve_token1 = token_info.ca.lower() == token1_address.lower()
        supply = int(api.get_supply(token_info.ca, token_info.chain))
        eth = ""
        token_res = ""
        if is_reserve_token0:
            eth = contract.functions.getReserves().call()[1]
            token_res = contract.functions.getReserves().call()[0]
        elif is_reserve_token1:
            eth = contract.functions.getReserves().call()[0]
            token_res = contract.functions.getReserves().call()[1]
        liq = int(eth) * api.get_native_price(token_info.chain) * 2
        formatted_liq = "${:,.2f}".format(liq / (10 ** 18))
        if token_info.decimals < 18:
            token_price = liq / supply / (10 ** token_info.decimals)
        else:
            token_price = liq / supply
        formatted_token_price = "${:.8f}".format(token_price)
        mcap = token_price * supply
        formatted_mcap = "${:,.0f}".format(mcap / (10 ** token_info.decimals))
        im1 = Image.open((random.choice(media.blackhole)))
        try:
            img = Image.open(requests.get(token_info.logo, stream=True).raw)
            result = img.convert("RGBA")
            result.save(r"media/tokenlogo.png")
            im2 = Image.open(r"media/tokenlogo.png")
        except Exception:
            if token_info.chain == "eth":
                im2 = Image.open(media.eth_logo)
            if token_info.chain == "bsc":
                im2 = Image.open(media.bsc_logo)
            if token_info.chain == "poly":
                im2 = Image.open(media.poly_logo)
            if token_info.chain == "arb":
                im2 = Image.open(media.arb_logo)
            if token_info.chain == "opti":
                im2 = Image.open(media.opti_logo)

        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (26, 30),
            f'Xchange Pair Info\n\n{search.upper()}\n\n'
            f"Liquidity: {formatted_liq}\n"
            f"Market Cap: {formatted_mcap}\n"
            f"Token Price: {formatted_token_price}\n"
            f"Holders: {holders}\n\n\n\n\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f'*Xchange Pair Info\n\n{search.upper()}*\n\n'
                    f'`{token_info.ca}`\n\n'
                    f"Liquidity: {formatted_liq}\n"
                    f"Market Cap: {formatted_mcap}\n"
                    f"Token Price: {formatted_token_price}\n"
                    f"Holders: {holders}\n\n"
            f"{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="Chart", url=f"{dext}{token_info.pair}")],
                [InlineKeyboardButton(text="Buy", url=f"{url.xchange}/#/swap?outputCurrency={token_info.ca}")],
            ]),
        )
    

async def proposal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"{text.proposals}\n\n{api.get_quote()}",
        parse_mode="Markdown",
    )


async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"{text.refer}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Application",
                        url=f"{url.referral}",
                    )
                ],
            ]
        ),
    )


async def roadmap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    def draw_progress_bar(d, x, y, w, h, progress, bg="black", fg="white"):
        im1.ellipse((x + w, y, x + h + w, y + h), fill=bg)
        im1.ellipse((x, y, x + h, y + h), fill=bg)
        im1.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=bg)
        w *= progress
        im1.ellipse((x + w, y, x + h + w, y + h), fill=fg)
        im1.ellipse((x, y, x + h, y + h), fill=fg)
        im1.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=fg)
        return im1

    out = Image.open((random.choice(media.blackhole)))
    im1 = ImageDraw.Draw(out)
    myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
    ws1_1 = draw_progress_bar(im1, 80, 80, 200, 25, text.ws1_1)
    ws1_2 = draw_progress_bar(im1, 80, 180, 200, 25, text.ws1_2)
    ws2 = draw_progress_bar(im1, 80, 280, 200, 25, text.ws2)
    ws3 = draw_progress_bar(im1, 80, 380, 200, 25, text.ws3)
    ws4 = draw_progress_bar(im1, 80, 480, 200, 25, text.ws4)
    ws5 = draw_progress_bar(im1, 480, 80, 200, 25, text.ws5)
    ws6 = draw_progress_bar(im1, 480, 180, 200, 25, text.ws6)
    ws7 = draw_progress_bar(im1, 480, 280, 200, 25, text.ws7)
    ws8 = draw_progress_bar(im1, 480, 380, 200, 25, text.ws8)
    ws9 = draw_progress_bar(im1, 480, 480, 200, 25, text.ws9)
    im1.text(
        (80, 36),
        f"WS 1.1 - {text.ws1_1 * 100}% \n\n\n"
        f"WS 1.2 - {text.ws1_2 * 100}% \n\n\n"
        f"WS 2 - {text.ws2 * 100}% \n\n\n"
        f"WS 3 - {text.ws3 * 100}% \n\n\n"
        f"WS 4 - {text.ws4 * 100}% \n\n\n",
        font=myfont,
        fill=(255, 255, 255),
    )
    im1.text(
        (480, 36),
        f"WS 5 - {text.ws5 * 100}% \n\n\n"
        f"WS 6 - {text.ws6 * 100}%\n\n\n"
        f"WS 7 - {text.ws7 * 100}%\n\n\n"
        f"WS 8 - {text.ws8 * 100}%\n\n\n"
        f"WS 9 - {text.ws9 * 100}%\n\n\n",
        font=myfont,
        fill=(255, 255, 255),
    )
    out.save(r"media/blackhole.png")
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=f"*X7 Finance Work Stream Status*\n\n"
        f'WS1.1: Omni routing (multi dex routing "library" code) - {text.ws1_1*100}% \n\n'
        f'WS1.2: Omni routing (multi dex routing "select" code) - {text.ws1_2*100}% \n\n'
        f"WS2: Omni routing (UI) - {text.ws2*100}% \n\n"
        f"WS3: Borrowing UI - {text.ws3*100}% \n\n"
        f"WS4: Lending and Liquidation UI - {text.ws4*100}% \n\n"
        f"WS5: DAO smart contracts - {text.ws5*100}% \n\n"
        f"WS6: X7 DAO UI - {text.ws6*100}%\n\n"
        f'WS7: Marketing "Pitch Deck" - {text.ws7*100}%\n\n'
        f"WS8: Decentralization in hosting - {text.ws8*100}%\n\n"
        f"WS9: Developer Tools and Example Smart Contracts - {text.ws9*100}%\n\n{api.get_quote()}",
        parse_mode="Markdown",
    )


async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"{api.get_quote()}",
        parse_mode="Markdown",
    )


async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Routers*\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="ETH", url=f"{url.ether_address}{ca.router}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="BSC", url=f"{url.bsc_address}{ca.router}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Polygon", url=f"{url.poly_address}{ca.router}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Arbitrum", url=f"{url.arb_address}{ca.router}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Optimism", url=f"{url.opti_address}{ca.router}"
                    )
                ],
            ]
        ),
    )


async def say(update: Update, context: ContextTypes.DEFAULT_TYPE):
    engine = pyttsx3.init()
    engine.save_to_file(" ".join(context.args), "media/voicenote.mp3")
    engine.runAndWait()
    await update.message.reply_audio(audio=open("media/voicenote.mp3", "rb"))


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wiki = wikipediaapi.Wikipedia("en")
    keyword = " ".join(context.args)
    page_py = wiki.page(keyword)
    if keyword == "":
        await update.message.reply_photo(
            photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
            caption="Please follow the command with your search",
        )
    if page_py.exists():
        await update.message.reply_photo(
            photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
            caption=f"Your search: {page_py.title}\n\n"
            f"{(page_py.summary[0:800])}"
            f"....[continue reading on wiki]({page_py.fullurl})\n\n"
            f"[Google](https://www.google.com/search?q={keyword})\n"
            f"[Twitter](https://twitter.com/search?q={keyword}&src=typed_query)\n"
            f"[Etherscan](https://etherscan.io/search?f=0&q={keyword})\n\n"
            f"{api.get_quote()}",
            parse_mode="markdown",
        )
    else:
        await update.message.reply_photo(
            photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
            caption=f"Your search: {keyword}\n\nNo description available\n\n"
            f"[Google](https://www.google.com/search?q={keyword})\n"
            f"[Twitter](https://twitter.com/search?q={keyword}&src=typed_query)\n"
            f"[Etherscan](https://etherscan.io/search?f=0&q={keyword})\n\n"
            f"{api.get_quote()}",
            parse_mode="markdown",
        )


async def signers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_name = ""
    chain_url = ""
    dev_response = None
    com_response = None
    if chain in ["eth", ""]:
        chain = "eth"
        dev_response = api.get_signers(ca.dev_multi_eth)
        com_response = api.get_signers(ca.com_multi_eth)
        chain_name = "(ETH)"
        chain_url = url.ether_address
    elif chain in ["poly", "polygon"]:
        chain = "polygon"
        dev_response = api.get_signers(ca.dev_multi_poly)
        com_response = api.get_signers(ca.com_multi_poly)
        chain_name = "(POLYGON)"
        chain_url = url.poly_address
    elif chain in ["bsc", "bnb"]:
        chain = "bsc"
        dev_response = api.get_signers(ca.dev_multi_bsc)
        com_response = api.get_signers(ca.com_multi_bsc)
        chain_name = "(BSC)"
        chain_url = url.poly_address
    elif chain in ["arb", "arbitrum"]:
        chain = "arbitrum"
        dev_response = api.get_signers(ca.dev_multi_arb)
        com_response = api.get_signers(ca.com_multi_arb)
        chain_name = "(ARB)"
        chain_url = url.arb_address
    elif chain in ["opti", "optimism"]:
        chain = "optimism"
        dev_response = api.get_signers(ca.dev_multi_opti)
        com_response = api.get_signers(ca.com_multi_opti)
        chain_name = "(OPTIMISM)"
        chain_url = url.opti_address
    else:
        await update.message.reply_text("Invalid chain. Please specify a valid chain.")
        return
    dev_list = dev_response["owners"]
    dev_address = "\n\n".join(map(str, dev_list))
    com_list = com_response["owners"]
    com_address = "\n\n".join(map(str, com_list))
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Multi-Sig Signers {chain_name}*\n"
        f"Use `/signers [chain-name]` or other chains\n\n"
        f"*Developer Signers*\n`{dev_address}`\n\n*Community Signers*\n`{com_address}`\n\n"
        f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7 Developer Multi-Sig",
                        url=f"{chain_url}{ca.dev_multi_eth}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 Community Multi-Sig",
                        url=f"{chain_url}{ca.com_multi_eth}",
                    )
                ],
            ]
        ),
    )


async def smart(update: Update, context: ContextTypes.DEFAULT_TYPE = None):
    if context is None:
        context = ContextTypes.DEFAULT_TYPE()
    chain = " ".join(context.args).lower()
    chain_name = ""
    chain_url = ""
    chain_mappings = {
        "eth": ("(ETH)", url.ether_address),
        "arbitrum": ("(ARB)", url.arb_address),
        "arb": ("(ARB)", url.arb_address),
        "poly": ("(POLYGON)", url.poly_address),
        "polygon": ("(POLYGON)", url.poly_address),
        "bsc": ("(BSC)", url.bsc_address),
        "bnb": ("(BSC)", url.bsc_address),
        "op": ("(OP)", url.opti_address),
        "optimism": ("(OP)", url.opti_address),
        "opti": ("(OP)", url.opti_address),
    }
    if chain in chain_mappings:
        chain_name, chain_url = chain_mappings[chain]
    else:
        chain_name, chain_url = chain_mappings["eth"]
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Smart Contracts {chain_name}*\nUse `/smart [chain-name]` or other chains\n\n"
        f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Contracts Directory - by MikeMurpher",
                        url=f"{url.ca_directory}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7100 Liquidity Hub", url=f"{chain_url}{ca.x7100_liq_hub}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7R Liquidity Hub", url=f"{chain_url}{ca.x7r_liq_hub}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7DAO Liquidity Hub", url=f"{chain_url}{ca.x7dao_liq_hub}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 Token Burner", url=f"{chain_url}{ca.burner}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7100 Discount Authority",
                        url=f"{chain_url}{ca.x7100_discount}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7R Discount Authority",
                        url=f"{chain_url}{ca.x7r_discount}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7DAO Discount Authority",
                        url=f"{chain_url}{ca.x7dao_discount}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 Token Time Lock", url=f"{chain_url}{ca.time_lock}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 Ecosystem Splitter",
                        url=f"{chain_url}{ca.eco_splitter}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 Treasury Splitter",
                        url=f"{chain_url}{ca.treasury_splitter}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 Lending Pool Reserve",
                        url=f"{chain_url}{ca.lpool_reserve}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 Xchange Discount Authority",
                        url=f"{chain_url}{ca.xchange_discount}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 Lending Discount Authority",
                        url=f"{chain_url}{ca.lending_discount}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 Xchange Router", url=f"{chain_url}{ca.router}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 Xchange Router with Discounts",
                        url=f"{chain_url}{ca.discount_router}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 Lending Pool Contract", url=f"{chain_url}{ca.lpool}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 Xchange Factory", url=f"{chain_url}{ca.factory}"
                    )
                ],
            ]
        ),
    )


async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    snapshot = api.get_snapshot()
    end = datetime.utcfromtimestamp(snapshot["data"]["proposals"][0]["end"]).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    start = datetime.utcfromtimestamp(
        snapshot["data"]["proposals"][0]["start"]
    ).strftime("%Y-%m-%d %H:%M:%S")
    then = datetime.utcfromtimestamp(snapshot["data"]["proposals"][0]["end"])
    now = datetime.utcnow()
    duration = then - now
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    if duration < timedelta(0):
        countdown = "Vote Closed"
        caption = "View"
        print(days, hours, minutes)
    else:
        countdown = f"Vote Closing in: {int(days[0])} days, {int(hours[0])} hours and {int(minutes[0])} minutes"
        caption = "Vote"
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f"*X7 Finance Community Snapshot*\n\n"
        f"Latest Proposal:\n\n"
        f'{snapshot["data"]["proposals"][0]["title"]} by - '
        f'{snapshot["data"]["proposals"][0]["author"][-5:]}\n\n'
        f"Voting Start: {start} UTC\n"
        f"Voting End:   {end} UTC\n\n"
        f'{snapshot["data"]["proposals"][0]["choices"][0]} - '
        f'{"{:0,.0f}".format(snapshot["data"]["proposals"][0]["scores"][0])} DAO Votes\n'
        f'{snapshot["data"]["proposals"][0]["choices"][1]} - '
        f'{"{:0,.0f}".format(snapshot["data"]["proposals"][0]["scores"][1])} DAO Votes\n\n'
        f'{"{:0,.0f}".format(snapshot["data"]["proposals"][0]["scores_total"])} Total DAO Votes\n\n'
        f"{countdown}\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=f"{caption} Here",
                        url=f"{url.snapshot}/proposal/"
                        f'{snapshot["data"]["proposals"][0]["id"]}',
                    )
                ],
            ]
        ),
    )


async def splitters(update: Update, context):
    chain_mappings = {
        "eth": {
            "chain_name": "(ETH)",
            "link": url.ether_address,
            "native": "eth",
            "chain": "eth"
        },
        "bsc": {
            "chain_name": "(BSC)",
            "link": url.bsc_address,
            "native": "bnb",
            "chain": "bsc"
        },
        "bnb": {
            "chain_name": "(BSC)",
            "link": url.bsc_address,
            "native": "bnb",
            "chain": "bsc"
        },
        "polygon": {
            "chain_name": "(POLYGON)",
            "link": url.poly_address,
            "native": "matic",
            "chain": "poly"
        },
        "poly": {
            "chain_name": "(POLYGON)",
            "link": url.poly_address,
            "native": "matic",
            "chain": "poly"
        },
        "optimism": {
            "chain_name": "(OPTIMISM)",
            "link": url.opti_address,
            "native": "eth",
            "chain": "opti"
        },
        "opti": {
            "chain_name": "(OPTIMISM)",
            "link": url.opti_address,
            "native": "eth",
            "chain": "opti"
        },
        "arbitrum": {
            "chain_name": "(ARB)",
            "link": url.arb_address,
            "native": "eth",
            "chain": "arb"
        },
        "arb": {
            "chain_name": "(ARB)",
            "link": url.arb_address,
            "native": "eth",
            "chain": "arb"
        }
    }
    if len(context.args) > 1:
        eth_value = float(context.args[1])
        chain = context.args[0].lower()
        if chain in chain_mappings:
            mapping = chain_mappings[chain]
            chain_name = mapping["chain_name"]
            link = mapping["link"]
            native = mapping["native"]
            chain = mapping["chain"]
        else:
            await update.message.reply_text("Invalid chain. Please provide a valid chain name.")
            return
        distribution = api.get_split(eth_value)
        message = f"*X7 Finance Ecosystem Splitters {chain_name}* \n\n{eth_value} {native.upper()}\n\n"
        for location, share in distribution.items():
            if location == "Treasury":
                message += f"\n{location}: {share:.2f} {native.upper()}:\n"
            else:
                message += f"{location}: {share:.2f} {native.upper()}\n"

        await update.message.reply_photo(
            photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
            caption=f"{message}\n\n{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text="Ecosystem Splitter", url=f"{link}{ca.eco_splitter}")],
                    [InlineKeyboardButton(text="Treasury Splitter", url=f"{link}{ca.treasury_splitter}")],
                ]
            ),
        )
    elif len(context.args) == 1:
        chain = context.args[0].lower()

        if chain in chain_mappings:
            mapping = chain_mappings[chain]
            chain_name = mapping["chain_name"]
            link = mapping["link"]
            native = mapping["native"]
            chain = mapping["chain"]
            treasury_eth = api.get_native_balance(ca.treasury_splitter, chain)
            eco_eth = api.get_native_balance(ca.eco_splitter, chain)
            native_price = api.get_native_price(native)
            eco_dollar = float(eco_eth) * float(native_price)
            treasury_dollar = float(treasury_eth) * float(native_price)
            await update.message.reply_photo(
                photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
                caption=
                    f"*X7 Finance Ecosystem Splitters {chain_name}*\n\n"
                    f"Ecosystem Splitter: {eco_eth[:6]} {native.upper()} (${'{:0,.0f}'.format(eco_dollar)})\n"
                    f"Treasury Splitter: {treasury_eth[:6]} {native.upper()} (${'{:0,.0f}'.format(treasury_dollar)})\n\n"
                    f"For example of splitter allocation use\n`/splitter [chain-name] [amount]`\n\n{api.get_quote()}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(text="Ecosystem Splitter", url=f"{link}{ca.eco_splitter}")],
                        [InlineKeyboardButton(text="Treasury Splitter", url=f"{link}{ca.treasury_splitter}")],
                    ]
                ),
            )
        else:
            await update.message.reply_text("Invalid chain. Please provide a valid chain name.")
    else:
        chain = "eth"  # Assuming eth as the default chain

        if chain in chain_mappings:
            mapping = chain_mappings[chain]
            chain_name = mapping["chain_name"]
            link = mapping["link"]
            native = mapping["native"]
            chain = mapping["chain"]
            treasury_eth = api.get_native_balance(ca.treasury_splitter, chain)
            eco_eth = api.get_native_balance(ca.eco_splitter, chain)
            native_price = api.get_native_price(native)
            eco_dollar = float(eco_eth) * float(native_price)
            treasury_dollar = float(treasury_eth) * float(native_price)
            await update.message.reply_photo(
                photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
                caption=
                    f"*X7 Finance Ecosystem Splitters {chain_name}*\n\n"
                    f"Ecosystem Splitter: {eco_eth[:6]} {native.upper()} (${'{:0,.0f}'.format(eco_dollar)})\n"
                    f"Treasury Splitter: {treasury_eth[:6]} {native.upper()} (${'{:0,.0f}'.format(treasury_dollar)})\n\n"
                    f"For example of splitter allocation use\n`/splitter [chain-name] [amount]`\n\n{api.get_quote()}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(text="Ecosystem Splitter", url=f"{link}{ca.eco_splitter}")],
                        [InlineKeyboardButton(text="Treasury Splitter", url=f"{link}{ca.treasury_splitter}")],
                    ]
                ),
            )
        else:
            await update.message.reply_text("Invalid chain. Please provide a valid chain name or amount.")


async def supply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token_pairs = {
        "x7r": (ca.x7r_pair_eth, ca.x7r),
        "x7dao": (ca.x7dao_pair_eth, ca.x7dao),
        "x7101": (ca.x7101_pair_eth, ca.x7101),
        "x7102": (ca.x7102_pair_eth, ca.x7102),
        "x7103": (ca.x7103_pair_eth, ca.x7103),
        "x7104": (ca.x7104_pair_eth, ca.x7104),
        "x7105": (ca.x7105_pair_eth, ca.x7105),
    }
    prices = api.get_cg_price("x7r, x7dao, x7101, x7102, x7103, x7104, x7105")
    supply_info = {}
    for token, (pair, contract) in token_pairs.items():
        balance = api.get_token_balance(pair, contract, "eth")
        dollar_value = balance * prices[token]["usd"]
        percent = round(balance / ca.supply * 100, 2)
        supply_info[token] = {
            "balance": balance,
            "dollar_value": dollar_value,
            "percent": percent,
        }
    img = Image.open((random.choice(media.blackhole)))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("media/FreeMonoBold.ttf", 20)
    caption_lines = []
    for token, info in supply_info.items():
        balance_str = "{:0,.0f}".format(info["balance"])
        dollar_value_str = "${:0,.0f}".format(info["dollar_value"])
        percent_str = f"{info['percent']}%"
        line = f"{token.upper()}\n{balance_str} {token.upper()} ({dollar_value_str}) {percent_str}"
        caption_lines.append(line)
    caption_text = "\n\n".join(caption_lines)
    for i, line in enumerate(caption_lines):
        y_offset = 36 + i * 72
        draw.text((28, y_offset), line, font=font, fill=(255, 255, 255))
    utc_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    draw.text((28, y_offset + 72), f"UTC: {utc_time}", font=font, fill=(255, 255, 255))
    img.save("media/blackhole.png")
    await update.message.reply_photo(
        photo=open("media/blackhole.png", "rb"), caption=f"*X7 Finance Uniswap Supply*\n\n{caption_text}", parse_mode="Markdown"
    )


async def swap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_sticker(
        sticker=media.swap,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Xchange", url=f"{url.xchange}"
                    )
                ],
            ]
        ),
    )


async def tax_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    tax_info = tax.generate_info(chain)

    if not chain:
        chain = "eth"
        tax_info = tax.generate_info(chain)
    
    if tax_info:
        caption = f"{tax_info}"
    else:
        await update.message.reply_text("Invalid or missing chain. Please provide a valid chain (eth, arb, poly, bsc, opti).")
        return
    caption = f"{chain.upper()}:\n{caption}\n\n{api.get_quote()}"
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=caption,
        parse_mode="Markdown",
    )


async def time(update: Update, context: CallbackContext):
    message = update.message.text.split(" ")
    timezones = [
        ("America/Los_Angeles", "PST"),
        ("America/New_York", "EST"),
        ("UTC", "UTC"),
        ("Europe/Dublin", "IST"),
        ("Europe/London", "GMT"),
        ("Europe/Berlin", "CET"),
        ("Asia/Dubai", "GST"),
        ("Asia/Tokyo", "JST"),
        ("Australia/Sydney", "AEST"),
    ]
    current_time = datetime.now(pytz.timezone("UTC"))
    local_time = current_time.astimezone(pytz.timezone("UTC"))
    try:
        if len(message) > 1:
            time_variable = message[1]
            time_format = "%I%p"
            if re.match(r"\d{1,2}:\d{2}([ap]m)?", time_variable):
                time_format = (
                    "%I:%M%p"
                    if re.match(r"\d{1,2}:\d{2}am", time_variable, re.IGNORECASE)
                    else "%I:%M%p"
                )
            input_time = datetime.strptime(time_variable, time_format).replace(
                year=local_time.year, month=local_time.month, day=local_time.day
            )
            if len(message) > 2:
                time_zone = message[2]
                for tz, tz_name in timezones:
                    if time_zone.lower() == tz_name.lower():
                        tz_time = pytz.timezone(tz).localize(input_time)
                        time_info = f"{input_time.strftime('%A %B %d %Y')}\n"
                        time_info += f"{input_time.strftime('%I:%M %p')} - {time_zone.upper()}\n\n"
                        for tz_inner, tz_name_inner in timezones:
                            converted_time = tz_time.astimezone(pytz.timezone(tz_inner))
                            time_info += f"{converted_time.strftime('%I:%M %p')} - {tz_name_inner}\n"
                        await update.message.reply_text(
                            time_info, parse_mode="Markdown"
                        )
                        return
            time_info = f"{input_time.strftime('%A %B %d %Y')}\n"
            time_info += (
                f"{input_time.strftime('%I:%M %p')} - {time_variable.upper()}\n\n"
            )
            for tz, tz_name in timezones:
                tz_time = input_time.astimezone(pytz.timezone(tz))
                time_info += f"{tz_time.strftime('%I:%M %p')} - {tz_name}\n"
            await update.message.reply_text(time_info, parse_mode="Markdown")
            return
        time_info = f"{local_time.strftime('%A %B %d %Y')}\n"
        time_info += (
            f"{local_time.strftime('%I:%M %p')} - {local_time.strftime('%Z')}\n\n"
        )
        for tz, tz_name in timezones:
            tz_time = local_time.astimezone(pytz.timezone(tz))
            time_info += f"{tz_time.strftime('%I:%M %p')} - {tz_name}\n"
        await update.message.reply_text(time_info, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text(
            "use `/time HH:MMPM or HHAM TZ`", parse_mode="Markdown"
        )


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = api.get_today()
    today = random.choice(data["data"]["Events"])
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f'`On this day in {today["year"]}:\n\n{today["text"]}`',
        parse_mode="Markdown",
    )


async def treasury(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain in ["eth", ""]:
        im2 = Image.open(media.eth_logo)
        chain_moralis = "eth"
        chain_name = "(ETH)"
        link = url.ether_address
        native = "eth"
        chain = "eth"
        com_multi = ca.com_multi_eth
        dev_multi = ca.dev_multi_eth
    elif chain == "bsc" or chain == "bnb":
        im2 = Image.open(media.bsc_logo)
        chain_moralis = "bsc"
        chain_name = "(BSC)"
        link = url.bsc_address
        native = "bnb"
        chain = "bsc"
        com_multi = ca.com_multi_bsc
        dev_multi = ca.dev_multi_bsc
    elif chain == "polygon" or chain == "poly":
        im2 = Image.open(media.poly_logo)
        chain_moralis = "polygon"
        chain_name = "(POLYGON)"
        link = url.poly_address
        native = "matic"
        chain = "poly"
        com_multi = ca.com_multi_poly
        dev_multi = ca.dev_multi_poly
    elif chain == "optimism" or chain == "opti":
        im2 = Image.open(media.opti_logo)
        chain_moralis = "optimism"
        chain_name = "(OPTIMISM)"
        link = url.opti_address
        native = "eth"
        chain = "opti"
        com_multi = ca.com_multi_opti
        dev_multi = ca.dev_multi_opti
    elif chain == "arbitrum" or chain == "arb":
        im2 = Image.open(media.arb_logo)
        chain_moralis = "arbitrum"
        chain_name = "(ARB)"
        link = url.arb_address
        native = "eth"
        chain = "arb"
        com_multi = ca.com_multi_arb
        dev_multi = ca.dev_multi_arb
    native_price = api.get_native_price(native)
    dev_eth = api.get_native_balance(dev_multi, chain)
    com_eth = api.get_native_balance(com_multi, chain)
    dev_dollar = float(dev_eth) * float(native_price)
    com_dollar = float(com_eth) * float(native_price)
    treasury_eth = api.get_native_balance(ca.treasury_splitter, chain)
    eco_eth = api.get_native_balance(ca.eco_splitter, chain)
    eco_dollar = float(eco_eth) * float(native_price)
    treasury_dollar = float(treasury_eth) * float(native_price)
    try:
        com_x7r_balance = api.get_token_balance(com_multi, ca.x7r, chain)
        com_x7r_price = com_x7r_balance * api.get_price(ca.x7r, chain_moralis)
    except Exception:
        com_x7r_balance = 0
        com_x7r_price = 0
    try:
        com_x7dao_balance = api.get_token_balance(com_multi, ca.x7dao, chain)
        com_x7dao_price = com_x7dao_balance * api.get_price(ca.x7dao, chain_moralis)
    except Exception:
        com_x7dao_balance = 0
        com_x7dao_price = 0
    try:
        com_x7d_balance = api.get_token_balance(com_multi, ca.x7d, chain)
        com_x7d_price = com_x7d_balance * api.get_native_price(native)
    except Exception:
        com_x7d_balance = 0
        com_x7d_price = 0
    com_total = com_x7r_price + com_dollar + com_x7d_price + com_x7dao_price
    im1 = Image.open((random.choice(media.blackhole)))
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 24)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (28, 36),
        f"X7 Finance Treasury {chain_name}\n\n"
        f"Developer Wallet:\n{dev_eth[:6]} {native.upper()} (${'{:0,.0f}'.format(dev_dollar)})\n\n"
        f"Community Wallet:\n{com_eth[:6]} {native.upper()} (${'{:0,.0f}'.format(com_dollar)})\n"
        f"{com_x7d_balance} X7D (${'{:0,.0f}'.format(com_x7d_price)})\n"
        f"{com_x7r_balance} X7R (${'{:0,.0f}'.format(com_x7r_price)})\n"
        f"{com_x7dao_balance} X7DAO (${'{:0,.0f}'.format(com_x7dao_price)})\n"
        f"Total: (${'{:0,.0f}'.format(com_total)})\n\n"
        f"Ecosystem Splitter: {eco_eth[:6]} {native.upper()} (${'{:0,.0f}'.format(eco_dollar)})\n"
        f"Treasury Splitter: {treasury_eth[:6]} {native.upper()} (${'{:0,.0f}'.format(treasury_dollar)})\n\n"
        f"UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}",
        font=myfont,
        fill=(255, 255, 255),
    )

    img_path = os.path.join("media", "blackhole.png")
    im1.save(img_path)
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=f"*X7 Finance Treasury {chain_name}*\nUse `/treasury [chain-name]` for other chains\n\n"
        f'Developer Wallet:\n{dev_eth[:6]} {native.upper()} (${"{:0,.0f}".format(dev_dollar)})\n\n'
        f'Community Wallet:\n{com_eth[:6]} {native.upper()} (${"{:0,.0f}".format(com_dollar)})\n'
        f'{com_x7d_balance} X7D (${"{:0,.0f}".format(com_x7d_price)})\n'
        f'{"{:0,.0f}".format(com_x7r_balance)} X7R (${"{:0,.0f}".format(com_x7r_price)})\n'
        f'{"{:0,.0f}".format(com_x7dao_balance)} X7DAO (${"{:0,.0f}".format(com_x7dao_price)})\n'
        f'Total: (${"{:0,.0f}".format(com_total)})\n\n'
        f"Ecosystem Splitter: {eco_eth[:6]} {native.upper()} (${'{:0,.0f}'.format(eco_dollar)})\n"
        f"Treasury Splitter: {treasury_eth[:6]} {native.upper()} (${'{:0,.0f}'.format(treasury_dollar)})\n\n"
        f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Developer Multi-sig Wallet",
                        url=f"{link}{dev_multi}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Community Multi-sig Wallet",
                        url=f"{link}{com_multi}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Ecosystem Splitter Contract",
                        url=f"{link}{ca.eco_splitter}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Treasury Splitter Contract",
                        url=f"{link}{ca.treasury_splitter}",
                    )
                ],
                
            ]
        ),
    )


async def volume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    execution_id = dune.execute_query("2637346","medium")
    t.sleep(10)
    response = dune.get_query_results(execution_id)
    data = response.json()
    live_vol_value = data["result"]["rows"][0]["live_vol"]
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=f'*Xchange Total Volume*\n\n${"{:0,.0f}".format(live_vol_value)}\n\n{api.get_quote()}',
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="@Mike_X7F X7 Dune Dashboard ", url=f"{url.dune}"
                    )
                ],
            ]
        ),
    )


async def voting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"{text.voting}\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Website", url="https://x7.finance")],
                [
                    InlineKeyboardButton(
                        text="X7 Finance Whitepaper",
                        url=f"{url.wp_link}",
                    )
                ],
            ]
        ),
    )


async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) >= 2:
        chain = context.args[1].lower()
        wallet = context.args[0]
    else:
        await update.message.reply_text(
            f"Please use `/wallet wallet_address chain_name ` to see details",
            parse_mode="Markdown",
        )
        return
    if chain in ["eth", ""]:
        im2 = Image.open(media.eth_logo)
        chain_moralis = "eth"
        chain_name = "(ETH)"
        link = url.ether_address
        native = "eth"
        chain = "eth"
    elif chain == "bsc" or chain == "bnb":
        im2 = Image.open(media.bsc_logo)
        chain_moralis = "bsc"
        chain_name = "(BSC)"
        link = url.bsc_address
        native = "bnb"
        chain = "bsc"
    elif chain == "polygon" or chain == "poly":
        im2 = Image.open(media.poly_logo)
        chain_moralis = "polygon"
        chain_name = "(POLYGON)"
        link = url.poly_address
        native = "matic"
        chain = "poly"
    elif chain == "optimism" or chain == "opti":
        im2 = Image.open(media.opti_logo)
        chain_moralis = "optimism"
        chain_name = "(OPTIMISM)"
        link = url.opti_address
        native = "eth"
        chain = "opti"
    elif chain == "arbitrum" or chain == "arb":
        im2 = Image.open(media.arb_logo)
        chain_moralis = "arbitrum"
        chain_name = "(ARB)"
        link = url.arb_address
        native = "eth"
        chain = "arb"
    native_price = api.get_native_price(native)
    eth = api.get_native_balance(wallet, chain)
    dollar = float(eth) * float(native_price)
    try:
        x7r_balance = api.get_token_balance(wallet, ca.x7r, chain)
        x7r_price = x7r_balance * api.get_price(ca.x7r, chain_moralis)
    except Exception:
        x7r_balance = 0
        x7r_price = 0
    try:
        x7dao_balance = api.get_token_balance(wallet, ca.x7dao, chain)
        x7dao_price = x7dao_balance * api.get_price(ca.x7dao, chain_moralis)
    except Exception:
        x7dao_balance = 0
        x7dao_price = 0
    try:
        x7101_balance = api.get_token_balance(wallet, ca.x7101, chain)
        x7101_price = x7101_balance * api.get_price(ca.x7101, chain_moralis)
    except Exception:
        x7101_balance = 0
        x7101_price = 0
    try:
        x7102_balance = api.get_token_balance(wallet, ca.x7102, chain)
        x7102_price = x7102_balance * api.get_price(ca.x7102, chain_moralis)
    except Exception:
        x7102_balance = 0
        x7102_price = 0
    try:
        x7103_balance = api.get_token_balance(wallet, ca.x7103, chain)
        x7103_price = x7103_balance * api.get_price(ca.x7103, chain_moralis)
    except Exception:
        x7103_balance = 0
        x7103_price = 0
    try:
        x7104_balance = api.get_token_balance(wallet, ca.x7104, chain)
        x7dao_price = x7104_balance * api.get_price(ca.x7104, chain_moralis)
    except Exception:
        x7104_balance = 0
        x7104_price = 0
    try:
        x7105_balance = api.get_token_balance(wallet, ca.x7105, chain)
        x7105_price = x7105_balance * api.get_price(ca.x7105, chain_moralis)
    except Exception:
        x7105_balance = 0
        x7105_price = 0
    try:
        x7d_balance = api.get_token_balance(wallet, ca.x7d, chain)
        x7d_price = x7d_balance * api.get_native_price(native)
    except Exception:
        x7d_balance = 0
        x7d_price = 0
    total = x7d_price + x7r_price + x7dao_price + x7101_price + x7102_price + x7103_price + x7104_price + x7105_price
    im1 = Image.open((random.choice(media.blackhole)))
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 24)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (28, 36),
        f"X7 Finance Wallet Info {chain_name}\n\n"
        f"{eth[:6]} {native.upper()} (${'{:0,.0f}'.format(dollar)})\n\n"
        f"{x7r_balance} X7R (${'{:0,.0f}'.format(x7r_price)})\n"
        f"{x7dao_balance} X7DAO (${'{:0,.0f}'.format(x7dao_price)})\n"
        f"{x7101_balance} X7101 (${'{:0,.0f}'.format(x7101_price)})\n"
        f"{x7102_balance} X7102 (${'{:0,.0f}'.format(x7102_price)})\n"
        f"{x7103_balance} X7103 (${'{:0,.0f}'.format(x7103_price)})\n"
        f"{x7104_balance} X7104 (${'{:0,.0f}'.format(x7104_price)})\n"
        f"{x7105_balance} X7105 (${'{:0,.0f}'.format(x7105_price)})\n"
        f"{x7d_balance} X7D (${'{:0,.0f}'.format(x7d_price)})\n\n"
        f"Total X7 Finance token value ${'{:0,.0f}'.format(total)}\n\n"
        f"UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}",
        font=myfont,
        fill=(255, 255, 255),
    )

    img_path = os.path.join("media", "blackhole.png")
    im1.save(img_path)
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=f"*X7 Finance Wallet Info {chain_name}*\nUse `/wallet [chain-name] [wallet_address]` for other chains\n\n"
        f'`{wallet}`\n\n'
        f"{eth[:6]} {native.upper()} (${'{:0,.0f}'.format(dollar)})\n\n"
        f"{x7r_balance} X7R (${'{:0,.0f}'.format(x7r_price)})\n"
        f"{x7dao_balance} X7DAO (${'{:0,.0f}'.format(x7dao_price)})\n"
        f"{x7101_balance} X7101 (${'{:0,.0f}'.format(x7101_price)})\n"
        f"{x7102_balance} X7102 (${'{:0,.0f}'.format(x7102_price)})\n"
        f"{x7103_balance} X7103 (${'{:0,.0f}'.format(x7103_price)})\n"
        f"{x7104_balance} X7104 (${'{:0,.0f}'.format(x7104_price)})\n"
        f"{x7105_balance} X7105 (${'{:0,.0f}'.format(x7105_price)})\n"
        f"{x7d_balance} X7D (${'{:0,.0f}'.format(x7d_price)})\n\n"
        f"Total X7 Finance token value ${'{:0,.0f}'.format(total)}\n\n"
        f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Wallet Link",
                        url=f"{link}{wallet}",
                    )
                ],
                
            ]
        ),
    )


async def website(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        caption=
        f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Xchange", url=f"{url.xchange}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7.Finance", url=f"{url.website}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7Finance.org", url=f"{url.dashboard}",
                    )
                ],
            ]
        ),
    )


async def wei(update: Update, context: ContextTypes.DEFAULT_TYPE):
    eth = " ".join(context.args)
    wei = int(float(eth) * 10**18)
    await update.message.reply_text(
        f"{eth} ETH is equal to \n" f"`{wei}` wei", parse_mode="Markdown"
    )


async def wp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=f"*X7 Finance Whitepaper Quote*\n\n{random.choice(text.quotes)}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Website", url=f"{url.dashboard}")],
                [InlineKeyboardButton(text="Full WP", url=f"{url.wp_link}")],
                [InlineKeyboardButton(text="Short WP", url=f"{url.short_wp_link}")],
            ]
        ),
    )


async def x7r(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    dollar = chain.startswith("$")
    price = api.get_cg_price("x7r")
    if price["x7r"]["usd_24h_change"] is None:
        price["x7r"]["usd_24h_change"] = 0
    if dollar:
        amount = round(float(chain[1:]) / float(price["x7r"]["usd"]), 2)
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7r_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (26, 30),
            f"X7R Info (ETH)\n\n"
            f'{chain} is currently worth:\n\n{"{:0,.0f}".format(amount)} '
            f"X7R (ETH) Tokens (before tax)\n\n\n\n\n\n\n\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f'{chain} is currently worth:\n\n{"{:0,.0f}".format(amount)} '
            f"X7R (ETH) Tokens (Before Tax)\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )
    if chain.isdigit():
        amount = float(chain) * float(price["x7r"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7r_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (26, 30),
            f"X7R Info (ETH)\n\n"
            f'{chain} X7R (ETH) Currently Costs:\n\n${"{:0,.0f}".format(amount)}\n\n\n\n\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f'{chain} X7R (ETH) Currently Costs:\n\n${"{:0,.0f}".format(amount)}'
            f"\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )
    if chain == "" or chain == "eth":
        x7r_ath_change = str(api.get_ath("x7r")[1])
        x7r_ath = api.get_ath("x7r")[0]
        chain_name = ""
        scan_url = ""
        chart_url = ""
        scan_name = ""
        holders = api.get_holders(ca.x7r)
        burn = api.get_token_balance(ca.dead, ca.x7r, "eth")
        percent = round(((burn / ca.supply) * 100), 6)
        x7r = api.get_liquidity(ca.x7r_pair_eth, "eth")
        x7r_token = float(x7r["reserve0"])
        x7r_weth = float(x7r["reserve1"]) / 10**18
        x7r_weth_dollar = float(x7r_weth) * float(api.get_native_price("eth"))
        x7r_token_dollar = float(price["x7r"]["usd"]) * float(x7r_token) / 10**18
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7r_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(R"media/FreeMonoBold.ttf", 25)
        im1.save(r"media/blackhole.png", quality=95)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (26, 30),
            f"X7R Info (ETH)\n\n"
            f'X7R Price: ${price["x7r"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7r"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(price["x7r"]["usd"] * ca.supply)}\n'
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7r"]["usd_24h_vol"])}\n'
            f'ATH: ${x7r_ath} (${"{:0,.0f}".format(x7r_ath * ca.supply)}) {x7r_ath_change[:3]}%\n'
            f"Holders: {holders}\n\n"
            f"Liquidity:\n"
            f'{"{:0,.0f}".format(x7r_token)[:4]}M X7R (${"{:0,.0f}".format(x7r_token_dollar)})\n'
            f'{"{:0,.0f}".format(x7r_weth)} WETH (${"{:0,.0f}".format(x7r_weth_dollar)})\n'
            f'Total Liquidity ${"{:0,.0f}".format(x7r_weth_dollar + x7r_token_dollar)}\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f"*X7R Info (ETH)*\nUse `/x7r [chain-name]` for other chains\n\n"
            f'X7R Price: ${price["x7r"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7r"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(price["x7r"]["usd"] * ca.supply)}\n'
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7r"]["usd_24h_vol"])}\n'
            f'ATH: ${x7r_ath} (${"{:0,.0f}".format(x7r_ath * ca.supply)}) {x7r_ath_change[:3]}%\n'
            f"Holders: {holders}\n\n"
            f"X7R Tokens Burned:\n"
            f'{"{:,}".format(burn)}\n'
            f"{percent}% of Supply\n\n"
            f"Liquidity:\n"
            f'{"{:0,.0f}".format(x7r_token)[:4]}M X7R (${"{:0,.0f}".format(x7r_token_dollar)})\n'
            f'{"{:0,.0f}".format(x7r_weth)} WETH (${"{:0,.0f}".format(x7r_weth_dollar)})\n'
            f'Total Liquidity ${"{:0,.0f}".format(x7r_weth_dollar + x7r_token_dollar)}\n\n'
            f"Contract Address:\n`{ca.x7r}`\n\n{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Etherscan", url=f"{url.ether_token}{ca.x7r}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Chart", url=f"{url.dex_tools_eth}{ca.x7r_pair_eth}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Buy", url=f"{url.xchange_buy_eth}{ca.x7r}"
                        )
                    ],
                ]
            ),
        )
        return
    if chain == "bsc" or chain == "bnb":
        chain_name = "(BSC)"
        scan_url = url.bsc_token + ca.x7r
        chart_url = url.dex_tools_bsc + ca.x7r_pair_bsc
        scan_name = "BSCscan"
    if chain == "opti" or chain == "optimism":
        chain_name = "(OPTI)"
        scan_url = url.opti_token + ca.x7r
        chart_url = url.dex_tools_opti + ca.x7r_pair_opti
        scan_name = "Optimistic"
    if chain == "arb" or chain == "arbitrum":
        chain_name = "(ARB)"
        scan_url = url.arb_token + ca.x7r
        chart_url = url.dex_tools_arb + ca.x7r_pair_arb
        scan_name = "Arbiscan"
    if chain == "poly" or chain == "polygon":
        chain_name = "(POLYGON)"
        scan_url = url.poly_token + ca.x7r
        chart_url = url.dex_tools_poly + ca.x7r_pair_poly
        scan_name = "Polygonscan"
        await update.message.reply_photo(
            photo=open(media.x7r_logo, "rb"),
            caption=f"*X7R Info {chain_name}*\nUse `/x7r [chain-name]` for other chains\n\n"
            f"Contract Address:\n`{ca.x7r}`\n\n{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text=f"{scan_name}", url=f"{scan_url}")],
                    [InlineKeyboardButton(text="Chart", url=f"{chart_url}")],
                    [
                        InlineKeyboardButton(
                            text="Buy", url=f"{url.xchange_buy_eth}{ca.x7r}"
                        )
                    ],
                ]
            ),
        )


async def x7d(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    supply = ""
    holders = ""
    dollar = ""
    chain_name = ""
    chain_url = ""
    if chain == "" or chain == "eth":
        lpool_reserve = api.get_native_balance(ca.lpool_reserve, "eth")
        lpool_reserve_dollar = (float(lpool_reserve) * float(api.get_native_price("eth")) / 1**18)
        lpool = api.get_native_balance(ca.lpool, "eth")
        lpool_dollar = float(lpool) * float(api.get_native_price("eth")) / 1**18
        dollar = lpool_reserve_dollar + lpool_dollar
        supply = round(float(lpool_reserve) + float(lpool), 2)
        holders = api.get_holders(ca.x7d)
        chain_name = "(ETH)"
        chain_url = url.ether_address
    if chain == "bsc" or chain == "bnb":
        lpool_reserve = api.get_native_balance(ca.lpool_reserve, "bsc")
        lpool_reserve_dollar = (float(lpool_reserve) * float(api.get_native_price("bnb")) / 1**18)
        lpool = api.get_native_balance(ca.lpool, "bsc")
        lpool_dollar = float(lpool) * float(api.get_native_price("bnb")) / 1**18
        dollar = lpool_reserve_dollar + lpool_dollar
        supply = round(float(lpool_reserve) + float(lpool), 2)
        chain_name = "(BSC)"
        chain_url = url.bsc_address
    if chain == "polygon" or chain == "poly":
        lpool_reserve = api.get_native_balance(ca.lpool_reserve, "poly")
        lpool_reserve_dollar = (float(lpool_reserve) * float(api.get_native_price("matic")) / 1**18)
        lpool = api.get_native_balance(ca.lpool, "poly")
        lpool_dollar = float(lpool) * float(api.get_native_price("matic")) / 1**18
        dollar = lpool_reserve_dollar + lpool_dollar
        supply = round(float(lpool_reserve) + float(lpool), 2)
        chain_name = "(POLYGON)"
        chain_url = url.poly_address
    if chain == "optimism" or chain == "opti":
        lpool_reserve = api.get_native_balance(ca.lpool_reserve, "opit")
        lpool_reserve_dollar = (float(lpool_reserve) * float(api.get_native_price("eth")) / 1**18)
        lpool = api.get_native_balance(ca.lpool, "opti")
        lpool_dollar = float(lpool) * float(api.get_native_price("eth")) / 1**18
        dollar = lpool_reserve_dollar + lpool_dollar
        supply = round(float(lpool_reserve) + float(lpool), 2)
        chain_name = "(OPTIMISM)"
        chain_url = url.opti_address
    if chain == "arbitrum" or chain == "arb":
        lpool_reserve = api.get_native_balance(ca.lpool_reserve, "arb")
        lpool_reserve_dollar = (float(lpool_reserve) * float(api.get_native_price("eth")) / 1**18)
        lpool = api.get_native_balance(ca.lpool, "arb")
        lpool_dollar = float(lpool) * float(api.get_native_price("eth")) / 1**18
        dollar = lpool_reserve_dollar + lpool_dollar
        supply = round(float(lpool_reserve) + float(lpool), 2)
        chain_name = "(ARB)"
        chain_url = url.arb_address

    im1 = Image.open((random.choice(media.blackhole)))
    im2 = Image.open(media.x7d_logo)
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 28)
    i1.text(
        (28, 36),
        f"X7D {chain_name} Info\n\n"
        f'Supply: {supply} X7D (${"{:0,.0f}".format(dollar)})\n'
        f"Holders: {holders}\n\n\n\n\n\n\n\n\n"
        f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font=myfont,
        fill=(255, 255, 255),
    )
    img_path = os.path.join("media", "blackhole.png")
    im1.save(img_path)
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=f"*X7D {chain_name} Info*\n"
        f"For other chains use `/x7d [chain-name]`\n\n"
        f'Supply: {supply} X7D (${"{:0,.0f}".format(dollar)})\n'
        f"Holders: {holders}\n\n"
        f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7D Funding Dashboard",
                        url="https://app.x7.finance/#/fund",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 Deposit Contract", url=f"{chain_url}{ca.x7d}#code"
                    )
                ],
            ]
        ),
    )


async def x7dao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_name = ""
    scan_url = ""
    chart_url = ""
    scan_name = ""
    dollar = chain.startswith("$")
    price = api.get_cg_price("x7dao")
    if price["x7dao"]["usd_24h_change"] is None:
        price["x7dao"]["usd_24h_change"] = 0
    if dollar:
        amount = float(chain[1:]) / float(price["x7dao"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7dao_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (26, 30),
            f"X7DAO Info (ETH)\n\n"
            f'{chain} is currently worth:\n\n{"{:0,.0f}".format(amount)} '
            f"X7R (ETH) Tokens (before tax)\n\n\n\n\n\n\n\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f'{chain} Is currently worth:\n\n{"{:0,.0f}".format(amount)}'
            f" X7DAO (ETH) Tokens (before tax)\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )
    if chain == "proposal":
        chain = "500000"
    if chain == "500000":
        amount = float(chain) * float(price["x7dao"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7dao_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (26, 30),
            f"X7DAO Info (ETH)\n\n"
            f"Holding {chain} X7DAO Tokens will earn you\n"
            f"the right to make proposals on X7 DAO dApp\n\n"
            f'{chain} X7DAO (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f"Holding {chain} X7DAO Tokens will earn you the right to make proposals on X7 DAO dApp\n\n"
            f'{chain} X7DAO (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)}\n\n{api.get_quote()}',
            parse_mode="Markdown",
        )
        return
    if chain.isdigit():
        amount = float(chain) * float(price["x7dao"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7dao_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (26, 30),
            f"X7DAO Info (ETH)\n\n"
            f'{chain} X7DAO (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n\n\n\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f'{chain} X7DAO (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n'
            f"{api.get_quote()}",
            parse_mode="Markdown",
        )
    if chain == "" or chain == "eth":
        x7dao_ath_change = str(api.get_ath("x7dao")[1])
        x7dao_ath = api.get_ath("x7dao")[0]
        holders = api.get_holders(ca.x7dao)
        x7dao = api.get_liquidity(ca.x7dao_pair_eth, "eth")
        x7dao_token = float(x7dao["reserve0"])
        x7dao_weth = float(x7dao["reserve1"]) / 10**18
        x7dao_weth_dollar = float(x7dao_weth) * float(api.get_native_price("eth"))
        x7dao_token_dollar = (
            float(price["x7dao"]["usd"]) * float(x7dao_token) / 10**18
        )
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7dao_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 25)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (28, 36),
            f"X7DAO Info (ETH)\n\n"
            f'X7DAO Price: ${price["x7dao"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7dao"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(price["x7dao"]["usd"] * ca.supply)}\n'
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7dao"]["usd_24h_vol"])}\n'
            f'ATH: ${x7dao_ath} (${"{:0,.0f}".format(x7dao_ath * ca.supply)}) {x7dao_ath_change[:3]}%\n'
            f"Holders: {holders}\n\n"
            f"Liquidity:\n"
            f'{"{:0,.0f}".format(x7dao_token)[:4]}M X7DAO (${"{:0,.0f}".format(x7dao_token_dollar)})\n'
            f'{"{:0,.0f}".format(x7dao_weth)} WETH (${"{:0,.0f}".format(x7dao_weth_dollar)})\n'
            f'Total Liquidity ${"{:0,.0f}".format(x7dao_weth_dollar + x7dao_token_dollar)}\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f"*X7DAO (ETH) Info*\n\n"
            f'X7DAO Price: ${price["x7dao"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7dao"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(price["x7dao"]["usd"] * ca.supply)}\n'
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7dao"]["usd_24h_vol"])}\n'
            f'ATH: ${x7dao_ath} (${"{:0,.0f}".format(x7dao_ath * ca.supply)}) {x7dao_ath_change[:3]}%\n'
            f"Holders: {holders}\n\n"
            f"Liquidity:\n"
            f'{"{:0,.0f}".format(x7dao_token)[:4]}M X7DAO (${"{:0,.0f}".format(x7dao_token_dollar)})\n'
            f'{"{:0,.0f}".format(x7dao_weth)} WETH (${"{:0,.0f}".format(x7dao_weth_dollar)})\n'
            f'Total Liquidity ${"{:0,.0f}".format(x7dao_weth_dollar + x7dao_token_dollar)}\n\n'
            f"Contract Address:\n`{ca.x7dao}`\n\n{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Etherscan", url=f"{url.ether_token}{ca.x7dao}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Chart", url=f"{url.dex_tools_eth}{ca.x7dao_pair_eth}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Buy", url=f"{url.xchange_buy_eth}{ca.x7dao}"
                        )
                    ],
                ]
            ),
        )
        return
    if chain == "bsc" or chain == "bnb":
        chain_name = "(BSC)"
        scan_url = url.bsc_token + ca.x7dao
        chart_url = url.dex_tools_bsc + ca.x7dao_pair_bsc
        scan_name = "BSCscan"
    if chain == "opti" or chain == "optimism":
        chain_name = "(OPTI)"
        scan_url = url.opti_token + ca.x7dao
        chart_url = url.dex_tools_opti + ca.x7dao_pair_opti
        scan_name = "Optimistic"
    if chain == "arb" or chain == "arbitrum":
        chain_name = "(ARB)"
        scan_url = url.arb_token + ca.x7dao
        chart_url = url.dex_tools_arb + ca.x7dao_pair_arb
        scan_name = "Arbiscan"
    if chain == "poly" or chain == "polygon":
        chain_name = "(POLYGON)"
        scan_url = url.poly_token + ca.x7dao
        chart_url = url.dex_tools_poly + ca.x7dao_pair_poly
        scan_name = "Polygonscan"
    await update.message.reply_photo(
        photo=open(media.x7dao_logo, "rb"),
        caption=f"*X7DAO {chain_name} Info*\nUse `/x7dao [chain-name]` for other chains\n\n"
        f"Contract Address:\n`{ca.x7dao}`\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=f"{scan_name}", url=f"{scan_url}")],
                [InlineKeyboardButton(text="Chart", url=f"{chart_url}")],
                [
                    InlineKeyboardButton(
                        text="Buy", url=f"{url.xchange_buy_eth}{ca.x7dao}"
                    )
                ],
            ]
        ),
    )


async def x7101(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_name = ""
    scan_url = ""
    chart_url = ""
    scan_name = ""
    dollar = chain.startswith("$")
    price = api.get_cg_price("x7101")
    if price["x7101"]["usd_24h_change"] is None:
        price["x7101"]["usd_24h_change"] = 0
    if dollar:
        amount = float(chain[1:]) / float(price["x7101"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7101_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (26, 30),
            f"X7101 Info (ETH)\n\n"
            f'{chain} is currently worth:\n\n{"{:0,.0f}".format(amount)} '
            f"X7101 (ETH) Tokens (before tax)\n\n\n\n\n\n\n\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f'{chain} Is currently worth:\n\n{"{:0,.0f}".format(amount)}'
            f" X7101 (ETH) Tokens (before tax)\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )
    if chain.isdigit():
        amount = float(chain) * float(price["x7101"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7101_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (26, 30),
            f"X7101 Info (ETH)\n\n"
            f'{chain} X7101 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n\n\n\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f'{chain} X7101 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n'
            f"{api.get_quote()}",
            parse_mode="Markdown",
        )
    if chain == "" or chain == "eth":
        x7101_ath_change = str(api.get_ath("x7101")[1])
        x7101_ath = api.get_ath("x7101")[0]
        holders = api.get_holders(ca.x7101)
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7101_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1.text(
            (28, 36),
            f"X7101 Info (ETH)\n\n"
            f'X7101 Price: ${price["x7101"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7101"]["usd_24h_change"]), 1}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(price["x7101"]["usd"] * ca.supply)}\n'
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7101"]["usd_24h_vol"])}\n'
            f'ATH: ${x7101_ath} (${"{:0,.0f}".format(x7101_ath * ca.supply)}) {x7101_ath_change[:3]}%\n'
            f"Holders: {holders}\n\n\n\n\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f"*X7101 (ETH) Info*\nUse `/X7101 [chain-name]` for other chains\n\n"
            f'X7101 Price: ${price["x7101"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7101"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(price["x7101"]["usd"] * ca.supply)}\n'
            f'24 Hour Volume: ${round(price["x7101"]["usd_24h_vol"])}\n'
            f'ATH: ${x7101_ath} (${"{:0,.0f}".format(x7101_ath * ca.supply)}) {x7101_ath_change[:3]}%\n'
            f"Holders: {holders}\n\n"
            f"*X7101 Contract*\n`{ca.x7101}`\n\n{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Etherscan", url=f"{url.ether_token}{ca.x7101}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Chart", url=f"{url.dex_tools_eth}{ca.x7101_pair_eth}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Buy", url=f"{url.xchange_buy_eth}{ca.x7101}"
                        )
                    ],
                ]
            ),
        )
        return
    if chain == "bsc" or chain == "bnb":
        chain_name = "(BSC)"
        scan_url = url.bsc_token + ca.x7101
        chart_url = url.dex_tools_bsc + ca.x7101_pair_bsc
        scan_name = "BSCscan"
    if chain == "opti" or chain == "optimism":
        chain_name = "(OPTI)"
        scan_url = url.opti_token + ca.x7101
        chart_url = url.dex_tools_opti + ca.x7101_pair_opti
        scan_name = "Optimistic"
    if chain == "arb" or chain == "arbitrum":
        chain_name = "(ARB)"
        scan_url = url.arb_token + ca.x7101
        chart_url = url.dex_tools_arb + ca.x7101_pair_arb
        scan_name = "Arbiscan"
    if chain == "poly" or chain == "polygon":
        chain_name = "(POLYGON)"
        scan_url = url.poly_token + ca.x7101
        chart_url = url.dex_tools_poly + ca.x7101_pair_poly
        scan_name = "Polygonscan"
    await update.message.reply_photo(
        photo=open(media.x7dao_logo, "rb"),
        caption=f"*X7DAO {chain_name} Info*\nUse `/x7101 [chain-name]` for other chains\n\n"
        f"Contract Address:\n`{ca.x7101}`\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=f"{scan_name}", url=f"{scan_url}")],
                [InlineKeyboardButton(text="Chart", url=f"{chart_url}")],
                [
                    InlineKeyboardButton(
                        text="Buy", url=f"{url.xchange_buy_eth}{ca.x7101}"
                    )
                ],
            ]
        ),
    )


async def x7102(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_name = ""
    scan_url = ""
    chart_url = ""
    scan_name = ""
    dollar = chain.startswith("$")
    price = api.get_cg_price("x7102")
    if price["x7102"]["usd_24h_change"] is None:
        price["x7102"]["usd_24h_change"] = 0
    if dollar:
        amount = float(chain[1:]) / float(price["x7102"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7102_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (26, 30),
            f"X7102 Info (ETH)\n\n"
            f'{chain} is currently worth:\n\n{"{:0,.0f}".format(amount)} '
            f"X102 (ETH) Tokens (before tax)\n\n\n\n\n\n\n\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f'{chain} Is currently worth:\n\n{"{:0,.0f}".format(amount)}'
            f" X7102 (ETH) Tokens (before tax)\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )
    if chain.isdigit():
        amount = float(chain) * float(price["x7102"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7102_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (26, 30),
            f"X7102 Info (ETH)\n\n"
            f'{chain} X7102 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n\n\n\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f'{chain} X7102 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n'
            f"{api.get_quote()}",
            parse_mode="Markdown",
        )
    if chain == "" or chain == "eth":
        x7102_ath_change = str(api.get_ath("x7102")[1])
        x7102_ath = api.get_ath("x7102")[0]
        holders = api.get_holders(ca.x7102)
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7102_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1.text(
            (28, 36),
            f"X7102 Info (ETH)\n\n"
            f'X7102 Price: ${price["x7102"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7102"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(price["x7102"]["usd"] * ca.supply)}\n'
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7102"]["usd_24h_vol"])}\n'
            f'ATH: ${x7102_ath} (${"{:0,.0f}".format(x7102_ath * ca.supply)}) {x7102_ath_change[:3]}%\n'
            f"Holders: {holders}\n\n\n\n\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f"*X7102 (ETH) Info*\nUse `/x7102 [chain-name]` for other chains\n\n"
            f'X7102 Price: ${price["x7102"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7102"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(price["x7102"]["usd"] * ca.supply)}\n'
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7102"]["usd_24h_vol"])}\n'
            f'ATH: ${x7102_ath} (${"{:0,.0f}".format(x7102_ath * ca.supply)}) {x7102_ath_change[:3]}%\n'
            f"Holders: {holders}\n\n"
            f"*X7102 Contract*\n`{ca.x7102}`\n\n{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Etherscan", url=f"{url.ether_token}{ca.x7102}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Chart", url=f"{url.dex_tools_eth}{ca.x7102_pair_eth}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Buy", url=f"{url.xchange_buy_eth}{ca.x7102}"
                        )
                    ],
                ]
            ),
        )
        return
    if chain == "bsc" or chain == "bnb":
        chain_name = "(BSC)"
        scan_url = url.bsc_token + ca.x7102
        chart_url = url.dex_tools_bsc + ca.x7102_pair_bsc
        scan_name = "BSCscan"
    if chain == "opti" or chain == "optimism":
        chain_name = "(OPTI)"
        scan_url = url.opti_token + ca.x7102
        chart_url = url.dex_tools_opti + ca.x7102_pair_opti
        scan_name = "Optimistic"
    if chain == "arb" or chain == "arbitrum":
        chain_name = "(ARB)"
        scan_url = url.arb_token + ca.x7102
        chart_url = url.dex_tools_arb + ca.x7102_pair_arb
        scan_name = "Arbiscan"
    if chain == "poly" or chain == "polygon":
        chain_name = "(POLYGON)"
        scan_url = url.poly_token + ca.x7102
        chart_url = url.dex_tools_poly + ca.x7102_pair_poly
        scan_name = "Polygonscan"
    await update.message.reply_photo(
        photo=open(media.x7dao_logo, "rb"),
        caption=f"*X7DAO {chain_name} Info*\nUse `/x7102 [chain-name]` for other chains\n\n"
        f"Contract Address:\n`{ca.x7102}`\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=f"{scan_name}", url=f"{scan_url}")],
                [InlineKeyboardButton(text="Chart", url=f"{chart_url}")],
                [
                    InlineKeyboardButton(
                        text="Buy", url=f"{url.xchange_buy_eth}{ca.x7102}"
                    )
                ],
            ]
        ),
    )


async def x7103(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_name = ""
    scan_url = ""
    chart_url = ""
    scan_name = ""
    dollar = chain.startswith("$")
    price = api.get_cg_price("x7103")
    if price["x7103"]["usd_24h_change"] is None:
        price["x7103"]["usd_24h_change"] = 0
    if dollar:
        amount = float(chain[1:]) / float(price["x7103"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7103_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (26, 30),
            f"X7103 Info (ETH)\n\n"
            f'{chain} is currently worth:\n\n{"{:0,.0f}".format(amount)} '
            f"X7103 (ETH) Tokens (before tax)\n\n\n\n\n\n\n\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f'{chain} Is currently worth:\n\n{"{:0,.0f}".format(amount)}'
            f" X7103 (ETH) Tokens (before tax)\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )
    if chain.isdigit():
        amount = round(float(chain) * float(price["x7103"]["usd"]), 2)
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7103_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (26, 30),
            f"X7103 Info (ETH)\n\n"
            f'{chain} X7103 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n\n\n\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f'{chain} X7103 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n'
            f"{api.get_quote()}",
            parse_mode="Markdown",
        )
    if chain == "" or chain == "eth":
        x7103_ath_change = str(api.get_ath("x7103")[1])
        x7103_ath = api.get_ath("x7103")[0]
        holders = api.get_holders(ca.x7103)
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7103_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 25)
        i1.text(
            (28, 36),
            f"X7103 Info (ETH)\n\n"
            f'X7103 Price: ${price["x7103"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7103"]["usd_24h_change"],1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(price["x7103"]["usd"] * ca.supply)}\n'
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7103"]["usd_24h_vol"])}\n'
            f'ATH: ${x7103_ath} (${"{:0,.0f}".format(x7103_ath * ca.supply)}) {x7103_ath_change[:3]}%\n'
            f"Holders: {holders}\n\n\n\n\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f"*X7103 (ETH) Info*\nUse `/x7103` [chain-name] for other chains\n\n"
            f'X7103 Price: ${price["x7103"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7103"]["usd_24h_change"],1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(price["x7103"]["usd"] * ca.supply)}\n'
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7103"]["usd_24h_vol"])}\n'
            f'ATH: ${x7103_ath} (${"{:0,.0f}".format(x7103_ath * ca.supply)}) {x7103_ath_change[:3]}%\n'
            f"Holders: {holders}\n\n"
            f"*X7103 Contract*\n`{ca.x7103}`\n\n{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Etherscan", url=f"{url.ether_token}{ca.x7103}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Chart", url=f"{url.dex_tools_eth}{ca.x7103_pair_eth}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Buy", url=f"{url.xchange_buy_eth}{ca.x7103}"
                        )
                    ],
                ]
            ),
        )
        return
    if chain == "bsc" or chain == "bnb":
        chain_name = "(BSC)"
        scan_url = url.bsc_token + ca.x7103
        chart_url = url.dex_tools_bsc + ca.x7103_pair_bsc
        scan_name = "BSCscan"
    if chain == "opti" or chain == "optimism":
        chain_name = "(OPTI)"
        scan_url = url.opti_token + ca.x7103
        chart_url = url.dex_tools_opti + ca.x7103_pair_opti
        scan_name = "Optimistic"
    if chain == "arb" or chain == "arbitrum":
        chain_name = "(ARB)"
        scan_url = url.arb_token + ca.x7103
        chart_url = url.dex_tools_arb + ca.x7103_pair_arb
        scan_name = "Arbiscan"
    if chain == "poly" or chain == "polygon":
        chain_name = "(POLYGON)"
        scan_url = url.poly_token + ca.x7103
        chart_url = url.dex_tools_poly + ca.x7103_pair_poly
        scan_name = "Polygonscan"
    await update.message.reply_photo(
        photo=open(media.x7dao_logo, "rb"),
        caption=f"*X7DAO {chain_name} Info*\nUse `/x7103 [chain-name]` for other chains\n\n"
        f"Contract Address:\n`{ca.x7103}`\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=f"{scan_name}", url=f"{scan_url}")],
                [InlineKeyboardButton(text="Chart", url=f"{chart_url}")],
                [
                    InlineKeyboardButton(
                        text="Buy", url=f"{url.xchange_buy_eth}{ca.x7103}"
                    )
                ],
            ]
        ),
    )


async def x7104(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_name = ""
    scan_url = ""
    chart_url = ""
    scan_name = ""
    dollar = chain.startswith("$")
    price = api.get_cg_price("x7104")
    if price["x7104"]["usd_24h_change"] is None:
        price["x7104"]["usd_24h_change"] = 0
    if dollar:
        amount = float(chain[1:]) / float(price["x7104"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7104_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (26, 30),
            f"X7104 Info (ETH)\n\n"
            f'{chain} is currently worth:\n\n{"{:0,.0f}".format(amount)} '
            f"X7104 (ETH) Tokens (before tax)\n\n\n\n\n\n\n\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f'{chain} Is currently worth:\n\n{"{:0,.0f}".format(amount)}'
            f" X7104 (ETH) Tokens (before tax)\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )
    if chain.isdigit():
        amount = float(chain) * float(price["x7104"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7104_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 25)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (26, 30),
            f"X7104 Info (ETH)\n\n"
            f'{chain} X7104 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n\n\n\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f'{chain} X7104 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n'
            f"{api.get_quote()}",
            parse_mode="Markdown",
        )
    if chain == "" or chain == "eth":
        x7104_ath_change = str(api.get_ath("x7104")[1])
        x7104_ath = api.get_ath("x7104")[0]
        holders = api.get_holders(ca.x7104)
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7104_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (28, 36),
            f"X7104 Info (ETH)\n\n"
            f'X7104 Price: ${price["x7104"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7104"]["usd_24h_change"],1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(price["x7104"]["usd"] * ca.supply)}\n'
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7104"]["usd_24h_vol"])}\n'
            f'ATH: ${x7104_ath} (${"{:0,.0f}".format(x7104_ath * ca.supply)}) {x7104_ath_change[:3]}%\n'
            f"Holders: {holders}\n\n\n\n\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f"*X7104 (ETH) Info*\n`Use /x7104 [chain-name]` for other chains\n\n"
            f'X7104 Price: ${price["x7104"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7104"]["usd_24h_change"],1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(price["x7104"]["usd"] * ca.supply)}\n'
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7104"]["usd_24h_vol"])}\n'
            f'ATH: ${x7104_ath} (${"{:0,.0f}".format(x7104_ath * ca.supply)}) {x7104_ath_change[:3]}%\n'
            f"Holders: {holders}\n\n"
            f"*X7104 Contract*\n`{ca.x7104}`\n\n{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Etherscan", url=f"{url.ether_token}{ca.x7104}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Chart", url=f"{url.dex_tools_eth}{ca.x7104_pair_eth}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Buy", url=f"{url.xchange_buy_eth}{ca.x7104}"
                        )
                    ],
                ]
            ),
        )
        return
    if chain == "bsc" or chain == "bnb":
        chain_name = "(BSC)"
        scan_url = url.bsc_token + ca.x7104
        chart_url = url.dex_tools_bsc + ca.x7104_pair_bsc
        scan_name = "BSCscan"
    if chain == "opti" or chain == "optimism":
        chain_name = "(OPTI)"
        scan_url = url.opti_token + ca.x7104
        chart_url = url.dex_tools_opti + ca.x7104_pair_opti
        scan_name = "Optimistic"
    if chain == "arb" or chain == "arbitrum":
        chain_name = "(ARB)"
        scan_url = url.arb_token + ca.x7104
        chart_url = url.dex_tools_arb + ca.x7104_pair_arb
        scan_name = "Arbiscan"
    if chain == "poly" or chain == "polygon":
        chain_name = "(POLYGON)"
        scan_url = url.poly_token + ca.x7104
        chart_url = url.dex_tools_poly + ca.x7104_pair_poly
        scan_name = "Polygonscan"
    await update.message.reply_photo(
        photo=open(media.x7dao_logo, "rb"),
        caption=f"*X7DAO {chain_name} Info*\nUse `/x7104 [chain-name]` for other chains\n\n"
        f"Contract Address:\n`{ca.x7104}`\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=f"{scan_name}", url=f"{scan_url}")],
                [InlineKeyboardButton(text="Chart", url=f"{chart_url}")],
                [
                    InlineKeyboardButton(
                        text="Buy", url=f"{url.xchange_buy_eth}{ca.x7104}"
                    )
                ],
            ]
        ),
    )


async def x7105(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_name = ""
    scan_url = ""
    chart_url = ""
    scan_name = ""
    dollar = chain.startswith("$")
    price = api.get_cg_price("x7105")
    if price["x7105"]["usd_24h_change"] is None:
        price["x7105"]["usd_24h_change"] = 0
    if dollar:
        amount = float(chain[1:]) / float(price["x7105"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7105_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (26, 30),
            f"X7105 Info (ETH)\n\n"
            f'{chain} is currently worth:\n\n{"{:0,.0f}".format(amount)} '
            f"X7105 (ETH) Tokens (before tax)\n\n\n\n\n\n\n\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f'{chain} Is currently worth:\n\n{"{:0,.0f}".format(amount)}'
            f" X7105 (ETH) Tokens (before tax)\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )
    if chain.isdigit():
        amount = float(chain) * float(price["x7105"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7105_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (26, 30),
            f"X7105 Info (ETH)\n\n"
            f'{chain} X7105 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n\n\n\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f'{chain} X7105 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n'
            f"{api.get_quote()}",
            parse_mode="Markdown",
        )
    if chain == "" or chain == "eth":
        x7105_ath_change = str(api.get_ath("x7105")[1])
        x7105_ath = api.get_ath("x7105")[0]
        holders = api.get_holders(ca.x7105)
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7105_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (28, 36),
            f"X7105 Info (ETH)\n\n"
            f'X7105 Price: ${price["x7105"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7105"]["usd_24h_change"],1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(price["x7105"]["usd"] * ca.supply)}\n'
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7105"]["usd_24h_vol"])}\n'
            f'ATH: ${x7105_ath} (${"{:0,.0f}".format(x7105_ath * ca.supply)}) {x7105_ath_change[:3]}%\n'
            f"Holders: {holders}\n\n\n\n\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont,
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=f"*X7105 (ETH) Info*\nUse `/x7105 [chain-name]` for other chains\n"
            f'X7105 Price: ${price["x7105"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7105"]["usd_24h_change"],1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(price["x7105"]["usd"] * ca.supply)}\n'
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7105"]["usd_24h_vol"])}\n'
            f'ATH: ${x7105_ath} (${"{:0,.0f}".format(x7105_ath * ca.supply)}) {x7105_ath_change[:3]}%\n'
            f"Holders: {holders}\n\n"
            f"*X7105 Contract*\n`{ca.x7105}`\n\n{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Etherscan", url=f"{url.ether_token}{ca.x7105}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Chart", url=f"{url.dex_tools_eth}{ca.x7105_pair_eth}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Buy", url=f"{url.xchange_buy_eth}{ca.x7105}"
                        )
                    ],
                ]
            ),
        )
        return
    if chain == "bsc" or chain == "bnb":
        chain_name = "(BSC)"
        scan_url = url.bsc_token + ca.x7105
        chart_url = url.dex_tools_bsc + ca.x7105_pair_bsc
        scan_name = "BSCscan"
    if chain == "opti" or chain == "optimism":
        chain_name = "(OPTI)"
        scan_url = url.opti_token + ca.x7105
        chart_url = url.dex_tools_opti + ca.x7105_pair_opti
        scan_name = "Optimistic"
    if chain == "arb" or chain == "arbitrum":
        chain_name = "(ARB)"
        scan_url = url.arb_token + ca.x7105
        chart_url = url.dex_tools_arb + ca.x7105_pair_arb
        scan_name = "Arbiscan"
    if chain == "poly" or chain == "polygon":
        chain_name = "(POLYGON)"
        scan_url = url.poly_token + ca.x7105
        chart_url = url.dex_tools_poly + ca.x7105_pair_poly
        scan_name = "Polygonscan"
    await update.message.reply_photo(
        photo=open(media.x7dao_logo, "rb"),
        caption=f"*X7DAO {chain_name} Info*\nUse `/x7105 [chain-name]` for other chains\n\n"
        f"Contract Address:\n`{ca.x7105}`\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=f"{scan_name}", url=f"{scan_url}")],
                [InlineKeyboardButton(text="Chart", url=f"{chart_url}")],
                [
                    InlineKeyboardButton(
                        text="Buy", url=f"{url.xchange_buy_eth}{ca.x7105}"
                    )
                ],
            ]
        ),
    )


# TWITTER COMMANDS
async def count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tweet = context.args[0]
    start = tweet.index("status/")
    end = tweet.index("?", start + 1)
    tweet_id = tweet[start + 7 : end]
    response = api.twitter_v2.get_retweeters(tweet_id)
    status = api.twitter.get_status(tweet_id)
    retweet_count = status.retweet_count
    rt_names = "\n".join(str(p) for p in response.data)
    await update.message.reply_sticker(sticker=media.twitter_sticker)
    await update.message.reply_text(
        f"Retweeted {retweet_count} times, by the following members:\n\n{rt_names}"
    )


async def draw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        tweet = context.args[0]
        start = tweet.index("status/")
        end = tweet.index("?", start + 1)
        tweet_id = tweet[start + 7 : end]
        response = api.twitter_v2.get_retweeters(tweet_id)
        status = api.twitter.get_status(tweet_id)
        retweet_count = status.retweet_count
        rt_names = "\n".join(str(p) for p in response.data)
        await update.message.reply_sticker(sticker=media.twitter_sticker)
        await update.message.reply_text(f"{retweet_count} Entries:\n\n{rt_names}")
        await update.message.reply_text(
            f"The Winner is....\n\n{random.choice(response.data)}\n\n"
            f"Congratulations, Please DM @X7_Finance to verify your account"
        )
    else:
        await update.message.reply_text(f"{text.mods_only}")


async def raid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        username = random.choice(text.usernamelist)
        tweet = api.twitter.user_timeline(
            screen_name=username, count=1, include_rts="false", exclude_replies="true"
        )
        await update.message.reply_sticker(sticker=media.twitter_sticker)
        await update.message.reply_text(
            f"🚨🚨 Raid {username} 🚨🚨\n\n"
            f"{tweet[0].text}\n\n"
            f"https://twitter.com/intent/tweet?text=@X7_Finance&hashtags=LongLiveDefi&in_reply_to={tweet[0].id}\n\n"
            f"{random.choice(text.twitter_replies)}",
            disable_web_page_preview=True,
        )
    else:
        await update.message.reply_text(f"{text.mods_only}")


async def spaces(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = api.twitter_v2.get_spaces(user_ids=1561721566689386496)
    if response[0] is None:
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), "rb"),
            caption=f"X7 Finance Twitter space\n\nPlease check back for more details"
            f"\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )
    else:
        data = str(response[0])
        start = data.index("=")
        end = data.index(" ", start)
        space_id = data[start + 1 : end]

        def get_space():
            url = f"https://api.twitter.com/2/spaces/{space_id}?space.fields=scheduled_start,title"
            headers = {
                "Authorization": "Bearer {}".format(os.getenv("TWITTER_BEARER")),
                "User-Agent": "v2SpacesLookupPython",
            }
            response = requests.request("GET", url, headers=headers)
            result = response.json()
            return result["data"]

        space = get_space()
        then = parser.parse(space["scheduled_start"]).astimezone(pytz.utc)
        now = datetime.now(timezone.utc)
        duration = then - now
        duration_in_s = duration.total_seconds()
        days = divmod(duration_in_s, 86400)
        hours = divmod(days[1], 3600)
        minutes = divmod(hours[1], 60)
        await update.message.reply_sticker(sticker=media.twitter_sticker)
        await update.message.reply_text(
            text=f"Next X7 Finance Twitter space:\n\n"
            f'{space["title"]}\n\n'
            f'{then.strftime("%A %B %d %Y %I:%M %p")} (UTC)\n\n'
            f"{int(days[0])} days, {int(hours[0])} hours and {int(minutes[0])} minutes\n\n"
            f"[Click here](https://twitter.com/i/spaces/{space_id}) to set a reminder!"
            f"\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )


async def twitter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ext = " ".join(context.args)
    username = "@x7_finance"
    if ext == "":
        try:
            tweet = api.twitter.user_timeline(screen_name=username, count=1, exclude_replies=True, include_rts=False)
            await update.message.reply_sticker(sticker=media.twitter_sticker)
            await update.message.reply_text(
                f"Latest X7 Finance Tweet\n\n{tweet[0].text}\n\n"
                f"{url.twitter}status/{tweet[0].id}\n\n"
                f"{random.choice(text.twitter_replies)}"
            )
        except Exception as e:
            await update.message.reply_sticker(sticker=media.twitter_sticker)
            await update.message.reply_text(
                f"*X7 Finance Twitter*\n\n"
                f"{random.choice(text.twitter_replies)}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="X7 Finance Twitter",
                            url=f"{url.twitter}",
                        )
                    ],
                ]
            ),
            )
    if ext == "count":
        chat_admins = await update.effective_chat.get_administrators()
        if update.effective_user in (admin.user for admin in chat_admins):
            tweet = api.twitter.user_timeline(screen_name=username, count=1, exclude_replies=True, include_rts=False)
            response = api.twitter_v2.get_retweeters(tweet[0].id)
            status = api.twitter.get_status(tweet[0].id)
            retweet_count = status.retweet_count
            count = "\n".join(str(p) for p in response.data)
            await update.message.reply_sticker(sticker=media.twitter_sticker)
            await update.message.reply_text(
                f"Latest X7 Finance Tweet\n\n{tweet[0].text}\n\n"
                f"{url.twitter}status/{tweet[0].id}\n\n"
                f"Retweeted {retweet_count} times, by the following members:\n\n{count}"
            )
        else:
            await update.message.reply_text(f"{text.mods_only}")


# TRANSLATOR
async def german(update: Update, context: ContextTypes.DEFAULT_TYPE):
    translator = Translator(from_lang="english", to_lang="german")
    phrase = " ".join(context.args).lower()
    translation = translator.translate(phrase)
    await update.message.reply_text(translation)


async def japanese(update: Update, context: ContextTypes.DEFAULT_TYPE):
    translator = Translator(from_lang="english", to_lang="japanese")
    phrase = " ".join(context.args).lower()
    translation = translator.translate(phrase)
    await update.message.reply_text(translation)


# GENERAL MESSAGES
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        await update.message.reply_text(
            f"{text.admin_commands}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Rose Bot Anti-flood",
                            url="https://missrose.org/guide/antiflood/",
                        )
                    ],
                ]
            ),
        )
    else:
        await update.message.reply_text(f"{text.mods_only}")


async def countdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    then = times.countdown.astimezone(pytz.utc)
    now = datetime.now(timezone.utc)
    duration = then - now

    if duration < timedelta(0):
        await update.message.reply_photo(
            photo=open(random.choice(media.logos), "rb"),
            caption=f"*X7 Finance Countdown*\n\nNo countdown set, Please check back for more details\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )
        return

    duration_in_s = duration.total_seconds()
    days, remainder = divmod(duration_in_s, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    await update.message.reply_text(
        text=f"*X7 Finance Countdown:*\n\n"
        f'{times.countdown_title}\n\n{then.strftime("%A %B %d %Y %I:%M %p")} (UTC)\n\n'
        f"{int(days)} days, {int(hours)} hours and {int(minutes)} minutes\n\n"
        f"{times.countdown_desc}\n\n{api.get_quote()}",
        parse_mode="Markdown",
    )


async def mods(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text.mods)

