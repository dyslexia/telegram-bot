from telegram.ext import *
from telegram import *
import api
import ca
from datetime import datetime, timedelta, timezone
from dateutil import parser
import keys
import pytz
import loans
import main
import media
import nfts
from PIL import Image, ImageDraw, ImageFont
import random
import requests
import tax
import text
import textwrap
import times
from translate import Translator
import tweepy
import pandas as pd
import pyttsx3
import url
import wikipediaapi
import re

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    est_timezone = pytz.timezone('US/Eastern')
    utc_timezone = pytz.timezone('UTC')

    # Extract the time variable from the message
    message = update.message.text.split(' ')
    time_variable = message[1]

    # Parse the time variable to a datetime object
    est_time = datetime.strptime(time_variable, "%I%p")
    est_time = est_timezone.localize(est_time)

    # Convert EST time to UTC time
    utc_time = est_time.astimezone(utc_timezone)
    utc_time_str = utc_time.strftime("%I %p")

    # Send the converted time as a response
    response = f"The equivalent UTC time is {utc_time_str}"
    await update.message.reply_text(
        f'{response}',
        parse_mode='Markdown')

# COMMANDS
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f'{text.about}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url=f'{url.website}')],
            [InlineKeyboardButton(text='Community Dashboard', url=f'{url.dashboard}')],
            [InlineKeyboardButton(text='Linktree', url=f'{url.linktree}')],
            [InlineKeyboardButton(text='Medium', url=f'{url.medium}')], ]))

async def airdrop(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def alumni(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Alumni*\n\n'
                f'@Callmelandlord - The Godfather of the X7 Finance community, the OG, the creator - X7 God\n\n'
                f'@WoxieX - Creator of the OG dashboard -  x7community.space\n\n'
                f'@Zaratustra  - Defi extraordinaire and protocol prophet\n\n'
                f'{api.get_quote()}', parse_mode='Markdown')

async def announcements(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption='Check out the link below for the announcement channel',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='X7 Announcement Channel', url="https://t.me/X7announcements")], ]))

async def beta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'https://beta.x7.finance/')

async def bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'{text.commands}')

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
        "arb": ("(ARB)", url.xchange_buy_arb)
    }
    if chain in chain_mappings:
        chain_name, chain_url = chain_mappings[chain]
    else:
        chain_name, chain_url = chain_mappings["eth"]
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Buy Links {chain_name}*\nUse `/buy [chain-name]` for other chains\n'
                f'Use `/constellations` for constellations\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='X7R - Rewards Token', url=f'{chain_url}{ca.x7r}')],
            [InlineKeyboardButton(text='X7DAO - Governance Token', url=f'{chain_url}{ca.x7dao}')], ]))

async def buy_bots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Bobby Buy Bot Channels*\n\n{api.get_quote()}', parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Xchange Alerts', url='https://t.me/x7_alerts)')],
             [InlineKeyboardButton(text='Ethereum', url='https://t.me/X7constellation)')],
             [InlineKeyboardButton(text='Arbitrum', url='https://t.me/x7arbbuybots')],
             [InlineKeyboardButton(text='BSC', url='https://t.me/x7bscbuybots')],
             [InlineKeyboardButton(text='Optimism', url='https://t.me/x7optibuybots')],
             [InlineKeyboardButton(text='Polygon', url='https://t.me/x7polygonbuybots')], ]))

async def buy_evenly(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def contracts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Contract Addresses for all chains*\n\n'
                f'*X7R - Rewards Token *\n`{ca.x7r}`\n\n'
                f'*X7DAO - Governance Token*\n`{ca.x7dao}`\n\n'
                f'For advanced trading and arbitrage opportunities see `/constellations`\n\n'
                f'{api.get_quote()}',
        parse_mode='Markdown')

async def channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Community TG Channels*\n\n{api.get_quote()}', parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Community Chat', url='https://t.me/X7m105portal')],
             [InlineKeyboardButton(text='Announcements', url='https://t.me/X7announcements')],
             [InlineKeyboardButton(text='Xchange Alerts', url='https://t.me/x7_alerts)')],
             [InlineKeyboardButton(text='Media', url='https://t.me/X7MediaChannel')],
             [InlineKeyboardButton(text='Research Notes', url='https://t.me/X7m105_Research')],
             [InlineKeyboardButton(text='Chinese Community', url='https://t.me/X7CNPortal')], ]))

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
        "arb": (url.dex_tools_arb, "(ARB)")
    }
    if chain in chain_mappings:
        chain_url, chain_name = chain_mappings[chain]
    else:
        chain_url, chain_name = chain_mappings["eth"]
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Chart Links* {chain_name}\nUse `/chart [chain-name]` for other chains\n'
                f'Use `/constellations` for constellations\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='X7R - Rewards Token', url=f'{chain_url}{ca.x7r_pair_eth}')],
            [InlineKeyboardButton(text='X7DAO - Governance Token', url=f'{chain_url}{ca.x7dao_pair_eth}')], ]))

async def community(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f'{text.multi_sig}',
        parse_mode='Markdown')

async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def deployer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tx = api.get_tx(ca.deployer, "eth")
    time = datetime.utcfromtimestamp(int(tx["result"][0]["timeStamp"]))
    now = datetime.utcnow()
    duration = now - time
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    if str(tx["result"][0]["to"]).lower() == "0x000000000000000000000000000000000000dead":
        message = bytes.fromhex(tx[0]["input"][2:]).decode('utf-8')
        await update.message.reply_text(
            f'*Last On Chain Message:*\n\n{time} (UTC)\n'
            f'{int(days[0])} days, {int(hours[0])} hours and {int(minutes[0])} minutes ago:\n\n'
            f'`{message}`\n',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='View on chain', url=f'{url.ether_tx}{tx["result"][0]["hash"]}')],
                 [InlineKeyboardButton(text='View all on chains', url=f'{url.dashboard}onchains')], ]))
    else:
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption=f'*Deployer Wallet last TX*\n\n{time} (UTC)\n'
                    f'{int(days[0])} days, {int(hours[0])} hours and {int(minutes[0])} minutes ago:\n\n'
                    f'*{tx["result"][0]["functionName"]}*\n\n'
                    f'This command will pull last TX on the X7 Finance deployer wallet.'
                    f' To view last on chain use `/on_chain`\n\n'
                    f'{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='View on chain', url=f'{url.ether_tx}{tx["result"][0]["hash"]}')],
                 [InlineKeyboardButton(text='View all on chains', url=f'{url.dashboard}onchains')], ]))

async def discount(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def draw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tweet = context.args[0]
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        start = tweet.index('status/')
        end = tweet.index('?', start + 1)
        tweet_id = tweet[start + 7:end]
        rt_client = tweepy.Client(keys.twitter_bearer)
        rt_auth = tweepy.OAuthHandler(keys.twitter_api, keys.twitter_api_secret)
        rt_auth.set_access_token(keys.twitter_access, keys.twitter_access_secret)
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

async def ebb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "eth" or chain == "":
        chain_name = "(ETH)"
        chain_url = url.ether_address
        now = datetime.utcnow()

        def get_liquidity_data(hub_address):
            hub = api.get_tx_internal(hub_address, "eth")
            hub_filter = [d for d in hub["result"] if d['from'] in str(hub_address).lower()]
            value_raw = int(hub_filter[0]["value"]) / 10 ** 18
            value = str(value_raw)
            dollar = float(value) * float(api.get_native_price("eth")) / 1 ** 18
            time = datetime.utcfromtimestamp(int(hub_filter[0]["timeStamp"]))
            duration = now - time
            duration_in_s = duration.total_seconds()
            days = divmod(duration_in_s, 86400)
            hours = divmod(days[1], 3600)
            minutes = divmod(hours[1], 60)
            return value, dollar, time, int(days[0]), int(hours[0]), int(minutes[0])
        x7r_value, x7r_dollar, x7r_time, x7r_days, x7r_hours, x7r_minutes = get_liquidity_data(ca.x7r_liq_hub)
        x7dao_value, x7dao_dollar, x7dao_time, x7dao_days, x7dao_hours, x7dao_minutes = \
            get_liquidity_data(ca.x7dao_liq_hub)
        x7100_value, x7100_dollar, x7100_time, x7100_days, x7100_hours, x7100_minutes = \
            get_liquidity_data(ca.x7100_liq_hub)
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption=f'*X7 Finance Liquidity Hubs {chain_name}*\nUse `/ebb [chain-name]` for other chains\n\n'
            f'Last X7R Buy Back: {x7r_time}\n{x7r_value[:5]} ETH (${"{:0,.0f}".format(x7r_dollar)})\n'
            f'{x7r_days} days, {x7r_hours} hours and {x7r_minutes} minutes ago\n\n'
            f'Last X7DAO Buy Back: {x7dao_time}\n{x7dao_value[:5]} ETH (${"{:0,.0f}".format(x7dao_dollar)})\n'
            f'{x7dao_days} days, {x7dao_hours} hours and {x7dao_minutes} minutes ago\n\n'
            f'Last X7100 Buy Back: {x7100_time}\n{x7100_value[:5]} ETH (${"{:0,.0f}".format(x7100_dollar)})\n'
            f'{x7100_days} days, {x7100_hours} hours and {x7100_minutes} minutes ago\n\n'
            f'{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R Liquidity Hub', url=f'{chain_url}{ca.x7r_liq_hub}')],
                [InlineKeyboardButton(text='X7DAO Liquidity Hub', url=f'{chain_url}{ca.x7dao_liq_hub}')],
                [InlineKeyboardButton(text='X7100 Liquidity Hub', url=f'{chain_url}{ca.x7100_liq_hub}')], ]))

