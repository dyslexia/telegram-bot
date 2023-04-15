import logging
from telegram.ext import *
from telegram import *
import keys
from datetime import datetime, timedelta, timezone
import pytz
import wikipediaapi
import random
import requests
import ca
import variables
import tweepy
import pyttsx3
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import api
import media
import url
import text
import loans

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
print('Bot Restarted')

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    test = api.get_nft_holder_list(ca.eco, "eth")
    print(test)

# COMMANDS
async def bot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'{text.commands}')


async def ecosystem_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f'{text.ecosystem}'
        f'\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url='https://x7.finance')],
            [InlineKeyboardButton(text='Community Dashboard', url='https://x7community.space/')],
            [InlineKeyboardButton(text='Linktree', url='https://linktr.ee/X7_Finance')],
            [InlineKeyboardButton(text='Medium', url='https://medium.com/@X7Finance')], ]))


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f'{text.about}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url=f'{url.website}')],
            [InlineKeyboardButton(text='Community Dashboard', url=f'{url.dashboard}')],
            [InlineKeyboardButton(text='Linktree', url=f'{url.linktree}')],
            [InlineKeyboardButton(text='Medium', url=f'{url.twitter}')], ]))


async def links_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance links*\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url=f'{url.website}')],
            [InlineKeyboardButton(text='Community Dashboard', url=f'{url.dashboard}')],
            [InlineKeyboardButton(text='Linktree', url=f'{url.linktree}')],
            [InlineKeyboardButton(text='Medium', url=f'{url.medium}')],
            [InlineKeyboardButton(text='Twitter', url=f'{url.twitter}')],
            [InlineKeyboardButton(text='Discord', url=f'{url.discord}')],
            [InlineKeyboardButton(text='Reddit', url=f'{url.reddit}')],
            [InlineKeyboardButton(text='Youtube', url=f'{url.youtube}')],
            [InlineKeyboardButton(text='Github', url=f'{url.github}')], ]))


async def nft_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_name = ""
    chain_api = ""
    chain_url = ""
    eco_price = ""
    borrow_price = ""
    dex_price = ""
    liq_price = ""
    magister_price = ""
    if chain == "" or chain == "eth":
        chain_name = "(ETH)"
        chain_api = "?chain=eth-main"
        chain_url = url.poly_address
        eco_price = api.get_nft_price("eco", "eth")
        borrow_price = api.get_nft_price("borrow", "eth")
        dex_price = api.get_nft_price("dex", "eth")
        liq_price = api.get_nft_price("liq", "eth")
        magister_price = api.get_nft_price("magister", "eth")
    if chain == "poly" or chain == "polygon":
        chain_name = "(POLYGON)"
        chain_api = "?chain=poly-main"
        chain_url = url.ether_address
        eco_price = api.get_nft_price("eco", "poly")
        borrow_price = api.get_nft_price("borrow", "poly")
        dex_price = api.get_nft_price("dex", "poly")
        liq_price = api.get_nft_price("liq", "poly")
        magister_price = api.get_nft_price("magister", "poly")
    if chain == "bsc" or chain == "bnb":
        chain_name = "(BSC)"
        chain_api = ""
        chain_url = url.bsc_address
        eco_price = api.get_nft_price("eco", "bsc")
        borrow_price = api.get_nft_price("borrow", "bsc")
        dex_price = api.get_nft_price("dex", "bsc")
        liq_price = api.get_nft_price("liq", "eth")
        magister_price = api.get_nft_price("magister", "bsc")
    if chain == "opti" or chain == "optimism" or chain == "op":
        chain_name = "(OPTIMISM)"
        chain_api = "?chain=optimism-main"
        chain_url = url.opti_address
        eco_price = api.get_nft_price("eco", "opti")
        borrow_price = api.get_nft_price("borrow", "opti")
        dex_price = api.get_nft_price("dex", "opti")
        liq_price = api.get_nft_price("liq", "opti")
        magister_price = api.get_nft_price("magister", "opti")
    if chain == "arb" or chain == "arbitrum":
        chain_name = "(ARB)"
        chain_api = "?chain=arbitrum"
        chain_url = url.arb_address
        eco_price = api.get_nft_price("eco", "arb")
        borrow_price = api.get_nft_price("borrow", "arb")
        dex_price = api.get_nft_price("dex", "arb")
        liq_price = api.get_nft_price("liq", "arb")
        magister_price = api.get_nft_price("magister", "arb")
    print(eco_price)
    await update.message.reply_video(
        video=open(media.nft_logo, 'rb'),
        caption=f'*X7 Finance NFT Information {chain_name}*\nUse `/nft [chain-name]` for other chains\n\n'
                f'*Ecosystem Maxi*\n{eco_price}\n'
                f'Available - {500-int(api.get_nft_holder_count(ca.eco, chain_api))}\n'
                f'> 25% discount on X7100 tax\n'
                f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n*'
                f'Liquidity Maxi*\n{liq_price}\n'
                f'Available - {250-int(api.get_nft_holder_count(ca.liq, chain_api))}\n'
                f'> 50 % discount on X7100tax\n> 25 % discount on X7R tax\n'
                f'> 15 % discount on X7DAO tax\n\n'
                f'*Dex Maxi*\n{dex_price}\n'
                f'Available - {150-int(api.get_nft_holder_count(ca.dex, chain_api))}\n'
                f'> LP Fee Discounts while trading on X7 DEX\n\n'
                f'*Borrowing Maxi*\n{borrow_price}\n'
                f'Available - {100-int(api.get_nft_holder_count(ca.borrow, chain_api))}\n'
                f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n'
                f'*Magister*\n{magister_price}\n'
                f'Available - {49-int(api.get_nft_holder_count(ca.magister, chain_api))}\n'
                f'> 25% discount on X7100 tax\n'        
                f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n*Pioneer*\n'
                f' > 6% of profits that come into the X7 Treasury Splitter are now being allocated to the reward '
                f'pool. Each X7 Pioneer NFT grants you a proportional share of this pool\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Mint Here', url='https://x7.finance/x/nft/mint')],
            [InlineKeyboardButton(text='Ecosystem Maxi', url=f'{chain_url}{ca.eco}')],
            [InlineKeyboardButton(text='Liquidity Maxi', url=f'{chain_url}{ca.liq}')],
            [InlineKeyboardButton(text='DEX Maxi', url=f'{chain_url}{ca.dex}')],
            [InlineKeyboardButton(text='Borrowing Maxi', url=f'{chain_url}{ca.borrow}')],
            [InlineKeyboardButton(text='Magister', url=f'{chain_url}{ca.magister}')],
            [InlineKeyboardButton(text='Pioneer', url=f'{chain_url}{ca.pioneer}')], ]))


async def opensea_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "" or chain == "eth":
        await update.message.reply_photo(
            photo=open(media.opensea_logo, 'rb'),
            caption=f'*X7 Finance Opensea Links (ETH)*\nUse `/nft [chain-name]` for other chains\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Ecosystem Maxi', url='https://opensea.io/collection/x7-ecosystem-maxi')],
                [InlineKeyboardButton(text='Liquidity Maxi', url='https://opensea.io/collection/x7-liquidity-maxi')],
                [InlineKeyboardButton(text='DEX Maxi', url='https://opensea.io/collection/x7-dex-maxi')],
                [InlineKeyboardButton(text='Borrowing Maxi', url='https://opensea.io/collection/x7-borrowing-max')],
                [InlineKeyboardButton(text='Magister', url='https://opensea.io/collection/x7-magister')],
                [InlineKeyboardButton(text='Pioneer', url='https://opensea.io/collection/x7-pioneer')], ]))
    if chain == "arb" or chain == "arbitrum":
        await update.message.reply_photo(
            photo=open(media.opensea_logo, 'rb'),
            caption=f'*X7 Finance Opensea Links (ARB)*\nUse `/nft [chain-name]` for other chains\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Ecosystem Maxi',
                                      url='https://opensea.io/collection/x7-ecosystem-maxi-arbitrum')],
                [InlineKeyboardButton(text='Liquidity Maxi',
                                      url='https://opensea.io/collection/x7-liquidity-maxi-arbitrum')],
                [InlineKeyboardButton(text='DEX Maxi',
                                      url='https://opensea.io/collection/x7-dex-maxi-arbitrum')],
                [InlineKeyboardButton(text='Borrowing Maxi',
                                      url='https://opensea.io/collection/x7-borrowing-max-arbitrum')],
                [InlineKeyboardButton(text='Magister',
                                      url='https://opensea.io/collection/x7-magister-arbitrum')], ]))
    if chain == "optimism" or chain == "opti":
        await update.message.reply_photo(
            photo=open(media.opensea_logo, 'rb'),
            caption=f'*X7 Finance Opensea Links (OPTI)*\nUse `/nft [chain-name]` for other chains\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Ecosystem Maxi',
                                      url='https://opensea.io/collection/x7-ecosystem-maxi-optimism')],
                [InlineKeyboardButton(text='Liquidity Maxi',
                                      url='https://opensea.io/collection/x7-liquidity-maxi-optimism')],
                [InlineKeyboardButton(text='DEX Maxi',
                                      url='https://opensea.io/collection/x7-dex-maxi-optimism')],
                [InlineKeyboardButton(text='Borrowing Maxi',
                                      url='https://opensea.io/collection/x7-borrowing-max-optimism')],
                [InlineKeyboardButton(text='Magister',
                                      url='https://opensea.io/collection/x7-magister-optimism')], ]))
    if chain == "bnb" or chain == "bsc" or chain == "binance":
        await update.message.reply_photo(
            photo=open(media.opensea_logo, 'rb'),
            caption=f'*X7 Finance Opensea Links (BSC)*\nUse `/nft [chain-name]` for other chains\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Ecosystem Maxi',
                                      url='https://opensea.io/collection/x7-ecosystem-maxi-binance')],
                [InlineKeyboardButton(text='Liquidity Maxi',
                                      url='https://opensea.io/collection/x7-liquidity-maxi-binance')],
                [InlineKeyboardButton(text='DEX Maxi',
                                      url='https://opensea.io/collection/x7-dex-maxi-binance')],
                [InlineKeyboardButton(text='Borrowing Maxi',
                                      url='https://opensea.io/collection/x7-borrowing-max-binance')],
                [InlineKeyboardButton(text='Magister',
                                      url='https://opensea.io/collection/x7-magister-binance')], ]))
    if chain == "poly" or chain == "polygon":
        await update.message.reply_photo(
            photo=open(media.opensea_logo, 'rb'),
            caption=f'*X7 Finance Opensea Links (POLYGON)*\nUse `/nft [chain-name]` for other chains\n\n'
                    f'{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Ecosystem Maxi',
                                      url='https://opensea.io/collection/x7-ecosystem-maxi-polygon')],
                [InlineKeyboardButton(text='Liquidity Maxi',
                                      url='https://opensea.io/collection/x7-liquidity-maxi-polygon')],
                [InlineKeyboardButton(text='DEX Maxi',
                                      url='https://opensea.io/collection/x7-dex-maxi-polygon')],
                [InlineKeyboardButton(text='Borrowing Maxi',
                                      url='https://opensea.io/collection/x7-borrowing-max-polygon')],
                [InlineKeyboardButton(text='Magister',
                                      url='https://opensea.io/collection/x7-magister-polygon')], ]))


async def website_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Website Links*\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url=f'{url.website}')],
            [InlineKeyboardButton(text='Community Dashboard', url=f'{url.dashboard}')], ]))


async def wp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=f'*X7 Finance Whitepaper Quote*\n\n{random.choice(text.quotes)}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url=f'{url.website}')],
            [InlineKeyboardButton(text='Full WP', url=f'{url.wp_link}')],
            [InlineKeyboardButton(text='Short WP', url=f'{url.short_wp_link}')], ]))


async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Buy Links*\nUse `/x7token-name` for all other details\n'
                f'Use `/constellations` for constellations\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='X7R - Rewards Token', url=f'{url.xchange_buy}{ca.x7r}')],
            [InlineKeyboardButton(text='X7DAO - Governance Token', url=f'{url.xchange_buy}{ca.x7dao}')], ]))


async def chart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "":
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption='*X7 Finance Chart Links (ETH)*\nUse `/chart [chain-name]` for other chains\n'
                    f'Use `/constellations` for constellations\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R - Rewards Token',
                                      url=f'{url.dex_tools_eth}{ca.x7r_pair_eth}')],
                [InlineKeyboardButton(text='X7DAO - Governance Token',
                                      url=f'{url.dex_tools_eth}{ca.x7dao_pair_eth}')], ]))
    if chain == "opti" or chain == "optimism":
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption='*X7 Finance Chart Links (OPTIMISM)*\nUse `/chart [chain-name]` for other chains\n'
                    f'Use `/constellations` for constellations\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R - Rewards Token',
                                      url=f'{url.dex_tools_opti}{ca.x7r_pair_opti}')],
                [InlineKeyboardButton(text='X7DAO - Governance Token',
                                      url=f'{url.dex_tools_opti}{ca.x7dao_pair_opti}')], ]))
    if chain == "bsc" or chain == "bnb":
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption='*X7 Finance Chart Links (BSC)*\nUse `/chart [chain-name]` for other chains\n'
                    f'Use `/constellations` for constellations\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R - Rewards Token',
                                      url=f'{url.dex_tools_bsc}{ca.x7r_pair_bsc}')],
                [InlineKeyboardButton(text='X7DAO - Governance Token',
                                      url=f'{url.dex_tools_bsc}{ca.x7dao_pair_bsc}')], ]))
    if chain == "poly" or chain == "polygon":
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption='*X7 Finance Chart Links (POLYGON)*\nUse `/chart [chain-name]` for other chains\n'
                    f'Use `/constellations` for constellations\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R - Rewards Token',
                                      url=f'{url.dex_tools_poly}{ca.x7r_pair_poly}')],
                [InlineKeyboardButton(text='X7DAO - Governance Token',
                                      url=f'{url.dex_tools_poly}{ca.x7dao_pair_poly}')], ]))
    if chain == "arb" or chain == "arbitrum":
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption='*X7 Finance Chart Links (ARBITRUM)*\nUse `/chart [chain-name]` for other chains\n'
                    f'Use `/constellations` for constellations\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R - Rewards Token',
                                      url=f'{url.dex_tools_arb}{ca.x7r_pair_arb}')],
                [InlineKeyboardButton(text='X7DAO - Governance Token',
                                      url=f'{url.dex_tools_arb}{ca.x7dao_pair_arb}')], ]))


async def smart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_name = ""
    chain_url = ""
    if chain == "" or chain == "eth":
        chain_name = "(ETH)"
        chain_url = url.ether_address
    if chain == "arbitrum" or chain == "arb":
        chain_name = "(ARB)"
        chain_url = url.arb_address
    if chain == "poly" or chain == "polygon":
        chain_name = "(POLYGON)"
        chain_url = url.poly_address
    if chain == "bsc" or chain == "bnb":
        chain_name = "(BSC)"
        chain_url = url.bsc_address
    if chain == "op" or chain == "optimism" or chain == "opti":
        chain_name = "(OP)"
        chain_url = url.opti_address
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Smart Contracts {chain_name}*\nUse `/smart [chain-name]` or other chains\n\n'
                f'{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Contracts Directory - by MikeMurpher',
                                  url=f'{url.ca_directory}')],
            [InlineKeyboardButton(text='X7100 Liquidity Hub',
                                  url=f'{chain_url}{ca.x7100_liq_hub}')],
            [InlineKeyboardButton(text='X7R Liquidity Hub',
                                  url=f'{chain_url}{ca.x7r_liq_hub}')],
            [InlineKeyboardButton(text='X7DAO Liquidity Hub',
                                  url=f'{chain_url}{ca.x7dao_liq_hub}')],
            [InlineKeyboardButton(text='X7 Token Burner',
                                  url=f'{chain_url}{ca.burner}')],
            [InlineKeyboardButton(text='X7100 Discount Authority',
                                  url=f'{chain_url}{ca.x7100_discount}')],
            [InlineKeyboardButton(text='X7R Discount Authority',
                                  url=f'{chain_url}{ca.x7r_discount}')],
            [InlineKeyboardButton(text='X7DAO Discount Authority',
                                  url=f'{chain_url}{ca.x7dao_discount}')],
            [InlineKeyboardButton(text='X7 Token Time Lock',
                                  url=f'{chain_url}{ca.time_lock}')],
            [InlineKeyboardButton(text='X7 Ecosystem Splitter',
                                  url=f'{chain_url}{ca.eco_splitter}')],
            [InlineKeyboardButton(text='X7 Treasury Splitter',
                                  url=f'{chain_url}{ca.treasury_splitter}')],
            [InlineKeyboardButton(text='X7 Lending Pool Reserve',
                                  url=f'{chain_url}{ca.lpool_reserve}')],
            [InlineKeyboardButton(text='X7 Xchange Discount Authority',
                                  url=f'{chain_url}{ca.xchange_discount}')],
            [InlineKeyboardButton(text='X7 Lending Discount Authority',
                                  url=f'{chain_url}{ca.lending_discount}')],
            [InlineKeyboardButton(text='X7 Xchange Router',
                                  url=f'{chain_url}{ca.router}')],
            [InlineKeyboardButton(text='X7 Xchange Router with Discounts',
                                  url=f'{chain_url}{ca.discount_router}')],
            [InlineKeyboardButton(text='X7 Lending Pool Contract',
                                  url=f'{chain_url}{ca.lpool}')],
            [InlineKeyboardButton(text='X7 Xchange Factory',
                                  url=f'{chain_url}{ca.factory}')],
        ]))


async def ca_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Contract Addresses for all chains*\n\n'
                f'*X7R*\n`{ca.x7r}`\n\n'
                f'*X7DAO*\n`{ca.x7dao}`\n\n'
                f'*X7101*\n`{ca.x7101}`\n\n'
                f'*X7102*\n`{ca.x7102}`\n\n'
                f'*X7103*\n`{ca.x7103}`\n\n'
                f'*X7104*\n`{ca.x7104}`\n\n'
                f'*X7105*\n`{ca.x7105}`\n\n'
                f'*X7D*\n`{ca.x7d}`\n\n{api.get_quote()}',
        parse_mode='Markdown')