async def ecosystem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f'{text.ecosystem}'
        f'\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url=f'{url.website}')],
            [InlineKeyboardButton(text='Community Dashboard', url=f'{url.dashboard}')],
            [InlineKeyboardButton(text='Linktree', url=f'{url.linktree}')],
            [InlineKeyboardButton(text='Medium', url=f'{url.medium}')], ]))

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def fg(update, context):
    fear_response = requests.get('https://api.alternative.me/fng/?limit=0')
    fear_data = fear_response.json()

    fear_values = []
    for i in range(7):
        timestamp = float(fear_data["data"][i]["timestamp"])
        localtime = datetime.fromtimestamp(timestamp)
        fear_values.append((fear_data["data"][i]["value"], fear_data["data"][i]["value_classification"], localtime))
    duration_in_s = float(fear_data["data"][0]["time_until_update"])
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    caption = '*Market Fear and Greed Index*\n\n'
    caption += f'{fear_values[0][0]} - {fear_values[0][1]} - {fear_values[0][2].strftime("%A %B %d")}\n\n'
    caption += 'Change:\n'
    for i in range(1, 7):
        caption += f'{fear_values[i][0]} - {fear_values[i][1]} - {fear_values[i][2].strftime("%A %B %d")}\n'
    caption += '\nNext Update:\n'
    caption += f'{int(hours[0])} hours and {int(minutes[0])} minutes\n\n{api.get_quote()}'
    await update.message.reply_photo(
        photo='https://alternative.me/crypto/fear-and-greed-index.png',
        caption=caption,
        parse_mode='Markdown'
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
        chain_url = 'https://polygon.com/gastracker'
    if im2 is None:
        await update.message.reply_text(
            "Invalid chain. Please provide a valid chain name.",
            parse_mode="Markdown")
        return
    im1 = Image.open(random.choice(media.blackhole))
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (26, 30),
        f'{chain_name} Gas Prices:\n\n'
        f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n'
        f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n'
        f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n\n\n\n\n\n\n\n'
        f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font=myfont,
        fill=(255, 255, 255))
    im1.save("media/blackhole.png")
    await update.message.reply_photo(
        photo=open("media/blackhole.png", 'rb'),
        caption=f'*{chain_name} Gas Prices:*\n'
                f'For other chains use `/gas [chain-name]`\n\n'
                f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n'
                f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n'
                f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n'
                f'{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text=f'{chain_name} Gas Tracker', url=chain_url)]]))

async def giveaway(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ext = " ".join(context.args)
    excel = r"raffle.csv"
    df = pd.read_csv(excel)
    addresses = list(df.Address)
    last5 = [entry[-5:] for entry in addresses]
    giveaway_time = times.giveaway_time.astimezone(pytz.utc)
    snapshot1 = times.snapshot1.astimezone(pytz.utc)
    snapshot2 = times.snapshot2.astimezone(pytz.utc)
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
            update_utc = times.giveaway_update.astimezone(pytz.utc)
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

async def holders(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    img = Image.open((random.choice(media.blackhole)))
    i1 = ImageDraw.Draw(img)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 28)
    wrapper = textwrap.TextWrapper(width=50)
    word_list = wrapper.wrap(text=text)
    caption_new = ""
    for ii in word_list:
        caption_new = caption_new + ii + '\n'
    i1.text((50, img.size[1] / 8), caption_new, font=myfont, fill=(255, 255, 255))
    img.save(r"media\blackhole.png")
    i1.text((50, 460),
            f'{update.message.from_user.username}\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont, fill=(255, 255, 255))
    img.save(r"media\blackhole.png")
    await update.message.reply_photo(
        photo=open(r"media\blackhole.png", 'rb'))

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def launch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    launch_raw = datetime(2022, 8, 13, 14, 10, 17)
    migration_raw = datetime(2022, 9, 25, 5, 00, 11)
    launch = launch_raw.astimezone(pytz.utc)
    migration = migration_raw.astimezone(pytz.utc)
    now = datetime.now(timezone.utc)
    launch_duration = now - launch
    launch_days, launch_remainder = divmod(launch_duration.total_seconds(), 86400)
    launch_hours, launch_remainder = divmod(launch_remainder, 3600)
    launch_minutes, _ = divmod(launch_remainder, 60)
    migration_duration = now - migration
    migration_days, migration_remainder = divmod(migration_duration.total_seconds(), 86400)
    migration_hours, migration_remainder = divmod(migration_remainder, 3600)
    migration_minutes, _ = divmod(migration_remainder, 60)
    await update.message.reply_photo(
        photo=open(random.choice(media.logos), 'rb'),
        caption=f'*X7 Finance Launch Info*\n\nX7M105 Stealth Launch\n{launch.strftime("%A %B %d %Y %I:%M %p")} (UTC)\n'
                f'{int(launch_days)} days, {int(launch_hours)} hours and {int(launch_minutes)} minutes ago\n\n'
                f'V2 Migration\n{migration.strftime("%A %B %d %Y %I:%M %p")} (UTC)\n'
                f'{int(migration_days)} days, {int(migration_hours)} hours and {int(migration_minutes)} minutes ago\n\n'
                f'{api.get_quote()}',
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                text='X7M105 Launch TX',
                url='https://etherscan.io/tx/0x11ff5b6a860170eaac5b33930680bf79dbf0656292cac039805dbcf34e8abdbf')],
            [InlineKeyboardButton(
                text='Migration Go Live TX',
                url='https://etherscan.io/tx/0x13e8ed59bcf97c5948837c8069f1d61e3b0f817d6912015427e468a77056fe41')], ]))

async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance links*\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url=f'{url.website}')],
            [InlineKeyboardButton(text='Community Dashboard', url=f'{url.dashboard}')],
            [InlineKeyboardButton(text='Snapshot', url=f'{url.snapshot}')],
            [InlineKeyboardButton(text='Linktree', url=f'{url.linktree}')],
            [InlineKeyboardButton(text='Medium', url=f'{url.medium}')],
            [InlineKeyboardButton(text='Twitter', url=f'{url.twitter}')],
            [InlineKeyboardButton(text='Discord', url=f'{url.discord}')],
            [InlineKeyboardButton(text='Reddit', url=f'{url.reddit}')],
            [InlineKeyboardButton(text='Youtube', url=f'{url.youtube}')],
            [InlineKeyboardButton(text='Github', url=f'{url.github}')], ]))

async def loans_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loan_type = " ".join(context.args).lower()
    loan_name = ""
    loan_terms = ""
    loan_ca = ""
    if loan_type == "":
        await update.message.reply_text(
            f'{loans.overview}\n\n{api.get_quote()}',
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='X7 Finance Whitepaper', url=f'{url.wp_link}')], ]))
        return
    loan_types = {
        "ill001": (loans.ill001_name, loans.ill001_terms, ca.ill001),
        "ill002": (loans.ill002_name, loans.ill002_terms, ca.ill002),
        "ill003": (loans.ill003_name, loans.ill003_terms, ca.ill003)
    }
    if loan_type in loan_types:
        loan_name, loan_terms, loan_ca = loan_types[loan_type]
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'{loan_name}\n\n{loan_terms}\n\n',
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=f'Ethereum', url=f'{url.ether_address}{loan_ca}')],
             [InlineKeyboardButton(text=f'BSC', url=f'{url.bsc_address}{loan_ca}')],
             [InlineKeyboardButton(text=f'Polygon', url=f'{url.poly_address}{loan_ca}')],
             [InlineKeyboardButton(text=f'Arbitrum', url=f'{url.arb_address}{loan_ca}')],
             [InlineKeyboardButton(text=f'Optimism', url=f'{url.opti_address}{loan_ca}')], ]))

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
    magisters = [holder['owner_of'] for holder in response["result"]]
    address = '\n\n'.join(map(str, magisters))
    await update.message.reply_photo(
        photo=open(random.choice(media.logos), 'rb'),
        caption=f'*X7 Finance Magister Holders {chain_name}*\n'
                f'Use `/magisters [chain-name]` or other chains\n\n'
                f'Holders - {holders}\n\n'
                f'`{address}`\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                text='Magister Holder List', url=f'{chain_url}{ca.magister}#balances')], ]))

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

async def nft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_name = ""
    eco_count = ""
    borrow_count = ""
    dex_count = ""
    liq_count = ""
    magister_count = ""
    chain_url = ""
    eco_price = ""
    borrow_price = ""
    dex_price = ""
    liq_price = ""
    magister_price = ""
    if chain == "" or chain == "eth":
        chain_name = "(ETH)"
        eco_count = int(api.get_nft_holder_count(ca.eco, "?chain=eth-main"))
        borrow_count = int(api.get_nft_holder_count(ca.borrow, "?chain=eth-main"))
        dex_count = int(api.get_nft_holder_count(ca.dex, "?chain=eth-main"))
        liq_count = int(api.get_nft_holder_count(ca.liq, "?chain=eth-main"))
        magister_count = int(api.get_nft_holder_count(ca.magister, "?chain=eth-main"))
        chain_url = url.ether_address
        eco_price = nfts.eco_price_eth
        borrow_price = nfts.borrow_price_eth
        dex_price = nfts.dex_price_eth
        liq_price = nfts.liq_price_eth
        magister_price = nfts.magister_price_eth
        await update.message.reply_video(
            video=open(media.nft_logo, 'rb'),
            caption=f'*X7 Finance NFT Information {chain_name}*\nUse `/nft [chain-name]` for other chains\n\n'
                    f'*Ecosystem Maxi*\n{eco_price}\n'
                    f'Available - {500 - eco_count}\n'
                    f'> {tax.eco_discount_x7100}% discount on X7100 tax\n'
                    f'> {tax.eco_discount_x7r}% discount on X7R tax\n'
                    f'> {tax.eco_discount_x7dao}% discount on X7DAO tax\n\n'
                    f'*Liquidity Maxi*\n{liq_price}\n'
                    f'Available - {250 - liq_count}\n'
                    f'> {tax.liq_discount_x7100}% discount on X7100 tax\n'
                    f'> {tax.liq_discount_x7r}% discount on X7R tax\n'
                    f'> {tax.liq_discount_x7dao}% discount on X7DAO tax\n\n'
                    f'*Dex Maxi*\n{dex_price}\n'
                    f'Available - {150 - dex_count}\n'
                    f'> LP Fee Discounts while trading on X7 DEX\n\n'
                    f'*Borrowing Maxi*\n{borrow_price}\n'
                    f'Available - {100 - borrow_count}\n'
                    f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n'
                    f'*Magister*\n{magister_price}\n'
                    f'Available - {49 - magister_count}\n'
                    f'> {tax.magister_discount_x7100}% discount on X7100 tax\n'
                    f'> {tax.magister_discount_x7r}% discount on X7R tax\n> No discount on X7DAO tax\n\n'
                    f'*Pioneer*\n'
                    f' > 6% of profits that come into the X7 Treasury Splitter are allocated to the reward '
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
        return
    if chain == "poly" or chain == "polygon":
        chain_name = "(POLYGON)"
        eco_count = int(api.get_nft_holder_count(ca.eco, "?chain=poly-main"))
        borrow_count = int(api.get_nft_holder_count(ca.borrow, "?chain=poly-main"))
        dex_count = int(api.get_nft_holder_count(ca.dex, "?chain=poly-main"))
        liq_count = int(api.get_nft_holder_count(ca.liq, "?chain=poly-main"))
        magister_count = int(api.get_nft_holder_count(ca.magister, "?chain=poly-main"))
        chain_url = url.poly_address
        eco_price = nfts.eco_price_poly
        borrow_price = nfts.borrow_price_poly
        dex_price = nfts.dex_price_poly
        liq_price = nfts.liq_price_poly
        magister_price = nfts.magister_price_poly
    if chain == "bsc" or chain == "bnb":
        chain_name = "(BSC)"
        eco_count = 0
        borrow_count = 0
        dex_count = 0
        liq_count = 0
        magister_count = 0
        chain_url = url.bsc_address
        eco_price = nfts.eco_price_bsc
        borrow_price = nfts.borrow_price_bsc
        dex_price = nfts.dex_price_bsc
        liq_price = nfts.liq_price_bsc
        magister_price = nfts.magister_price_bsc
    if chain == "opti" or chain == "optimism" or chain == "op":
        chain_name = "(OPTIMISM)"
        eco_count = int(api.get_nft_holder_count(ca.eco, "?chain=optimism-main"))
        borrow_count = int(api.get_nft_holder_count(ca.borrow, "?chain=optimism-main"))
        dex_count = int(api.get_nft_holder_count(ca.dex, "?chain=optimism-main"))
        liq_count = int(api.get_nft_holder_count(ca.liq, "?chain=optimism-main"))
        magister_count = int(api.get_nft_holder_count(ca.magister, "?chain=optimism-main"))
        chain_url = url.opti_address
        eco_price = nfts.eco_price_opti
        borrow_price = nfts.borrow_price_opti
        dex_price = nfts.dex_price_opti
        liq_price = nfts.liq_price_opti
        magister_price = nfts.magister_price_opti
    if chain == "arb" or chain == "arbitrum":
        chain_name = "(ARB)"
        eco_count = int(api.get_nft_holder_count(ca.eco, "?chain=arbitrum-main"))
        borrow_count = int(api.get_nft_holder_count(ca.borrow, "?chain=arbitrum-main"))
        dex_count = int(api.get_nft_holder_count(ca.dex, "?chain=arbitrum-main"))
        liq_count = int(api.get_nft_holder_count(ca.liq, "?chain=arbitrum-main"))
        magister_count = int(api.get_nft_holder_count(ca.magister, "?chain=arbitrum-main"))
        chain_url = url.arb_address
        eco_price = nfts.eco_price_arb
        borrow_price = nfts.borrow_price_arb
        dex_price = nfts.dex_price_arb
        liq_price = nfts.liq_price_arb
        magister_price = nfts.magister_price_arb
    await update.message.reply_video(
        video=open(media.nft_logo, 'rb'),
        caption=f'*X7 Finance NFT Information {chain_name}*\nUse `/nft [chain-name]` for other chains\n\n'
                f'*Ecosystem Maxi*\n{eco_price}\n'
                f'Available - {500 - eco_count}\n'
                f'> {tax.eco_discount_x7100}% discount on X7100 tax\n'
                f'> {tax.eco_discount_x7r}% discount on X7R tax\n'
                f'> {tax.eco_discount_x7dao}% discount on X7DAO tax\n\n*'
                f'Liquidity Maxi*\n{liq_price}\n'
                f'Available - {250 - liq_count}\n'
                f'> {tax.liq_discount_x7100}% discount on X7100 tax\n'
                f'> {tax.liq_discount_x7r}% discount on X7R tax\n'
                f'> {tax.liq_discount_x7dao}% discount on X7DAO tax\n\n'
                f'*Dex Maxi*\n{dex_price}\n'
                f'Available - {150 - dex_count}\n'
                f'> LP Fee Discounts while trading on X7 DEX\n\n'
                f'*Borrowing Maxi*\n{borrow_price}\n'
                f'Available - {100 - borrow_count}\n'
                f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n'
                f'*Magister*\n{magister_price}\n'
                f'Available - {49 - magister_count}\n'
                f'> {tax.magister_discount_x7100}% discount on X7100 tax\n'
                f'> {tax.magister_discount_x7r}% discount on X7R tax\n> No discount on X7DAO tax\n\n'
                f'{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Mint Here', url='https://x7.finance/x/nft/mint')],
            [InlineKeyboardButton(text='Ecosystem Maxi', url=f'{chain_url}{ca.eco}')],
            [InlineKeyboardButton(text='Liquidity Maxi', url=f'{chain_url}{ca.liq}')],
            [InlineKeyboardButton(text='DEX Maxi', url=f'{chain_url}{ca.dex}')],
            [InlineKeyboardButton(text='Borrowing Maxi', url=f'{chain_url}{ca.borrow}')],
            [InlineKeyboardButton(text='Magister', url=f'{chain_url}{ca.magister}')], ]))

async def on_chain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.utcnow()
    tx = api.get_tx(ca.deployer, "eth")
    tx_filter = [d for d in tx["result"] if d['to'] in str(ca.dead).lower()]
    message = bytes.fromhex(tx_filter[0]["input"][2:]).decode('utf-8')
    time = datetime.utcfromtimestamp(int(tx_filter[0]["timeStamp"]))
    duration = now - time
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    print(tx_filter[0])
    await update.message.reply_text(
        f'*Last On Chain Message:*\n\n{time} (UTC)\n'
        f'{int(days[0])} days, {int(hours[0])} hours and {int(minutes[0])} minutes ago\n\n'
        f'`{message}`', parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='View on chain', url=f'{url.ether_tx}{tx_filter[0]["hash"]}')],
            [InlineKeyboardButton(text='View all on chains', url=f'{url.dashboard}onchains')], ]))

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
        photo=open(media.opensea_logo, 'rb'),
        caption=f'*X7 Finance Opensea Links {chain_name}*\nUse `/nft [chain-name]` '
                f'for other chains\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Ecosystem Maxi', url=f'{url.os_eco}{chain_url}')],
            [InlineKeyboardButton(text='Liquidity Maxi', url=f'{url.os_liq}{chain_url}')],
            [InlineKeyboardButton(text='DEX Maxi', url=f'{url.os_dex}{chain_url}')],
            [InlineKeyboardButton(text='Borrowing Maxi', url=f'{url.os_borrow}{chain_url}')],
            [InlineKeyboardButton(text='Magister', url=f'{url.os_magister}{chain_url}')], ]))

async def pioneer(update: Update, context: ContextTypes.DEFAULT_TYPE = None):
    pioneer_id = " ".join(context.args)
    data = api.get_os_nft("/x7-pioneer")
    floor = api.get_nft_floor(ca.pioneer, "?chain=eth-main")
    floor_dollar = floor * float(api.get_native_price("eth")) / 1 ** 18
    traits = data["collection"]["traits"]["Transfer Lock Status"]["unlocked"]
    cap = round(data["collection"]["stats"]["market_cap"], 2)
    cap_dollar = cap * float(api.get_native_price("eth")) / 1 ** 18
    sales = data["collection"]["stats"]["total_sales"]
    owners = data["collection"]["stats"]["num_owners"]
    price = round(data["collection"]["stats"]["average_price"], 2)
    price_dollar = price * float(api.get_native_price("eth")) / 1 ** 18
    volume = round(data["collection"]["stats"]["total_volume"], 2)
    volume_dollar = volume * float(api.get_native_price("eth")) / 1 ** 18
    pioneer_pool = api.get_native_balance(ca.pioneer, "eth")
    total_dollar = float(pioneer_pool) * float(api.get_native_price("eth")) / 1 ** 18
    if pioneer_id == "":
        img = Image.open(random.choice(media.blackhole))
        i1 = ImageDraw.Draw(img)
        myfont = ImageFont.truetype(r"media\FreeMonoBold.ttf", 28)
        i1.text(
            (28, 36),
            f"X7 Pioneer NFT Info\n\n"
            f"Floor Price: {floor} ETH (${'{:0,.0f}'.format(floor_dollar)})\n"
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
        img.save(r"media\blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", "rb"),
            caption=f"*X7 Pioneer NFT Info*\n\n"
            f"Floor Price: {floor} ETH (${'{:0,.0f}'.format(floor_dollar)})\n"
            f"Average Price: {price} ETH (${'{:0,.0f}'.format(price_dollar)})\n"
            f"Market Cap: {cap} ETH (${'{:0,.0f}'.format(cap_dollar)})\n"
            f"Total Volume: {volume} ETH (${'{:0,.0f}'.format(volume_dollar)})\n"
            f"Number of Owners: {owners}\n"
            f"Pioneers Unlocked: {traits}\n\n"
            f"Pioneer Pool: {pioneer_pool[:3]} ETH (${'{:0,.0f}'.format(total_dollar)})\n\n"
            f"{api.get_quote()}",
            parse_mode="markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="X7 Pioneer Dashboard", url="https://x7.finance/x/nft/pioneer")],
                 [InlineKeyboardButton(text="Blur Marketplace",
                                       url="https://blur.io/collection/x7-pioneer"
                                           "?traits=%7B%22Transfer%20Lock%20Status%22%3A%5B%22Unlocked%22%5D%7D")], ]))
    else:
        base_url = "https://api.opensea.io/api/v1/asset/"
        slug = ca.pioneer + "/"
        headers = {"X-API-KEY": keys.os}
        single_url = base_url + slug + pioneer_id + "/"
        single_response = requests.get(single_url, headers=headers)
        single_data = single_response.json()
        status = single_data["traits"][0]["value"]
        await update.message.reply_text(
            f"*X7 Pioneer {pioneer_id} NFT Info*\n\n"
            f"Transfer Lock Status: {status}\n\n"
            f"https://opensea.io/assets/ethereum/0x70000299ee8910ccacd97b1bb560e34f49c9e4f7/{pioneer_id}\n\n"
            f"{api.get_quote()}",
            parse_mode="markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="X7 Pioneer Dashboard", url="https://x7.finance/x/nft/pioneer")],
                 [InlineKeyboardButton(text="Blur Marketplace",
                                       url="https://blur.io/collection/x7-pioneer?"
                                           "traits=%7B%22Transfer%20Lock%20Status%22%3A%5B%22Unlocked%22%5D%7D")], ]))