async def x7d_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    supply = ""
    holders = ""
    x7d_dollar = ""
    chain_name = ""
    chain_url = ""
    if chain == "" or chain == "eth":
        supply = api.get_native_balance(ca.lpool_reserve, "eth")
        holders = api.get_holders(ca.x7d)
        x7d_dollar = float(supply) * float(api.get_native_price("eth")) / 1 ** 18
        chain_name = "(ETH)"
        chain_url = url.ether_address
    if chain == "bsc" or chain == "bnb":
        supply = api.get_native_balance(ca.lpool_reserve, "bnb")
        x7d_dollar = float(supply) * float(api.get_native_price("bnb")) / 1 ** 18
        chain_name = "(BSC)"
        chain_url = url.bsc_address
    if chain == "polygon" or chain == "poly":
        supply = api.get_native_balance(ca.lpool_reserve, "poly")
        x7d_dollar = float(supply) * float(api.get_native_price("matic")) / 1 ** 18
        chain_name = "(POLYGON)"
        chain_url = url.poly_address
    if chain == "optimism" or chain == "opti":
        supply = api.get_native_balance(ca.lpool_reserve, "opti")
        x7d_dollar = float(supply) * float(api.get_native_price("eth")) / 1 ** 18
        chain_name = "(OPTIMISM)"
        chain_url = url.opti_address
    if chain == "arbitrum" or chain == "arb":
        supply = api.get_native_balance(ca.lpool_reserve, "arb")
        x7d_dollar = float(supply) * float(api.get_native_price("eth")) / 1 ** 18
        chain_name = "(ARB)"
        chain_url = url.arb_address
    im1 = Image.open((random.choice(media.blackhole)))
    im2 = Image.open(media.x7d_logo)
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 18)
    i1.text((28, 36),
            f'X7D {chain_name} Info\n\n'
            f'Supply: {supply[:5]} X7D (${"{:0,.0f}".format(x7d_dollar)})\n'
            f'Holders: {holders}\n\n'
            f'To receive X7D:\n'
            '1. Send ETH (Not Swap) to the Lending Pool Reserve Contract:\n'
            f'{ca.lpool_reserve}\n\n'
            '2. Import the X7D contract address to your custom tokens in your wallet\nto see your tokens:\n'
            f'{ca.x7d}\n\nYou will receive X7D in your wallet which has a 1:1 price X7D:ETH\n\n'
            'Note:\n'
            'Do not interact directly with the X7D contract\n'
            'Do not send from a CEX\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await update.message.reply_photo(
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'*X7D {chain_name} Info*\n'
                f'For other chains use `/x7d [chain-name]`\n\n'
                f'Supply: {supply[:5]} X7D (${"{:0,.0f}".format(x7d_dollar)})\n'
                f'Holders: {holders}\n\n'
                f'To receive X7D:\n\n'
                '1. Send ETH (Not Swap) to the Lending Pool Reserve Contract:\n'
                f'`{ca.lpool_reserve}`\n\n'
                '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n'
                f'`{ca.x7d}`\n\nYou will receive X7D in your wallet which has a 1:1 price X7D:ETH\n\n'
                'Note:\n'
                'Do not interact directly with the X7D contract\n'
                'Do not send from a CEX\n\n'
                f'{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='X7 Lending Pool Reserve Contract',
                                   url=f'{chain_url}{ca.lpool_reserve}#code')],
             [InlineKeyboardButton(text='X7 Deposit Contract',
                                   url=f'{chain_url}{ca.x7d}#code')], ]))


async def media_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Media Links*\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='X7 Official Images', url='https://imgur.com/a/WEszZTa')],
             [InlineKeyboardButton(text='X7 Official Token Logos Pack 1', url='https://t.me/X7announcements/58')],
             [InlineKeyboardButton(text='X7 Official Token Logos Pack 2', url='https://t.me/X7announcements/141')],
             [InlineKeyboardButton(text='X7 TG Sticker Pack 1', url='https://t.me/addstickers/x7financestickers')],
             [InlineKeyboardButton(text='X7 TG Sticker Pack 2', url='https://t.me/addstickers/X7finance')],
             [InlineKeyboardButton(text='X7 TG Sticker Pack 3', url='https://t.me/addstickers/x7financ')],
             [InlineKeyboardButton(text='X7 TG Sticker Pack 4', url='https://t.me/addstickers/GavalarsX7')],
             [InlineKeyboardButton(text='X7 Emojis Pack', url='https://t.me/addemoji/x7FinanceEmojis')], ]))


async def buy_evenly_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '*Buy All X7 Finance Constellation Tokens Evenly (ETH)*\n\n'
        'Simply connect to https://dapp.x7community.space/constellation via metamask mobile or desktop'
        ' and enter your desired Eth amount\n\n'
        'Alternatively you can interact with the follow contract and follow the steps '
        'below:\n\n'
        '1. Head over to the Buy Evenly contract:\nhttps://etherscan.io/address/0x0419074afe1a137dfa6afd5b6af5'
        '771c3ffbea49#code\n'
        '1.1. Press on "Contract" If it\'s not already selected.\n2. Press on "Write contract"\n'
        '3. Press on "Connect to Web3" and connect your desired wallet to the website. \n'
        '4. Deposit the desired values\n4.1. depositIntoX7SeriesTokens -> amount of ETH you want to spend (e.g. 0.5).\n'
        '4.2. slippagePercent  -> desired slippage (e.g. 4)\n4.3 deadline -> Go to [epoch-converter]'
        '(https://www.epochconverter.com/) and add like 500 to the current epoch. Click "Timestamp to Human date" '
        'and verify that Relative is at least "In 1 minute" (e.g. 1667508502).\n'
        '4.4 Copy the epoch to the "deadline" field\n4.4 Press "Write" and confirm the transaction in your wallet.\n'
        '4.5 You should receive tokens to your wallet in few blocks.\n\n'
        '*Testrun TX*:\n'
        'https://etherscan.io/tx/0x321e5bb6cc1695d5d7085eceb92f01143b69c2274402aab46e4a0a47d069d0af\n\n'
        f'Credit: @WoxieX\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Via Dashboard', url='https://dapp.x7community.space/')],
             [InlineKeyboardButton(text='Via Etherscan', url='https://etherscan.io/address/0x0419074afe1a'
                                                             '137dfa6afd5b6af5771c3ffbea49#code')],
             [InlineKeyboardButton(text='Epoch Convertor', url='https://www.epochconverter.com/')], ]))


async def channels_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Community TG Channels*\n\n{api.get_quote()}', parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Community Chat', url='https://t.me/X7m105portal')],
             [InlineKeyboardButton(text='Announcements', url='https://t.me/X7announcements')],
             [InlineKeyboardButton(text='Media', url='https://t.me/X7MediaChannel')],
             [InlineKeyboardButton(text='Research Notes', url='https://t.me/X7m105_Research')],
             [InlineKeyboardButton(text='Chinese Community', url='https://t.me/X7CNPortal')], ]))


async def buy_bots_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Bobby Buy Bot Channels*\n\n{api.get_quote()}', parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Arbitrum', url='https://t.me/x7arbbuybots')],
             [InlineKeyboardButton(text='BSC', url='https://t.me/x7bscbuybots')],
             [InlineKeyboardButton(text='Optimism', url='https://t.me/x7optibuybots')],
             [InlineKeyboardButton(text='Polygon', url='https://t.me/x7polygonbuybots')], ]))


async def pioneer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pioneer_id = " ".join(context.args)
    data = api.get_os_nft("/x7-pioneer")
    floor = (data["collection"]["stats"]["floor_price"])
    floor_dollar = floor * float(api.get_native_price("eth")) / 1 ** 18
    floor_dollar = floor * float(api.get_native_price("eth")) / 1 ** 18
    traits = (data["collection"]["traits"]["Transfer Lock Status"]["unlocked"])
    cap = round(data["collection"]["stats"]["market_cap"], 2)
    cap_dollar = cap * float(api.get_native_price("eth")) / 1 ** 18
    sales = (data["collection"]["stats"]["total_sales"])
    owners = (data["collection"]["stats"]["num_owners"])
    price = round(data["collection"]["stats"]["average_price"], 2)
    price_dollar = price * float(api.get_native_price("eth")) / 1 ** 18
    volume = round(data["collection"]["stats"]["total_volume"], 2)
    volume_dollar = volume * float(api.get_native_price("eth")) / 1 ** 18
    pioneer_pool = api.get_native_balance(ca.pioneer, "eth")
    total_dollar = float(pioneer_pool) * float(api.get_native_price("eth")) / 1 ** 18
    if pioneer_id == "":
        img = Image.open((random.choice(media.blackhole)))
        i1 = ImageDraw.Draw(img)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 28)
        i1.text((28, 36),
                f'X7 Pioneer NFT Info\n\nFloor Price: {floor} ETH (${"{:0,.0f}".format(floor_dollar)})\n'
                f'Average Price: {price} ETH (${"{:0,.0f}".format(price_dollar)})\n'
                f'Market Cap: {cap} ETH (${"{:0,.0f}".format(cap_dollar)})\n'
                f'Total Volume: {volume} ETH (${"{:0,.0f}".format(volume_dollar)})\n'
                f'Total Sales: {sales}\n'
                f'Number of Owners: {owners}\n'
                f'Pioneers Unlocked: {traits}\n\n\n'
                f'Pioneer Pool: {pioneer_pool[:3]} ETH (${"{:0,.0f}".format(total_dollar)})\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        img.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*X7 Pioneer NFT Info*\n\nFloor Price: {floor} ETH (${"{:0,.0f}".format(floor_dollar)})\n'
                    f'Average Price: {price} ETH (${"{:0,.0f}".format(price_dollar)})\n'
                    f'Market Cap: {cap} ETH (${"{:0,.0f}".format(cap_dollar)})\n'
                    f'Total Volume: {volume} ETH (${"{:0,.0f}".format(volume_dollar)})\n'
                    f'Number of Owners: {owners}\n'
                    f'Pioneers Unlocked: {traits}\n\n'
                    f'Pioneer Pool: {pioneer_pool[:3]} ETH (${"{:0,.0f}".format(total_dollar)})\n\n'
                    f'{api.get_quote()}',
            parse_mode='markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='X7 Pioneer Dashboard', url='https://x7.finance/x/nft/pioneer')],
                 [InlineKeyboardButton(text='Opensea', url='https://opensea.io/collection/x7-pioneer')], ]))
    else:
        baseurl = "https://api.opensea.io/api/v1/asset/"
        slug = ca.pioneer + "/"
        headers = {"X-API-KEY": keys.os}
        single_url = baseurl + slug + pioneer_id + "/"
        single_response = requests.get(single_url, headers=headers)
        single_data = single_response.json()
        status = (single_data["traits"][0]["value"])
        await update.message.reply_text(
            f'*X7 Pioneer {pioneer_id} NFT Info*\n\n'
            f'Transfer Lock Status: {status}\n\n'
            f'https://opensea.io/assets/ethereum/0x70000299ee8910ccacd97b1bb560e34f49c9e4f7/'
            f'{pioneer_id}\n\n{api.get_quote()}',
            parse_mode='markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='X7 Pioneer Dashboard', url='https://x7.finance/x/nft/pioneer')],
                 [InlineKeyboardButton(text='Opensea', url='https://opensea.io/collection/x7-pioneer')], ]))


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wiki = wikipediaapi.Wikipedia('en')
    keyword = " ".join(context.args)
    page_py = wiki.page(keyword)
    if keyword == "":
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption='Please follow the command with your search')
    if page_py.exists():
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption=f'Your search: {page_py.title}\n\n'
                    f'{(page_py.summary[0:800])}'
                    f'....[continue reading on wiki]({page_py.fullurl})\n\n'
                    f'[Google](https://www.google.com/search?q={keyword})\n'
                    f'[Twitter](https://twitter.com/search?q={keyword}&src=typed_query)\n'
                    f'[Etherscan](https://etherscan.io/search?f=0&q={keyword})\n\n'
                    f'{api.get_quote()}',
            parse_mode="markdown")

    else:
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption=f'Your search: {keyword}\n\nNo description available\n\n'
                    f'[Google](https://www.google.com/search?q={keyword})\n'
                    f'[Twitter](https://twitter.com/search?q={keyword}&src=typed_query)\n'
                    f'[Etherscan](https://etherscan.io/search?f=0&q={keyword})\n\n'
                    f'{api.get_quote()}',
            parse_mode="markdown")


async def pool_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    eth_pool = api.get_native_balance(ca.lpool_reserve, "eth")
    pool_dollar = float(eth_pool) * float(api.get_native_price("eth")) / 1 ** 18
    bsc_pool = api.get_native_balance(ca.lpool_reserve, "bsc")
    bsc_pool_dollar = float(bsc_pool) * float(api.get_native_price("bnb")) / 1 ** 18
    arb_pool = api.get_native_balance(ca.lpool_reserve, "arb")
    arb_pool_dollar = float(arb_pool) * float(api.get_native_price("eth")) / 1 ** 18
    poly_pool = api.get_native_balance(ca.lpool_reserve, "poly")
    poly_pool_dollar = float(poly_pool) * float(api.get_native_price("matic")) / 1 ** 18
    opti_pool = api.get_native_balance(ca.lpool_reserve, "opti")
    opti_pool_dollar = float(opti_pool) * float(api.get_native_price("eth")) / 1 ** 18
    total_dollar = poly_pool_dollar + bsc_pool_dollar + opti_pool_dollar + arb_pool_dollar + pool_dollar
    if chain == "":
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7d_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 28)
        i1.text((28, 36),
                f'X7 Finance Lending Pool Info\n\n'
                f'ETH: {eth_pool[:5]} ETH (${"{:0,.0f}".format(pool_dollar)})\n'
                f'ARB: {arb_pool[:4]} ETH (${"{:0,.0f}".format(arb_pool_dollar)})\n'
                f'OPTI: {opti_pool[:4]} ETH (${"{:0,.0f}".format(opti_pool_dollar)})\n'
                f'BSC: {bsc_pool[:4]} BNB (${"{:0,.0f}".format(bsc_pool_dollar)})\n'
                f'POLY: {poly_pool[:6]} MATIC (${"{:0,.0f}".format(poly_pool_dollar)})\n\n'
                f'TOTAL: ${"{:0,.0f}".format(total_dollar)}\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*X7 Finance Lending Pool Info *\nUse `/pool [chain-name]` for individual chains\n\n'
                    f'ETH: {eth_pool[:5]} ETH (${"{:0,.0f}".format(pool_dollar)})\n'
                    f'ARB: {arb_pool[:4]} ETH (${"{:0,.0f}".format(arb_pool_dollar)})\n'
                    f'OPTI: {opti_pool[:4]} ETH (${"{:0,.0f}".format(opti_pool_dollar)})\n'
                    f'BSC: {bsc_pool[:4]} BNB (${"{:0,.0f}".format(bsc_pool_dollar)})\n'
                    f'POLY: {poly_pool[:6]} MATIC (${"{:0,.0f}".format(poly_pool_dollar)})\n\n'
                    f'TOTAL: ${"{:0,.0f}".format(total_dollar)}\n\n'
                    f'{api.get_quote()}', parse_mode='Markdown')
    if chain == "eth":
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.eth_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 28)
        i1.text((28, 36),
                f'X7 Finance Lending Pool Info (ETH)\n\n'
                f'{eth_pool[:5]} ETH (${"{:0,.0f}".format(pool_dollar)})\n\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*X7 Finance Lending Pool Info (ETH)*\nUse `/pool [chain-name]` for other chains\n\n'
                    f'{eth_pool[:5]} ETH (${"{:0,.0f}".format(pool_dollar)})\n\n'
                    f'{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='Lending Pool Reserve Contract',
                                       url=f'{url.ether_address}{ca.lpool_reserve}')],
                 [InlineKeyboardButton(text='X7 Deposit Contract',
                                       url=f'{url.ether_address}{ca.x7d}#code')], ]))
    if chain == "bsc" or chain == "bnb":
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.bsc_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 28)
        i1.text((28, 36),
                f'X7 Finance Lending Pool Info (BSC)\n\n'
                f'{bsc_pool[:4]} BNB (${"{:0,.0f}".format(bsc_pool_dollar)})\n\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*X7 Finance Lending Pool Info (BSC)*\nUse `/pool [chain-name]` for other chains\n\n'
                    f'{bsc_pool[:4]} BNB (${"{:0,.0f}".format(bsc_pool_dollar)})\n\n'
                    f'{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='Lending Pool Reserve Contract',
                                       url=f'{url.bsc_address}{ca.lpool_reserve}')],
                 [InlineKeyboardButton(text='X7 Deposit Contract',
                                       url=f'{url.bsc_address}{ca.x7d}#code')], ]))
    if chain == "arbitrum" or chain == "arb":
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.arb_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 28)
        i1.text((28, 36),
                f'X7 Finance Lending Pool Info (ARB)\n\n'
                f'{arb_pool[:4]} ETH (${"{:0,.0f}".format(arb_pool_dollar)})\n\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*X7 Finance Lending Pool Info (ARB)*\nUse `/pool [chain-name]` for other chains\n\n'
                    f'{arb_pool[:4]} ETH (${"{:0,.0f}".format(arb_pool_dollar)})\n\n'
                    f'{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='Lending Pool Reserve Contract',
                                       url=f'{url.arb_address}{ca.lpool_reserve}')],
                 [InlineKeyboardButton(text='X7 Deposit Contract',
                                       url=f'{url.arb_address}{ca.x7d}#code')], ]))
    if chain == "optimism" or chain == "opti":
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.opti_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 28)
        i1.text((28, 36),
                f'X7 Finance Lending Pool Info (OPTIMISM)\n\n'
                f'{opti_pool[:4]} ETH (${"{:0,.0f}".format(opti_pool_dollar)})\n\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*X7 Finance Lending Pool Info (OPTIMISM)*\nUse `/pool [chain-name]` for other chains\n\n'
                    f'{opti_pool[:4]} ETH (${"{:0,.0f}".format(opti_pool_dollar)})\n\n'
                    f'{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='Lending Pool Reserve Contract',
                                       url=f'{url.opti_address}{ca.lpool_reserve}')],
                 [InlineKeyboardButton(text='X7 Deposit Contract',
                                       url=f'{url.opti_address}{ca.x7d}#code')], ]))
    if chain == "polygon" or chain == "poly":
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.poly_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 28)
        i1.text((28, 36),
                f'X7 Finance Lending Pool Info (POLYGON)\n\n'
                f'{poly_pool[:6]} MATIC (${"{:0,.0f}".format(poly_pool_dollar)})\n\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*X7 Finance Lending Pool Info (POLYGON)*\nUse `/pool [chain-name]` for other chains\n\n'
                    f'{poly_pool[:6]} MATIC (${"{:0,.0f}".format(poly_pool_dollar)})\n\n'
                    f'{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='Lending Pool Reserve Contract',
                                       url=f'{url.poly_address}{ca.lpool_reserve}')],
                 [InlineKeyboardButton(text='X7 Deposit Contract',
                                       url=f'{url.poly_address}{ca.x7d}#code')], ]))


async def tax_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Tax Info*\n\n'
                f'X7R: 6%\nX7DAO: 6%\n'
                f'X7101-X7105: 2%\n\n'
                f'*Tax with NFTs*\n'
                f'Liquidity Maxi:\nX7R: 4.50%\n7DAO: 5.10%\nX7101-X7105: 1.00%\n\n'
                f'Ecosystem Maxi:\nX7R: 5.40%\nX7DAO: 5.40%\nX7101-X7105: 1.50%\n\n'
                f'Magister:\nX7R: 4.50%\nX7DAO: 6.00%\nX7101-X7105: 1.50%\n\n{api.get_quote()}',
        parse_mode='Markdown')


async def swap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_sticker(
        sticker=media.swap,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Xchange', url='https://app.x7.finance/#/swap')],
             [InlineKeyboardButton(text='Feedback', url='https://discord.com/channels/101665704'
                                                        '4553617428/1053206402065256498')], ]))


async def spaces_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    then = variables.spaces_time.astimezone(pytz.utc)
    now = datetime.now(timezone.utc)
    duration = then - now
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    if duration < timedelta(0):
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption=f'X7 Finance Twitter space\n\nPlease check back for more details'
            f'\n\n{api.get_quote()}', parse_mode="Markdown")
    else:
        await update.message.reply_sticker(sticker=media.twitter_sticker)
        await update.message.reply_text(
            text=f'Next X7 Finance Twitter space is:\n\n{then.strftime("%A %B %d %Y %I:%M %p")} (UTC)\n\n'
                 f'{int(days[0])} days, {int(hours[0])} hours and {int(minutes[0])} minutes\n\n'
                 f'[Click here]({variables.spaces_link}) to set a reminder!'
                 f'\n\n{api.get_quote()}', parse_mode="Markdown")