async def pool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_name = ""
    chain_token = ""
    pool = ""
    pool_dollar = ""
    im2 = None
    chain_url = ""
    eth_pool = api.get_native_balance(ca.lpool_reserve, "eth")
    eth_dollar = float(eth_pool) * float(api.get_native_price("eth")) / 1 ** 18
    bsc_pool = api.get_native_balance(ca.lpool_reserve, "bsc")
    bsc_pool_dollar = float(bsc_pool) * float(api.get_native_price("bnb")) / 1 ** 18
    arb_pool = api.get_native_balance(ca.lpool_reserve, "arb")
    arb_pool_dollar = float(arb_pool) * float(api.get_native_price("eth")) / 1 ** 18
    poly_pool = api.get_native_balance(ca.lpool_reserve, "poly")
    poly_pool_dollar = float(poly_pool) * float(api.get_native_price("matic")) / 1 ** 18
    opti_pool = api.get_native_balance(ca.lpool_reserve, "opti")
    opti_pool_dollar = float(opti_pool) * float(api.get_native_price("eth")) / 1 ** 18
    total_dollar = poly_pool_dollar + bsc_pool_dollar + opti_pool_dollar + arb_pool_dollar + eth_dollar
    if chain == "":
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7d_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 28)
        i1.text((28, 36),
                f'X7 Finance Lending Pool Info\n\n'
                f'ETH: {eth_pool[:5]} ETH (${"{:0,.0f}".format(eth_dollar)})\n'
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
                    f'ETH: {eth_pool[:5]} ETH (${"{:0,.0f}".format(eth_dollar)})\n'
                    f'ARB: {arb_pool[:4]} ETH (${"{:0,.0f}".format(arb_pool_dollar)})\n'
                    f'OPTI: {opti_pool[:4]} ETH (${"{:0,.0f}".format(opti_pool_dollar)})\n'
                    f'BSC: {bsc_pool[:4]} BNB (${"{:0,.0f}".format(bsc_pool_dollar)})\n'
                    f'POLY: {poly_pool[:6]} MATIC (${"{:0,.0f}".format(poly_pool_dollar)})\n\n'
                    f'TOTAL: ${"{:0,.0f}".format(total_dollar)}\n\n'
                    f'{api.get_quote()}', parse_mode='Markdown')
        return
    if chain == "eth":
        chain_name = "(ETH)"
        chain_token = "ETH"
        pool = eth_pool[:4]
        chain_url = url.ether_address
        pool_dollar = float(pool) * float(api.get_native_price("eth")) / 1 ** 18
        im2 = Image.open(media.eth_logo)
    if chain == "bsc" or chain == "bnb":
        chain_name = "(BSC)"
        chain_token = "BNB"
        pool = bsc_pool[:4]
        chain_url = url.bsc_address
        pool_dollar = float(pool) * float(api.get_native_price("bnb")) / 1 ** 18
        im2 = Image.open(media.bsc_logo)
    if chain == "arbitrum" or chain == "arb":
        chain_name = "(ARB)"
        chain_token = "ETH"
        pool = arb_pool[:4]
        chain_url = url.arb_address
        pool_dollar = float(pool) * float(api.get_native_price("eth")) / 1 ** 18
        im2 = Image.open(media.arb_logo)
    if chain == "optimism" or chain == "opti":
        chain_name = "(OPTI)"
        chain_token = "ETH"
        pool = opti_pool[:4]
        chain_url = url.opti_address
        pool_dollar = float(pool) * float(api.get_native_price("eth")) / 1 ** 18
        im2 = Image.open(media.opti_logo)
    if chain == "polygon" or chain == "poly":
        chain_name = "(POLYGON)"
        chain_token = "MATIC"
        pool = poly_pool[:6]
        chain_url = url.poly_address
        pool_dollar = float(pool) * float(api.get_native_price("matic")) / 1 ** 18
        im2 = Image.open(media.poly_logo)
    im1 = Image.open((random.choice(media.blackhole)))
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 28)
    i1.text((28, 36),
            f'X7 Finance Lending Pool Info {chain_name}\n\n'
            f'{pool} {chain_token} (${"{:0,.0f}".format(pool_dollar)})\n\n\n\n\n\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await update.message.reply_photo(
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'*X7 Finance Lending Pool Info {chain_name}*\nUse `/pool [chain-name]` for other chains\n\n'
                f'{pool} {chain_token} (${"{:0,.0f}".format(pool_dollar)})\n\n'
                f'{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Lending Pool Reserve Contract', url=f'{chain_url}{ca.lpool_reserve}')],
             [InlineKeyboardButton(text='X7 Deposit Contract', url=f'{chain_url}{ca.x7d}#code')], ]))

async def proposal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption='*Listing proposal:*\n'
                'X7 Finance does not prioritize paid listings. Instead, for CEXs to acquire the desired supply '
                'amount needed to list X7 on their exchange, they will need to purchase it from existing markets.\n\n'
                '*Marketing proposal:*\n'
                'X7 Finance does not incur expenses for requested marketing activities. Instead, our team leverages '
                'its extensive network and connections in the market to independently select and collaborate with '
                'relevant parties.\n\n'
                'If, despite this information, you still find it necessary to get in touch, you can always send a '
                'DM to our Twitter account. Please be aware that responses to such DMs are not guaranteed.\n\n'
                f'{api.get_quote()}', parse_mode="Markdown")

async def potw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption='*Pioneer Of The Week*\n\n'
                'The following Pioneers have shown exemplary contributions towards X7 Finance\n\n'
                'Week 15 - @Ahmed812007\n'
                'Week 17 - @X7Nobody\n\n'
                f'{api.get_quote()}', parse_mode="Markdown")

async def question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Thanks {update.effective_message.from_user.username}, '
                                    f'your question has been received')
    message = str(update.effective_message.text[9:])
    await context.bot.send_message(
        keys.ama_id,
        f'{message}\n\n'
        f' - `{update.effective_message.from_user.name}`', parse_mode='Markdown')

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'{api.get_quote()}',
        parse_mode="Markdown")

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
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
    ws1 = draw_progress_bar(im1, 80, 80, 200, 25, text.ws1)
    ws2 = draw_progress_bar(im1, 80, 180, 200, 25, text.ws2)
    ws3 = draw_progress_bar(im1, 80, 280, 200, 25, text.ws3)
    ws4 = draw_progress_bar(im1, 80, 380, 200, 25, text.ws4)
    ws5 = draw_progress_bar(im1, 80, 480, 200, 25, text.ws5)
    ws6 = draw_progress_bar(im1, 480, 80, 200, 25, text.ws6)
    ws7 = draw_progress_bar(im1, 480, 180, 200, 25, text.ws7)
    ws8 = draw_progress_bar(im1, 480, 280, 200, 25, text.ws8)
    ws9 = draw_progress_bar(im1, 480, 380, 200, 25, text.ws9)
    im1.text((80, 36),
             f'WS 1 - {text.ws1 * 100}% \n\n\n'
             f'WS 2 - {text.ws2 * 100}% \n\n\n'
             f'WS 3 - {text.ws3 * 100}% \n\n\n'
             f'WS 4 - {text.ws4 * 100}% \n\n\n'
             f'WS 5 - {text.ws5 * 100}% \n\n\n',
             font=myfont, fill=(255, 255, 255))
    im1.text((480, 36),
             f'WS 6 - {text.ws6 * 100}%\n\n\n'
             f'WS 7 - {text.ws7 * 100}%\n\n\n'
             f'WS 8 - {text.ws8 * 100}%\n\n\n'
             f'WS 9 - {text.ws9 * 100}%\n\n\n',
             font=myfont, fill=(255, 255, 255))
    out.save(r"media\blackhole.png")
    await update.message.reply_photo(
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'*X7 Finance Work Stream Status*\n\n'
                f'WS1: Omni routing (multi dex routing "library" code) - {text.ws1*100}% \n\n'
                f'WS2: Omni routing (UI) - {text.ws2*100}% \n\n'
                f'WS3: Borrowing UI - {text.ws3*100}% \n\n'
                f'WS4: Lending and Liquidation UI - {text.ws4*100}% \n\n'
                f'WS5: DAO smart contracts - {text.ws5*100}% \n\n'
                f'WS6: X7 DAO UI - {text.ws6*100}%\n\n'
                f'WS7: Marketing "Pitch Deck" - {text.ws7*100}%\n\n'
                f'WS8: Decentralization in hosting - {text.ws8*100}%\n\n'
                f'WS9: Developer Tools and Example Smart Contracts - {text.ws9*100}%\n\n{api.get_quote()}',
        parse_mode='Markdown')

async def say(update: Update, context: ContextTypes.DEFAULT_TYPE):
    engine = pyttsx3.init()
    engine.save_to_file(" ".join(context.args), 'media/voicenote.mp3')
    engine.runAndWait()
    await update.message.reply_audio(audio=open('media/voicenote.mp3', 'rb'))

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    dev_address = '\n\n'.join(map(str, dev_list))
    com_list = com_response["owners"]
    com_address = '\n\n'.join(map(str, com_list))
    await update.message.reply_photo(
        photo=open(random.choice(media.logos), 'rb'),
        caption=f'*X7 Finance Multi-Sig Signers {chain_name}*\n'
                f'Use `/signers [chain-name]` or other chains\n\n'
                f'*Developer Signers*\n`{dev_address}`\n\n*Community Signers*\n`{com_address}`\n\n'
                f'{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                text='X7 Developer Multi-Sig', url=f'{chain_url}{ca.dev_multi_eth}')],
            [InlineKeyboardButton(
                text='X7 Community Multi-Sig', url=f'{chain_url}{ca.com_multi_eth}')], ]))

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
        "opti": ("(OP)", url.opti_address)
    }
    if chain in chain_mappings:
        chain_name, chain_url = chain_mappings[chain]
    else:
        chain_name, chain_url = chain_mappings["eth"]
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Smart Contracts {chain_name}*\nUse `/smart [chain-name]` or other chains\n\n'
                f'{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Contracts Directory - by MikeMurpher', url=f'{url.ca_directory}')],
            [InlineKeyboardButton(text='X7100 Liquidity Hub', url=f'{chain_url}{ca.x7100_liq_hub}')],
            [InlineKeyboardButton(text='X7R Liquidity Hub', url=f'{chain_url}{ca.x7r_liq_hub}')],
            [InlineKeyboardButton(text='X7DAO Liquidity Hub', url=f'{chain_url}{ca.x7dao_liq_hub}')],
            [InlineKeyboardButton(text='X7 Token Burner', url=f'{chain_url}{ca.burner}')],
            [InlineKeyboardButton(text='X7100 Discount Authority', url=f'{chain_url}{ca.x7100_discount}')],
            [InlineKeyboardButton(text='X7R Discount Authority', url=f'{chain_url}{ca.x7r_discount}')],
            [InlineKeyboardButton(text='X7DAO Discount Authority', url=f'{chain_url}{ca.x7dao_discount}')],
            [InlineKeyboardButton(text='X7 Token Time Lock', url=f'{chain_url}{ca.time_lock}')],
            [InlineKeyboardButton(text='X7 Ecosystem Splitter', url=f'{chain_url}{ca.eco_splitter}')],
            [InlineKeyboardButton(text='X7 Treasury Splitter', url=f'{chain_url}{ca.treasury_splitter}')],
            [InlineKeyboardButton(text='X7 Lending Pool Reserve', url=f'{chain_url}{ca.lpool_reserve}')],
            [InlineKeyboardButton(text='X7 Xchange Discount Authority', url=f'{chain_url}{ca.xchange_discount}')],
            [InlineKeyboardButton(text='X7 Lending Discount Authority', url=f'{chain_url}{ca.lending_discount}')],
            [InlineKeyboardButton(text='X7 Xchange Router', url=f'{chain_url}{ca.router}')],
            [InlineKeyboardButton(text='X7 Xchange Router with Discounts', url=f'{chain_url}{ca.discount_router}')],
            [InlineKeyboardButton(text='X7 Lending Pool Contract', url=f'{chain_url}{ca.lpool}')],
            [InlineKeyboardButton(text='X7 Xchange Factory', url=f'{chain_url}{ca.factory}')], ]))

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    snapshot = api.get_snapshot()
    end = datetime.utcfromtimestamp(snapshot["data"]["proposals"][0]["end"]).strftime('%Y-%m-%d %H:%M:%S')
    start = datetime.utcfromtimestamp(snapshot["data"]["proposals"][0]["start"]).strftime('%Y-%m-%d %H:%M:%S')
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
        countdown = f'Vote Closing in: {int(days[0])} days, {int(hours[0])} hours and {int(minutes[0])} minutes'
        caption = "Vote"
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Community Snapshot*\n\n'
                f'Latest Proposal:\n\n'
                f'{snapshot["data"]["proposals"][0]["title"]} by - '
                f'{snapshot["data"]["proposals"][0]["author"][-5:]}\n\n'
                f'Voting Start: {start} UTC\n'
                f'Voting End:   {end} UTC\n\n'
                f'{snapshot["data"]["proposals"][0]["choices"][0]} - '
                f'{"{:0,.0f}".format(snapshot["data"]["proposals"][0]["scores"][0])} DAO Votes\n'
                f'{snapshot["data"]["proposals"][0]["choices"][1]} - '
                f'{"{:0,.0f}".format(snapshot["data"]["proposals"][0]["scores"][1])} DAO Votes\n\n'
                f'{"{:0,.0f}".format(snapshot["data"]["proposals"][0]["scores_total"])} Total DAO Votes\n\n'
                f'{countdown}\n\n{api.get_quote()}', parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text=f'{caption} Here', url=f'{url.snapshot}/proposal/'
                                                              f'{snapshot["data"]["proposals"][0]["id"]}')], ]))