async def roadmap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f'Devs are making incremental final progress against all ecosystem deliverables, we expect the '
        f'following order of delivery:\n\n'
        f'1. Whitepaper ✅\n'
        f'2. Pioneer NFT & Reward Pool ✅\n'
        f'3. DEX and Leveraged Initial Liquidity:\n'
        f'3.1. X7D token contract ✅\n'
        f'3.2. A gnosis multi-sig wallet that will be used to manage the X7D token ownership prior to DAO '
        f'control turnover ✅\n'
        f'3.3. Lending pool reserve contract ✅\n'
        f'3.4. v1 lending pool contract ✅\n'
        f'3.5. First three Loan Term NFT contracts ✅\n'
        f'3.6. Lending Pool Discount Authority contract ✅\n'
        f'3.7. XchangeFactory and XchangePair contracts ✅\n'
        f'3.8. V1 XchangeRouter ✅\n'
        f'3.9. V1 XchangeOmniRouter, ✅\n'
        f'4. Lender dApp 🔄\n'
        f'5. X7D minting ✅\n'
        f'6. X7D staking 🔄\n'
        f'7. X7D dApp 🔄\n'
        f'8. Governance contracts 🔄\n'
        f'9. Governance dApp 🔄\n'
        f'X. Initial DAO control turnover 🔄\n\n'
        f'In addition to the above development milestones, the following additional deliveries can be '
        f'expected:\n\n'
        f'*Marketing Materials:*\n'
        f'> Investor deck / summary\n'
        f'> Prettified ecosystem diagrams and explanations\n\n'
        f'*Development Tooling and Documentation:*\n'
        f'> Technical design document for all smart contracts\n'
        f'> Smart contract trust diagram\n'
        f'> Technical User Guide for DAO interactions\n'
        f'> Integration Guide for third party integrations\n'
        f'> Open sourced SDKs for smart contract interactions\n'
        f'> Open sourced testing and development tooling\n\n{api.get_quote()}',
        parse_mode="Markdown")


async def giveaway_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ext = " ".join(context.args)
    excel = r"raffle.csv"
    df = pd.read_csv(excel)
    addresses = list(df.Address)
    last5 = [entry[-5:] for entry in addresses]
    giveaway_time = variables.giveaway_time.astimezone(pytz.utc)
    snapshot1 = variables.snapshot1.astimezone(pytz.utc)
    snapshot2 = variables.snapshot2.astimezone(pytz.utc)
    now = datetime.now(timezone.utc)
    duration = giveaway_time - now
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    if duration < timedelta(0):
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption=f'X7 Finance Giveaway is now closed\n\nPlease check back for more details'
            f'\n\n{api.get_quote()}', parse_mode="Markdown")
    else:
        if ext == "":
            await update.message.reply_photo(
                photo=open((random.choice(media.logos)), 'rb'),
                caption=f'*X7 Finance 20,000 X7R Giveaway!*\n\n'
                        f'X7 Finance Giveaway ends:\n\n{giveaway_time.strftime("%A %B %d %Y %I:%M %p")} (UTC)\n\n'
                        f'{int(days[0])} days, {int(hours[0])} hours and {int(minutes[0])} minutes\n\n'
                        'For every 0.1 X7D minted,1 entry into the draw was generated!\n\n'
                        f'A Snapshot of minters was taken at {snapshot1.strftime("%A %B %d %Y %I:%M %p")} (UTC) '
                        f'and a second was at {snapshot2.strftime("%A %B %d %Y %I:%M %p")} (UTC)\n\n'
                        f'The Diamond hands that have held for the entire duration are in the draw! The more minted, '
                        f'the better the chance!\n\n'
                        'Any withdrawals were deducted from the entries at the second snapshot.\n\n'
                        'To view entries '
                        '[click here](https://github.com/x7finance/telegram-bot/blob/main/raffle.csv)\n\n'
                        f'The draw will be made on {giveaway_time.strftime("%A %B %d %Y %I:%M %p")} (UTC)\n\n'
                        f'Credit: Defi Dipper!'
                        f'\n\n{api.get_quote()}', parse_mode="Markdown")
        if ext == "entries":
            update_utc = variables.giveaway_update.astimezone(pytz.utc)
            await update.message.reply_photo(
                photo=open((random.choice(media.logos)), 'rb'),
                caption=f'The following addresses are in the draw, weighted by minted amount'
                        f' (last 5 digits only):\n\n{last5}\n\nLast updated: '
                        f'{update_utc.strftime("%A %B %d %Y %I:%M %p")} UTC\n\n'
                        f'{api.get_quote()}',
                parse_mode="Markdown")
        if ext == "run":
            chat_admins = await update.effective_chat.get_administrators()
            if update.effective_user in (admin.user for admin in chat_admins):
                await update.message.reply_photo(
                    photo=open((random.choice(media.logos)), 'rb'),
                    caption=f'*X7 Finance 20,000 X7R Giveaway!*\n\n'
                            f'The winner of the *X7 Finance 20,000 X7R Giveaway!* is:\n\n'
                            f'{random.choice(last5)} (last 5 digits only)\n\n'
                            f'Trust no one, trust code. Long live Defi!\n\n{api.get_quote()}',
                    parse_mode="Markdown")
            else:
                await update.message.reply_text(f'{text.mods_only}')


async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joke_response = requests.get('https://v2.jokeapi.dev/joke/Any?safe-mode')
    joke = joke_response.json()
    if joke["type"] == "single":
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption=f'`{joke["joke"]}`',
            parse_mode="Markdown")
    else:
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption=f'`{joke["setup"]}\n\n{joke["delivery"]}`',
            parse_mode="Markdown")


async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = api.get_today()
    today = (random.choice(data["data"]["Events"]))
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'`On this day in {today["year"]}:\n\n{today["text"]}`',
        parse_mode="Markdown")


async def fg_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fear_response = requests.get('https://api.alternative.me/fng/?limit=0')
    fear_data = fear_response.json()
    timestamp0 = float(fear_data["data"][0]["timestamp"])
    localtime0 = datetime.fromtimestamp(timestamp0)
    timestamp1 = float(fear_data["data"][1]["timestamp"])
    localtime1 = datetime.fromtimestamp(timestamp1)
    timestamp2 = float(fear_data["data"][2]["timestamp"])
    localtime2 = datetime.fromtimestamp(timestamp2)
    timestamp3 = float(fear_data["data"][3]["timestamp"])
    localtime3 = datetime.fromtimestamp(timestamp3)
    timestamp4 = float(fear_data["data"][4]["timestamp"])
    localtime4 = datetime.fromtimestamp(timestamp4)
    timestamp5 = float(fear_data["data"][5]["timestamp"])
    localtime5 = datetime.fromtimestamp(timestamp5)
    timestamp6 = float(fear_data["data"][6]["timestamp"])
    localtime6 = datetime.fromtimestamp(timestamp6)
    duration_in_s = float(fear_data["data"][0]["time_until_update"])
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    await update.message.reply_photo(
        photo='https://alternative.me/crypto/fear-and-greed-index.png',
        caption=f'*Market Fear and Greed Index*\n\n'
                f'{fear_data["data"][0]["value"]} - {fear_data["data"][0]["value_classification"]} - '
                f'{localtime0.strftime("%A %B %d")} \n\n'
                f'Change:\n'
                f'{fear_data["data"][1]["value"]} - {fear_data["data"][1]["value_classification"]} - '
                f'{localtime1.strftime("%A %B %d")}\n'
                f'{fear_data["data"][2]["value"]} - {fear_data["data"][2]["value_classification"]} - '
                f'{localtime2.strftime("%A %B %d")}\n'
                f'{fear_data["data"][3]["value"]} - {fear_data["data"][3]["value_classification"]} - '
                f'{localtime3.strftime("%A %B %d")}\n'
                f'{fear_data["data"][4]["value"]} - {fear_data["data"][4]["value_classification"]} - '
                f'{localtime4.strftime("%A %B %d")}\n'
                f'{fear_data["data"][5]["value"]} - {fear_data["data"][5]["value_classification"]} - '
                f'{localtime5.strftime("%A %B %d")}\n'
                f'{fear_data["data"][6]["value"]} - {fear_data["data"][6]["value_classification"]} - '
                f'{localtime6.strftime("%A %B %d")}\n\n'
                f'Next Update:\n'
                f'{int(hours[0])} hours and {int(minutes[0])} minutes\n\n{api.get_quote()}', parse_mode='Markdown')


async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'{api.get_quote()}',
        parse_mode="Markdown")


async def loans_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loan_type = " ".join(context.args).lower()
    loan_name = ""
    chain_url = ""
    loan_terms = ""
    if loan_type == "":
        await update.message.reply_text(
            '*X7 Finance Loan Terms*\n\n'
            f'Use `/loans ill001 - ill003` for more details on individual loan contracts\n\n'
            'Loan terms are defined by standalone smart contracts that provide the following:\n\n'
            '1. Loan origination fee\n'
            '2. Loan retention premium fee schedule\n'
            '3. Principal repayment condition/maximum loan duration\n'
            '4. Liquidation conditions and Reward\n'
            '5. Loan duration\n\n'
            'The lending process delegates the loan terms to standalone smart contracts (see whitepaper below for more'
            ' details). These loan terms contracts must be deployed, and then “added” or “removed” from the Lending '
            'Pool as “available” loan terms for new loans. The DAO will be able to add or remove these term '
            'contracts.\n\nLoan term contracts may be created by any interested third party, enabling a market '
            'process by which new loan terms may be invented, provided they implement the proper interface.\n\n'
            f'{api.get_quote()}',
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='X7 Finance Whitepaper', url=f'{url.wp_link}')], ]))
    if loan_type == "ill001":
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption=f'{loans.ill001_name}\n\n'
                    f'{loans.ill001_terms}\n\n',
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text=f'Ethereum', url=f'{url.ether_address}{ca.ill001}')],
                 [InlineKeyboardButton(text=f'BSC', url=f'{url.bsc_address}{ca.ill001}')],
                 [InlineKeyboardButton(text=f'Polygon', url=f'{url.poly_address}{ca.ill001}')],
                 [InlineKeyboardButton(text=f'Arbitrum', url=f'{url.arb_address}{ca.ill001}')],
                 [InlineKeyboardButton(text=f'Optimism', url=f'{url.opti_address}{ca.ill001}')],
                 ]))
    if loan_type == "ill002":
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption=f'{loans.ill002_name}\n\n'
                    f'{loans.ill002_terms}\n\n',
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text=f'Ethereum', url=f'{url.ether_address}{ca.ill002}')],
                 [InlineKeyboardButton(text=f'BSC', url=f'{url.bsc_address}{ca.ill002}')],
                 [InlineKeyboardButton(text=f'Polygon', url=f'{url.poly_address}{ca.ill002}')],
                 [InlineKeyboardButton(text=f'Arbitrum', url=f'{url.arb_address}{ca.ill002}')],
                 [InlineKeyboardButton(text=f'Optimism', url=f'{url.opti_address}{ca.ill002}')],
                 ]))
    if loan_type == "ill003":
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption=f'{loans.ill003_name}\n\n'
                    f'{loans.ill003_terms}\n\n',
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text=f'Ethereum', url=f'{url.ether_address}{ca.ill003}')],
                 [InlineKeyboardButton(text=f'BSC', url=f'{url.bsc_address}{ca.ill003}')],
                 [InlineKeyboardButton(text=f'Polygon', url=f'{url.poly_address}{ca.ill003}')],
                 [InlineKeyboardButton(text=f'Arbitrum', url=f'{url.arb_address}{ca.ill003}')],
                 [InlineKeyboardButton(text=f'Optimism', url=f'{url.opti_address}{ca.ill003}')],
                 ]))


async def twitter_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ext = " ".join(context.args)
    auth = tweepy.OAuthHandler(keys.twitterapi, keys.secret)
    auth.set_access_token(keys.access, keys.accesssecret)
    username = '@x7_finance'
    client = tweepy.API(auth)
    tweet = client.user_timeline(screen_name=username, count=1)
    if ext == "":
        await update.message.reply_sticker(sticker=media.twitter_sticker)
        await update.message.reply_text(
            f'Latest X7 Finance Tweet\n\n{tweet[0].text}\n\n'
            f'https://twitter.com/X7_Finance/status/{tweet[0].id}\n\n'
            f'{random.choice(text.twitter_replies)}')
    if ext == "count":
        chat_admins = await update.effective_chat.get_administrators()
        if update.effective_user in (admin.user for admin in chat_admins):
            rt_client = tweepy.Client(keys.bearer)
            rt_auth = tweepy.OAuthHandler(keys.twitterapi, keys.secret)
            rt_auth.set_access_token(keys.access, keys.accesssecret)
            twitterapi = tweepy.API(rt_auth)
            response = rt_client.get_retweeters(tweet[0].id)
            status = twitterapi.get_status(tweet[0].id)
            retweet_count = status.retweet_count
            count = '\n'.join(str(p) for p in response.data)
            await update.message.reply_sticker(sticker=media.twitter_sticker)
            await update.message.reply_text(
                f'Latest X7 Finance Tweet\n\n{tweet[0].text}\n\n'
                f'https://twitter.com/X7_Finance/status/{tweet[0].id}\n\n'
                f'Retweeted {retweet_count} times, by the following members:\n\n{count}')
        else:
            await update.message.reply_text(f'{text.mods_only}')


async def discount_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '*X7 Finance Discount*\n\n'
        '20 Lucrative X7 Borrowing Incentive NFTs have been minted, granting;\n\n'
        '50% Origination fee discount\n'
        '50% Premium fee discount\n\n'
        'These are a consumable utility NFT offering fee discounts when borrowing funds for initial liquidity on '
        'Xchange. The discount will be determined by the X7 Lending Discount Authority smart contract.\n\n'
        'Usage will cause a token owned by the holder to be burned\n\n'
        'To apply for a limited NFT see the link below\n\n'
        ' --------------- \n\n'
        'There are four mechanisms to receive loan origination and premium discounts:\n\n'
        '1. Holding the Borrowing Maxi NFT\n'
        '2. Holding (and having consumed) the Borrowing Incentive NFT\n'
        '3. Borrowing a greater amount\n'
        '4. Borrowing for a shorter time\n\n'
        'All discounts are additive.\n\n'
        'The NFTs provide a fixed percentage discount. The Borrowing Incentive NFT is consumed upon '
        'loan origination.\n\n'
        'The latter two discounts provide a linear sliding scale, based on the minimum and maximum loan amounts and '
        'loan periods. The starting values for these discounts are 0-10% discount.\n\n'
        'The time based discount is imposing an opportunity cost of lent funds - and incentivizing taking out the '
        'shortest loan possible.\n'
        'The amount based discount is recognizing that a loan origination now is more valuable than a possible loan '
        'origination later.\n\nThese sliding scales can be modified to ensure they have optimal market fit.',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Discount Application', url=url.dac)],
             [InlineKeyboardButton(text='X7 Lending Discount Contract',
                                   url=f'{url.ether_address}{ca.lending_discount}#code')], ]))


async def withdraw_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_name = ""
    chain_url = ""
    if chain == "eth" or chain == "":
        chain_name = "(ETH)"
        chain_url = url.ether_address
    if chain == "poly" or chain == "polygon":
        chain_name = "(POLYGON)"
        chain_url = url.poly_address
    if chain == "arb" or chain == "arbitrum":
        chain_name = "(ARB)"
        chain_url = url.arb_address
    if chain == "opti" or chain == "optimism":
        chain_name = "(OPTIMISM)"
        chain_url = url.opti_address
    if chain == "bsc" or chain == "bnb":
        chain_name = "(BSC)"
        chain_url = url.bsc_address
    await update.message.reply_text(
        f'*X7D Withdrawal {chain_name}*\n'
        'For other chains use `/withdraw [chain-name]`\n\n'
        'To Withdraw X7D Head over to the X7 Lending pool reserve contract below and follow the steps:\n\n'
        '1. Write Contract\n'
        '2. Connect to Web3 (This will connect via your chosen wallet)\n'
        '3. Select Function `13. withdrawETH`\n'
        '3. Input your desired amount in wei\n'
        '4. Write\n'
        '5. Confirm TX in chosen wallet\n\n'
        'Note: use command `/wei [amount]` in TG to quickly convert into wei division',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='X7 Lending Pool Reserve', url=f'{chain_url}{ca.lpool_reserve}#code')], ]))


async def say_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    engine = pyttsx3.init()
    engine.save_to_file(" ".join(context.args), 'media/voicenote.mp3')
    engine.runAndWait()
    await update.message.reply_audio(audio=open('media/voicenote.mp3', 'rb'))


async def deployer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deployer = api.get_tx(ca.deployer, "eth")
    date = deployer["result"][0]["block_timestamp"].split("-")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2][:2])
    then = datetime(year, month, day)
    now = datetime.now()
    duration = now - then
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    if deployer["result"][0]['to_address'] == "0x000000000000000000000000000000000000dEaD" or \
            deployer["result"][0]['to_address'] == ca.deployer:
        message = bytes.fromhex(api.get_tx(ca.deployer, "eth")["result"][0]["input"][2:]).decode('utf-8')
        await update.message.reply_text(
            '*X7 Finance DAO Founders*\n\n'
            f'Deployer Wallet last TX -  {int(days[0])} days ago:\n\n'
            f'`{message}`\n\n{url.ether_tx}{deployer["result"][0]["hash"]}',
            parse_mode='Markdown')
    else:
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption='*X7 Finance DAO Founders*\n\n'
                    f'Deployer Wallet last TX -  {int(days[0])} days ago:\n\n'
                    f'{url.ether_tx}{deployer["result"][0]["hash"]}\n\n{api.get_quote()}',
            parse_mode='Markdown')


async def announcements_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption='Check out the link below for the announcement channel',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='X7 Announcement Channel', url="https://t.me/X7announcements")], ]))


async def voting_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '*Proposals and Voting*\n\nVoting will occur in multiple phases, each of which has either a minimum or maximum'
        ' time phase duration.\n\n*Phase 1: Quorum-seeking*\nX7DAO token holders will be able to stake their tokens as '
        'X7sDAO, a non-transferable staked version of X7DAO.\n\nA quorum is reached when more than 50% of circulating '
        'X7DAO has been staked as X7sDAO.\n\nOnce a quorum is reached and a minimum quorum-seeking time period has '
        'passed, the X7sDAO tokens are temporarily locked (and no more X7DAO tokens may be staked until the next Quorum'
        ' seeking period) and the governance process moves to the next phase\n\n*Phase 2: Proposal creation*\nA '
        'proposal is created by running a transaction on the governance contract which specifies a specific transaction'
        ' on a specific contract (e.g. setFeeNumerator(0) on the X7R token contract).\n\nProposals are ordered, and any'
        ' proposals that are passed/adopted must be run in the order that they were created.\n\nProposals can be made '
        'by X7sDAO stakes of 500,000 tokens or more. Additionally, holders of Magister tokens may make proposals. '
        'Proposals may require a refundable proposal fee to prevent process griefing.\n\n*Phase 3: Proposal voting*\n'
        'Each proposal may be voted on once by each address. The voter may specify the weight of their vote between 0 '
        'and the total amount of X7sDAO they have staked.\n\nProposals pass by a majority vote of the quorum of X7sDAO '
        'tokens.\n\nA parallel voting process will occur with Magister tokens, where each Magister token carries one '
        'vote.\n\nIf a majority of magister token holders vote against a proposal, the proposal must reach an X7sDAO '
        'vote of 75% of the quorum of X7sDAO tokens.\n\n*Phase 4: Proposal adoption*\nDuring this phase, proposals that'
        ' have passed will be enqueued for execution. This step ensures proper ordering and is a guard against various '
        'forms of process griefing.\n\n*Phase 5: Proposal execution*\nAfter proposal adoption, all passed proposals '
        f'must be executed before a new Quorum Seeking phase may commence.\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url='https://x7.finance')],
            [InlineKeyboardButton(text='X7 Finance Whitepaper', url='https://x7.finance/whitepaper')], ]))


async def snapshot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_sticker(sticker=media.chains)
    await update.message.reply_text(
        f'*X7 Finance Airdrop Information*\n\nThe rollout of the Ecosystem Contracts on BNB Smart Chain, Polygon ' 
        f'(MATIC), Arbitrum, and Optimism has begun.\n\n'
        f'We will go live with Xchange, borrowing, lending, revenue ' 
        f'splitting, and profit splitting on other chains as soon as we can in concert with the full release on ' 
        f'Ethereum.\n\nThe tokens however will not go live until we have built up a sufficient amount of initial ' 
        f'liquidity for the tokens on any particular chain.\n\nWhen the tokens do go live all X7 token holders on ' 
        f'Ethereum will be airdropped vested tokens and/or be given an opportunity to take a cash payout for their ' 
        f'share of tokens. We will set prices and payouts to ensure that there will be no incentive to exit an ' 
        f'Ethereum X7 Token position in order to gain an "early" L1 or L2 ecosystem X7 token position. On the ' 
        f'contrary, the more tokens held on Ethereum, the greater the reward will be when the tokens and ecosystem ' 
        f'are released on other chains.\n\nThese airdrop snapshots will occur just prior to the token launch\n\n'
        f'{api.get_quote()}', parse_mode='Markdown')


async def gas_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_name = ""
    chain_url = ""
    gas_data = ""
    im2 = ""
    if chain == "" or chain == "eth":
        gas_data = api.get_gas("eth")
        im2 = Image.open(media.eth_logo)
        chain_name = "(ETH)"
        chain_url = "https://etherscan.io/gastracker"
    if chain == "bsc":
        gas_data = api.get_gas("bsc")
        im2 = Image.open(media.bsc_logo)
        chain_name = "(BSC)"
        chain_url = "https://bscscan.com/gastracker"
    if chain == "polygon" or chain == "poly":
        gas_data = api.get_gas("poly")
        im2 = Image.open(media.poly_logo)
        chain_name = "(POLYGON)"
        chain_url = 'https://polygon.com/gastracker'
    im1 = Image.open((random.choice(media.blackhole)))
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
    i1 = ImageDraw.Draw(im1)
    i1.text((26, 30),
            f'{chain_name} Gas Prices:\n\n'
            f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n'
            f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n'
            f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n\n\n\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await update.message.reply_photo(
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'*{chain_name} Gas Prices:*\n'
                f'For other chains use `/gas [chain-name]`\n\n'
                f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n'
                f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n'
                f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n'
                f'{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text=f'{chain_name} Gas Tracker', url=f'{chain_url}')], ]))


async def count_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tweet = context.args[0]
    start = tweet.index('status/')
    end = tweet.index('?', start + 1)
    tweet_id = tweet[start + 7:end]
    rt_client = tweepy.Client(keys.bearer)
    rt_auth = tweepy.OAuthHandler(keys.twitterapi, keys.secret)
    rt_auth.set_access_token(keys.access, keys.accesssecret)
    twitterapi = tweepy.API(rt_auth)
    rt_response = rt_client.get_retweeters(tweet_id)
    status = twitterapi.get_status(tweet_id)
    retweet_count = status.retweet_count
    rt_names = '\n'.join(str(p) for p in rt_response.data)
    await update.message.reply_sticker(sticker=media.twitter_sticker)
    await update.message.reply_text(
        f'Retweeted {retweet_count} times, by the following members:\n\n{rt_names}')


async def draw_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tweet = context.args[0]
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        start = tweet.index('status/')
        end = tweet.index('?', start + 1)
        tweet_id = tweet[start + 7:end]
        rt_client = tweepy.Client(keys.bearer)
        rt_auth = tweepy.OAuthHandler(keys.twitterapi, keys.secret)
        rt_auth.set_access_token(keys.access, keys.accesssecret)
        twitterapi = tweepy.API(rt_auth)
        response = rt_client.get_retweeters(tweet_id)
        status = twitterapi.get_status(tweet_id)
        retweet_count = status.retweet_count
        count = '\n'.join(str(p) for p in response.data)
        await update.message.reply_sticker(sticker=media.twitter_sticker)
        await update.message.reply_text(
            f'{retweet_count} Entries:\n\n{count}')
        await update.message.reply_text(f'The Winner is....\n\n{random.choice(response.data)}\n\n'
                                        f'Congratulations, Please DM @X7_Finance to verify your account')
    else:
        await update.message.reply_text(f'{text.mods_only}')


async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    west_coast_raw = pytz.timezone("America/Los_Angeles")
    west_coast = datetime.now(west_coast_raw)
    west_coast_time = west_coast.strftime("%I:%M %p")
    east_coast_raw = pytz.timezone("America/New_York")
    east_coast = datetime.now(east_coast_raw)
    east_coast_time = east_coast.strftime("%I:%M %p")
    london_raw = pytz.timezone("Europe/London")
    london = datetime.now(london_raw)
    london_time = london.strftime("%I:%M %p")
    berlin_raw = pytz.timezone("Europe/Berlin")
    berlin = datetime.now(berlin_raw)
    berlin_time = berlin.strftime("%I:%M %p")
    tokyo_raw = pytz.timezone("Asia/Tokyo")
    tokyo = datetime.now(tokyo_raw)
    tokyo_time = tokyo.strftime("%I:%M %p")
    dubai_raw = pytz.timezone("Asia/Dubai")
    dubai = datetime.now(dubai_raw)
    dubai_time = dubai.strftime("%I:%M %p")
    await update.message.reply_text(f'GM or GN Wherever you are...\n\n'
                                    f'{datetime.now(timezone.utc).strftime("%A %B %d %Y")}\n'
                                    f'{datetime.now(timezone.utc).strftime("%I:%M %p")} - UTC\n\n'
                                    f'{west_coast_time} - PST\n'
                                    f'{east_coast_time} - EST\n'
                                    f'{london_time} - GMT\n'
                                    f'{berlin_time} - CET\n'
                                    f'{dubai_time} - GST\n'
                                    f'{tokyo_time} - JST\n',
                                    parse_mode="Markdown")


async def wei_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    eth = " ".join(context.args)
    wei_raw = float(eth)
    wei = wei_raw * 10 ** 18
    await update.message.reply_text(
        f'{eth} ETH is equal to \n\n'
        f'`{wei:.0f}` wei',
        parse_mode="Markdown")


async def dashboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Dashboard*\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Live', url='https://www.x7finance.org/')],
            [InlineKeyboardButton(text='Docs', url='https://www.x7finance.org/docs/')],
            [InlineKeyboardButton(text='On-Chains', url='https://www.x7finance.org/onchains')],
            [InlineKeyboardButton(text='Contracts', url='https://www.x7finance.org/contracts/')],
            [InlineKeyboardButton(text='Loans', url='https://www.x7finance.org/loans/')],
            [InlineKeyboardButton(text='Community',
                                  url='https://www.x7finance.org/community/')],
            [InlineKeyboardButton(text='NFTs', url='https://www.x7finance.org/nfts/')],
            [InlineKeyboardButton(text='Whitepaper', url='https://www.x7finance.org/whitepaper/')],
            [InlineKeyboardButton(text='FAQs', url='https://www.x7finance.org/faq/')], ]))


async def faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance FAQ*\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Constellation Tokens', url='https://www.x7finance.org/faq/constellations')],
            [InlineKeyboardButton(text='Developer Questions', url='https://www.x7finance.org/faq/devs')],
            [InlineKeyboardButton(text='General Questions', url='https://www.x7finance.org/faq/general')],
            [InlineKeyboardButton(text='Governance Questions', url='https://www.x7finance.org/faq/governance')],
            [InlineKeyboardButton(text='Investor Questions', url='https://www.x7finance.org/faq/investors')],
            [InlineKeyboardButton(text='Liquidity Lending Questions',
                                  url='https://www.x7finance.org/faq/liquiditylending')],
            [InlineKeyboardButton(text='NFT Questions', url='https://www.x7finance.org/faq/nfts')],
            [InlineKeyboardButton(text='Xchange Questions', url='https://www.x7finance.org/faq/xchange')], ]))


async def holders_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    x7dao_holders = api.get_holders(ca.x7dao)
    x7r_holders = api.get_holders(ca.x7r)
    img = Image.open((random.choice(media.blackhole)))
    i1 = ImageDraw.Draw(img)
    myfont = ImageFont.truetype(R'media\FreeMonoBold.ttf', 28)
    i1.text((28, 36),
            f'X7 Finance Token Holders (ETH)\n\n'
            f'X7R Holders: {x7r_holders}\n'
            f'X7DAO Holders: {x7dao_holders}\n\n\n\n\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont, fill=(255, 255, 255))
    img.save(r"media\blackhole.png")
    await update.message.reply_photo(
        photo=open(r'media\blackhole.png', 'rb'),
        caption=f'*X7 Finance Token Holders (ETH)*\n\n'
                f'X7R Holders: {x7r_holders}\n'
                f'X7DAO Holders: {x7dao_holders}\n\n'
                f'{api.get_quote()}',
        parse_mode='Markdown')


async def alumni_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Alumni*\n\n'
                f'@Callmelandlord - The Godfather of the X7 Finance community, the OG, the creator - X7 God\n\n'
                f'@WoxieX - Creator of the OG dashboard -  x7community.space\n\n'
                f'@Zaratustra  - Defi extraordinaire and protocol prophet\n\n'
                f'{api.get_quote()}', parse_mode='Markdown')


async def magisters_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_name = ""
    chain_url = ""
    response = ""
    holders = ""
    if chain == "eth" or chain == "":
        response = api.get_nft_holder_list(ca.magister, "eth")
        chain_name = "(ETH)"
        chain_url = url.ether_address
        holders = api.get_nft_holder_count(ca.magister, "?chain=eth-main")
    if chain == "bsc" or chain == "bnb":
        response = api.get_nft_holder_list(ca.magister, "bsc")
        chain_name = "(BSC)"
        chain_url = url.bsc_address
    if chain == "polygon" or chain == "poly":
        response = api.get_nft_holder_list(ca.magister, "polygon")
        chain_name = "(POLYGON)"
        chain_url = url.poly_address
        holders = api.get_nft_holder_count(ca.magister, "?chain=poly-main")
    if chain == "optimism" or chain == "opti":
        response = api.get_nft_holder_list(ca.magister, "optimism")
        chain_name = "(OPTIMISM)"
        chain_url = url.opti_address
        holders = api.get_nft_holder_count(ca.magister, "?chain=optimism-main")
    if chain == "arbitrum" or chain == "arb":
        response = api.get_nft_holder_list(ca.magister, "arbitrum")
        chain_name = "(ARB)"
        chain_url = url.arb_address
        holders = api.get_nft_holder_count(ca.magister, "?chain=arbitrum")
    magisters = list(map(lambda x: x['owner_of'], response["result"]))
    address = '\n\n'.join(map(str, magisters))
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Magister Holders {chain_name}*\n'
                'Use `/magisters [chain-name]` or other chains\n\n'
                f'Holders - {holders}\n\n'
                f'`{address}`\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                text='Magister Holder List', url=f'{chain_url}{ca.magister}#balances')], ]))


async def signers_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    dev_response = api.get_signers(ca.dev_multi_eth)
    com_response = api.get_signers(ca.com_multi_eth)
    chain_name = ""
    chain_url = ""
    if chain == "eth" or chain == "":
        dev_response = api.get_signers(ca.dev_multi_eth)
        com_response = api.get_signers(ca.com_multi_eth)
        chain_name = "(ETH)"
        chain_url = url.ether_address
    if chain == "poly" or chain == "polygon":
        dev_response = api.get_signers(ca.dev_multi_poly)
        com_response = api.get_signers(ca.com_multi_poly)
        chain_name = "(POLYGON)"
        chain_url = url.poly_address
    if chain == "bsc" or chain == "bnb":
        dev_response = api.get_signers(ca.dev_multi_bsc)
        com_response = api.get_signers(ca.com_multi_bsc)
        chain_name = "(BSC)"
        chain_url = url.poly_address
    if chain == "arb" or chain == "arbitrum":
        dev_response = api.get_signers(ca.dev_multi_arb)
        com_response = api.get_signers(ca.com_multi_arb)
        chain_name = "(ARB)"
        chain_url = url.arb_address
    if chain == "opti" or chain == "optimism":
        dev_response = api.get_signers(ca.dev_multi_opti)
        com_response = api.get_signers(ca.com_multi_opti)
        chain_name = "(OPTIMISM)"
        chain_url = url.opti_address
    dev_list = dev_response["owners"]
    dev_address = '\n\n'.join(map(str, dev_list))
    com_list = com_response["owners"]
    com_address = '\n\n'.join(map(str, com_list))
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Multi-Sig Singers {chain_name}*\n'
                'Use `/signers [chain-name]` or other chains\n\n'
                f'*Developer Signers*\n`{dev_address}`\n\n*Community Signers*\n`{com_address}`\n\n'
                f'{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='X7 Developer Multi-Sig', url=f'{chain_url}{ca.dev_multi_eth}')],
             [InlineKeyboardButton(text='X7 Community Multi-Sig', url=f'{chain_url}{ca.com_multi_eth}')], ]))


async def launch_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    launch_raw = datetime(2022, 8, 13, 14, 10, 17)
    migration_raw = datetime(2022, 9, 25, 5, 00, 11)
    launch = launch_raw.astimezone(pytz.utc)
    migration = migration_raw.astimezone(pytz.utc)
    now = datetime.now(timezone.utc)
    launch_duration = now - launch
    launch_duration_in_s = launch_duration.total_seconds()
    launch_days = divmod(launch_duration_in_s, 86400)
    launch_hours = divmod(launch_days[1], 3600)
    launch_minutes = divmod(launch_hours[1], 60)
    migration_duration = now - migration
    migration_duration_in_s = migration_duration.total_seconds()
    migration_days = divmod(migration_duration_in_s, 86400)
    migration_hours = divmod(migration_days[1], 3600)
    migration_minutes = divmod(migration_hours[1], 60)
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Launch Info*\n\nX7M105 Stealth Launch\n{launch.strftime("%A %B %d %Y %I:%M %p")} (UTC)\n'
                f'{int(launch_days[0])} days, {int(launch_hours[0])} hours and {int(launch_minutes[0])} minutes ago\n\n'
                f'V2 Migration\n{migration.strftime("%A %B %d %Y %I:%M %p")} (UTC)\n'
                f'{int(migration_days[0])} days, {int(migration_hours[0])} hours and '
                f'{int(migration_minutes[0])} minutes ago\n\n'
                f'{api.get_quote()}',
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='X7M105 Launch TX', url=f'https://etherscan.io/tx/'
                                        f'0x11ff5b6a860170eaac5b33930680bf79dbf0656292cac039805dbcf34e8abdbf')],
             [InlineKeyboardButton(text='Migration Go Live TX', url=f'https://etherscan.io/tx/'
                                        f'0x13e8ed59bcf97c5948837c8069f1d61e3b0f817d6912015427e468a77056fe41')], ]))


async def potw_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption='*Pioneer of the week*\n\n'
                'The following Pioneers have shown exemplary contributions towards X7 Finance\n\n'
                'Week 15 - @Ahmed812007\n\n'
                f'{api.get_quote()}', parse_mode="Markdown")