async def supply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token_pairs = {
        "x7r": (ca.x7r_pair_eth, ca.x7r),
        "x7dao": (ca.x7dao_pair_eth, ca.x7dao),
        "x7101": (ca.x7101_pair_eth, ca.x7101),
        "x7102": (ca.x7102_pair_eth, ca.x7102),
        "x7103": (ca.x7103_pair_eth, ca.x7103),
        "x7104": (ca.x7104_pair_eth, ca.x7104),
        "x7105": (ca.x7105_pair_eth, ca.x7105)
    }
    prices = api.get_cg_price("x7r, x7dao, x7101, x7102, x7103, x7104, x7105")
    supply_info = {}
    for token, (pair, contract) in token_pairs.items():
        balance = api.get_token_balance(pair, contract, "eth")
        dollar_value = balance * prices[token]["usd"]
        percent = round(balance / ca.supply * 100, 2)
        supply_info[token] = {"balance": balance, "dollar_value": dollar_value, "percent": percent}
    img = Image.open((random.choice(media.blackhole)))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("media/FreeMonoBold.ttf", 22)
    caption_lines = []
    for token, info in supply_info.items():
        balance_str = "{:0,.0f}".format(info["balance"])
        dollar_value_str = "${:0,.0f}".format(info["dollar_value"])
        percent_str = f"{info['percent']}%"
        line = f"*{token.upper()}*\n{balance_str} {token.upper()} ({dollar_value_str}) {percent_str}"
        caption_lines.append(line)
    utc_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    caption = (
        f"*X7 Finance Uniswap Supply*\n\n" + "\n\n".join(caption_lines) + f"\n\nUTC: {utc_time}\n{api.get_quote()}")
    for i, line in enumerate(caption_lines):
        y_offset = 36 + i * 72
        draw.text((28, y_offset), line, font=font, fill=(255, 255, 255))
    img.save("media/blackhole.png")
    await update.message.reply_photo(
        photo=open("media/blackhole.png", "rb"),
        caption=caption,
        parse_mode="Markdown")

async def swap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_sticker(
        sticker=media.swap,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Xchange', url='https://app.x7.finance/#/swap')],
             [InlineKeyboardButton(text='Feedback', url='https://discord.com/channels/101665704'
                                                        '4553617428/1053206402065256498')], ]))

async def tax_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_tax = ""
    chain_name = ""
    if chain == "eth" or chain == "":
        chain_name = "(ETH)"
        chain_tax = tax.eth
    if chain == "bsc" or chain == "bnb":
        chain_name = "(BSC)"
        chain_tax = tax.bsc
    if chain == "polygon" or chain == "poly":
        chain_name = "(POLYGON)"
        chain_tax = tax.poly
    if chain == "optimism" or chain == "opti":
        chain_name = "(OPTIMISM)"
        chain_tax = tax.opti
    if chain == "arbitrum" or chain == "arb":
        chain_name = "(ARB)"
        chain_tax = tax.arb
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Tax Info {chain_name}*\nUse `/tax [chain-name]` for other chains\n\n'
                f'{chain_tax}\n\n{api.get_quote()}',
        parse_mode='Markdown')

async def time(update: Update, context: CallbackContext):
    message = update.message.text.split(' ')
    timezones = [
        ("America/Los_Angeles", "PST"),
        ("America/New_York", "EST"),
        ("UTC", "UTC"),
        ("Europe/London", "GMT"),
        ("Europe/Berlin", "CET"),
        ("Asia/Dubai", "GST"),
        ("Asia/Tokyo", "JST")]

    current_time = datetime.now(pytz.timezone("UTC"))
    local_time = current_time.astimezone(pytz.timezone("GMT"))

    if len(message) > 1:
        time_variable = message[1]
        time_format = "%I%p"
        if re.match(r"\d{1,2}:\d{2}([ap]m)?", time_variable):
            time_format = "%I:%M%p" if re.match(r"\d{1,2}:\d{2}am", time_variable, re.IGNORECASE) else "%I:%M%p"
        input_time = datetime.strptime(time_variable, time_format).replace(
            year=local_time.year, month=local_time.month, day=local_time.day)

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
                    await update.message.reply_text(time_info, parse_mode="Markdown")
                    return

        time_info = f"{input_time.strftime('%A %B %d %Y')}\n"
        time_info += f"{input_time.strftime('%I:%M %p')} - {time_variable.upper()}\n\n"
        for tz, tz_name in timezones:
            tz_time = input_time.astimezone(pytz.timezone(tz))
            time_info += f"{tz_time.strftime('%I:%M %p')} - {tz_name}\n"
        await update.message.reply_text(time_info, parse_mode="Markdown")
        return

    time_info = f"{local_time.strftime('%A %B %d %Y')}\n"
    time_info += f"{local_time.strftime('%I:%M %p')} - {local_time.strftime('%Z')}\n\n"
    for tz, tz_name in timezones:
        tz_time = local_time.astimezone(pytz.timezone(tz))
        time_info += f"{tz_time.strftime('%I:%M %p')} - {tz_name}\n"
    await update.message.reply_text(time_info, parse_mode="Markdown")


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = api.get_today()
    today = (random.choice(data["data"]["Events"]))
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'`On this day in {today["year"]}:\n\n{today["text"]}`',
        parse_mode="Markdown")

async def token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = " ".join(context.args)
    info_eth = api.get_token_data(token, "eth")
    info_bsc = api.get_token_data(token, "bsc")
    await update.message.reply_text(f'ETH\n\n'
                                    f'Name: {info_eth[0]["name"]}\n'
                                    f'Decimals: {info_eth[0]["decimals"]}\n'
                                    f'Logo: {info_eth[0]["logo"]}\n'
                                    f'Created: {info_eth[0]["created_at"]}\n'
                                    f'Possible Spam?: {info_eth[0]["possible_spam"]}\n\n'
                                    f'BSC\n\n'
                                    f'Name: {info_bsc[0]["name"]}\n'
                                    f'Decimals: {info_bsc[0]["decimals"]}\n'
                                    f'Logo: {info_bsc[0]["logo"]}\n'
                                    f'Created: {info_bsc[0]["created_at"]}\n'
                                    f'Possible Spam?: {info_bsc[0]["possible_spam"]}')

async def voting(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def website(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance Website Links*\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url=f'{url.website}')],
            [InlineKeyboardButton(text='Community Dashboard', url=f'{url.dashboard}')], ]))

async def wei(update: Update, context: ContextTypes.DEFAULT_TYPE):
    eth = " ".join(context.args)
    wei_raw = float(eth)
    wei = wei_raw * 10 ** 18
    await update.message.reply_text(
        f'{eth} ETH is equal to \n\n'
        f'`{wei:.0f}` wei',
        parse_mode="Markdown")

async def wp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=f'*X7 Finance Whitepaper Quote*\n\n{random.choice(text.quotes)}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url=f'{url.website}')],
            [InlineKeyboardButton(text='Full WP', url=f'{url.wp_link}')],
            [InlineKeyboardButton(text='Short WP', url=f'{url.short_wp_link}')], ]))

async def x7d(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 28)
    i1.text((28, 36),
            f'X7D {chain_name} Info\n\n'
            f'Supply: {supply[:5]} X7D (${"{:0,.0f}".format(x7d_dollar)})\n'
            f'Holders: {holders}\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await update.message.reply_photo(
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'*X7D {chain_name} Info*\n'
                f'For other chains use `/x7d [chain-name]`\n\n'
                f'Supply: {supply[:5]} X7D (${"{:0,.0f}".format(x7d_dollar)})\n'
                f'Holders: {holders}\n\n'
                f'{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='X7D Funding Dashboard', url='https://beta.x7.finance/#/fund')],
             [InlineKeyboardButton(text='X7 Lending Pool Reserve Contract', url=f'{chain_url}{ca.lpool_reserve}#code')],
             [InlineKeyboardButton(text='X7 Deposit Contract', url=f'{chain_url}{ca.x7d}#code')], ]))