async def supply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prices = api.get_cg_price("x7r, x7dao, x7101, x7102, x7103, x7104, x7105")
    x7r = api.get_token_balance(ca.x7r_pair_eth, "eth", ca.x7r)
    x7dao = api.get_token_balance(ca.x7dao_pair_eth, "eth", ca.x7dao)
    x7101 = api.get_token_balance(ca.x7101_pair_eth, "eth", ca.x7101)
    x7102 = api.get_token_balance(ca.x7102_pair_eth, "eth", ca.x7102)
    x7103 = api.get_token_balance(ca.x7103_pair_eth, "eth", ca.x7103)
    x7104 = api.get_token_balance(ca.x7104_pair_eth, "eth", ca.x7104)
    x7105 = api.get_token_balance(ca.x7105_pair_eth, "eth", ca.x7105)
    x7r_dollar = x7r * prices["x7r"]["usd"]
    x7dao_dollar = x7dao * prices["x7dao"]["usd"]
    x7101_dollar = x7101 * prices["x7101"]["usd"]
    x7102_dollar = x7102 * prices["x7102"]["usd"]
    x7103_dollar = x7103 * prices["x7103"]["usd"]
    x7104_dollar = x7104 * prices["x7104"]["usd"]
    x7105_dollar = x7105 * prices["x7105"]["usd"]
    x7r_percent = round(x7r / ca.supply * 100, 2)
    x7dao_percent = round(x7dao / ca.supply * 100, 2)
    x7101_percent = round(x7101 / ca.supply * 100, 2)
    x7102_percent = round(x7102 / ca.supply * 100, 2)
    x7103_percent = round(x7103 / ca.supply * 100, 2)
    x7104_percent = round(x7104 / ca.supply * 100, 2)
    x7105_percent = round(x7105 / ca.supply * 100, 2)
    img = Image.open((random.choice(media.blackhole)))
    i1 = ImageDraw.Draw(img)
    myfont = ImageFont.truetype(R'media\FreeMonoBold.ttf', 22)
    i1.text((28, 36),
            f'X7 Finance Uniswap Supply\n\n'
            f'X7R: {"{:0,.0f}".format(x7r)} X7R (${"{:0,.0f}".format(x7r_dollar)}) {x7r_percent}%\n\n'
            f'X7DAO: {"{:0,.0f}".format(x7dao)} X7DAO (${"{:0,.0f}".format(x7dao_dollar)}) {x7dao_percent}%\n\n'
            f'X7101: {"{:0,.0f}".format(x7101)} X7101 (${"{:0,.0f}".format(x7101_dollar)}) {x7101_percent}%\n\n'
            f'X7102: {"{:0,.0f}".format(x7102)} X7102 (${"{:0,.0f}".format(x7102_dollar)}) {x7102_percent}%\n\n'
            f'X7103: {"{:0,.0f}".format(x7103)} X7103 (${"{:0,.0f}".format(x7103_dollar)}) {x7103_percent}%\n\n'
            f'X7104: {"{:0,.0f}".format(x7104)} X7104 (${"{:0,.0f}".format(x7104_dollar)}) {x7104_percent}%\n\n'
            f'X7105: {"{:0,.0f}".format(x7105)} X7105 (${"{:0,.0f}".format(x7105_dollar)}) {x7105_percent}%\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont, fill=(255, 255, 255))
    img.save(r"media\blackhole.png")
    await update.message.reply_photo(
            photo=open(r'media\blackhole.png', 'rb'),
            caption=f'*X7 Finance Uniswap Supply*\n\n'
                    f'*X7R*\n'
                    f'{"{:0,.0f}".format(x7r)} X7R (${"{:0,.0f}".format(x7r_dollar)}) {x7r_percent}%\n\n'
                    f'*X7DAO*\n'
                    f'{"{:0,.0f}".format(x7dao)} X7DAO (${"{:0,.0f}".format(x7dao_dollar)}) {x7dao_percent}%\n\n'
                    f'*X7101*\n'
                    f'{"{:0,.0f}".format(x7101)} X7101 (${"{:0,.0f}".format(x7101_dollar)}) {x7101_percent}%\n\n'
                    f'*X7102*\n'
                    f'{"{:0,.0f}".format(x7102)} X7102 (${"{:0,.0f}".format(x7102_dollar)}) {x7102_percent}%\n\n'
                    f'*X7103*\n'
                    f'{"{:0,.0f}".format(x7103)} X7103 (${"{:0,.0f}".format(x7103_dollar)}) {x7103_percent}%\n\n'
                    f'*X7104*\n'
                    f'{"{:0,.0f}".format(x7104)} X7104 (${"{:0,.0f}".format(x7104_dollar)}) {x7104_percent}%\n\n'
                    f'*X7105*\n'
                    f'{"{:0,.0f}".format(x7105)} X7105 (${"{:0,.0f}".format(x7105_dollar)}) {x7105_percent}%\n\n'
                    f'{api.get_quote()}', parse_mode="Markdown")


# CG COMMANDS
async def x7r_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    dollar = chain.startswith("$")
    price = api.get_cg_price("x7r")
    if price["x7r"]["usd_24h_change"] is None:
        price["x7r"]["usd_24h_change"] = 0
    if dollar:
        amount = round(float(chain[1:]) / float(price["usd"]), 2)
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7r_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((26, 30),
                f'X7R Info (ETH)\n\n'
                f'{chain} is currently worth:\n\n{"{:0,.0f}".format(amount)} '
                f'X7R (ETH) Tokens (before tax)\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'{chain} is currently worth:\n\n{"{:0,.0f}".format(amount)} '
                    f'X7R (ETH) Tokens (Before Tax)\n\n{api.get_quote()}',
            parse_mode='Markdown')
    if chain.isdigit():
        amount = float(chain) * float(price["x7r"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7r_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((26, 30),
                f'X7R Info (ETH)\n\n'
                f'{chain} X7R (ETH) Currently Costs:\n\n${"{:0,.0f}".format(amount)}\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'{chain} X7R (ETH) Currently Costs:\n\n${"{:0,.0f}".format(amount)}'
                    f'\n\n{api.get_quote()}',
            parse_mode='Markdown')
    if chain == "" or chain == "eth":
        holders = api.get_holders(ca.x7r)
        burn = api.get_token_balance(ca.dead, "eth", ca.x7r)
        percent = round(((burn / ca.supply) * 100), 6)
        x7r = api.get_liquidity(ca.x7r_pair_eth)
        x7r_token = float(x7r["reserve0"])
        x7r_weth = float(x7r["reserve1"]) / 10 ** 18
        x7r_weth_dollar = float(x7r_weth) * float(api.get_native_price("eth"))
        x7r_token_dollar = float(price["x7r"]["usd"]) * float(x7r_token) / 10 ** 18
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7r_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(R'media\FreeMonoBold.ttf', 28)
        im1.save(r"media\blackhole.png", quality=95)
        i1 = ImageDraw.Draw(im1)
        i1.text((26, 30),
                f'X7R Info (ETH)\n\n'
                f'X7R Price: ${price["x7r"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7r"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(price["x7r"]["usd"] * ca.supply)}\n'
                f'24 Hour Volume: ${"{:0,.0f}".format(price["x7r"]["usd_24h_vol"])}\n'
                f'Holders: {holders}\n\n'
                f'Liquidity:\n'
                f'{"{:0,.0f}".format(x7r_token)[:4]}M X7R (${"{:0,.0f}".format(x7r_token_dollar)})\n'
                f'{"{:0,.0f}".format(x7r_weth)} WETH (${"{:0,.0f}".format(x7r_weth_dollar)})\n'
                f'Total Liquidity ${"{:0,.0f}".format(x7r_weth_dollar + x7r_token_dollar)}\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*X7R Info (ETH)*\nUse `/x7r [chain-name]` for other chains\n\n'
                    f'X7R Price: ${price["x7r"]["usd"]}\n'
                    f'24 Hour Change: {round(price["x7r"]["usd_24h_change"], 1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(price["x7r"]["usd"] * ca.supply)}\n'
                    f'24 Hour Volume: ${"{:0,.0f}".format(price["x7r"]["usd_24h_vol"])}\n'
                    f'Holders: {holders}\n\n'
                    f'X7R Tokens Burned:\n'
                    f'{"{:,}".format(burn)}\n'
                    f'{percent}% of Supply\n\n'
                    f'Liquidity:\n'
                    f'{"{:0,.0f}".format(x7r_token)[:4]}M X7R (${"{:0,.0f}".format(x7r_token_dollar)})\n'
                    f'{"{:0,.0f}".format(x7r_weth)} WETH (${"{:0,.0f}".format(x7r_weth_dollar)})\n'
                    f'Total Liquidity ${"{:0,.0f}".format(x7r_weth_dollar + x7r_token_dollar)}\n\n'
                    f'Contract Address:\n`{ca.x7r}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{url.ether_token}{ca.x7r}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_eth}{ca.x7r_pair_eth}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7r}')], ]))
    if chain == "arb" or chain == "arbitrum":
        await update.message.reply_photo(
            photo=open(media.x7r_logo, 'rb'),
            caption=f'*X7R Info (ARBITRUM)*\nUse `/x7r [chain-name]` for other chains\n\n'
                    f'Contract Address:\n`{ca.x7r}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Arbiscan', url=f'{url.arb_token}{ca.x7r}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_arb}{ca.x7r_pair_arb}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7r}')], ]))
    if chain == "poly" or chain == "polygon":
        await update.message.reply_photo(
            photo=open(media.x7r_logo, 'rb'),
            caption=f'*X7R Info (POLYGON)*\nUse `/x7r [chain-name]` for other chains\n\n'
                    f'Contract Address:\n`{ca.x7r}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Polygonscan', url=f'{url.poly_token}{ca.x7r}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_poly}{ca.x7r_pair_poly}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7r}')], ]))
    if chain == "bsc" or chain == "bnb":
        await update.message.reply_photo(
            photo=open(media.x7r_logo, 'rb'),
            caption=f'*X7R Info (BSC)*\nUse `/x7r [chain-name]` for other chains\n\n'
                    f'Contract Address:\n`{ca.x7r}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='BSCscan', url=f'{url.bsc_token}{ca.x7r}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_bsc}{ca.x7r_pair_bsc}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7r}')], ]))
    if chain == "opti" or chain == "optimism":
        await update.message.reply_photo(
            photo=open(media.x7r_logo, 'rb'),
            caption=f'*X7R Info (OPTIMISM)*\nUse `/x7r [chain-name]` for other chains\n\n'
                    f'Contract Address:\n`{ca.x7r}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Optimistic.etherscan', url=f'{url.opti_token}{ca.x7r}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_opti}{ca.x7r_pair_opti}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7r}')], ]))


async def x7dao_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    dollar = chain.startswith("$")
    price = api.get_cg_price("x7dao")
    if price["x7dao"]["usd_24h_change"] is None:
        price["x7dao"]["usd_24h_change"] = 0
    if dollar:
        amount = float(chain[1:]) / float(price["x7dao"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7dao_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((26, 30),
                f'X7DAO Info (ETH)\n\n'
                f'{chain} is currently worth:\n\n{"{:0,.0f}".format(amount)} '
                f'X7R (ETH) Tokens (before tax)\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'{chain} Is currently worth:\n\n{"{:0,.0f}".format(amount)}'
                    f' X7DAO (ETH) Tokens (before tax)\n\n{api.get_quote()}',
            parse_mode='Markdown')
    if chain == "proposal":
        chain = "500000"
    if chain == "500000":
        amount = float(chain) * float(price["x7dao"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7dao_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((26, 30),
                f'X7DAO Info (ETH)\n\n'
                f'Holding {chain} X7DAO Tokens will earn you\n'
                f'the right to make proposals on X7 DAO dApp\n\n'
                f'{chain} X7DAO (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'Holding {chain} X7DAO Tokens will earn you the right to make proposals on X7 DAO dApp\n\n'
                    f'{chain} X7DAO (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)}\n\n{api.get_quote()}',
            parse_mode='Markdown')
        return
    if chain.isdigit():
        amount = float(chain)*float(price["x7dao"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7dao_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((26, 30),
                f'X7DAO Info (ETH)\n\n'
                f'{chain} X7DAO (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'{chain} X7DAO (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n'
                    f'{api.get_quote()}',
            parse_mode='Markdown')
    if chain == "" or chain == "eth":
        holders = api.get_holders(ca.x7dao)
        x7dao = api.get_liquidity(ca.x7dao_pair_eth)
        x7dao_token = float(x7dao["reserve0"])
        x7dao_weth = float(x7dao["reserve1"]) / 10 ** 18
        x7dao_weth_dollar = float(x7dao_weth) * float(api.get_native_price("eth"))
        x7dao_token_dollar = float(price["x7dao"]["usd"]) * float(x7dao_token) / 10 ** 18
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7dao_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((28, 36),
                f'X7DAO Info (ETH)\n\n'
                f'X7DAO Price: ${price["x7dao"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7dao"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(price["x7dao"]["usd"] * ca.supply)}\n'
                f'24 Hour Volume: ${"{:0,.0f}".format(price["x7dao"]["usd_24h_vol"])}\n'
                f'Holders: {holders}\n\n'
                f'Liquidity:\n'
                f'{"{:0,.0f}".format(x7dao_token)[:4]}M X7DAO (${"{:0,.0f}".format(x7dao_token_dollar)})\n'
                f'{"{:0,.0f}".format(x7dao_weth)} WETH (${"{:0,.0f}".format(x7dao_weth_dollar)})\n'
                f'Total Liquidity ${"{:0,.0f}".format(x7dao_weth_dollar + x7dao_token_dollar)}\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*X7DAO (ETH) Info*\n\n'
            f'X7DAO Price: ${price["x7dao"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7dao"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(price["x7dao"]["usd"] * ca.supply)}\n'
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7dao"]["usd_24h_vol"])}\n'
            f'Holders: {holders}\n\n'
            f'Liquidity:\n'
            f'{"{:0,.0f}".format(x7dao_token)[:4]}M X7DAO (${"{:0,.0f}".format(x7dao_token_dollar)})\n'
            f'{"{:0,.0f}".format(x7dao_weth)} WETH (${"{:0,.0f}".format(x7dao_weth_dollar)})\n'
            f'Total Liquidity ${"{:0,.0f}".format(x7dao_weth_dollar + x7dao_token_dollar)}\n\n'
            f'Contract Address:\n`{ca.x7dao}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{url.ether_token}{ca.x7dao}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_eth}{ca.x7dao_pair_eth}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7dao}')], ]))
    if chain == "bsc" or chain == "bnb":
        await update.message.reply_photo(
            photo=open(media.x7dao_logo, 'rb'),
            caption=f'*X7DAO (BSC) Info*\nUse `/x7dao [chain-name]` for other chains\n\n'
            f'Contract Address:\n`{ca.x7dao}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='BSCscan', url=f'{url.bsc_token}{ca.x7dao}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_bsc}{ca.x7dao_pair_bsc}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7dao}')], ]))
    if chain == "opti" or chain == "optimism":
        await update.message.reply_photo(
            photo=open(media.x7dao_logo, 'rb'),
            caption=f'*X7DAO (OPTIMISM) Info*\nUse `/x7dao [chain-name]` for other chains\n\n'
            f'Contract Address:\n`{ca.x7dao}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Optimistic.etherscan', url=f'{url.opti_token}{ca.x7dao}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_opti}{ca.x7dao_pair_opti}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7dao}')], ]))
    if chain == "arb" or chain == "arbitrum":
        await update.message.reply_photo(
            photo=open(media.x7dao_logo, 'rb'),
            caption=f'*X7DAO (ARBITRUM) Info*\nUse `/x7dao [chain-name]` for other chains\n\n'
            f'Contract Address:\n`{ca.x7dao}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Arbiscan', url=f'{url.arb_token}{ca.x7dao}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_arb}{ca.x7dao_pair_arb}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7dao}')], ]))
    if chain == "poly" or chain == "polygon":
        await update.message.reply_photo(
            photo=open(media.x7dao_logo, 'rb'),
            caption=f'*X7DAO (POLYGON) Info*\nUse `/x7dao [chain-name]` for other chains\n\n'
            f'Contract Address:\n`{ca.x7dao}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Polygonscan', url=f'{url.poly_token}{ca.x7dao}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_poly}{ca.x7dao_pair_poly}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7dao}')], ]))


async def x7101_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    dollar = chain.startswith("$")
    price = api.get_cg_price("x7101")
    if price["x7101"]["usd_24h_change"] is None:
        price["x7101"]["usd_24h_change"] = 0
    if dollar:
        amount = float(chain[1:]) / float(price["x7101"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7101_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((26, 30),
                f'X7101 Info (ETH)\n\n'
                f'{chain} is currently worth:\n\n{"{:0,.0f}".format(amount)} '
                f'X7101 (ETH) Tokens (before tax)\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'{chain} Is currently worth:\n\n{"{:0,.0f}".format(amount)}' 
                    f' X7101 (ETH) Tokens (before tax)\n\n{api.get_quote()}', parse_mode='Markdown')
    if chain.isdigit():
        amount = float(chain)*float(price["x7101"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7101_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((26, 30),
                f'X7101 Info (ETH)\n\n'
                f'{chain} X7101 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'{chain} X7101 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n'
                    f'{api.get_quote()}',
            parse_mode='Markdown')
    if chain == "" or chain == "eth":
        holders = api.get_holders(ca.x7101)
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7101_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 28)
        i1.text((28, 36),
                f'X7101 Info (ETH)\n\n'
                f'X7101 Price: ${price["x7101"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7101"]["usd_24h_change"]),1}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(price["x7101"]["usd"] * ca.supply)}\n'
                f'24 Hour Volume: ${"{:0,.0f}".format(price["x7101"]["usd_24h_vol"])}\n'
                f'Holders: {holders}\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*X7101 (ETH) Info*\nUse `/X7101 [chain-name]` for other chains\n\n'
            f'X7101 Price: ${price["x7101"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7101"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(price["x7101"]["usd"] * ca.supply)}\n'
            f'24 Hour Volume: ${round(price["x7101"]["usd_24h_vol"])}\n'
            f'Holders: {holders}\n\n'
            f'*X7101 Contract*\n`{ca.x7101}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{url.ether_token}{ca.x7101}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_eth}{ca.x7101_pair_eth}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7101}')], ]))
    if chain == "arb" or chain == "arbitrum":
        await update.message.reply_photo(
            photo=open(media.x7101_logo, 'rb'),
            caption=f'*X7101 (ARBITRUM) Info*\nUse `/X7101 [chain-name]` for other chains\n\n'
            f'*X7101 Contract*\n`{ca.x7101}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Arbiscan', url=f'{url.arb_token}{ca.x7101}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_arb}{ca.x7101_pair_arb}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7101}')], ]))
    if chain == "poly" or chain == "polygon":
        await update.message.reply_photo(
            photo=open(media.x7101_logo, 'rb'),
            caption=f'*X7101 (POLYGON) Info*\nUse `/X7101 [chain-name]` for other chains\n\n'
            f'*X7101 Contract*\n`{ca.x7101}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Polygonscan', url=f'{url.poly_token}{ca.x7101}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_poly}{ca.x7101_pair_poly}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7101}')], ]))
    if chain == "bsc" or chain == "bnb":
        await update.message.reply_photo(
            photo=open(media.x7101_logo, 'rb'),
            caption=f'*X7101 (BSC) Info*\nUse `/X7101 [chain-name]` for other chains\n\n'
            f'*X7101 Contract*\n`{ca.x7101}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='BSCscan', url=f'{url.bsc_token}{ca.x7101}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_bsc}{ca.x7101_pair_bsc}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7101}')], ]))
    if chain == "opti" or chain == "optimism":
        await update.message.reply_photo(
            photo=open(media.x7101_logo, 'rb'),
            caption=f'*X7101 (OPTIMISM) Info*\nUse `/X7101 [chain-name]` for other chains\n\n'
            f'*X7101 Contract*\n`{ca.x7101}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Optimistic.etherscan', url=f'{url.opti_token}{ca.x7101}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_opti}{ca.x7101_pair_opti}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7101}')], ]))


async def x7102_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    dollar = chain.startswith("$")
    price = api.get_cg_price("x7102")
    if price["x7102"]["usd_24h_change"] is None:
        price["x7102"]["usd_24h_change"] = 0
    if dollar:
        amount = float(chain[1:]) / float(price["x7102"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7102_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((26, 30),
                f'X7102 Info (ETH)\n\n'
                f'{chain} is currently worth:\n\n{"{:0,.0f}".format(amount)} '
                f'X102 (ETH) Tokens (before tax)\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'{chain} Is currently worth:\n\n{"{:0,.0f}".format(amount)}'
                    f' X7102 (ETH) Tokens (before tax)\n\n{api.get_quote()}',
            parse_mode='Markdown')
    if chain.isdigit():
        amount = float(chain) * float(price["x7102"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7102_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((26, 30),
                f'X7102 Info (ETH)\n\n'
                f'{chain} X7102 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'{chain} X7102 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n'
                    f'{api.get_quote()}',
            parse_mode='Markdown')
    if chain == "" or chain == "eth":
        holders = api.get_holders(ca.x7102)
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7102_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 28)
        i1.text((28, 36),
                f'X7102 Info (ETH)\n\n'
                f'X7102 Price: ${price["x7102"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7102"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(price["x7102"]["usd"] * ca.supply)}\n'
                f'24 Hour Volume: ${"{:0,.0f}".format(price["x7102"]["usd_24h_vol"])}\n'
                f'Holders: {holders}\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*X7102 (ETH) Info*\nUse `/x7102 [chain-name]` for other chains\n\n'
                    f'X7102 Price: ${price["x7102"]["usd"]}\n'
                    f'24 Hour Change: {round(price["x7102"]["usd_24h_change"], 1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(price["x7102"]["usd"] * ca.supply)}\n'
                    f'24 Hour Volume: ${"{:0,.0f}".format(price["x7102"]["usd_24h_vol"])}\n'
                    f'Holders: {holders}\n\n'
                    f'*X7102 Contract*\n`{ca.x7102}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{url.ether_token}{ca.x7102}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_eth}{ca.x7102_pair_eth}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7102}')], ]))
    if chain == "bsc" or chain == "bnb":
        await update.message.reply_photo(
            photo=open(media.x7102_logo, 'rb'),
            caption=f'*X7102 (BSC) Info*\nUse `/x7102 [chain-name]` for other chains\n\n'
                    f'*X7102 Contract*\n`{ca.x7102}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='BSCscan', url=f'{url.bsc_token}{ca.x7102}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_bsc}{ca.x7102_pair_bsc}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7102}')], ]))
    if chain == "opti" or chain == "optimism":
        await update.message.reply_photo(
            photo=open(media.x7102_logo, 'rb'),
            caption=f'*X7102 (OPTIMISM) Info*\nUse `/x7102 [chain-name]` for other chains\n\n'
                    f'*X7102 Contract*\n`{ca.x7102}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Optimistic.etherscan', url=f'{url.opti_token}{ca.x7102}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_opti}{ca.x7102_pair_opti}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7102}')], ]))
    if chain == "poly" or chain == "polygon":
        await update.message.reply_photo(
            photo=open(media.x7102_logo, 'rb'),
            caption=f'*X7102 (POLYGON) Info*\nUse `/x7102 [chain-name]` for other chains\n\n'
                    f'*X7102 Contract*\n`{ca.x7102}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Polygonscan', url=f'{url.poly_token}{ca.x7102}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_poly}{ca.x7102_pair_poly}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7102}')], ]))
    if chain == "arb" or chain == "arbitrum":
        await update.message.reply_photo(
            photo=open(media.x7102_logo, 'rb'),
            caption=f'*X7102 (ARBITRUM) Info*\nUse `/x7102 [chain-name]` for other chains\n\n'
                    f'*X7102 Contract*\n`{ca.x7102}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Arbiscan', url=f'{url.arb_token}{ca.x7102}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_arb}{ca.x7102_pair_arb}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7102}')], ]))


async def x7103_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    dollar = chain.startswith("$")
    price = api.get_cg_price("x7103")
    if price["x7103"]["usd_24h_change"] is None:
        price["x7103"]["usd_24h_change"] = 0
    if dollar:
        amount = float(chain[1:]) / float(price["x7103"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7103_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((26, 30),
                f'X7103 Info (ETH)\n\n'
                f'{chain} is currently worth:\n\n{"{:0,.0f}".format(amount)} '
                f'X7103 (ETH) Tokens (before tax)\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'{chain} Is currently worth:\n\n{"{:0,.0f}".format(amount)}'
                    f' X7103 (ETH) Tokens (before tax)\n\n{api.get_quote()}',
            parse_mode='Markdown')
    if chain.isdigit():
        amount = round(float(chain) * float(price["x7103"]["usd"]), 2)
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7103_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((26, 30),
                f'X7103 Info (ETH)\n\n'
                f'{chain} X7103 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'{chain} X7103 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n'
                    f'{api.get_quote()}',
            parse_mode='Markdown')
    if chain == "" or chain == "eth":
        holders = api.get_holders(ca.x7103)
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7103_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 28)
        i1.text((28, 36),
                f'X7103 Info (ETH)\n\n'
                f'X7103 Price: ${price["x7103"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7103"]["usd_24h_change"],1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(price["x7103"]["usd"] * ca.supply)}\n'
                f'24 Hour Volume: ${"{:0,.0f}".format(price["x7103"]["usd_24h_vol"])}\n'
                f'Holders: {holders}\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*X7103 (ETH) Info*\nUse `/x7103` [chain-name] for other chains\n\n'
                    f'X7103 Price: ${price["x7103"]["usd"]}\n'
                    f'24 Hour Change: {round(price["x7103"]["usd_24h_change"],1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(price["x7103"]["usd"] * ca.supply)}\n'
                    f'24 Hour Volume: ${"{:0,.0f}".format(price["x7103"]["usd_24h_vol"])}\n'
                    f'Holders: {holders}\n\n'
                    f'*X7103 Contract*\n`{ca.x7103}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{url.ether_token}{ca.x7103}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_eth}{ca.x7103_pair_eth}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7103}')], ]))
    if chain == "bsc" or chain == "bnb":
        await update.message.reply_photo(
            photo=open(media.x7103_logo, 'rb'),
            caption=f'*X7103 (BSC) Info*\nUse `/x7103` [chain-name] for other chains\n\n'
                    f'*X7103 Contract*\n`{ca.x7103}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='BSCscan', url=f'{url.bsc_token}{ca.x7103}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_bsc}{ca.x7103_pair_bsc}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7103}')], ]))
    if chain == "polygon" or chain == "poly":
        await update.message.reply_photo(
            photo=open(media.x7103_logo, 'rb'),
            caption=f'*X7103 (POLYGON) Info*\nUse `/x7103` [chain-name] for other chains\n\n'
                    f'*X7103 Contract*\n`{ca.x7103}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Polygonscan', url=f'{url.poly_token}{ca.x7103}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_poly}{ca.x7103_pair_poly}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7103}')], ]))
    if chain == "arb" or chain == "arbitrum":
        await update.message.reply_photo(
            photo=open(media.x7103_logo, 'rb'),
            caption=f'*X7103 (ARBITRUM) Info*\nUse `/x7103` [chain-name] for other chains\n\n'
                    f'*X7103 Contract*\n`{ca.x7103}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Arbiscan', url=f'{url.arb_token}{ca.x7103}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_arb}{ca.x7103_pair_arb}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7103}')], ]))
    if chain == "opti" or chain == "optimism":
        await update.message.reply_photo(
            photo=open(media.x7103_logo, 'rb'),
            caption=f'*X7103 (OPTIMISM) Info*\nUse `/x7103` [chain-name] for other chains\n\n'
                    f'*X7103 Contract*\n`{ca.x7103}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Optimistic.etherscan', url=f'{url.opti_token}{ca.x7103}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_opti}{ca.x7103_pair_opti}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7103}')], ]))


async def x7104_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    dollar = chain.startswith("$")
    price = api.get_cg_price("x7104")
    if price["x7104"]["usd_24h_change"] is None:
        price["x7104"]["usd_24h_change"] = 0
    if dollar:
        amount = float(chain[1:]) / float(price["x7104"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7104_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((26, 30),
                f'X7104 Info (ETH)\n\n'
                f'{chain} is currently worth:\n\n{"{:0,.0f}".format(amount)} '
                f'X7104 (ETH) Tokens (before tax)\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'{chain} Is currently worth:\n\n{"{:0,.0f}".format(amount)}'
                    f' X7104 (ETH) Tokens (before tax)\n\n{api.get_quote()}',
            parse_mode='Markdown')
    if chain.isdigit():
        amount = float(chain) * float(price["x7104"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7104_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((26, 30),
                f'X7104 Info (ETH)\n\n'
                f'{chain} X7104 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'{chain} X7104 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n'
                    f'{api.get_quote()}',
            parse_mode='Markdown')
    if chain == "" or chain == "eth":
        holders = api.get_holders(ca.x7104)
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7104_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((28, 36),
                f'X7104 Info (ETH)\n\n'
                f'X7104 Price: ${price["x7104"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7104"]["usd_24h_change"],1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(price["x7104"]["usd"] * ca.supply)}\n'
                f'24 Hour Volume: ${"{:0,.0f}".format(price["x7104"]["usd_24h_vol"])}\n'
                f'Holders: {holders}\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*X7104 (ETH) Info*\n`Use /x7104 [chain-name]` for other chains\n\n'
                    f'X7104 Price: ${price["x7104"]["usd"]}\n'
                    f'24 Hour Change: {round(price["x7104"]["usd_24h_change"],1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(price["x7104"]["usd"] * ca.supply)}\n'
                    f'24 Hour Volume: ${"{:0,.0f}".format(price["x7104"]["usd_24h_vol"])}\n'
                    f'Holders: {holders}\n\n'
                    f'*X7104 Contract*\n`{ca.x7104}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{url.ether_token}{ca.x7104}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_eth}{ca.x7104_pair_eth}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7104}')], ]))
    if chain == "bsc" or chain == "bnb":
        await update.message.reply_photo(
            photo=open(media.x7104_logo, 'rb'),
            caption=f'*X7104 (BSC) Info*\n`Use /x7104 [chain-name]` for other chains\n\n'
                    f'*X7104 Contract*\n`{ca.x7104}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='BSCscan', url=f'{url.bsc_token}{ca.x7104}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_bsc}{ca.x7104_pair_bsc}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7104}')], ]))
    if chain == "poly" or chain == "polygon":
        await update.message.reply_photo(
            photo=open(media.x7104_logo, 'rb'),
            caption=f'*X7104 (POLYGON) Info*\n`Use /x7104 [chain-name]` for other chains\n\n'
                    f'*X7104 Contract*\n`{ca.x7104}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Polygonscan', url=f'{url.poly_token}{ca.x7104}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_poly}{ca.x7104_pair_poly}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7104}')], ]))
    if chain == "arb" or chain == "arbitrum":
        await update.message.reply_photo(
            photo=open(media.x7104_logo, 'rb'),
            caption=f'*X7104 (ARBITRUM) Info*\n`Use /x7104 [chain-name]` for other chains\n\n'
                    f'*X7104 Contract*\n`{ca.x7104}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Arbiscan', url=f'{url.arb_token}{ca.x7104}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_arb}{ca.x7104_pair_arb}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7104}')], ]))
    if chain == "opti" or chain == "optimism":
        await update.message.reply_photo(
            photo=open(media.x7104_logo, 'rb'),
            caption=f'*X7104 (OPTIMISM) Info*\n`Use /x7104 [chain-name]` for other chains\n\n'
                    f'*X7104 Contract*\n`{ca.x7104}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Optimistic.etherscan', url=f'{url.opti_token}{ca.x7104}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_opti}{ca.x7104_pair_opti}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7104}')], ]))


async def x7105_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    dollar = chain.startswith("$")
    price = api.get_cg_price("x7105")
    if price["x7105"]["usd_24h_change"] is None:
        price["x7105"]["usd_24h_change"] = 0
    if dollar:
        amount = float(chain[1:]) / float(price["x7105"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7105_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((26, 30),
                f'X7105 Info (ETH)\n\n'
                f'{chain} is currently worth:\n\n{"{:0,.0f}".format(amount)} '
                f'X7105 (ETH) Tokens (before tax)\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'{chain} Is currently worth:\n\n{"{:0,.0f}".format(amount)}'
                    f' X7105 (ETH) Tokens (before tax)\n\n{api.get_quote()}',
            parse_mode='Markdown')
    if chain.isdigit():
        amount = float(chain) * float(price["x7105"]["usd"])
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7105_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((26, 30),
                f'X7105 Info (ETH)\n\n'
                f'{chain} X7105 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'{chain} X7105 (ETH) currently costs:\n\n${"{:0,.0f}".format(amount)} (before tax)\n\n'
                    f'{api.get_quote()}',
            parse_mode='Markdown')
    if chain == "" or chain == "eth":
        holders = api.get_holders(ca.x7105)
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7105_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1 = ImageDraw.Draw(im1)
        i1.text((28, 36),
                f'X7105 Info (ETH)\n\n'
                f'X7105 Price: ${price["x7105"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7105"]["usd_24h_change"],1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(price["x7105"]["usd"] * ca.supply)}\n'
                f'24 Hour Volume: ${"{:0,.0f}".format(price["x7105"]["usd_24h_vol"])}\n'
                f'Holders: {holders}\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*X7105 (ETH) Info*\nUse `/x7105 [chain-name]` for other chains\n'
                    f'X7105 Price: ${price["x7105"]["usd"]}\n'
                    f'24 Hour Change: {round(price["x7105"]["usd_24h_change"],1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(price["x7105"]["usd"] * ca.supply)}\n'
                    f'24 Hour Volume: ${"{:0,.0f}".format(price["x7105"]["usd_24h_vol"])}\n'
                    f'Holders: {holders}\n\n'
                    f'*X7105 Contract*\n`{ca.x7105}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{url.ether_token}{ca.x7105}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_eth}{ca.x7105_pair_eth}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7105}')], ]))
    if chain == "bsc" or chain == "bnb":
        await update.message.reply_photo(
            photo=open(media.x7105_logo, 'rb'),
            caption=f'*X7105 (BSC) Info*\n`Use /x7104 [chain-name]` for other chains\n\n'
                    f'*X7105 Contract*\n`{ca.x7105}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='BSCscan', url=f'{url.bsc_token}{ca.x7105}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_bsc}{ca.x7105_pair_bsc}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7105}')], ]))
    if chain == "poly" or chain == "polygon":
        await update.message.reply_photo(
            photo=open(media.x7105_logo, 'rb'),
            caption=f'*X7105 (POLYGON) Info*\n`Use /x7104 [chain-name]` for other chains\n\n'
                    f'*X7105 Contract*\n`{ca.x7105}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Polygonscan', url=f'{url.poly_token}{ca.x7105}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_poly}{ca.x7105_pair_poly}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7105}')], ]))
    if chain == "arb" or chain == "arbitrum":
        await update.message.reply_photo(
            photo=open(media.x7105_logo, 'rb'),
            caption=f'*X7105 (ARBITRUM) Info*\n`Use /x7104 [chain-name]` for other chains\n\n'
                    f'*X7105 Contract*\n`{ca.x7105}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Arbiscan', url=f'{url.arb_token}{ca.x7105}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_arb}{ca.x7105_pair_arb}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7105}')], ]))
    if chain == "opti" or chain == "optimism":
        await update.message.reply_photo(
            photo=open(media.x7105_logo, 'rb'),
            caption=f'*X7105 (OPTIMISM) Info*\n`Use /x7104 [chain-name]` for other chains\n\n'
                    f'*X7105 Contract*\n`{ca.x7105}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Optimistic.etherscan', url=f'{url.opti_token}{ca.x7105}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_opti}{ca.x7105_pair_opti}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy}{ca.x7105}')], ]))


async def mcap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    x7r_supply = ca.supply - api.get_token_balance(ca.dead, "eth", ca.x7r)
    price = api.get_cg_price("x7r, x7dao, x7101, x7102, x7103, x7104, x7105")
    x7r_cap = price["x7r"]["usd"] * x7r_supply
    x7dao_cap = price["x7dao"]["usd"] * ca.supply
    x7101_cap = price["x7101"]["usd"] * ca.supply
    x7102_cap = price["x7102"]["usd"] * ca.supply
    x7103_cap = price["x7103"]["usd"] * ca.supply
    x7104_cap = price["x7104"]["usd"] * ca.supply
    x7105_cap = price["x7105"]["usd"] * ca.supply
    cons_cap = x7101_cap + x7102_cap + x7103_cap + x7104_cap + x7105_cap
    total_cap = x7r_cap + x7dao_cap + x7101_cap + x7102_cap + x7103_cap + x7104_cap + x7105_cap
    im1 = Image.open((random.choice(media.blackhole)))
    im2 = Image.open(media.eth_logo)
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 22)
    i1 = ImageDraw.Draw(im1)
    i1.text((28, 36),
            f'X7 Finance Market Cap Info (ETH)\n\n'
            f'X7R:         ${"{:0,.0f}".format(x7r_cap)}\n'
            f'X7DAO:       ${"{:0,.0f}".format(x7dao_cap)}\n'
            f'X7101:       ${"{:0,.0f}".format(x7101_cap)}\n'
            f'X7102:       ${"{:0,.0f}".format(x7102_cap)}\n'
            f'X7103:       ${"{:0,.0f}".format(x7103_cap)}\n'
            f'X7104:       ${"{:0,.0f}".format(x7104_cap)}\n'
            f'X7105:       ${"{:0,.0f}".format(x7105_cap)}\n\n'
            f'Constellations Combined:\n'
            f'${"{:0,.0f}".format(cons_cap)}\n\n'
            f'Total Token Market Cap:\n'
            f'${"{:0,.0f}".format(total_cap)}\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await update.message.reply_photo(
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'*X7 Finance Market Cap Info (ETH)*\n\n'
                f'X7R:           ${"{:0,.0f}".format(x7r_cap)}\n'
                f'X7DAO:      ${"{:0,.0f}".format(x7dao_cap)}\n'     
                f'X7101:       ${"{:0,.0f}".format(x7101_cap)}\n'
                f'X7102:       ${"{:0,.0f}".format(x7102_cap)}\n'
                f'X7103:       ${"{:0,.0f}".format(x7103_cap)}\n'
                f'X7104:       ${"{:0,.0f}".format(x7104_cap)}\n'
                f'X7105:       ${"{:0,.0f}".format(x7105_cap)}\n\n'
                f'Constellations Combined:\n'
                f'${"{:0,.0f}".format(cons_cap)}\n\n'
                f'Total Token Market Cap:\n'
                f'${"{:0,.0f}".format(total_cap)}'
                f'\n\n{api.get_quote()}',
        parse_mode="Markdown")