# CG COMMANDS
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
        x7r_weth = float(x7r["reserve1"]) / 10 ** 18
        x7r_weth_dollar = float(x7r_weth) * float(api.get_native_price("eth"))
        x7r_token_dollar = float(price["x7r"]["usd"]) * float(x7r_token) / 10 ** 18
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7r_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(R'media\FreeMonoBold.ttf', 25)
        im1.save(r"media\blackhole.png", quality=95)
        i1 = ImageDraw.Draw(im1)
        i1.text((26, 30),
                f'X7R Info (ETH)\n\n'
                f'X7R Price: ${price["x7r"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7r"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(price["x7r"]["usd"] * ca.supply)}\n'
                f'24 Hour Volume: ${"{:0,.0f}".format(price["x7r"]["usd_24h_vol"])}\n'
                f'ATH: ${x7r_ath} (${"{:0,.0f}".format(x7r_ath * ca.supply)}) {x7r_ath_change[:3]}%\n'
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
                    f'ATH: ${x7r_ath} (${"{:0,.0f}".format(x7r_ath * ca.supply)}) {x7r_ath_change[:3]}%\n'
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
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy_eth}{ca.x7r}')], ]))
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
            photo=open(media.x7r_logo, 'rb'),
            caption=f'*X7R Info {chain_name}*\nUse `/x7r [chain-name]` for other chains\n\n'
                    f'Contract Address:\n`{ca.x7r}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text=f'{scan_name}', url=f'{chart_url}')],
                 [InlineKeyboardButton(text='Chart', url=f'{chart_url}')],
                 [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy_eth}{ca.x7r}')], ]))

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
        x7dao_ath_change = str(api.get_ath("x7dao")[1])
        x7dao_ath = api.get_ath("x7dao")[0]
        holders = api.get_holders(ca.x7dao)
        x7dao = api.get_liquidity(ca.x7dao_pair_eth, "eth")
        x7dao_token = float(x7dao["reserve0"])
        x7dao_weth = float(x7dao["reserve1"]) / 10 ** 18
        x7dao_weth_dollar = float(x7dao_weth) * float(api.get_native_price("eth"))
        x7dao_token_dollar = float(price["x7dao"]["usd"]) * float(x7dao_token) / 10 ** 18
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7dao_logo)
        im1.paste(im2, (720, 20), im2)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 25)
        i1 = ImageDraw.Draw(im1)
        i1.text((28, 36),
                f'X7DAO Info (ETH)\n\n'
                f'X7DAO Price: ${price["x7dao"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7dao"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(price["x7dao"]["usd"] * ca.supply)}\n'
                f'24 Hour Volume: ${"{:0,.0f}".format(price["x7dao"]["usd_24h_vol"])}\n'
                f'ATH: ${x7dao_ath} (${"{:0,.0f}".format(x7dao_ath * ca.supply)}) {x7dao_ath_change[:3]}%\n'
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
            f'ATH: ${x7dao_ath} (${"{:0,.0f}".format(x7dao_ath * ca.supply)}) {x7dao_ath_change[:3]}%\n'
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
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy_eth}{ca.x7dao}')], ]))
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
        photo=open(media.x7dao_logo, 'rb'),
        caption=f'*X7DAO {chain_name} Info*\nUse `/x7dao [chain-name]` for other chains\n\n'
                f'Contract Address:\n`{ca.x7dao}`\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=f'{scan_name}', url=f'{chart_url}')],
             [InlineKeyboardButton(text='Chart', url=f'{chart_url}')],
             [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy_eth}{ca.x7dao}')], ]))

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
        x7101_ath_change = str(api.get_ath("x7101")[1])
        x7101_ath = api.get_ath("x7101")[0]
        holders = api.get_holders(ca.x7101)
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7101_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1.text((28, 36),
                f'X7101 Info (ETH)\n\n'
                f'X7101 Price: ${price["x7101"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7101"]["usd_24h_change"]),1}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(price["x7101"]["usd"] * ca.supply)}\n'
                f'24 Hour Volume: ${"{:0,.0f}".format(price["x7101"]["usd_24h_vol"])}\n'
                f'ATH: ${x7101_ath} (${"{:0,.0f}".format(x7101_ath * ca.supply)}) {x7101_ath_change[:3]}%\n'
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
            f'ATH: ${x7101_ath} (${"{:0,.0f}".format(x7101_ath * ca.supply)}) {x7101_ath_change[:3]}%\n'
            f'Holders: {holders}\n\n'
            f'*X7101 Contract*\n`{ca.x7101}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{url.ether_token}{ca.x7101}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_eth}{ca.x7101_pair_eth}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy_eth}{ca.x7101}')], ]))
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
        photo=open(media.x7dao_logo, 'rb'),
        caption=f'*X7DAO {chain_name} Info*\nUse `/x7101 [chain-name]` for other chains\n\n'
                f'Contract Address:\n`{ca.x7101}`\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=f'{scan_name}', url=f'{chart_url}')],
             [InlineKeyboardButton(text='Chart', url=f'{chart_url}')],
             [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy_eth}{ca.x7101}')], ]))

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
        x7102_ath_change = str(api.get_ath("x7102")[1])
        x7102_ath = api.get_ath("x7102")[0]
        holders = api.get_holders(ca.x7102)
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7102_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
        i1.text((28, 36),
                f'X7102 Info (ETH)\n\n'
                f'X7102 Price: ${price["x7102"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7102"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(price["x7102"]["usd"] * ca.supply)}\n'
                f'24 Hour Volume: ${"{:0,.0f}".format(price["x7102"]["usd_24h_vol"])}\n'
                f'ATH: ${x7102_ath} (${"{:0,.0f}".format(x7102_ath * ca.supply)}) {x7102_ath_change[:3]}%\n'
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
                    f'ATH: ${x7102_ath} (${"{:0,.0f}".format(x7102_ath * ca.supply)}) {x7102_ath_change[:3]}%\n'
                    f'Holders: {holders}\n\n'
                    f'*X7102 Contract*\n`{ca.x7102}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{url.ether_token}{ca.x7102}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_eth}{ca.x7102_pair_eth}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy_eth}{ca.x7102}')], ]))
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
        photo=open(media.x7dao_logo, 'rb'),
        caption=f'*X7DAO {chain_name} Info*\nUse `/x7102 [chain-name]` for other chains\n\n'
                f'Contract Address:\n`{ca.x7102}`\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=f'{scan_name}', url=f'{chart_url}')],
             [InlineKeyboardButton(text='Chart', url=f'{chart_url}')],
             [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy_eth}{ca.x7102}')], ]))

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
        x7103_ath_change = str(api.get_ath("x7103")[1])
        x7103_ath = api.get_ath("x7103")[0]
        holders = api.get_holders(ca.x7103)
        im1 = Image.open((random.choice(media.blackhole)))
        im2 = Image.open(media.x7103_logo)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 25)
        i1.text((28, 36),
                f'X7103 Info (ETH)\n\n'
                f'X7103 Price: ${price["x7103"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7103"]["usd_24h_change"],1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(price["x7103"]["usd"] * ca.supply)}\n'
                f'24 Hour Volume: ${"{:0,.0f}".format(price["x7103"]["usd_24h_vol"])}\n'
                f'ATH: ${x7103_ath} (${"{:0,.0f}".format(x7103_ath * ca.supply)}) {x7103_ath_change[:3]}%\n'
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
                    f'ATH: ${x7103_ath} (${"{:0,.0f}".format(x7103_ath * ca.supply)}) {x7103_ath_change[:3]}%\n'
                    f'Holders: {holders}\n\n'
                    f'*X7103 Contract*\n`{ca.x7103}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{url.ether_token}{ca.x7103}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_eth}{ca.x7103_pair_eth}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy_eth}{ca.x7103}')], ]))
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
        photo=open(media.x7dao_logo, 'rb'),
        caption=f'*X7DAO {chain_name} Info*\nUse `/x7103 [chain-name]` for other chains\n\n'
                f'Contract Address:\n`{ca.x7103}`\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=f'{scan_name}', url=f'{chart_url}')],
             [InlineKeyboardButton(text='Chart', url=f'{chart_url}')],
             [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy_eth}{ca.x7103}')], ]))

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
        myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 25)
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
        x7104_ath_change = str(api.get_ath("x7104")[1])
        x7104_ath = api.get_ath("x7104")[0]
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
                f'ATH: ${x7104_ath} (${"{:0,.0f}".format(x7104_ath * ca.supply)}) {x7104_ath_change[:3]}%\n'
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
                    f'ATH: ${x7104_ath} (${"{:0,.0f}".format(x7104_ath * ca.supply)}) {x7104_ath_change[:3]}%\n'
                    f'Holders: {holders}\n\n'
                    f'*X7104 Contract*\n`{ca.x7104}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{url.ether_token}{ca.x7104}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_eth}{ca.x7104_pair_eth}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy_eth}{ca.x7104}')], ]))
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
        photo=open(media.x7dao_logo, 'rb'),
        caption=f'*X7DAO {chain_name} Info*\nUse `/x7104 [chain-name]` for other chains\n\n'
                f'Contract Address:\n`{ca.x7104}`\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=f'{scan_name}', url=f'{chart_url}')],
             [InlineKeyboardButton(text='Chart', url=f'{chart_url}')],
             [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy_eth}{ca.x7104}')], ]))

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
        x7105_ath_change = str(api.get_ath("x7105")[1])
        x7105_ath = api.get_ath("x7105")[0]
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
                f'ATH: ${x7105_ath} (${"{:0,.0f}".format(x7105_ath * ca.supply)}) {x7105_ath_change[:3]}%\n'
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
                    f'ATH: ${x7105_ath} (${"{:0,.0f}".format(x7105_ath * ca.supply)}) {x7105_ath_change[:3]}%\n'
                    f'Holders: {holders}\n\n'
                    f'*X7105 Contract*\n`{ca.x7105}`\n\n{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{url.ether_token}{ca.x7105}')],
                [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_eth}{ca.x7105_pair_eth}')],
                [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy_eth}{ca.x7105}')], ]))
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
        photo=open(media.x7dao_logo, 'rb'),
        caption=f'*X7DAO {chain_name} Info*\nUse `/x7105 [chain-name]` for other chains\n\n'
                f'Contract Address:\n`{ca.x7105}`\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=f'{scan_name}', url=f'{chart_url}')],
             [InlineKeyboardButton(text='Chart', url=f'{chart_url}')],
             [InlineKeyboardButton(text='Buy', url=f'{url.xchange_buy_eth}{ca.x7105}')], ]))

async def ath(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coins = ["x7r", "x7dao"]

    def get_ath_info(coin):
        ath, ath_change, date = api.get_ath(coin)
        ath_change_str = str(ath_change)
        return ath, ath_change_str[:3], date
    x7r_ath, x7r_ath_change, x7r_date = get_ath_info("x7r")
    x7dao_ath, x7dao_ath_change, x7dao_date = get_ath_info("x7dao")
    img = Image.open((random.choice(media.blackhole)))
    i1 = ImageDraw.Draw(img)
    myfont = ImageFont.truetype(R'media\FreeMonoBold.ttf', 26)
    i1.text((28, 36),
            f'X7 Finance ATH Info\n\n'
            f'X7R   - ${x7r_ath} (${"{:0,.0f}".format(x7r_ath * ca.supply)}) {x7r_ath_change}%\n'
            f'{x7r_date}\n\n'
            f'X7DAO - ${x7dao_ath} (${"{:0,.0f}".format(x7dao_ath * ca.supply)}) {x7dao_ath_change}%\n'
            f'{x7dao_date}'
            f'\n\n\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont, fill=(255, 255, 255))
    img.save(r"media\blackhole.png")
    caption = (
        f'*X7 Finance ATH Info*\n\n'
        f'X7R - ${x7r_ath} (${"{:0,.0f}".format(x7r_ath * ca.supply)}) {x7r_ath_change}%\n'
        f'{x7r_date}\n\n'
        f'X7DAO - ${x7dao_ath} (${"{:0,.0f}".format(x7dao_ath * ca.supply)}) {x7dao_ath_change}%\n'
        f'{x7dao_date}\n\n'
        f'{api.get_quote()}')
    await update.message.reply_photo(
        photo=open(r'media\blackhole.png', 'rb'),
        caption=caption,
        parse_mode="Markdown")

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
        burn_dollar = api.get_cg_price("x7r")["x7r"]["usd"] * float(burn)
        im2 = Image.open(media.eth_logo)
        native = f'{str(burn_dollar / api.get_native_price("eth"))[:5]} ETH'
    if chain == "bsc" or chain == "bnb":
        chain_name = "(BSC)"
        chain_url = url.bsc_token
        burn = api.get_token_balance(ca.dead, ca.x7r, "bsc")
        percent = round(burn / ca.supply * 100, 2)
        im2 = Image.open(media.bsc_logo)
        native = f'{str(burn_dollar / api.get_native_price("bnb"))[:7]} BNB'
    if chain == "polygon" or chain == "poly":
        chain_name = "(POLYGON)"
        chain_url = url.poly_token
        burn = api.get_token_balance(ca.dead, ca.x7r, "poly")
        percent = round(burn / ca.supply * 100, 2)
        im2 = Image.open(media.poly_logo)
        native = f'{str(burn_dollar / api.get_native_price("matic"))[:7]} MATIC'
    if chain == "arbitrum" or chain == "arb":
        chain_name = "(ARB)"
        chain_url = url.arb_token
        burn = api.get_token_balance(ca.dead, ca.x7r, "arb")
        percent = round(burn / ca.supply * 100, 2)
        im2 = Image.open(media.arb_logo)
        native = f'{str(burn_dollar / api.get_native_price("eth"))[:5]} ETH'
    if chain == "optimism" or chain == "arb":
        chain_name = "(OPTIMISM)"
        chain_url = url.opti_token
        burn = api.get_token_balance(ca.dead, ca.x7r, "opti")
        percent = round(burn / ca.supply * 100, 2)
        im2 = Image.open(media.opti_logo)
        native = f'{str(burn_dollar / api.get_native_price("eth"))[:5]} ETH'
    im1 = Image.open((random.choice(media.blackhole)))
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 28)
    i1.text((28, 36),
            f'X7R {chain_name} Tokens Burned:\n\n'
            f'{"{:0,.0f}".format(float(burn))} / {native} (${"{:0,.0f}".format(float(burn_dollar))})\n'
            f'{percent}% of Supply\n\n\n\n\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await update.message.reply_photo(
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'\n\nX7R {chain_name} Tokens Burned:\nUse `/burn [chain-name]` for other chains\n\n'
                f'{"{:0,.0f}".format(float(burn))} / {native} (${"{:0,.0f}".format(float(burn_dollar))})\n'
                f'{percent}% of Supply\n\n{api.get_quote()}',
        parse_mode="markdown",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Etherscan Burn Wallet', url=f'{chain_url}{ca.x7r}?a={ca.dead}')], ]))

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
        price = api.get_cg_price("x7r, x7dao, x7101, x7102, x7103, x7104, x7105")
        x7r_price = (price["x7r"]["usd"])
        x7dao_price = (price["x7dao"]["usd"])
        x7101_price = (price["x7101"]["usd"])
        x7102_price = (price["x7102"]["usd"])
        x7103_price = (price["x7103"]["usd"])
        x7104_price = (price["x7104"]["usd"])
        x7105_price = (price["x7105"]["usd"])
        x7r = api.get_liquidity(ca.x7r_pair_eth, "eth")
        x7dao = api.get_liquidity(ca.x7dao_pair_eth, "eth")
        x7101 = api.get_liquidity(ca.x7101_pair_eth, "eth")
        x7102 = api.get_liquidity(ca.x7102_pair_eth, "eth")
        x7103 = api.get_liquidity(ca.x7103_pair_eth, "eth")
        x7104 = api.get_liquidity(ca.x7104_pair_eth, "eth")
        x7105 = api.get_liquidity(ca.x7105_pair_eth, "eth")
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
    x7dao_dollar = float(x7dao_amount) * float(api.get_native_price(chain_token_api)) / 1 ** 18
    x7r_dollar = float(x7r_amount) * float(api.get_native_price(chain_token_api)) / 1 ** 18
    cons_dollar = float(cons_amount) * float(api.get_native_price(chain_token_api)) / 1 ** 18
    im1 = Image.open((random.choice(media.blackhole)))
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
    i1.text((28, 36),
            f'X7 Finance Initial Liquidity {chain_title}\n\n'
            f'X7R:\n{x7r_amount} {chain_token_name} (${"{:0,.0f}".format(x7r_dollar)})\n\n'
            f'X7DAO:\n{x7dao_amount} {chain_token_name} (${"{:0,.0f}".format(x7dao_dollar)})\n\n'
            f'X7100:\n{cons_amount} BNB (${"{:0,.0f}".format(cons_dollar)})\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await update.message.reply_photo(
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'*X7 Finance Initial Liquidity {chain_title}*\nUse `/liquidity [chain-name]` for other chains\n\n'
                f'X7R:\n{x7r_amount} {chain_token_name} (${"{:0,.0f}".format(x7r_dollar)})\n\n'
                f'X7DAO:\n{x7dao_amount} {chain_token_name} (${"{:0,.0f}".format(x7dao_dollar)})\n\n'
                f'X7100:\n{cons_amount} {chain_token_name} (${"{:0,.0f}".format(cons_dollar)})\n\n{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='X7R Initial Liquidity',
                                  url=f'{chain_url}{ca.x7r_liq_lock}')],
            [InlineKeyboardButton(text='X7DAO Initial Liquidity',
                                  url=f'{chain_url}{ca.x7dao_liq_lock}')],
            [InlineKeyboardButton(text='X7100 Initial Liquidity',
                                  url=f'{chain_url}{ca.cons_liq_lock}')], ]))