async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    search = " ".join(context.args).lower()
    token = api.get_cg_search(search)
    token_id = token["coins"][0]["api_symbol"]
    symbol = token["coins"][0]["symbol"]
    thumb = token["coins"][0]["large"]
    price = api.get_cg_price("x7r, x7dao")
    x7r_change = price["x7r"]["usd_24h_change"]
    x7dao_change = price["x7dao"]["usd_24h_change"]
    token_price = api.get_cg_price(token_id)
    if search == "":
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(r'media\logo11.png')
        im1.paste(im2, (740, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(R'media\FreeMonoBold.ttf', 28)
        i1.text((28, 36),
                f'X7 Finance Token Price Info (ETH)\n\n'
                f'X7R:      ${price["x7r"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7r"]["usd_24h_change"], 1)}%\n\n'
                f'X7DAO:  ${price["x7dao"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7dao"]["usd_24h_change"], 0)}%\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*X7 Finance Token Price Info (ETH)*\n'
                    f'Use `/x7r [chain]` or `/x7dao [chain]` for all other details\n'
                    f'Use `/constellations` for constellations\n\n'
                    f'X7R:      ${price["x7r"]["usd"]}\n'
                    f'24 Hour Change: {round(price["x7r"]["usd_24h_change"], 1)}%\n\n'
                    f'X7DAO:  ${price["x7dao"]["usd"]}\n'
                    f'24 Hour Change: {round(price["x7dao"]["usd_24h_change"], 0)}%\n\n'
                    f'{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='X7R Chart - Rewards Token',
                                       url=f'{url.dex_tools_eth}{ca.x7r_pair_eth}')],
                 [InlineKeyboardButton(text='X7DAO Chart - Governance Token',
                                       url=f'{url.dex_tools_eth}{ca.x7dao_pair_eth}')], ]))
        return
    if search == "eth":
        eth = api.get_cg_price("ethereum")
        gas_data = api.get_gas("eth")
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(requests.get(thumb, stream=True).raw)
        im1.paste(im2, (680, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(R'media\FreeMonoBold.ttf', 28)
        i1.text((28, 36),
                f'{symbol} price\n\n'
                f'Price: ${eth["ethereum"]["usd"]}\n'
                f'24 Hour Change: {round(eth["ethereum"]["usd_24h_change"], 1)}%\n\n'
                f'Gas Prices:\n'
                f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n'
                f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n'
                f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*{symbol} price*\n\n'
                    f'Price: ${eth["ethereum"]["usd"]}\n'
                    f'24 Hour Change: {round(eth["ethereum"]["usd_24h_change"], 1)}%\n\n'
                    f'Gas Prices:\n'
                    f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n'
                    f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n'
                    f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n'
                    f'{api.get_quote()}', parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Chart', url=f'https://www.coingecko.com/en/coins/ethereum')], ]))
        return
    if search == "bnb":
        bnb = api.get_cg_price("binancecoin")
        gas_data = api.get_gas("bsc")
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(requests.get(thumb, stream=True).raw)
        im1.paste(im2, (680, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(R'media\FreeMonoBold.ttf', 28)
        i1.text((28, 36),
                f'{symbol} price\n\n'
                f'Price: ${bnb["binancecoin"]["usd"]}\n'
                f'24 Hour Change: {round(bnb["binancecoin"]["usd_24h_change"], 1)}%\n\n'
                f'Gas Prices:\n'
                f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n'
                f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n'
                f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*{symbol} price*\n\n'
                    f'Price: ${bnb["binancecoin"]["usd"]}\n'
                    f'24 Hour Change: {round(bnb["binancecoin"]["usd_24h_change"], 1)}%\n\n'
                    f'Gas Prices:\n'
                    f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n'
                    f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n'
                    f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n'
                    f'{api.get_quote()}', parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Chart', url=f'https://www.coingecko.com/en/coins/bnb')], ]))
        return
    if search == "matic" or search == "poly" or search == "polygon":
        matic = api.get_cg_price("matic-network")
        gas_data = api.get_gas("poly")
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(requests.get(thumb, stream=True).raw)
        im1.paste(im2, (680, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(R'media\FreeMonoBold.ttf', 28)
        i1.text((28, 36),
                f'{symbol} price\n\n'
                f'Price: ${matic["matic-network"]["usd"]}\n'
                f'24 Hour Change: {round(matic["matic-network"]["usd_24h_change"], 1)}%\n\n'
                f'Gas Prices:\n'
                f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n'
                f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n'
                f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*{symbol} price*\n\n'
                    f'Price: ${matic["matic-network"]["usd"]}\n'
                    f'24 Hour Change: {round(matic["matic-network"]["usd_24h_change"], 1)}%\n\n'
                    f'Gas Prices:\n'
                    f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n'
                    f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n'
                    f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n'
                    f'{api.get_quote()}', parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Chart', url=f'https://www.coingecko.com/en/coins/polygon')], ]))
        return
    else:
        img = Image.open(requests.get(thumb, stream=True).raw)
        result = img.convert('RGBA')
        result.save(r'media\cgtokenlogo.png')
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(r'media\cgtokenlogo.png')
        im1.paste(im2, (680, 20), im2)
        myfont = ImageFont.truetype(R'media\FreeMonoBold.ttf', 28)
        i1 = ImageDraw.Draw(im1)
        i1.text((28, 36),
                f'{symbol} price\n\n'
                f'Price: ${float(token_price[token_id]["usd"])}\n'
                f'24 Hour Change: {round(token_price[token_id]["usd_24h_change"], 1)}%\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png", quality=95)
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*{symbol} price*\n\n'
                    f'Price: ${float(token_price[token_id]["usd"])}\n'
                    f'24 Hour Change: {round(token_price[token_id]["usd_24h_change"], 1)}%\n\n'
                    f'{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Chart', url=f'https://www.coingecko.com/en/coins/{token_id}')], ]))


async def constellations_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        myfont = ImageFont.truetype(R'media\FreeMonoBold.ttf', 20)
        i1.text((28, 36),
                f'X7 Finance Constellation Token Prices (ETH)\n\n'
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
                font=myfont, fill=(255, 255, 255))
        i1.text((522, 90),
                f'X7104:      ${price["x7104"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7104"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(x7104mc)}\n\n'
                f'X7105:      ${price["x7105"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7105"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(x7105mc)}\n\n'
                f'Combined Market Cap:\n${"{:0,.0f}".format(const_mc)}\n',
                font=myfont, fill=(255, 255, 255))
        img.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r'media\blackhole.png', 'rb'),
            caption=f'*X7 Finance Constellation Token Prices (ETH)*\n\n'
                    f'For more info use `/x7token-name`\n\n'
                    f'X7101:      ${price["x7101"]["usd"]}\n'
                    f'24 Hour Change: {round(price["x7101"]["usd_24h_change"], 1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(x7101mc)}\n'
                    f'CA: `{ca.x7101}\n\n`'
                    f'X7102:      ${price["x7102"]["usd"]}\n'
                    f'24 Hour Change: {round(price["x7102"]["usd_24h_change"], 1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(x7102mc)}\n'
                    f'CA: `{ca.x7102}\n\n`'
                    f'X7103:      ${price["x7103"]["usd"]}\n'
                    f'24 Hour Change: {round(price["x7103"]["usd_24h_change"], 1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(x7103mc)}\n'
                    f'CA: `{ca.x7103}\n\n`'
                    f'X7104:      ${price["x7104"]["usd"]}\n'
                    f'24 Hour Change: {round(price["x7104"]["usd_24h_change"], 1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(x7104mc)}\n'
                    f'CA: `{ca.x7104}\n\n`'
                    f'X7105:      ${price["x7105"]["usd"]}\n'
                    f'24 Hour Change: {round(price["x7105"]["usd_24h_change"], 1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(x7105mc)}\n'
                    f'CA: `{ca.x7105}\n\n`'
                    f'Combined Market Cap: ${"{:0,.0f}".format(const_mc)}\n\n'
                    f'{api.get_quote()}', parse_mode="Markdown")


async def treasury_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "" or chain == "eth":
        dev_eth = api.get_native_balance(ca.dev_multi_eth, "eth")
        com_eth = api.get_native_balance(ca.com_multi_eth, "eth")
        pioneer_eth = api.get_native_balance(ca.pioneer, "eth")
        dev_dollar = float(dev_eth) * float(api.get_native_price("eth")) / 1 ** 18
        com_dollar = float(com_eth) * float(api.get_native_price("eth")) / 1 ** 18
        pioneer_dollar = float(pioneer_eth) * float(api.get_native_price("eth")) / 1 ** 18
        com_x7r = api.get_token_balance(ca.com_multi_eth, "eth", ca.x7r)
        com_x7r_price = com_x7r * api.get_cg_price("x7r")["x7r"]["usd"]
        com_x7d = api.get_token_balance(ca.com_multi_eth, "eth", ca.x7d)
        com_x7d_price = com_x7d * api.get_native_price("eth")
        com_total = com_x7r_price + com_dollar + com_x7d_price
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.eth_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 20)
        i1 = ImageDraw.Draw(im1)
        i1.text((28, 36),
                f'X7 Finance Treasury (ETH)\n\n'
                f'Pioneer Pool:\n{pioneer_eth[:4]}ETH (${"{:0,.0f}".format(pioneer_dollar)})\n\n'
                f'Developer Wallet:\n{dev_eth[:4]}ETH (${"{:0,.0f}".format(dev_dollar)})\n\n'
                f'Community Wallet:\n{com_eth[:4]}ETH (${"{:0,.0f}".format(com_dollar)})\n'
                f'{com_x7d} X7D (${"{:0,.0f}".format(com_x7d_price)})\n'
                f'{"{:0,.0f}".format(com_x7r)} X7R (${"{:0,.0f}".format(com_x7r_price)})\n'
                f'Total: (${"{:0,.0f}".format(com_total)})\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption='*X7 Finance Treasury (ETH)*\nUse `/treasury [chain-name]` for other chains\n\n'
                    f'Pioneer Pool:\n{pioneer_eth[:4]}ETH (${"{:0,.0f}".format(pioneer_dollar)})\n\n'
                    f'Developer Wallet:\n{dev_eth[:4]}ETH (${"{:0,.0f}".format(dev_dollar)})\n\n'
                    f'Community Wallet:\n{com_eth[:4]}ETH (${"{:0,.0f}".format(com_dollar)})\n'
                    f'{com_x7d} X7D (${"{:0,.0f}".format(com_x7d_price)})\n'
                    f'{"{:0,.0f}".format(com_x7r)} X7R (${"{:0,.0f}".format(com_x7r_price)})\n'
                    f'Total: (${"{:0,.0f}".format(com_total)})\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    text='Treasury Splitter Contract', url=f'{url.ether_address}{ca.treasury_splitter}')],
                [InlineKeyboardButton(
                    text='Developer Multi-sig Wallet', url=f'{url.ether_address}{ca.dev_multi_eth}')],
                [InlineKeyboardButton(
                    text='Community Multi-sig Wallet', url=f'{url.ether_address}{ca.com_multi_eth}')],
            ]))
    if chain == "bsc" or chain == "bnb":
        dev_eth = api.get_native_balance(ca.dev_multi_bsc, "bsc")
        com_eth = api.get_native_balance(ca.com_multi_bsc, "bsc")
        dev_dollar = float(dev_eth) * float(api.get_native_price("bnb")) / 1 ** 18
        com_dollar = float(com_eth) * float(api.get_native_price("bnb")) / 1 ** 18
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.bsc_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 20)
        i1 = ImageDraw.Draw(im1)
        i1.text((28, 36),
                'X7 Finance Treasury (BSC)\n\n'
                f'Developer Wallet:\n{dev_eth[:4]}BNB (${"{:0,.0f}".format(dev_dollar)})\n\n'
                f'Community Wallet:\n{com_eth[:4]}BNB (${"{:0,.0f}".format(com_dollar)})\n\n\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption='*X7 Finance Treasury (BSC)*\nUse `/treasury [chain-name]` for other chains\n\n'
                    f'Developer Wallet:\n{dev_eth[:4]}BNB (${"{:0,.0f}".format(dev_dollar)})\n\n'
                    f'Community Wallet:\n{com_eth[:4]}BNB (${"{:0,.0f}".format(com_dollar)})\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Treasury Splitter Contract',
                                      url=f'{url.bsc_address}{ca.treasury_splitter}')],
                [InlineKeyboardButton(text='Developer Multi-sig Wallet',
                                      url=f'{url.bsc_address}{ca.dev_multi_bsc}')],
                [InlineKeyboardButton(text='Community Multi-sig Wallet',
                                      url=f'{url.bsc_address}{ca.com_multi_bsc}')],
            ]))
    if chain == "arbitrum" or chain == "arb":
        dev_amount = api.get_native_balance(ca.dev_multi_arb, "arb")
        com_amount = api.get_native_balance(ca.dev_multi_arb, "arb")
        dev_dollar = float(dev_amount) * float(api.get_native_price("eth")) / 1 ** 18
        com_dollar = float(com_amount) * float(api.get_native_price("eth")) / 1 ** 18
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.arb_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 20)
        i1 = ImageDraw.Draw(im1)
        i1.text((28, 36),
                'X7 Finance Treasury (ARBITRUM)\n\n'
                f'Developer Wallet:\n{dev_amount[:4]}ETH (${"{:0,.0f}".format(dev_dollar)})\n\n'
                f'Community Wallet:\n{com_amount[:4]}ETH (${"{:0,.0f}".format(com_dollar)})\n\n\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption='*X7 Finance Treasury (ARBITRUM)*\nUse `/treasury [chain-name]` for other chains\n\n'
                    f'Developer Wallet:\n{dev_amount[:4]}ETH (${"{:0,.0f}".format(dev_dollar)})\n\n'
                    f'Community Wallet:\n{com_amount[:4]}ETH (${"{:0,.0f}".format(com_dollar)})\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Treasury Splitter Contract',
                                      url=f'{url.arb_address}{ca.treasury_splitter}')],
                [InlineKeyboardButton(text='Developer Multi-sig Wallet',
                                      url=f'{url.arb_address}{ca.dev_multi_arb}')],
                [InlineKeyboardButton(text='Community Multi-sig Wallet',
                                      url=f'{url.arb_address}{ca.com_multi_arb}')],
            ]))
    if chain == "polygon" or chain == "poly":
        dev_amount = api.get_native_balance(ca.dev_multi_poly, "poly")
        com_amount = api.get_native_balance(ca.com_multi_poly, "poly")
        dev_dollar = float(dev_amount) * float(api.get_native_price("matic")) / 1 ** 18
        com_dollar = float(com_amount) * float(api.get_native_price("matic")) / 1 ** 18
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.poly_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 20)
        i1 = ImageDraw.Draw(im1)
        i1.text((28, 36),
                'X7 Finance Treasury (POLY)\n\n'
                f'Developer Wallet:\n{dev_amount[:4]}MATIC (${"{:0,.0f}".format(dev_dollar)})\n\n'
                f'Community Wallet:\n{com_amount[:4]}MATIC (${"{:0,.0f}".format(com_dollar)})\n\n\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption='*X7 Finance Treasury (POLY)*\nUse `/treasury [chain-name]` for other chains\n\n'
                    f'Developer Wallet:\n{dev_amount[:4]}MATIC (${"{:0,.0f}".format(dev_dollar)})\n\n'
                    f'Community Wallet:\n{com_amount[:4]}MATIC (${"{:0,.0f}".format(com_dollar)})\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Treasury Splitter Contract',
                                      url=f'{url.poly_address}{ca.treasury_splitter}')],
                [InlineKeyboardButton(text='Developer Multi-sig Wallet',
                                      url=f'{url.poly_address}{ca.dev_multi_poly}')],
                [InlineKeyboardButton(text='Community Multi-sig Wallet',
                                      url=f'{url.poly_address}{ca.com_multi_poly}')],
            ]))
    if chain == "optimism" or chain == "opti":
        dev_amount = api.get_native_balance(ca.dev_multi_opti, "opti")
        com_amount = api.get_native_balance(ca.com_multi_opti, "opti")
        dev_dollar = float(dev_amount) * float(api.get_native_price("eth")) / 1 ** 18
        com_dollar = float(com_amount) * float(api.get_native_price("eth")) / 1 ** 18
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.opti_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 20)
        i1 = ImageDraw.Draw(im1)
        i1.text((28, 36),
                'X7 Finance Treasury (OPTI)\n\n'
                f'Developer Wallet:\n{dev_amount[:4]}ETH (${"{:0,.0f}".format(dev_dollar)})\n\n'
                f'Community Wallet:\n{com_amount[:4]}ETH (${"{:0,.0f}".format(com_dollar)})\n\n\n\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption='*X7 Finance Treasury (OPTI)*\nUse `/treasury [chain-name]` for other chains\n\n'
                    f'Developer Wallet:\n{dev_amount[:4]}ETH (${"{:0,.0f}".format(dev_dollar)})\n\n'
                    f'Community Wallet:\n{com_amount[:4]}ETH (${"{:0,.0f}".format(com_dollar)})\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Treasury Splitter Contract',
                                      url=f'{url.opti_address}{ca.treasury_splitter}')],
                [InlineKeyboardButton(text='Developer Multi-sig Wallet',
                                      url=f'{url.opti_address}{ca.dev_multi_opti}')],
                [InlineKeyboardButton(text='Community Multi-sig Wallet',
                                      url=f'{url.opti_address}{ca.com_multi_opti}')],
            ]))


async def liquidity_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "" or chain == "eth":
        price = api.get_cg_price("x7r, x7dao, x7101, x7102, x7103, x7104, x7105")
        x7r_price = (price["x7r"]["usd"])
        x7dao_price = (price["x7dao"]["usd"])
        x7101_price = (price["x7101"]["usd"])
        x7102_price = (price["x7102"]["usd"])
        x7103_price = (price["x7103"]["usd"])
        x7104_price = (price["x7104"]["usd"])
        x7105_price = (price["x7105"]["usd"])
        x7r = api.get_liquidity(ca.x7r_pair_eth)
        x7dao = api.get_liquidity(ca.x7dao_pair_eth)
        x7101 = api.get_liquidity(ca.x7101_pair_eth)
        x7102 = api.get_liquidity(ca.x7102_pair_eth)
        x7103 = api.get_liquidity(ca.x7103_pair_eth)
        x7104 = api.get_liquidity(ca.x7104_pair_eth)
        x7105 = api.get_liquidity(ca.x7105_pair_eth)
        x7r_token = float(x7r["reserve0"])
        x7r_weth = float(x7r["reserve1"]) / 10 ** 18
        x7r_weth_dollar = float(x7r_weth) * float(api.get_native_price("eth"))
        x7r_token_dollar = float(x7r_price) * float(x7r_token) / 10 ** 18
        x7dao_token = float(x7dao["reserve0"])
        x7dao_weth = float(x7dao["reserve1"]) / 10 ** 18
        x7dao_weth_dollar = float(x7dao_weth) * float(api.get_native_price("eth"))
        x7dao_token_dollar = float(x7dao_price) * float(x7dao_token) / 10 ** 18
        x7101_token = float(x7101["reserve0"])
        x7101_weth = float(x7101["reserve1"]) / 10 ** 18
        x7101_weth_dollar = float(x7101_weth) * float(api.get_native_price("eth"))
        x7101_token_dollar = float(x7101_price) * float(x7101_token) / 10 ** 18
        x7102_token = float(x7102["reserve0"])
        x7102_weth = float(x7102["reserve1"]) / 10 ** 18
        x7102_weth_dollar = float(x7102_weth) * float(api.get_native_price("eth"))
        x7102_token_dollar = float(x7102_price) * float(x7102_token) / 10 ** 18
        x7103_token = float(x7103["reserve0"])
        x7103_weth = float(x7103["reserve1"]) / 10 ** 18
        x7103_weth_dollar = float(x7103_weth) * float(api.get_native_price("eth"))
        x7103_token_dollar = float(x7103_price) * float(x7103_token) / 10 ** 18
        x7104_token = float(x7104["reserve0"])
        x7104_weth = float(x7104["reserve1"]) / 10 ** 18
        x7104_weth_dollar = float(x7104_weth) * float(api.get_native_price("eth"))
        x7104_token_dollar = float(x7104_price) * float(x7104_token) / 10 ** 18
        x7105_token = float(x7105["reserve0"])
        x7105_weth = float(x7105["reserve1"]) / 10 ** 18
        x7105_weth_dollar = float(x7105_weth) * float(api.get_native_price("eth"))
        x7105_token_dollar = float(x7105_price) * float(x7105_token) / 10 ** 18
        constellations_tokens = x7101_token+x7102_token+x7103_token+x7104_token+x7105_token
        constellations_weth = x7101_weth + x7102_weth + x7103_weth + x7104_weth + x7105_weth
        constellations_weth_dollar = \
            x7101_weth_dollar+x7102_weth_dollar+x7103_weth_dollar+x7104_weth_dollar+x7105_weth_dollar
        constellations_token_dollar = \
            x7101_token_dollar+x7102_token_dollar+x7103_token_dollar+x7104_token_dollar+x7105_token_dollar
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.eth_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 20)
        i1.text((28, 36),
                f'X7 Finance Token Liquidity (ETH)\n\n'
                f'X7R\n'
                f'{"{:0,.0f}".format(x7r_token)[:4]}M X7R (${"{:0,.0f}".format(x7r_token_dollar)})\n'
                f'{"{:0,.0f}".format(x7r_weth)} WETH (${"{:0,.0f}".format(x7r_weth_dollar)})\n'
                f'Total Liquidity ${"{:0,.0f}".format(x7r_weth_dollar + x7r_token_dollar)}\n\n'
                f'X7DAO\n'
                f'{"{:0,.0f}".format(x7dao_token)[:4]}M X7DAO (${"{:0,.0f}".format(x7dao_token_dollar)})\n'
                f'{"{:0,.0f}".format(x7dao_weth)} WETH (${"{:0,.0f}".format(x7dao_weth_dollar)})\n'
                f'Total Liquidity ${"{:0,.0f}".format(x7dao_weth_dollar + x7dao_token_dollar)}\n\n'
                f'Constellations\n'
                f'{"{:0,.0f}".format(constellations_tokens)[:4]}M X7100 '
                f'(${"{:0,.0f}".format(constellations_token_dollar)})\n'
                f'{"{:0,.0f}".format(constellations_weth)} WETH '
                f'(${"{:0,.0f}".format(constellations_weth_dollar)})\n'
                f'Total Liquidity ${"{:0,.0f}".format(constellations_weth_dollar+constellations_token_dollar)}\n'
                f'\nUTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*X7 Finance Token Liquidity (ETH)*\n'
                    f'To show initial liquidity for other chains, Use `/liquidity '
                    f'[chain-name]`\n\n'
                    f'*X7R*\n'
                    f'{"{:0,.0f}".format(x7r_token)[:4]}M X7R (${"{:0,.0f}".format(x7r_token_dollar)})\n'
                    f'{"{:0,.0f}".format(x7r_weth)} WETH (${"{:0,.0f}".format(x7r_weth_dollar)})\n'
                    f'Total Liquidity ${"{:0,.0f}".format(x7r_weth_dollar + x7r_token_dollar)}\n\n'
                    f'*X7DAO*\n'
                    f'{"{:0,.0f}".format(x7dao_token)[:4]}M X7DAO (${"{:0,.0f}".format(x7dao_token_dollar)})\n'
                    f'{"{:0,.0f}".format(x7dao_weth)} WETH (${"{:0,.0f}".format(x7dao_weth_dollar)})\n'
                    f'Total Liquidity ${"{:0,.0f}".format(x7dao_weth_dollar + x7dao_token_dollar)}\n\n'
                    f'*Constellations*\n'
                    f'{"{:0,.0f}".format(constellations_tokens)[:4]}M X7100 '
                    f'(${"{:0,.0f}".format(constellations_token_dollar)})\n'
                    f'{"{:0,.0f}".format(constellations_weth)} WETH '
                    f'(${"{:0,.0f}".format(constellations_weth_dollar)})\n'
                    f'Total Liquidity ${"{:0,.0f}".format(constellations_weth_dollar+constellations_token_dollar)}\n\n'
                    f'{api.get_quote()}', parse_mode='Markdown')
    if chain == "bsc" or chain == "bnb":
        x7r_amount = api.get_native_balance(ca.x7r_liq_lock, "bsc")
        x7dao_amount = api.get_native_balance(ca.x7dao_liq_lock, "bsc")
        cons_amount = api.get_native_balance(ca.cons_liq_lock, "bsc")
        x7dao_dollar = float(x7dao_amount) * float(api.get_native_price("bnb")) / 1 ** 18
        x7r_dollar = float(x7r_amount) * float(api.get_native_price("bnb")) / 1 ** 18
        cons_dollar = float(cons_amount) * float(api.get_native_price("bnb")) / 1 ** 18
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.bsc_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1.text((28, 36),
                f'X7 Finance Initial Liquidity (BSC)\n\n'
                f'X7R:\n{x7r_amount} BNB (${"{:0,.0f}".format(x7r_dollar)})\n\n'
                f'X7DAO:\n{x7dao_amount} BNB (${"{:0,.0f}".format(x7dao_dollar)})\n\n'
                f'X7100:\n{cons_amount} BNB (${"{:0,.0f}".format(cons_dollar)})\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption='*X7 Finance Initial Liquidity (BSC)*\nUse `/liquidity [chain-name]` for other chains\n\n'
                    f'X7R:\n{x7r_amount} BNB (${"{:0,.0f}".format(x7r_dollar)})\n\n'
                    f'X7DAO:\n{x7dao_amount} BNB (${"{:0,.0f}".format(x7dao_dollar)})\n\n'
                    f'X7100:\n{cons_amount} BNB (${"{:0,.0f}".format(cons_dollar)})\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R Initial Liquidity',
                                      url=f'{url.bsc_address}{ca.x7r_liq_lock}')],
                [InlineKeyboardButton(text='X7DAO Initial Liquidity',
                                      url=f'{url.bsc_address}{ca.x7dao_liq_lock}')],
                [InlineKeyboardButton(text='X7100 Initial Liquidity',
                                      url=f'{url.bsc_address}{ca.cons_liq_lock}')],
            ]))
    if chain == "arbitrum" or chain == "arb":
        x7r_amount = api.get_native_balance(ca.x7r_liq_lock, "arb")
        x7dao_amount = api.get_native_balance(ca.x7dao_liq_lock, "arb")
        cons_amount = api.get_native_balance(ca.cons_liq_lock, "arb")
        x7dao_dollar = float(x7dao_amount) * float(api.get_native_price("eth")) / 1 ** 18
        x7r_dollar = float(x7r_amount) * float(api.get_native_price("eth")) / 1 ** 18
        cons_dollar = float(cons_amount) * float(api.get_native_price("eth")) / 1 ** 18
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.arb_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1.text((28, 36),
                f'X7 Finance Initial Liquidity (ARBITRUM)\n\n'
                f'X7R:\n{x7r_amount} ETH (${"{:0,.0f}".format(x7r_dollar)})\n\n'
                f'X7DAO:\n{x7dao_amount} ETH (${"{:0,.0f}".format(x7dao_dollar)})\n\n'
                f'X7100:\n{cons_amount} ETH (${"{:0,.0f}".format(cons_dollar)})\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption='*X7 Finance Initial Liquidity (ARBITRUM)*\nUse `/liquidity [chain-name]` for other chains\n\n'
                    f'X7R:\n{x7r_amount} ETH (${"{:0,.0f}".format(x7r_dollar)})\n\n'
                    f'X7DAO:\n{x7dao_amount} ETH (${"{:0,.0f}".format(x7dao_dollar)})\n\n'
                    f'X7100:\n{cons_amount} ETH (${"{:0,.0f}".format(cons_dollar)})\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R Initial Liquidity',
                                      url=f'{url.arb_address}{ca.x7r_liq_lock}')],
                [InlineKeyboardButton(text='X7DAO Initial Liquidity',
                                      url=f'{url.arb_address}{ca.x7dao_liq_lock}')],
                [InlineKeyboardButton(text='X7100 Initial Liquidity',
                                      url=f'{url.arb_address}{ca.cons_liq_lock}')],
            ]))
    if chain == "optimism" or chain == "opti":
        x7r_amount = api.get_native_balance(ca.x7r_liq_lock, "opti")
        x7dao_amount = api.get_native_balance(ca.x7dao_liq_lock, "opti")
        cons_amount = api.get_native_balance(ca.cons_liq_lock, "opti")
        x7dao_dollar = float(x7dao_amount) * float(api.get_native_price("eth")) / 1 ** 18
        x7r_dollar = float(x7r_amount) * float(api.get_native_price("eth")) / 1 ** 18
        cons_dollar = float(cons_amount) * float(api.get_native_price("eth")) / 1 ** 18
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.opti_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1.text((28, 36),
                f'X7 Finance Initial Liquidity (OPTIMISM)\n\n'
                f'X7R:\n{x7r_amount} ETH (${"{:0,.0f}".format(x7r_dollar)})\n\n'
                f'X7DAO:\n{x7dao_amount} ETH (${"{:0,.0f}".format(x7dao_dollar)})\n\n'
                f'X7100:\n{cons_amount} ETH (${"{:0,.0f}".format(cons_dollar)})\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption='*X7 Finance Initial Liquidity (OPTIMISM)*\nUse `/liquidity [chain-name]` for other chains\n\n'
                    f'X7R:\n{x7r_amount} ETH (${"{:0,.0f}".format(x7r_dollar)})\n\n'
                    f'X7DAO:\n{x7dao_amount} ETH (${"{:0,.0f}".format(x7dao_dollar)})\n\n'
                    f'X7100:\n{cons_amount} ETH (${"{:0,.0f}".format(cons_dollar)})\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R Initial Liquidity',
                                      url=f'{url.opti_address}{ca.x7r_liq_lock}')],
                [InlineKeyboardButton(text='X7DAO Initial Liquidity',
                                      url=f'{url.opti_address}{ca.x7dao_liq_lock}')],
                [InlineKeyboardButton(text='X7100 Initial Liquidity',
                                      url=f'{url.opti_address}{ca.cons_liq_lock}')],
            ]))
    if chain == "polygon" or chain == "poly":
        x7r_amount = api.get_native_balance(ca.x7r_liq_lock, "poly")
        x7dao_amount = api.get_native_balance(ca.x7dao_liq_lock, "poly")
        cons_amount = api.get_native_balance(ca.cons_liq_lock, "poly")
        x7dao_dollar = float(x7dao_amount) * float(api.get_native_price("matic")) / 1 ** 18
        x7r_dollar = float(x7r_amount) * float(api.get_native_price("matic")) / 1 ** 18
        cons_dollar = float(cons_amount) * float(api.get_native_price("matic")) / 1 ** 18
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.poly_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1.text((28, 36),
                f'X7 Finance Initial Liquidity (POLYGON)\n\n'
                f'X7R:\n{x7r_amount} MATIC (${"{:0,.0f}".format(x7r_dollar)})\n\n'
                f'X7DAO:\n{x7dao_amount} MATIC (${"{:0,.0f}".format(x7dao_dollar)})\n\n'
                f'X7100:\n{cons_amount} MATIC (${"{:0,.0f}".format(cons_dollar)})\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption='*X7 Finance Initial Liquidity (POLYGON)*\nUse `/liquidity [chain-name]` for other chains\n\n'
                    f'X7R:\n{x7r_amount} MATIC (${"{:0,.0f}".format(x7r_dollar)})\n\n'
                    f'X7DAO:\n{x7dao_amount} MATIC (${"{:0,.0f}".format(x7dao_dollar)})\n\n'
                    f'X7100:\n{cons_amount} MATIC (${"{:0,.0f}".format(cons_dollar)})\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R Initial Liquidity',
                                      url=f'{url.poly_address}{ca.x7r_liq_lock}')],
                [InlineKeyboardButton(text='X7DAO Initial Liquidity',
                                      url=f'{url.poly_address}{ca.x7dao_liq_lock}')],
                [InlineKeyboardButton(text='X7100 Initial Liquidity',
                                      url=f'{url.poly_address}{ca.cons_liq_lock}')],
            ]))


async def burn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_url = ""
    chain_name = ""
    burn = ""
    im2 = ""
    burn_dollar = ""
    percent = ""
    if chain == "" or chain == "eth":
        chain_name = "(ETH)"
        chain_url = url.ether_address
        burn = api.get_token_balance(ca.dead, "eth", ca.x7r)
        percent = round(burn / ca.supply * 100, 2)
        burn_dollar = api.get_cg_price("x7r")["x7r"]["usd"] * float(burn)
        im2 = Image.open(media.eth_logo)
    if chain == "bsc" or chain == "bnb":
        chain_name = "(BSC)"
        chain_url = url.bsc_address
        amount = api.get_token_balance(ca.dead, "bsc", ca.x7r)
        percent = round(((amount / ca.supply) * 100), 6)
        im2 = Image.open(media.bsc_logo)
    if chain == "polygon" or chain == "poly":
        chain_name = "(POLYGON)"
        chain_url = url.poly_address
        amount = api.get_token_balance(ca.dead, "poly", ca.x7r)
        percent = round(((amount / ca.supply) * 100), 6)
        im2 = Image.open(media.poly_logo)
    if chain == "arbitrum" or chain == "arb":
        chain_name = "(ARB)"
        chain_url = url.arb_address
        amount = api.get_token_balance(ca.dead, "arb", ca.x7r)
        percent = round(((amount / ca.supply) * 100), 6)
        im2 = Image.open(media.arb_logo)
    if chain == "optimism" or chain == "arb":
        chain_name = "(OPTIMISM)"
        chain_url = url.opti_address
        amount = api.get_token_balance(ca.dead, "opti", ca.x7r)
        percent = round(((amount / ca.supply) * 100), 6)
        im2 = Image.open(media.opti_logo)
    im1 = Image.open((random.choice(media.blackhole)))
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 28)
    i1.text((28, 36),
            f'X7R {chain_name} Tokens Burned:\n\n'
            f'{"{:0,.0f}".format(float(burn))} (${"{:0,.0f}".format(float(burn_dollar))})\n'
            f'{percent}% of Supply\n\n\n\n\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await update.message.reply_photo(
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'\n\nX7R {chain_name} Tokens Burned:\nUse `/burn [chain-name]` for other chains\n\n'
                f'{burn} (${"{:0,.0f}".format(float(burn_dollar))})\n'
                f'{percent}% of Supply\n\n{api.get_quote()}',
        parse_mode="markdown",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Etherscan Burn Wallet', url=f'{chain_url}{ca.x7r}?a={ca.dead}')], ]))


# AUTO MESSAGES
async def wp_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.send_message(
        job.chat_id,
        text=f'*X7 Finance Whitepaper Quote*\n\n{random.choice(text.quotes)}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url=f'{url.website}')],
            [InlineKeyboardButton(text='Whitepaper', url=f'{url.wp_link}')], ]))


async def auto_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.send_photo(
        job.chat_id,
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f"{job.data}")


async def show_auto_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_admins = await update.effective_chat.get_administrators()
    job_names = [job.name for job in context.job_queue.jobs()]
    if update.effective_user in (admin.user for admin in chat_admins):
        await update.message.reply_text(f'X7 Finance Auto Messages set:\n\n{job_names}\n\nUse /stop_auto "name" '
                                        f'to stop')
    else:
        await update.message.reply_text(f'{text.mods_only}')


async def auto_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    chat_admins = await update.effective_chat.get_administrators()
    name = context.args[0]
    due = float(context.args[1])
    message = ' '.join(context.args[2:])
    user = update.message.from_user.username
    if update.effective_user in (admin.user for admin in chat_admins):
        if due < 0:
            await update.effective_message.reply_text("Sorry we can not go back to future!")
            return
        context.job_queue.run_repeating(auto_message, due*60*60, chat_id=chat_id, name=name, data=message)
        await update.effective_message.reply_text(f"X7 Finance Auto Message: '{name}'\n\nSet every {due} "
                                                  f"Hours\n\n{message}\n\nby {user}")
    else:
        await update.message.reply_text(f'{text.mods_only}')


async def stop_auto_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        for job in job_queue.get_jobs_by_name((" ".join(context.args))):
            job.schedule_removal()
            await update.message.reply_text(f"X7 Finance auto message, {context.args} Stopped!")
            return
        else:
            await update.message.reply_text(f"No active message named {context.args}.")
    else:
        await update.message.reply_text(f'{text.mods_only}')


# GENERAL MESSAGES
async def auto_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = str(update.effective_message.text).lower()
    print(f'{update.effective_message.from_user.username} says "{message}" in: '
          f'{update.effective_message.chat.title}')
    if "@devs" in message:
        result = round(((api.get_token_balance(ca.dead, "eth", ca.x7r) / ca.supply) * 100), 6)
        await update.message.reply_text(f'Please send 1000 X7R to the burn wallet:\n\n'
                                        f'`0x000000000000000000000000000000000000dEaD`\n\nThank you for your '
                                        f'contribution {update.message.from_user.username}\n\n'
                                        f'X7R (ETH) Tokens Burned:\n'
                                        f'{"{:,}".format(api.get_token_balance(ca.dead, "eth", ca.x7r))}\n'
                                        f'{result}% of Supply',
                                        parse_mode='Markdown')
    if "rob the bank" in message:
        await update.message.reply_text(f'{text.rob}', parse_mode='Markdown')
    if "delay" in message:
        await update.message.reply_text(f'{text.delay}', parse_mode="markdown")
    if "patience" in message:
        await update.message.reply_text(f'{text.patience}', parse_mode="markdown")
    if "https://twitter" in message:
        await update.message.reply_text(f'{random.choice(text.twitter_replies)}')
    if message.startswith("gm"):
        await update.message.reply_sticker(sticker=media.gm)
    if "new on chain message" in message:
        await update.message.reply_sticker(sticker=media.chain)
    if "lfg" in message:
        await update.message.reply_sticker(sticker=media.lfg)
    if "goat" in message:
        await update.message.reply_sticker(sticker=media.goat)
    if "smashed" in message:
        await update.message.reply_sticker(sticker=media.smashed)
    if "wagmi" in message:
        await update.message.reply_sticker(sticker=media.wagmi)
    if "slapped" in message:
        await update.message.reply_sticker(sticker=media.slapped)


async def admin_commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        await update.message.reply_text(
            f'{text.admin_commands}',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Rose Bot Anti-flood', url='https://missrose.org/guide/antiflood/')], ]))
    else:
        await update.message.reply_text(f'{text.mods_only}')


async def mods_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'{text.mods}')


async def error(update, context):
    print(f'Update {update} caused error: {context.error}')


# RUN
if __name__ == '__main__':
    application = ApplicationBuilder().token(keys.token).build()
    job_queue = application.job_queue
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_replies))
    application.add_error_handler(error)
    application.add_handler(CommandHandler('test', test_command))
    application.add_handler(CommandHandler('supply', supply_command))
    application.add_handler(CommandHandler('potw', potw_command))
    application.add_handler(CommandHandler('launch', launch_command))
    application.add_handler(CommandHandler('signers', signers_command))
    application.add_handler(CommandHandler('magisters', magisters_command))
    application.add_handler(CommandHandler(['on_chain', 'deployer', 'devs'], deployer_command))
    application.add_handler(CommandHandler(['links', 'socials'], links_command))
    application.add_handler(CommandHandler(['ca', 'contract', 'contracts'], ca_command))
    application.add_handler(CommandHandler('x7r', x7r_command))
    application.add_handler(CommandHandler(['x7dao', 'dao'], x7dao_command))
    application.add_handler(CommandHandler(['x7101', '101'], x7101_command))
    application.add_handler(CommandHandler(['x7102', '102'], x7102_command))
    application.add_handler(CommandHandler(['x7103', '103'], x7103_command))
    application.add_handler(CommandHandler(['x7104', '104'], x7104_command))
    application.add_handler(CommandHandler(['x7105', '105'], x7105_command))
    application.add_handler(CommandHandler(['nft', 'nfts'], nft_command))
    application.add_handler(CommandHandler('treasury', treasury_command))
    application.add_handler(CommandHandler(['website', 'site'], website_command))
    application.add_handler(CommandHandler(['whitepaper', 'wp', 'wpquote'], wp_command))
    application.add_handler(CommandHandler('buy', buy_command))
    application.add_handler(CommandHandler('smart', smart_command))
    application.add_handler(CommandHandler(['chart', 'charts'], chart_command))
    application.add_handler(CommandHandler(['opensea',  'os'], opensea_command))
    application.add_handler(CommandHandler('about', about_command))
    application.add_handler(CommandHandler('withdraw', withdraw_command))
    application.add_handler(CommandHandler(['price', 'prices'], price_command))
    application.add_handler(CommandHandler(['ecosystem', 'tokens'], ecosystem_command))
    application.add_handler(CommandHandler('media', media_command))
    application.add_handler(CommandHandler('buyevenly', buy_evenly_command))
    application.add_handler(CommandHandler(['bot', 'start', 'filters'], bot_command))
    application.add_handler(CommandHandler('channels', channels_command))
    application.add_handler(CommandHandler('pioneer', pioneer_command))
    application.add_handler(CommandHandler(['spaces', 'space'], spaces_command))
    application.add_handler(CommandHandler('burn', burn_command))
    application.add_handler(CommandHandler('search', search_command))
    application.add_handler(CommandHandler(['pool', 'lpool', 'lendingpool'], pool_command))
    application.add_handler(CommandHandler(['tax', 'slippage'], tax_command))
    application.add_handler(CommandHandler(['swap', 'xchange', 'dex'], swap_command))
    application.add_handler(CommandHandler('giveaway', giveaway_command))
    application.add_handler(CommandHandler(['mcap', 'marketcap', 'cap'], mcap_command))
    application.add_handler(CommandHandler('roadmap', roadmap_command))
    application.add_handler(CommandHandler(['time', 'clock'], time_command))
    application.add_handler(CommandHandler(['buybots', 'bobby', 'buybot'], buy_bots_command))
    application.add_handler(CommandHandler('joke', joke_command))
    application.add_handler(CommandHandler('faq', faq_command))
    application.add_handler(CommandHandler('quote', quote_command))
    application.add_handler(CommandHandler('today', today_command))
    application.add_handler(CommandHandler('holders', holders_command))
    application.add_handler(CommandHandler(['fg', 'feargreed'], fg_command))
    application.add_handler(CommandHandler('x7d', x7d_command))
    application.add_handler(CommandHandler('count', count_command))
    application.add_handler(CommandHandler('draw', draw_command))
    application.add_handler(CommandHandler(['constellations', 'constellation', 'quints'], constellations_command))
    application.add_handler(CommandHandler(['loans', 'borrow'], loans_command))
    application.add_handler(CommandHandler('start_auto', auto_command))
    application.add_handler(CommandHandler('stop_auto', stop_auto_command))
    application.add_handler(CommandHandler('show_auto', show_auto_command))
    application.add_handler(CommandHandler('twitter', twitter_command))
    application.add_handler(CommandHandler('announcements', announcements_command))
    application.add_handler(CommandHandler('say', say_command))
    application.add_handler(CommandHandler('liquidity', liquidity_command))
    application.add_handler(CommandHandler('mods', mods_command))
    application.add_handler(CommandHandler('voting', voting_command))
    application.add_handler(CommandHandler('gas', gas_command))
    application.add_handler(CommandHandler('wei', wei_command))
    application.add_handler(CommandHandler('alumni', alumni_command))
    application.add_handler(CommandHandler(['docs', 'dashboard'], dashboard_command))
    application.add_handler(CommandHandler(['snapshot', 'rollout', 'multichain', 'airdrop'], snapshot_command))
    application.add_handler(CommandHandler(['discount', 'dsc', 'dac'], discount_command))
    application.add_handler(CommandHandler(['admin_commands', 'admin', 'admincommands'], admin_commands_command))
    application.job_queue.run_repeating(
        wp_message, variables.wp_time * 60 * 60,
        chat_id=ca.main_id,
        name=str('WP Message'),
        data=variables.wp_time * 60 * 60)
    application.run_polling()