async def mcap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    price = api.get_cg_price("x7r, x7dao, x7101, x7102, x7103, x7104, x7105")
    x7r_supply = ca.supply - api.get_token_balance(ca.dead, ca.x7r, "eth")
    tokens = ["x7r", "x7dao", "x7101", "x7102", "x7103", "x7104", "x7105"]
    caps = {}
    for token in tokens:
        caps[token] = price[token]["usd"] * ca.supply
    cons_cap = sum(caps.values()) - caps["x7r"] - caps["x7dao"]
    total_cap = sum(caps.values())
    im1 = Image.open(random.choice(media.blackhole))
    im2 = Image.open(media.eth_logo)
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 22)
    i1 = ImageDraw.Draw(im1)
    market_cap_info = f'X7 Finance Market Cap Info (ETH)\n\n'
    for token in tokens:
        market_cap_info += f'{token.upper()}:   ${"{:0,.0f}".format(caps[token])}\n'
    market_cap_info += f'\nConstellations Combined:\n${"{:0,.0f}".format(cons_cap)}\n\n'
    market_cap_info += f'Total Token Market Cap:\n${"{:0,.0f}".format(total_cap)}\n\n'
    market_cap_info += f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}'
    i1.text((28, 36), market_cap_info, font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await update.message.reply_photo(
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'*X7 Finance Market Cap Info (ETH)*\n\n'
                f'X7R:            ${"{:0,.0f}".format(caps["x7r"])}\n'
                f'X7DAO:        ${"{:0,.0f}".format(caps["x7dao"])}\n'
                f'X7101:         ${"{:0,.0f}".format(caps["x7101"])}\n'
                f'X7102:         ${"{:0,.0f}".format(caps["x7102"])}\n'
                f'X7103:         ${"{:0,.0f}".format(caps["x7103"])}\n'
                f'X7104:         ${"{:0,.0f}".format(caps["x7104"])}\n'
                f'X7105:         ${"{:0,.0f}".format(caps["x7105"])}\n\n'
                f'Constellations Combined:\n'
                f'${"{:0,.0f}".format(cons_cap)}\n\n'
                f'Total Token Market Cap:\n'
                f'${"{:0,.0f}".format(total_cap)}'
                f'\n\n{api.get_quote()}',
        parse_mode="Markdown")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    search = " ".join(context.args).lower()
    cg_name = ""
    price = ""
    gas_data = ""
    im2 = ""
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
                f'X7R:    ${price["x7r"]["usd"]}\n'
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
                    f'X7R:    ${price["x7r"]["usd"]}\n'
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
    if search == "eth" or search == "bnb" or search == "matic" or search == "poly" or search == "polygon":
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
        im1 = Image.open((random.choice(media.blackhole)))
        im1.paste(im2, (680, 20), im2)
        i1 = ImageDraw.Draw(im1)
        myfont = ImageFont.truetype(R'media\FreeMonoBold.ttf', 28)
        i1.text((28, 36),
                f'{symbol} price\n\n'
                f'Price: ${price[cg_name]["usd"]}\n'
                f'24 Hour Change: {round(price[cg_name]["usd_24h_change"], 1)}%\n\n'
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
                    f'Price: ${price[cg_name]["usd"]}\n'
                    f'24 Hour Change: {round(price[cg_name]["usd_24h_change"], 1)}%\n\n'
                    f'Gas Prices:\n'
                    f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n'
                    f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n'
                    f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n'
                    f'{api.get_quote()}', parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Chart', url=f'https://www.coingecko.com/en/coins/{cg_name}')], ]))
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
                f'24 Hour Change: {round(token_price[token_id]["usd_24h_change"], 1)}%\n'
                f'Market Cap: ${"{:0,.0f}".format(token_price[token_id]["usd_market_cap"])}\n\n\n\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font=myfont, fill=(255, 255, 255))
        im1.save(r"media\blackhole.png", quality=95)
        await update.message.reply_photo(
            photo=open(r"media\blackhole.png", 'rb'),
            caption=f'*{symbol} price*\n\n'
                    f'Price: ${float(token_price[token_id]["usd"])}\n'
                    f'24 Hour Change: {round(token_price[token_id]["usd_24h_change"], 1)}%\n'
                    f'Market Cap: ${"{:0,.0f}".format(token_price[token_id]["usd_market_cap"])}\n\n'
                    f'{api.get_quote()}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='Chart', url=f'https://www.coingecko.com/en/coins/{token_id}')], ]))

async def treasury(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    chain_name = ""
    chain_token_api = ""
    chain_token_name = ""
    chain_title = ""
    im2 = ""
    chain_url = ""
    dev_eth = ""
    com_eth = ""
    dev_dollar = ""
    com_dollar = ""
    if chain == "" or chain == "eth":
        dev_eth = api.get_native_balance(ca.dev_multi_eth, "eth")
        com_eth = api.get_native_balance(ca.com_multi_eth, "eth")
        pioneer_eth = api.get_native_balance(ca.pioneer, "eth")
        dev_dollar = float(dev_eth) * float(api.get_native_price("eth")) / 1 ** 18
        com_dollar = float(com_eth) * float(api.get_native_price("eth")) / 1 ** 18
        pioneer_dollar = float(pioneer_eth) * float(api.get_native_price("eth")) / 1 ** 18
        com_x7r = api.get_token_balance(ca.com_multi_eth, ca.x7r, "eth")
        com_x7dao = api.get_token_balance(ca.com_multi_eth, ca.x7dao, "eth")
        com_x7dao_price = com_x7dao * api.get_cg_price("x7dao")["x7dao"]["usd"]
        com_x7r_price = com_x7r * api.get_cg_price("x7r")["x7r"]["usd"]
        com_x7d = api.get_token_balance(ca.com_multi_eth, ca.x7d, "eth")
        com_x7d_price = com_x7d * api.get_native_price("eth")
        com_total = com_x7r_price + com_dollar + com_x7d_price + com_x7dao_price
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
                f'{"{:0,.0f}".format(com_x7dao)} X7DAO (${"{:0,.0f}".format(com_x7dao_price)})\n'
                f'Total: (${"{:0,.0f}".format(com_total)})\n\n\n\n'
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
                    f'{"{:0,.0f}".format(com_x7dao)} X7DAO (${"{:0,.0f}".format(com_x7dao_price)})\n'
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
        return
    if chain == "bsc" or chain == "bnb":
        chain_name = "bsc"
        chain_token_name = "BNB"
        chain_title = "(BSC)"
        im2 = Image.open(media.bsc_logo)
        chain_url = url.bsc_address
        dev_eth = api.get_native_balance(ca.dev_multi_bsc, "bsc")
        com_eth = api.get_native_balance(ca.com_multi_bsc, "bsc")
        dev_dollar = float(dev_eth) * float(api.get_native_price("bnb")) / 1 ** 18
        com_dollar = float(com_eth) * float(api.get_native_price("bnb")) / 1 ** 18
    if chain == "arbitrum" or chain == "arb":
        chain_name = "arb"
        chain_token_name = "ETH"
        chain_title = "(ARB)"
        im2 = Image.open(media.arb_logo)
        chain_url = url.bsc_address
        dev_amount = api.get_native_balance(ca.dev_multi_arb, "arb")
        com_amount = api.get_native_balance(ca.dev_multi_arb, "arb")
        dev_dollar = float(dev_amount) * float(api.get_native_price("eth")) / 1 ** 18
        com_dollar = float(com_amount) * float(api.get_native_price("eth")) / 1 ** 18
    if chain == "polygon" or chain == "poly":
        chain_name = "poly"
        chain_token_name = "MATIC"
        chain_title = "(POLYGON)"
        chain_url = url.poly_address
        dev_amount = api.get_native_balance(ca.dev_multi_poly, "poly")
        com_amount = api.get_native_balance(ca.com_multi_poly, "poly")
        dev_dollar = float(dev_amount) * float(api.get_native_price("matic")) / 1 ** 18
        com_dollar = float(com_amount) * float(api.get_native_price("matic")) / 1 ** 18
        im2 = Image.open(media.poly_logo)
    if chain == "optimism" or chain == "opti":
        chain_name = "opti"
        chain_token_name = "ETH"
        chain_title = "(OPTI)"
        chain_url = url.opti_address
        dev_amount = api.get_native_balance(ca.dev_multi_opti, "opti")
        com_amount = api.get_native_balance(ca.com_multi_opti, "opti")
        dev_dollar = float(dev_amount) * float(api.get_native_price("eth")) / 1 ** 18
        com_dollar = float(com_amount) * float(api.get_native_price("eth")) / 1 ** 18
        im2 = Image.open(media.opti_logo)
    im1 = Image.open((random.choice(media.blackhole)))
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 20)
    i1 = ImageDraw.Draw(im1)
    i1.text((28, 36),
            f'X7 Finance Treasury {chain_title}\n\n'
            f'Developer Wallet:\n{dev_eth[:6]} {chain_token_name} (${"{:0,.0f}".format(dev_dollar)})\n\n'
            f'Community Wallet:\n{com_eth[:6]} {chain_token_name} (${"{:0,.0f}".format(com_dollar)})\n\n\n\n\n\n\n\n'
            f'\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await update.message.reply_photo(
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'*X7 Finance Treasury {chain_title}*\nUse `/treasury [chain-name]` for other chains\n\n'
                f'Developer Wallet:\n{dev_eth[:6]} {chain_token_name} (${"{:0,.0f}".format(dev_dollar)})\n\n'
                f'Community Wallet:\n{com_eth[:6]} {chain_token_name} (${"{:0,.0f}".format(com_dollar)})\n\n'
                f'{api.get_quote()}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Treasury Splitter Contract',
                                  url=f'{chain_url}{ca.treasury_splitter}')],
            [InlineKeyboardButton(text='Developer Multi-sig Wallet',
                                  url=f'{chain_url}{ca.dev_multi_bsc}')],
            [InlineKeyboardButton(text='Community Multi-sig Wallet',
                                  url=f'{chain_url}{ca.com_multi_bsc}')], ]))
    return


# TWITTER COMMANDS
async def count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tweet = context.args[0]
    start = tweet.index('status/')
    end = tweet.index('?', start + 1)
    tweet_id = tweet[start + 7:end]
    rt_response = api.twitter_bearer.get_retweeters(tweet_id)
    status = api.twitter.get_status(tweet_id)
    retweet_count = status.retweet_count
    rt_names = '\n'.join(str(p) for p in rt_response.data)
    await update.message.reply_sticker(sticker=media.twitter_sticker)
    await update.message.reply_text(
        f'Retweeted {retweet_count} times, by the following members:\n\n{rt_names}')

async def raid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        username = random.choice(text.usernamelist)
        tweet = api.twitter.user_timeline(screen_name=username, count=1, include_rts="false", exclude_replies="true")
        await update.message.reply_sticker(sticker=media.twitter_sticker)
        await update.message.reply_text(
            f'🚨🚨 Raid {username} 🚨🚨\n\n'
            f'{tweet[0].text}\n\n'
            f'https://twitter.com/intent/tweet?text=@X7_Finance&hashtags=LongLiveDefi&in_reply_to={tweet[0].id}\n\n'
            f'{random.choice(text.twitter_replies)}', disable_web_page_preview=True)
    else:
        await update.message.reply_text(f'{text.mods_only}')

async def spaces(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = api.twitter_bearer.get_spaces(user_ids=1561721566689386496)
    data = str(response[0])
    start = data.index('=')
    end = data.index(' ', start)
    space_id = data[start + 1:end]
    space = api.get_space(space_id)
    then = parser.parse(space["scheduled_start"]).astimezone(pytz.utc)
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
            text=f'Next X7 Finance Twitter space:\n\n'
                 f'{space["title"]}\n\n'
                 f'{then.strftime("%A %B %d %Y %I:%M %p")} (UTC)\n\n'
                 f'{int(days[0])} days, {int(hours[0])} hours and {int(minutes[0])} minutes\n\n'
                 f'[Click here](https://twitter.com/i/spaces/{space_id}) to set a reminder!'
                 f'\n\n{api.get_quote()}', parse_mode="Markdown")

async def twitter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ext = " ".join(context.args)
    username = '@x7_finance'
    tweet = api.twitter.user_timeline(screen_name=username, count=1)
    if ext == "":
        await update.message.reply_sticker(sticker=media.twitter_sticker)
        await update.message.reply_text(
            f'Latest X7 Finance Tweet\n\n{tweet[0].text}\n\n'
            f'https://twitter.com/X7_Finance/status/{tweet[0].id}\n\n'
            f'{random.choice(text.twitter_replies)}')
    if ext == "count":
        chat_admins = await update.effective_chat.get_administrators()
        if update.effective_user in (admin.user for admin in chat_admins):
            response = api.twitter_bearer.get_retweeters(tweet[0].id)
            print(response)
            status = api.twitter.get_status(tweet[0].id)
            retweet_count = status.retweet_count
            count = '\n'.join(str(p) for p in response.data)
            await update.message.reply_sticker(sticker=media.twitter_sticker)
            await update.message.reply_text(
                f'Latest X7 Finance Tweet\n\n{tweet[0].text}\n\n'
                f'https://twitter.com/X7_Finance/status/{tweet[0].id}\n\n'
                f'Retweeted {retweet_count} times, by the following members:\n\n{count}')
        else:
            await update.message.reply_text(f'{text.mods_only}')

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
            f'{text.admin_commands}',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Rose Bot Anti-flood', url='https://missrose.org/guide/antiflood/')], ]))
    else:
        await update.message.reply_text(f'{text.mods_only}')

async def countdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    then = times.countdown.astimezone(pytz.utc)
    now = datetime.now(timezone.utc)
    duration = then - now
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    if duration < timedelta(0):
        await update.message.reply_photo(
            photo=open((random.choice(media.logos)), 'rb'),
            caption=f'*X7 Finance Countdown*\n\nNo countdown set, Please check back for more details'
            f'\n\n{api.get_quote()}', parse_mode="Markdown")
    else:
        await update.message.reply_text(
            text=f'*X7 Finance Countdown:*\n\n'
                 f'{times.countdown_title}\n\n{then.strftime("%A %B %d %Y %I:%M %p")} (UTC)\n\n'
                 f'{int(days[0])} days, {int(hours[0])} hours and {int(minutes[0])} minutes\n\n'
                 f'{times.countdown_desc}'
                 f'\n\n{api.get_quote()}', parse_mode="Markdown")

async def mods(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'{text.mods}')

async def show_auto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_admins = await update.effective_chat.get_administrators()
    job_names = [job.name for job in context.job_queue.jobs()]
    if update.effective_user in (admin.user for admin in chat_admins):
        await update.message.reply_text(f'X7 Finance Auto Messages set:\n\n{job_names}\n\nUse /stop_auto "name" '
                                        f'to stop')
    else:
        await update.message.reply_text(f'{text.mods_only}')

async def start_auto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
        context.job_queue.run_repeating(main.auto_message, due*60*60, chat_id=chat_id, name=name, data=message)
        await update.effective_message.reply_text(f"X7 Finance Auto Message: '{name}'\n\nSet every {due} "
                                                  f"Hours\n\n{message}\n\nby {user}")
    else:
        await update.message.reply_text(f'{text.mods_only}')

async def stop_auto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        for job in main.job_queue.get_jobs_by_name((" ".join(context.args))):
            job.schedule_removal()
            await update.message.reply_text(f"X7 Finance auto message, {context.args} Stopped!")
            return
        else:
            await update.message.reply_text(f"No active message named {context.args}.")
    else:
        await update.message.reply_text(f'{text.mods_only}')
