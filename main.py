import logging
from telegram.ext import *
from telegram import *
import keys
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta
import wikipediaapi
import random
import requests
import items
import variables
import tweepy
import pyttsx3
import pandas as pd

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
print('Bot Restarted')


# COMMANDS
async def bot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'{variables.commands}')


async def ecosystem_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    await update.message.reply_text(
        '*X7 Finance Ecosystem*\n\n🌟 *X7R*\nX7\'s original launched token. Hodl as a percentage of all '
        'transaction fees are used to buy and burn tokens, reducing total supply of available tokens.\n\n'
        '🌟 *X7DAO*\nHolders of X7DAO tokens will be able to vote on fee rates, loan terms, funding terms, '
        'tradable token tax terms, distribution of capital flows and any additional settings on and off chain. '
        'This includes the establishment of committees and other foundational efforts off chain.\n\n'
        '🌟 *X7100 Constellation (X7101 - X7105)*\n'
        'A novel - eventually price consistent collection of five tokens. These act as the backstop to the '
        'Lending Pool. The X7100 series of tokens are burned on every transaction. While continually raising its '
        'floor price - it also provides further opportunities to mint new X7Deposit tokens.\n\n'
        '🌟 *X7 NFTs*\nNFTs within the ecosystem will be used to provide opportunities for staking, lending, '
        'discounts, rewards, access to higher governance privileges & much more.\n\n'
        '🌟 *X7Deposit*\nWith insurance of the investor at heart - individuals and '
        'institutions will hold these tokens '
        'just as they would underwrite treasury bills and other stable assets. Holders of X7D will be able to '
        'mint a time-based interest-bearing NFT. X7D is always exchangeable with Ethereum at a 1-to-1 ratio.\n'
        'The X7 Finance protocol will only permit minting of new X7 Deposit tokens when on-chain reserves permit.'
        f'\n\n{quote}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url='https://x7.finance')],
            [InlineKeyboardButton(text='Community Dashboard', url='https://x7community.space/')],
            [InlineKeyboardButton(text='Linktree', url='https://linktr.ee/X7_Finance')],
            [InlineKeyboardButton(text='Medium', url='https://medium.com/@X7Finance')], ]))


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    await update.message.reply_text(
        '*Welcome to X7 Finance*\n\nX7 is an ecosystem of innovative smart contracts that provide those with '
        'visionary ideas access to leveraged seed capital (e.g. Initial Liquidity Offerings, or ILOs) without '
        'lenders incurring the risk of losing the principal. This invention has massive implications not just '
        'for our users, but for all of DeFi 💡\n\n'
        '🌟 At its core, leveraged ILOs means anyone with a good idea can raise 10-1000X the amount of Eth in '
        'their wallet to launch projects on XChange, our world-class DEX. 🌟\n\n'
        '✅ Overtime, the network effect of product launches will result in billions of dollars in trading '
        'volume on our Decentralized Exchange.\n'
        '✅ The protocol will extend to other use case including but not limited to lending/borrowing, leveraged '
        'trading, liquidity locks, & more.\n'
        '✅ A novel DAO governance structure + IPFS website ensures complete decentralization and '
        'censorship-resistance. #LongLiveDefi\n'
        '✅ Our Telegram and Twitter are community-run, in the spirit of decentralization\n\n'
        '🥇 We will consider this project a success once it captures at least 1% of the $100b daily trading '
        'volume on Eth.\n\n'
        'There are many innovative technical and governance applications in this platform so we encourage you '
        'to dig and hop on this rocket ship! 🚀\n\n'
        '"X7’s founding team believes that capital should be available to those with great ideas and that the '
        'unflinching reliability of code and distributed consensus can provide capital while eliminating '
        'significant downside risk.\n\nFirst Initial Leveraged Liquidity DEX to launch\n\n'
        'Developers will be able to borrow initial liquidity to launch with for a small fee. This means projects '
        'can launch with more liquidity and will be very attractive for investors at the beginning.\n\nThe '
        'amount you will be able to borrow, depends on how much your capital is. The more you have, the more '
        'you will be able to borrow from the Lending Pool.\n\nThis is like a decentralized Bank on the '
        'Blockchain. Borrowing money for new projects without a risk, that profits everyone.\n\nEveryone will be '
        'able to loan to the Lending Pool. Lock your ETH in the Lending Pool for 1 month RISK FREE and gain a '
        'specific %  as reward on top of that when '
        'claiming that back (Just for example). This in turn makes the Lending Pool more liquid and helps with'
        ' its growth and success.\n\nAll profit from the DEX, goes back into the ecosystem (Tokens, Lending '
        f'Pool, Future Development etc.). Pumping your bag!" - X7DAO Founding Team\n\n{quote}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url='https://x7.finance')],
            [InlineKeyboardButton(text='Community Dashboard', url='https://x7community.space/')],
            [InlineKeyboardButton(text='Linktree', url='https://linktr.ee/X7_Finance')],
            [InlineKeyboardButton(text='Medium', url='https://medium.com/@X7Finance')], ]))


async def links_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    await update.message.reply_photo(
        photo=open((random.choice(items.logos)), 'rb'),
        caption=f'*X7 Finance links, Dont forget to follow us on socials*\n\n{quote}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url=f'{items.website}')],
            [InlineKeyboardButton(text='Community Dashboard', url=f'{items.dashboard}')],
            [InlineKeyboardButton(text='Linktree', url=f'{items.linktree}')],
            [InlineKeyboardButton(text='Medium', url=f'{items.medium}')],
            [InlineKeyboardButton(text='Twitter', url=f'{items.twitter}')],
            [InlineKeyboardButton(text='Discord', url=f'{items.discord}')],
            [InlineKeyboardButton(text='Reddit', url=f'{items.reddit}')],
            [InlineKeyboardButton(text='Youtube', url=f'{items.youtube}')],
            [InlineKeyboardButton(text='Github', url=f'{items.github}')], ]))


async def nft_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    chain = " ".join(context.args).lower()
    if chain == "":
        await update.message.reply_video(
            video=open(items.nftlogo, 'rb'),
            caption=f'*X7 Finance NFT Information (ETH)*\nUse `/nft [chain-name]` for other chains\n\n'
                    f'*Ecosystem Maxi*\n{items.ecopriceeth}\n'
                    f'> 25% discount on X7100 tax\n'
                    f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n*'
                    f'Liquidity Maxi*\n{items.liqpriceeth}\n'
                    f'> 50 % discount on X7100tax\n> 25 % discount on X7R tax\n'
                    f'> 15 % discount on X7DAO tax\n\n'
                    f'*Dex Maxi*\n{items.dexpriceeth}\n'
                    f'> LP Fee Discounts while trading on X7 DEX\n\n'
                    f'*Borrowing Maxi*\n{items.borrowpriceeth}\n'
                    f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n'
                    f'*Magister*\n{items.magisterpriceeth}\n> 25% discount on X7100 tax\n'
                    f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n*Pioneer*\n'
                    f' > 6% of profits that come into the X7 Treasury Splitter are now being allocated to the reward '
                    f'pool. Each X7 Pioneer NFT grants you a proportional share of this pool\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Mint Here', url='https://x7.finance/x/nft/mint')],
                [InlineKeyboardButton(text='Ecosystem Maxi', url=f'{items.ethertoken}{items.ecoca}')],
                [InlineKeyboardButton(text='Liquidity Maxi', url=f'{items.ethertoken}{items.liqca}')],
                [InlineKeyboardButton(text='DEX Maxi', url=f'{items.ethertoken}{items.dexca}')],
                [InlineKeyboardButton(text='Borrowing Maxi', url=f'{items.ethertoken}{items.borrowca}')],
                [InlineKeyboardButton(text='Magister', url=f'{items.ethertoken}{items.magisterca}')],
                [InlineKeyboardButton(text='Pioneer', url=f'{items.ethertoken}{items.pioneerca}')], ]))
    if chain == "bsc":
        await update.message.reply_video(
            video=open(items.nftlogo, 'rb'),
            caption=f'*X7 Finance NFT Information (BSC)*\nUse `/nft [chain-name]` for other chains\n\n'
                    f'*Ecosystem Maxi*\n{items.ecopricebsc}\n'
                    f'> 25% discount on X7100 tax\n'
                    f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n*Liquidity Maxi*\n{items.liqpricebsc}\n'
                    f'> 50 % discount on X7100tax\n> 25 % discount on X7R tax\n'
                    f'> 15 % discount on X7DAO tax\n\n*Dex Maxi*\n{items.dexpricebsc}\n'
                    f'> LP Fee Discounts while trading on X7 DEX\n\n'
                    f'*Borrowing Maxi*\n{items.borrowpricebsc}\n> Fee discounts for borrowing funds for ILO on X7 '
                    f'DEX\n\n'
                    f'*Magister*\n{items.magisterpricebsc}\n> 25% discount on X7100 tax\n'
                    f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Mint Here', url='https://x7.finance/x/nft/mint')],
                [InlineKeyboardButton(text='Ecosystem Maxi', url=f'{items.bsctoken}{items.ecoca}')],
                [InlineKeyboardButton(text='Liquidity Maxi', url=f'{items.bsctoken}{items.liqca}')],
                [InlineKeyboardButton(text='DEX Maxi', url=f'{items.bsctoken}{items.dexca}')],
                [InlineKeyboardButton(text='Borrowing Maxi', url=f'{items.bsctoken}{items.borrowca}')],
                [InlineKeyboardButton(text='Magister', url=f'{items.bsctoken}{items.magisterca}')], ]))
    if chain == "arbitrum" or chain == "arb":
        await update.message.reply_video(
            video=open(items.nftlogo, 'rb'),
            caption=f'*X7 Finance NFT Information (ARBITRUM)*\nUse `/nft [chain-name]` for other chains\n\n'
                    f'*Ecosystem Maxi*\n{items.ecopricearb}\n'
                    f'> 25% discount on X7100 tax\n'
                    f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n*Liquidity Maxi*\n{items.liqpricearb}\n'
                    f'> 50 % discount on X7100tax\n> 25 % discount on X7R tax\n'
                    f'> 15 % discount on X7DAO tax\n\n*Dex Maxi*\n{items.dexpricearb}\n'
                    f'> LP Fee Discounts while trading on X7 DEX\n\n'
                    f'*Borrowing Maxi*\n{items.borrowpricearb}\n> Fee discounts for borrowing funds for ILO on X7 '
                    f'DEX\n\n'
                    f'*Magister*\n{items.magisterpricearb}\n> 25% discount on X7100 tax\n'
                    f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Mint Here', url='https://x7.finance/x/nft/mint')],
                [InlineKeyboardButton(text='Ecosystem Maxi', url=f'{items.arbtoken}{items.ecoca}')],
                [InlineKeyboardButton(text='Liquidity Maxi', url=f'{items.arbtoken}{items.liqca}')],
                [InlineKeyboardButton(text='DEX Maxi', url=f'{items.arbtoken}{items.dexca}')],
                [InlineKeyboardButton(text='Borrowing Maxi', url=f'{items.arbtoken}{items.borrowca}')],
                [InlineKeyboardButton(text='Magister', url=f'{items.arbtoken}{items.magisterca}')], ]))
    if chain == "polygon" or chain == "poly":
        await update.message.reply_video(
            video=open(items.nftlogo, 'rb'),
            caption=f'*X7 Finance NFT Information (POLYGON)*\nUse `/nft [chain-name]` for other chains\n\n'
                    f'*Ecosystem Maxi*\n{items.ecopricepoly}\n'
                    f'> 25% discount on X7100 tax\n'
                    f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n'
                    f'*Liquidity Maxi*\n{items.liqpricepoly}\n'
                    f'> 50 % discount on X7100tax\n> 25 % discount on X7R tax\n'
                    f'> 15 % discount on X7DAO tax\n\n'
                    f'*Dex Maxi*\n{items.dexpricepoly}\n'
                    f'> LP Fee Discounts while trading on X7 DEX\n\n'
                    f'*Borrowing Maxi*\n{items.borrowpricepoly}\n> Fee discounts for borrowing funds for ILO on X7 '
                    f'DEX\n\n'
                    f'*Magister*\n{items.magisterpricepoly}\n> 25% discount on X7100 tax\n'
                    f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Mint Here', url='https://x7.finance/x/nft/mint')],
                [InlineKeyboardButton(text='Ecosystem Maxi', url=f'{items.polytoken}{items.ecoca}')],
                [InlineKeyboardButton(text='Liquidity Maxi', url=f'{items.polytoken}{items.liqca}')],
                [InlineKeyboardButton(text='DEX Maxi', url=f'{items.polytoken}{items.dexca}')],
                [InlineKeyboardButton(text='Borrowing Maxi', url=f'{items.polytoken}{items.borrowca}')],
                [InlineKeyboardButton(text='Magister', url=f'{items.polytoken}{items.magisterca}')], ]))
    if chain == "optimism" or chain == "opti":
        await update.message.reply_video(
            video=open(items.nftlogo, 'rb'),
            caption=f'*X7 Finance NFT Information (OPTIMISM)*\nUse `/nft [chain-name]` for other chains\n\n'
                    f'*Ecosystem Maxi*\n{items.ecopriceopti}\n'
                    f'> 25% discount on X7100 tax\n'
                    f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n'
                    f'*Liquidity Maxi*\n{items.liqpriceopti}\n'
                    f'> 50 % discount on X7100tax\n> 25 % discount on X7R tax\n'
                    f'> 15 % discount on X7DAO tax\n\n'
                    f'*Dex Maxi*\n{items.dexpriceopti}\n'
                    f'> LP Fee Discounts while trading on X7 DEX\n\n'
                    f'*Borrowing Maxi*\n{items.borrowpriceopti}\n> Fee discounts for borrowing funds for ILO on X7 '
                    f'DEX\n\n'
                    f'*Magister*\n{items.magisterpriceopti}\n> 25% discount on X7100 tax\n'
                    f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Mint Here', url='https://x7.finance/x/nft/mint')],
                [InlineKeyboardButton(text='Ecosystem Maxi', url=f'{items.optitoken}{items.ecoca}')],
                [InlineKeyboardButton(text='Liquidity Maxi', url=f'{items.optitoken}{items.liqca}')],
                [InlineKeyboardButton(text='DEX Maxi', url=f'{items.optitoken}{items.dexca}')],
                [InlineKeyboardButton(text='Borrowing Maxi', url=f'{items.optitoken}{items.borrowca}')],
                [InlineKeyboardButton(text='Magister', url=f'{items.optitoken}{items.magisterca}')], ]))


async def opensea_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    await update.message.reply_photo(
        photo=open(items.opensealogo, 'rb'),
        caption=f'*X7 Finance Opensea Links (ETH)*\n\n{quote}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Ecosystem Maxi', url='https://opensea.io/collection/x7-ecosystem-maxi')],
            [InlineKeyboardButton(text='Liquidity Maxi', url='https://opensea.io/collection/x7-liquidity-maxi')],
            [InlineKeyboardButton(text='DEX Maxi', url='https://opensea.io/collection/x7-dex-maxi')],
            [InlineKeyboardButton(text='Borrowing Maxi', url='https://opensea.io/collection/x7-borrowing-max')],
            [InlineKeyboardButton(text='Magister', url='https://opensea.io/collection/x7-magister')],
            [InlineKeyboardButton(text='Pioneer', url='https://opensea.io/collection/x7-pioneer')], ]))


async def treasury_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    cg = CoinGeckoAPI()
    cgx7rprice = (cg.get_price(ids='x7r', vs_currencies='usd', include_24hr_change='true',
                               include_24hr_vol='true', include_last_updated_at="true"))
    x7rprice = (cgx7rprice["x7r"]["usd"])
    treasuryurl = \
        items.ethbalanceapieth + items.devmultieth + ',' + items.commultieth + ',' + items.pioneerca + '&tag=latest' \
        + keys.ether
    treasuryresponse = requests.get(treasuryurl)
    treasurydata = treasuryresponse.json()
    dev = float(treasurydata["result"][0]["balance"])
    devamount = str(dev / 10 ** 18)
    com = float(treasurydata["result"][1]["balance"])
    comamount = str(com / 10 ** 18)
    pioneer = float(treasurydata["result"][2]["balance"])
    pioneeramount = str(pioneer / 10 ** 18)
    ethurl = items.ethpriceapi + keys.ether
    ethresponse = requests.get(ethurl)
    ethdata = ethresponse.json()
    ethvalue = float(ethdata["result"]["ethusd"])
    devdollar = float(devamount) * float(ethvalue) / 1 ** 18
    comdollar = float(comamount) * float(ethvalue) / 1 ** 18
    pioneerdollar = float(pioneeramount) * float(ethvalue) / 1 ** 18
    comx7rurl = items.tokenbalanceapieth + items.x7rca + '&address=' + items.commultieth + '&tag=latest' + keys.ether
    comx7rresponse = requests.get(comx7rurl)
    comx7rdata = comx7rresponse.json()
    comx7r = int(comx7rdata["result"][:-18])
    comx7rprice = comx7r * x7rprice
    comx7durl = items.tokenbalanceapieth + items.x7dca + '&address=' + items.commultieth + '&tag=latest' + keys.ether
    comx7dresponse = requests.get(comx7durl)
    comx7ddata = comx7dresponse.json()
    comx7d = int(comx7ddata["result"][:-18])
    comx7ddollar = float(comamount) * float(ethvalue) / 1 ** 18
    comx7dprice = comx7d * ethvalue
    comtotal = comx7rprice + comdollar + comx7ddollar
    if chain == "":
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption='*X7 Finance Treasury (ETH)*\nUse `/treasury [chain-name]` for other chains\n\n'
                    f'Pioneer Pool:\n{pioneeramount[:4]}ETH (${"{:0,.0f}".format(pioneerdollar)})\n\n'
                    f'Developer Wallet:\n{devamount[:4]}ETH (${"{:0,.0f}".format(devdollar)})\n\n'
                    f'Community Wallet:\n{comamount[:4]}ETH (${"{:0,.0f}".format(comdollar)})\n'
                    f'{comx7d} X7D (${"{:0,.0f}".format(comx7dprice)})\n'
                    f'{comx7r} X7R (${"{:0,.0f}".format(comx7rprice)})\n'
                    f'Total: (${"{:0,.0f}".format(comtotal)})\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    text='Treasury Splitter Contract', url=f'{items.etheraddress}{items.tsplitterca}')],
                [InlineKeyboardButton(
                    text='Developer Multisig Wallet', url=f'{items.etheraddress}{items.devmultieth}')],
                [InlineKeyboardButton(
                    text='Community Multisig Wallet', url=f'{items.etheraddress}{items.commultieth}')],
            ]))

    if chain == "bsc":
        treasuryurl = items.bnbbalanceapi + items.devmultibsc + ',' + items.commultibsc + '&tag=latest' + keys.bsc
        treasuryresponse = requests.get(treasuryurl)
        treasurydata = treasuryresponse.json()
        dev = float(treasurydata["result"][0]["balance"])
        devamount = str(dev / 10 ** 18)
        com = float(treasurydata["result"][1]["balance"])
        comamount = str(com / 10 ** 18)
        ethurl = items.bnbpriceapi + keys.bsc
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        devdollar = float(devamount) * float(ethvalue) / 1 ** 18
        comdollar = float(comamount) * float(ethvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption='*X7 Finance Treasury (BSC)*\nUse `/treasury [chain-name]` for other chains\n\n'
                    f'Developer Wallet:\n{devamount[:4]}BNB (${"{:0,.0f}".format(devdollar)})\n\n'
                    f'Community Wallet:\n{comamount[:4]}BNB (${"{:0,.0f}".format(comdollar)})\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Treasury Splitter Contract',
                                      url=f'{items.bscaddress}{items.tsplitterca}')],
                [InlineKeyboardButton(text='Developer Multisig Wallet',
                                      url=f'{items.bscaddress}{items.devmultibsc}')],
                [InlineKeyboardButton(text='Community Multisig Wallet',
                                      url=f'{items.bscaddress}{items.commultibsc}')],
            ]))
    if chain == "arbitrum" or chain == "arb":
        treasuryurl = items.ethbalanceapiarb + items.devmultiarb + ',' + items.commultiarb + '&tag=latest' + keys.arb
        treasuryresponse = requests.get(treasuryurl)
        treasurydata = treasuryresponse.json()
        dev = float(treasurydata["result"][0]["balance"])
        devamount = str(dev / 10 ** 18)
        com = float(treasurydata["result"][1]["balance"])
        comamount = str(com / 10 ** 18)
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        devdollar = float(devamount) * float(ethvalue) / 1 ** 18
        comdollar = float(comamount) * float(ethvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption='*X7 Finance Treasury (ARB)*\nUse `/treasury [chain-name]` for other chains\n\n'
                    f'Developer Wallet:\n{devamount[:4]}ETH (${"{:0,.0f}".format(devdollar)})\n\n'
                    f'Community Wallet:\n{comamount[:4]}ETH (${"{:0,.0f}".format(comdollar)})\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Treasury Splitter Contract',
                                      url=f'{items.arbaddress}{items.tsplitterca}')],
                [InlineKeyboardButton(text='Developer Multisig Wallet',
                                      url=f'{items.arbaddress}{items.devmultiarb}')],
                [InlineKeyboardButton(text='Community Multisig Wallet',
                                      url=f'{items.arbaddress}{items.commultiarb}')],
            ]))
    if chain == "polygon" or chain == "poly":
        treasuryurl = items.maticbalanceapi + items.devmultipoly + ',' + items.commultipoly + '&tag=latest' + keys.poly
        treasuryresponse = requests.get(treasuryurl)
        treasurydata = treasuryresponse.json()
        dev = float(treasurydata["result"][0]["balance"])
        devamount = str(dev / 10 ** 18)
        com = float(treasurydata["result"][1]["balance"])
        comamount = str(com / 10 ** 18)
        ethurl = items.maticpriceapi + keys.poly
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["maticusd"])
        devdollar = float(devamount) * float(ethvalue) / 1 ** 18
        comdollar = float(comamount) * float(ethvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption='*X7 Finance Treasury (POLY)*\nUse `/treasury [chain-name]` for other chains\n\n'
                    f'Developer Wallet:\n{devamount[:4]}MATIC (${"{:0,.0f}".format(devdollar)})\n\n'
                    f'Community Wallet:\n{comamount[:4]}MATIC (${"{:0,.0f}".format(comdollar)})\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Treasury Splitter Contract',
                                      url=f'{items.polyaddress}{items.tsplitterca}')],
                [InlineKeyboardButton(text='Developer Multisig Wallet',
                                      url=f'{items.polyaddress}{items.devmultipoly}')],
                [InlineKeyboardButton(text='Community Multisig Wallet',
                                      url=f'{items.polyaddress}{items.commultipoly}')],
            ]))
    if chain == "optimism" or chain == "opti":
        treasuryurl = items.ethbalanceapiopti + items.devmultiopti + ',' + items.commultiopti + '&tag=latest' +\
                      keys.opti
        treasuryresponse = requests.get(treasuryurl)
        treasurydata = treasuryresponse.json()
        dev = float(treasurydata["result"][0]["balance"])
        devamount = str(dev / 10 ** 18)
        com = float(treasurydata["result"][1]["balance"])
        comamount = str(com / 10 ** 18)
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        devdollar = float(devamount) * float(ethvalue) / 1 ** 18
        comdollar = float(comamount) * float(ethvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption='*X7 Finance Treasury (OPTI)*\nUse `/treasury [chain-name]` for other chains\n\n'
                    f'Developer Wallet:\n{devamount[:4]}ETH (${"{:0,.0f}".format(devdollar)})\n\n'
                    f'Community Wallet:\n{comamount[:4]}ETH (${"{:0,.0f}".format(comdollar)})\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Treasury Splitter Contract',
                                      url=f'{items.optiaddress}{items.tsplitterca}')],
                [InlineKeyboardButton(text='Developer Multisig Wallet',
                                      url=f'{items.optiaddress}{items.devmultiopti}')],
                [InlineKeyboardButton(text='Community Multisig Wallet',
                                      url=f'{items.optiaddress}{items.commultiopti}')],
            ]))


async def website_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    await update.message.reply_photo(
        photo=open((random.choice(items.logos)), 'rb'),
        caption=f'*X7 Finance Website Links*\n\n{quote}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url=f'{items.website}')],
            [InlineKeyboardButton(text='Community Dashboard', url=f'{items.dashboard}')], ]))


async def wp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=f'*X7 Finance Whitepaper Quote*\n\n{random.choice(items.quotes)}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url=f'{items.website}')],
            [InlineKeyboardButton(text='Full WP', url=f'{items.wplink}')],
            [InlineKeyboardButton(text='Short WP', url=f'{items.shortwplink}')], ]))


async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    await update.message.reply_photo(
        photo=open((random.choice(items.logos)), 'rb'),
        caption=f'*X7 Finance Buy Links*\nUse `/x7tokenname` for all other details\n'
                f'Use `/constellations` for constellations\n\n{quote}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='X7R - Rewards Token', url=f'{items.xchangebuy}{items.x7rca}')],
            [InlineKeyboardButton(text='X7DAO - Governance Token', url=f'{items.xchangebuy}{items.x7daoca}')], ]))


async def chart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    chain = " ".join(context.args).lower()
    if chain == "":
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption='*X7 Finance Chart Links (ETH)*\nUse `/chart [chain-name]` for other chains\n'
                    f'Use `/constellations` for constellations\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R - Rewards Token',
                                      url=f'{items.dextoolseth}{items.x7rpaireth}')],
                [InlineKeyboardButton(text='X7DAO - Governance Token',
                                      url=f'{items.dextoolseth}{items.x7daopaireth}')], ]))
    if chain == "opti" or chain == "optimism":
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption='*X7 Finance Chart Links (OPTIMISM)*\nUse `/chart [chain-name]` for other chains\n'
                    f'Use `/constellations` for constellations\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R - Rewards Token',
                                      url=f'{items.dextoolsopti}{items.x7rpairopti}')],
                [InlineKeyboardButton(text='X7DAO - Governance Token',
                                      url=f'{items.dextoolsopti}{items.x7daopairopti}')], ]))
    if chain == "bsc":
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption='*X7 Finance Chart Links (BSC)*\nUse `/chart [chain-name]` for other chains\n'
                    f'Use `/constellations` for constellations\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R - Rewards Token',
                                      url=f'{items.dextoolsbsc}{items.x7rpairbsc}')],
                [InlineKeyboardButton(text='X7DAO - Governance Token',
                                      url=f'{items.dextoolsbsc}{items.x7daopairbsc}')], ]))
    if chain == "poly" or chain == "polygon":
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption='*X7 Finance Chart Links (POLYGON)*\nUse `/chart [chain-name]` for other chains\n'
                    f'Use `/constellations` for constellations\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R - Rewards Token',
                                      url=f'{items.dextoolspoly}{items.x7rpairpoly}')],
                [InlineKeyboardButton(text='X7DAO - Governance Token',
                                      url=f'{items.dextoolspoly}{items.x7daopairpoly}')], ]))
    if chain == "arb" or chain == "arbitrum":
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption='*X7 Finance Chart Links (ARBITRUM)*\nUse `/chart [chain-name]` for other chains\n'
                    f'Use `/constellations` for constellations\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R - Rewards Token',
                                      url=f'{items.dextoolsarb}{items.x7rpairarb}')],
                [InlineKeyboardButton(text='X7DAO - Governance Token',
                                      url=f'{items.dextoolsarb}{items.x7daopairarb}')], ]))


async def smart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    chain = " ".join(context.args).lower()
    if chain == "":
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'*X7 Finance Smart Contracts (ETH)*\nUse `/smart [chain-name]` or other chains\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Contracts Directory - by MikeMurpher', url=f'{items.cadir}')],
                [InlineKeyboardButton(text='X7100 Liquidity Hub', url=f'{items.etheraddress}{items.consliqca}')],
                [InlineKeyboardButton(text='X7R Liquidity Hub', url=f'{items.etheraddress}{items.rliqhubca}')],
                [InlineKeyboardButton(text='X7DAO Liquidity Hub', url=f'{items.etheraddress}{items.daoliqhubca}')],
                [InlineKeyboardButton(text='X7 Token Burner', url=f'{items.etheraddress}{items.burnerca}')],
                [InlineKeyboardButton(text='X7100 Discount Authority', url=f'{items.etheraddress}{items.consdaca}')],
                [InlineKeyboardButton(text='X7R Discount Authority', url=f'{items.etheraddress}{items.rdaca}')],
                [InlineKeyboardButton(text='X7DAO Discount Authority', url=f'{items.etheraddress}{items.daodaca}')],
                [InlineKeyboardButton(text='X7 Token Time Lock', url=f'{items.etheraddress}{items.timelockca}')],
                [InlineKeyboardButton(text='X7 Ecosystem Splitter', url=f'{items.etheraddress}{items.esplitterca}')],
                [InlineKeyboardButton(text='X7 Treasury Splitter', url=f'{items.etheraddress}{items.tsplitterca}')],
                [InlineKeyboardButton(text='X7 Lending Pool Reserve', url=f'{items.etheraddress}{items.lpreserveca}')],
                [InlineKeyboardButton(text='X7 Xchange Discount Authority',
                                      url=f'{items.etheraddress}{items.xchangedisca}')],
                [InlineKeyboardButton(text='X7 Lending Discount Authority',
                                      url=f'{items.etheraddress}{items.lendingdisca}')],
                [InlineKeyboardButton(text='X7 Xchange Router', url=f'{items.etheraddress}{items.routerca}')],
                [InlineKeyboardButton(text='X7 Xchange Router with Discounts',
                                      url=f'{items.etheraddress}{items.discountrouterca}')],
                [InlineKeyboardButton(text='X7 Lending Pool Contract', url=f'{items.etheraddress}{items.lpca}')],
                [InlineKeyboardButton(text='X7 Xchange Factory', url=f'{items.etheraddress}{items.factoryca}')],
            ]))
    if chain == "arbitrum":
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'*X7 Finance Smart Contracts (ETH)*\nUse `/smart [chain-name]` or other chains\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Contracts Directory - by MikeMurpher', url=f'{items.cadir}')],
                [InlineKeyboardButton(text='X7100 Liquidity Hub', url=f'{items.arbaddress}{items.consliqca}')],
                [InlineKeyboardButton(text='X7R Liquidity Hub', url=f'{items.arbaddress}{items.rliqhubca}')],
                [InlineKeyboardButton(text='X7DAO Liquidity Hub', url=f'{items.arbaddress}{items.daoliqhubca}')],
                [InlineKeyboardButton(text='X7 Token Burner', url=f'{items.arbaddress}{items.burnerca}')],
                [InlineKeyboardButton(text='X7100 Discount Authority', url=f'{items.arbaddress}{items.consdaca}')],
                [InlineKeyboardButton(text='X7R Discount Authority', url=f'{items.arbaddress}{items.rdaca}')],
                [InlineKeyboardButton(text='X7DAO Discount Authority', url=f'{items.arbaddress}{items.daodaca}')],
                [InlineKeyboardButton(text='X7 Token Time Lock', url=f'{items.arbaddress}{items.timelockca}')],
                [InlineKeyboardButton(text='X7 Ecosystem Splitter', url=f'{items.arbaddress}{items.esplitterca}')],
                [InlineKeyboardButton(text='X7 Treasury Splitter', url=f'{items.arbaddress}{items.tsplitterca}')],
                [InlineKeyboardButton(text='X7 Lending Pool Reserve', url=f'{items.arbaddress}{items.lpreserveca}')],
                [InlineKeyboardButton(text='X7 Xchange Discount Authority',
                                      url=f'{items.arbaddress}{items.xchangedisca}')],
                [InlineKeyboardButton(text='X7 Lending Discount Authority',
                                      url=f'{items.arbaddress}{items.lendingdisca}')],
                [InlineKeyboardButton(text='X7 Xchange Router', url=f'{items.arbaddress}{items.routerca}')],
                [InlineKeyboardButton(text='X7 Xchange Router with Discounts',
                                      url=f'{items.arbaddress}{items.discountrouterca}')],
                [InlineKeyboardButton(text='X7 Lending Pool Contract', url=f'{items.arbaddress}{items.lpca}')],
                [InlineKeyboardButton(text='X7 Xchange Factory', url=f'{items.arbaddress}{items.factoryca}')],
            ]))
    if chain == "polygon":
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'*X7 Finance Smart Contracts (ETH)*\nUse `/smart [chain-name]` or other chains\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Contracts Directory - by MikeMurpher', url=f'{items.cadir}')],
                [InlineKeyboardButton(text='X7100 Liquidity Hub', url=f'{items.polyaddress}{items.consliqca}')],
                [InlineKeyboardButton(text='X7R Liquidity Hub', url=f'{items.polyaddress}{items.rliqhubca}')],
                [InlineKeyboardButton(text='X7DAO Liquidity Hub', url=f'{items.polyaddress}{items.daoliqhubca}')],
                [InlineKeyboardButton(text='X7 Token Burner', url=f'{items.polyaddress}{items.burnerca}')],
                [InlineKeyboardButton(text='X7100 Discount Authority', url=f'{items.polyaddress}{items.consdaca}')],
                [InlineKeyboardButton(text='X7R Discount Authority', url=f'{items.polyaddress}{items.rdaca}')],
                [InlineKeyboardButton(text='X7DAO Discount Authority', url=f'{items.polyaddress}{items.daodaca}')],
                [InlineKeyboardButton(text='X7 Token Time Lock', url=f'{items.polyaddress}{items.timelockca}')],
                [InlineKeyboardButton(text='X7 Ecosystem Splitter', url=f'{items.polyaddress}{items.esplitterca}')],
                [InlineKeyboardButton(text='X7 Treasury Splitter', url=f'{items.polyaddress}{items.tsplitterca}')],
                [InlineKeyboardButton(text='X7 Lending Pool Reserve', url=f'{items.polyaddress}{items.lpreserveca}')],
                [InlineKeyboardButton(text='X7 Xchange Discount Authority',
                                      url=f'{items.polyaddress}{items.xchangedisca}')],
                [InlineKeyboardButton(text='X7 Lending Discount Authority',
                                      url=f'{items.polyaddress}{items.lendingdisca}')],
                [InlineKeyboardButton(text='X7 Xchange Router', url=f'{items.polyaddress}{items.routerca}')],
                [InlineKeyboardButton(text='X7 Xchange Router with Discounts',
                                      url=f'{items.arbaddress}{items.discountrouterca}')],
                [InlineKeyboardButton(text='X7 Lending Pool Contract', url=f'{items.polyaddress}{items.lpca}')],
                [InlineKeyboardButton(text='X7 Xchange Factory', url=f'{items.polyaddress}{items.factoryca}')],
            ]))
    if chain == "bsc":
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'*X7 Finance Smart Contracts (ETH)*\nUse `/smart [chain-name]` or other chains\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Contracts Directory - by MikeMurpher', url=f'{items.cadir}')],
                [InlineKeyboardButton(text='X7100 Liquidity Hub', url=f'{items.bscaddress}{items.consliqca}')],
                [InlineKeyboardButton(text='X7R Liquidity Hub', url=f'{items.bscaddress}{items.rliqhubca}')],
                [InlineKeyboardButton(text='X7DAO Liquidity Hub', url=f'{items.bscaddress}{items.daoliqhubca}')],
                [InlineKeyboardButton(text='X7 Token Burner', url=f'{items.bscaddress}{items.burnerca}')],
                [InlineKeyboardButton(text='X7100 Discount Authority', url=f'{items.bscaddress}{items.consdaca}')],
                [InlineKeyboardButton(text='X7R Discount Authority', url=f'{items.bscaddress}{items.rdaca}')],
                [InlineKeyboardButton(text='X7DAO Discount Authority', url=f'{items.bscaddress}{items.daodaca}')],
                [InlineKeyboardButton(text='X7 Token Time Lock', url=f'{items.bscaddress}{items.timelockca}')],
                [InlineKeyboardButton(text='X7 Ecosystem Splitter', url=f'{items.bscaddress}{items.esplitterca}')],
                [InlineKeyboardButton(text='X7 Treasury Splitter', url=f'{items.bscaddress}{items.tsplitterca}')],
                [InlineKeyboardButton(text='X7 Lending Pool Reserve', url=f'{items.bscaddress}{items.lpreserveca}')],
                [InlineKeyboardButton(text='X7 Xchange Discount Authority',
                                      url=f'{items.bscaddress}{items.xchangedisca}')],
                [InlineKeyboardButton(text='X7 Lending Discount Authority',
                                      url=f'{items.bscaddress}{items.lendingdisca}')],
                [InlineKeyboardButton(text='X7 Xchange Router', url=f'{items.bscaddress}{items.routerca}')],
                [InlineKeyboardButton(text='X7 Xchange Router with Discounts',
                                      url=f'{items.bscaddress}{items.discountrouterca}')],
                [InlineKeyboardButton(text='X7 Lending Pool Contract', url=f'{items.bscaddress}{items.lpca}')],
                [InlineKeyboardButton(text='X7 Xchange Factory', url=f'{items.bscaddress}{items.factoryca}')],
            ]))
    if chain == "optimism":
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'*X7 Finance Smart Contracts (ETH)*\nUse `/smart [chain-name]` or other chains\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Contracts Directory - by MikeMurpher', url=f'{items.cadir}')],
                [InlineKeyboardButton(text='X7100 Liquidity Hub', url=f'{items.optiaddress}{items.consliqca}')],
                [InlineKeyboardButton(text='X7R Liquidity Hub', url=f'{items.optiaddress}{items.rliqhubca}')],
                [InlineKeyboardButton(text='X7DAO Liquidity Hub', url=f'{items.optiaddress}{items.daoliqhubca}')],
                [InlineKeyboardButton(text='X7 Token Burner', url=f'{items.optiaddress}{items.burnerca}')],
                [InlineKeyboardButton(text='X7100 Discount Authority', url=f'{items.optiaddress}{items.consdaca}')],
                [InlineKeyboardButton(text='X7R Discount Authority', url=f'{items.optiaddress}{items.rdaca}')],
                [InlineKeyboardButton(text='X7DAO Discount Authority', url=f'{items.optiaddress}{items.daodaca}')],
                [InlineKeyboardButton(text='X7 Token Time Lock', url=f'{items.optiaddress}{items.timelockca}')],
                [InlineKeyboardButton(text='X7 Ecosystem Splitter', url=f'{items.optiaddress}{items.esplitterca}')],
                [InlineKeyboardButton(text='X7 Treasury Splitter', url=f'{items.optiaddress}{items.tsplitterca}')],
                [InlineKeyboardButton(text='X7 Lending Pool Reserve', url=f'{items.optiaddress}{items.lpreserveca}')],
                [InlineKeyboardButton(text='X7 Xchange Discount Authority',
                                      url=f'{items.optiaddress}{items.xchangedisca}')],
                [InlineKeyboardButton(text='X7 Lending Discount Authority',
                                      url=f'{items.optiaddress}{items.lendingdisca}')],
                [InlineKeyboardButton(text='X7 Xchange Router', url=f'{items.optiaddress}{items.routerca}')],
                [InlineKeyboardButton(text='X7 Xchange Router with Discounts',
                                      url=f'{items.optiaddress}{items.discountrouterca}')],
                [InlineKeyboardButton(text='X7 Lending Pool Contract', url=f'{items.optiaddress}{items.lpca}')],
                [InlineKeyboardButton(text='X7 Xchange Factory', url=f'{items.optiaddress}{items.factoryca}')],
            ]))


async def ca_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    await update.message.reply_photo(
        photo=open((random.choice(items.logos)), 'rb'),
        caption=f'*X7 Finance Contract Addresses*\n\n*X7R*\n`{items.x7rca}`'
                f'\n\n*X7DAO*\n`{items.x7daoca}`\n\n'
                f'Use `/x7tokenname` for all other details\n\n{quote}',
        parse_mode='Markdown')


async def x7d_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    chain = " ".join(context.args).lower()
    if chain == "":
        x7dholdersurl = items.holdersapi + items.x7dca + keys.holders
        x7dholdersresponse = requests.get(x7dholdersurl)
        x7dholdersdata = x7dholdersresponse.json()
        x7dholders = x7dholdersdata["holdersCount"]
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        x7durl = items.ethbalanceapieth + items.lpreserveca + '&tag' + keys.ether
        x7dresponse = requests.get(x7durl)
        x7ddata = x7dresponse.json()
        damount = float(x7ddata["result"][0]["balance"])
        x7damount = str(damount / 10 ** 18)
        x7ddollar = float(x7damount) * float(ethvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open(items.x7dlogo, 'rb'),
            caption=f'*X7D (ETH) Info*\n'
                    f'For other chains use `/x7d [chainname]`\n\n'
                    f'Supply: {x7damount[:4]}ETH (${"{:0,.0f}".format(x7ddollar)})\n'
                    f'Holders: {x7dholders}\n\n'
                    f'To receive X7D:\n\n'
                    '1. Send ETH (Not Swap) to the Lending Pool Reserve Contract:\n'
                    f'`{items.lpreserveca}`\n\n'
                    '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n'
                    f'`{items.x7dca}`\n\nYou will receive X7D in your wallet which has a 1:1 price X7D:ETH\n\n'
                    'Note:\n'
                    'Do not interact directly with the X7D contract\n'
                    'Do not send from a CEX\n\n'
                    f'{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='X7 Lending Pool Reserve Contract',
                                       url=f'{items.etheraddress}{items.lpreserveca}#code')],
                 [InlineKeyboardButton(text='X7 Deposit Contract',
                                       url=f'{items.etheraddress}{items.x7dca}#code')],
                 ]))
    if chain == "bsc":
        ethurl = items.bnbpriceapi + keys.bsc
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        x7durl = items.ethbalanceapieth + items.lpreserveca + '&tag' + keys.ether
        x7dresponse = requests.get(x7durl)
        x7ddata = x7dresponse.json()
        damount = float(x7ddata["result"][0]["balance"])
        x7damount = str(damount / 10 ** 18)
        x7ddollar = float(x7damount) * float(ethvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open(items.x7dlogo, 'rb'),
            caption=f'*X7D (BSC) Info*\n\n'
                    f'Supply: {x7damount[:4]}BNB (${"{:0,.0f}".format(x7ddollar)})\n'
                    f'To receive X7D:\n\n'
                    '1. Send BNB (Not Swap) to the Lending Pool Reserve Contract:\n'
                    f'`{items.lpreserveca}`\n\n'
                    '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n'
                    f'`{items.x7dca}`\n\nYou will receive X7D in your wallet which has a 1:1 price X7D:BNB\n\n'
                    'Note:\n'
                    'Do not interact directly with the X7D contract\n'
                    'Do not send from a CEX\n\n'
                    f'{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='X7 Lending Pool Reserve Contract',
                                       url=f'{items.bscaddress}{items.lpreserveca}#code')],
                 [InlineKeyboardButton(text='X7 Deposit Contract',
                                       url=f'{items.bscaddress}{items.x7dca}#code')],
                 ]))
    if chain == "polygon" or chain == "poly":
        ethurl = items.maticpriceapi + keys.poly
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["maticusd"])
        x7durl = items.maticbalanceapi + items.lpreserveca + '&tag' + keys.poly
        x7dresponse = requests.get(x7durl)
        x7ddata = x7dresponse.json()
        damount = float(x7ddata["result"][0]["balance"])
        x7damount = str(damount / 10 ** 18)
        x7ddollar = float(x7damount) * float(ethvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open(items.x7dlogo, 'rb'),
            caption=f'*X7D (POLY) Info*\n\n'
                    f'Supply: {x7damount[:4]}MATIC (${"{:0,.0f}".format(x7ddollar)})\n'
                    f'To receive X7D.\n\n'
                    '1. Send MATIC (Not Swap) to the Lending Pool Reserve Contract:\n'
                    f'`{items.lpreserveca}`\n\n'
                    '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n'
                    f'`{items.x7dca}`\n\nYou will receive X7D in your wallet which has a 1:1 price X7D:MATIC\n\n'
                    'Note:\n'
                    'Do not interact directly with the X7D contract\n'
                    'Do not send from a CEX\n\n'
                    f'{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='X7 Lending Pool Reserve Contract',
                                       url=f'{items.polyaddress}{items.lpreserveca}#code')],
                 [InlineKeyboardButton(text='X7 Deposit Contract',
                                       url=f'{items.polyaddress}{items.x7dca}#code')],
                 ]))
    if chain == "optimism" or chain == "opti":
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        x7durl = items.ethbalanceapiopti + items.lpreserveca + '&tag' + keys.opti
        x7dresponse = requests.get(x7durl)
        x7ddata = x7dresponse.json()
        damount = float(x7ddata["result"][0]["balance"])
        x7damount = str(damount / 10 ** 18)
        x7ddollar = float(x7damount) * float(ethvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open(items.x7dlogo, 'rb'),
            caption=f'*X7D (OPTIMISM) Info*\n\n'
                    f'Supply: {x7damount[:4]}ETH (${"{:0,.0f}".format(x7ddollar)})\n'
                    f'To receive X7D.\n\n'
                    '1. Send ETH (Not Swap) to the Lending Pool Reserve Contract:\n'
                    f'`{items.lpreserveca}`\n\n'
                    '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n'
                    f'`{items.x7dca}`\n\nYou will receive X7D in your wallet which has a 1:1 price X7D:ETH\n\n'
                    'Note:\n'
                    'Do not interact directly with the X7D contract\n'
                    'Do not send from a CEX\n\n'
                    f'{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='X7 Lending Pool Reserve Contract',
                                       url=f'{items.optiaddress}{items.lpreserveca}#code')],
                 [InlineKeyboardButton(text='X7 Deposit Contract',
                                       url=f'{items.optiaddress}{items.x7dca}#code')],
                 ]))
    if chain == "arbitrum" or chain == "arb":
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        x7durl = items.ethbalanceapiarb + items.lpreserveca + '&tag' + keys.arb
        x7dresponse = requests.get(x7durl)
        x7ddata = x7dresponse.json()
        damount = float(x7ddata["result"][0]["balance"])
        x7damount = str(damount / 10 ** 18)
        x7ddollar = float(x7damount) * float(ethvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open(items.x7dlogo, 'rb'),
            caption=f'*X7D (ARBITRUM) Info*\n\n'
                    f'Supply: {x7damount[:4]}ETH (${"{:0,.0f}".format(x7ddollar)})\n'
                    f'To receive X7D.\n\n'
                    '1. Send ETH (Not Swap) to the Lending Pool Reserve Contract:\n'
                    f'`{items.lpreserveca}`\n\n'
                    '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n'
                    f'`{items.x7dca}`\n\nYou will receive X7D in your wallet which has a 1:1 price X7D:ETH\n\n'
                    'Note:\n'
                    'Do not interact directly with the X7D contract\n'
                    'Do not send from a CEX\n\n'
                    f'{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='X7 Lending Pool Reserve Contract',
                                       url=f'{items.arbaddress}{items.lpreserveca}#code')],
                 [InlineKeyboardButton(text='X7 Deposit Contract',
                                       url=f'{items.arbaddress}{items.x7dca}#code')],
                 ]))


async def media_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    await update.message.reply_photo(
        photo=open((random.choice(items.logos)), 'rb'),
        caption=f'*X7 Finance Media Links*\n\n{quote}',
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


async def buyevenly_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
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
        '4.2. slippagePercent  -> desired slippage (e.g. 4)\n4.3 deadline -> Go to [epochconverter]'
        '(https://www.epochconverter.com/) and add like 500 to the current epoch. Click "Timestamp to Human date" '
        'and verify that Relative is at least "In 1 minute" (e.g. 1667508502).\n'
        '4.4 Copy the epoch to the "deadline" field\n4.4 Press "Write" and confirm the transaction in your wallet.\n'
        '4.5 You should receive tokens to your wallet in few blocks.\n\n'
        '*Testrun TX*:\n'
        'https://etherscan.io/tx/0x321e5bb6cc1695d5d7085eceb92f01143b69c2274402aab46e4a0a47d069d0af\n\n'
        f'Credit: @WoxieX\n\n{quote}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Via Dashboard', url='https://dapp.x7community.space/')],
             [InlineKeyboardButton(text='Via Etherscan', url='https://etherscan.io/address/0x0419074afe1a'
                                                             '137dfa6afd5b6af5771c3ffbea49#code')],
             [InlineKeyboardButton(text='Epoch Convertor', url='https://www.epochconverter.com/')], ]))


async def channels_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    await update.message.reply_photo(
        photo=open((random.choice(items.logos)), 'rb'),
        caption=f'*X7 Finance Community TG Channels*\n\n{quote}', parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Community Chat', url='https://t.me/X7m105portal')],
             [InlineKeyboardButton(text='Announcements', url='https://t.me/X7announcements')],
             [InlineKeyboardButton(text='Media', url='https://t.me/X7MediaChannel')],
             [InlineKeyboardButton(text='Research Notes', url='https://t.me/X7m105_Research')],
             [InlineKeyboardButton(text='Chinese Community', url='https://t.me/X7CNPortal')], ]))


async def pioneer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    pioneerid = " ".join(context.args)
    if pioneerid == "":
        slug = "/x7-pioneer"
        headers = {"X-API-KEY": keys.os}
        pioneerurl = items.osapi + slug
        pioneerresponse = requests.get(pioneerurl, headers=headers)
        pioneerdata = pioneerresponse.json()
        floor = (pioneerdata["collection"]["stats"]["floor_price"])
        traits = (pioneerdata["collection"]["traits"]["Transfer Lock Status"]["unlocked"])
        cap = round(pioneerdata["collection"]["stats"]["market_cap"], 2)
        sales = (pioneerdata["collection"]["stats"]["total_sales"])
        owners = (pioneerdata["collection"]["stats"]["num_owners"])
        price = round(pioneerdata["collection"]["stats"]["average_price"], 2)
        volume = round(pioneerdata["collection"]["stats"]["total_volume"], 2)
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        pioneerethurl = items.ethbalanceapieth + items.pioneerca + '&tag=latest' + keys.ether
        pioneerethresponse = requests.get(pioneerethurl)
        pioneerethdata = pioneerethresponse.json()
        pioneer = float(pioneerethdata["result"][0]["balance"])
        totalamount = str(pioneer / 10 ** 18)
        totaldollarraw = float(totalamount) * float(ethvalue) / 1 ** 18
        totaldollar = str(totaldollarraw)
        pioneereamount = str(pioneer / 10 ** 18 / 639)
        pioneerdollarraw = float(totalamount) * float(ethvalue) / 1 ** 18 / 639
        pioneerdollar = str(pioneerdollarraw)
        await update.message.reply_photo(
            photo=open(items.pioneerlogo, 'rb'),
            caption=f'*X7 Pioneer NFT Info*\n\nFloor Price: {floor} ETH\n'
                    f'Average Price: {price} ETH\n'
                    f'Market Cap: {cap} ETH\n'
                    f'Total Volume: {volume} ETH\n'
                    f'Total Sales: {sales}\n'
                    f'Number of Owners: {owners}\n'
                    f'Pioneers Unlocked: {traits}\n'
                    f'Pioneer Pool: {totalamount[:3]} ETH (${totaldollar[:4]})\n\n'
                    f'Pioneer Earnings: {pioneereamount[:5]} ETH (${pioneerdollar[:4]})\n\n{quote}',
            parse_mode='markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='X7 Pioneer Dashboard', url='https://x7.finance/x/nft/pioneer')],
                 [InlineKeyboardButton(text='Opensea', url='https://opensea.io/collection/x7-pioneer')], ]))
    else:
        baseurl = "https://api.opensea.io/api/v1/asset/"
        slug = items.pioneerca+"/"
        headers = {"X-API-KEY": keys.os}
        singleurl = baseurl + slug + pioneerid + "/"
        singleresponse = requests.get(singleurl, headers=headers)
        singledata = singleresponse.json()
        status = (singledata["traits"][0]["value"])
        await update.message.reply_text(
            f'*X7 Pioneer {pioneerid} NFT Info*\n\n'
            f'Transfer Lock Status: {status}\n\n'
            f'https://opensea.io/assets/ethereum/0x70000299ee8910ccacd97b1bb560e34f49c9e4f7/'
            f'{pioneerid}\n\n{quote}',
            parse_mode='markdown')


async def burn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    if chain == "":
        burnurl = items.tokenbalanceapieth + items.x7rca + '&address=' + items.dead + '&tag=latest' + keys.ether
        burnresponse = requests.get(burnurl)
        burndata = burnresponse.json()
        burndata["result"] = int(burndata["result"][:-18])
        result = round(((burndata["result"] / items.supply) * 100), 6)
        await update.message.reply_photo(
            photo=open(items.x7rlogo, 'rb'),
            caption=f'\n\nX7R (ETH) Tokens Burned:\nUse `/burn [chain-name]` for other chains\n\n'
                    f'{"{:,}".format(burndata["result"])}\n'
                    f'{result}% of Supply\n\n'
                    f'[Etherscan]({items.ethertoken}{items.x7rca}?a={items.dead})\n\n{quote}',
            parse_mode="markdown")
    if chain == "bsc":
        burnurl = items.tokenbalanceapibsc + items.x7rca + '&address=' + items.dead + '&tag=latest' + keys.bsc
        burnresponse = requests.get(burnurl)
        burndata = burnresponse.json()
        burndata["result"] = int(burndata["result"][:-18])
        result = round(((burndata["result"] / items.supply) * 100), 6)
        await update.message.reply_photo(
            photo=open(items.x7rlogo, 'rb'),
            caption=f'\n\nX7R (BSC) Tokens Burned:\nUse `/burn [chain-name]` for other chains\n\n'
                    f'{"{:,}".format(burndata["result"])}\n'
                    f'{result}% of Supply\n\n'
                    f'[BSCscan]({items.ethertoken}{items.x7rca}?a={items.dead})\n\n{quote}',
            parse_mode="markdown")
    if chain == "polygon" or chain == "poly":
        burnurl = items.tokenbalanceapipoly + items.x7rca + '&address=' + items.dead + '&tag=latest' + keys.poly
        burnresponse = requests.get(burnurl)
        burndata = burnresponse.json()
        burndata["result"] = int(burndata["result"][:-18])
        result = round(((burndata["result"] / items.supply) * 100), 6)
        await update.message.reply_photo(
            photo=open(items.x7rlogo, 'rb'),
            caption=f'\n\nX7R (POLYGON) Tokens Burned:\n\n'
                    f'{"{:,}".format(burndata["result"])}\n'
                    f'{result}% of Supply\n\n'
                    f'[Polygonscan]({items.polytoken}{items.x7rca}?a={items.dead})\n\n{quote}',
            parse_mode="markdown")
    if chain == "arbitrum" or chain == "arb":
        burnurl = items.tokenbalanceapibsc + items.x7rca + '&address=' + items.dead + '&tag=latest' + keys.arb
        burnresponse = requests.get(burnurl)
        burndata = burnresponse.json()
        burndata["result"] = int(burndata["result"][:-18])
        result = round(((burndata["result"] / items.supply) * 100), 6)
        await update.message.reply_photo(
            photo=open(items.x7rlogo, 'rb'),
            caption=f'\n\nX7R (ARBITRUM) Tokens Burned:\nUse `/burn [chain-name]` for other chains\n\n'
                    f'{"{:,}".format(burndata["result"])}\n'
                    f'{result}% of Supply\n\n'
                    f'[Arbiscan]({items.arbtoken}{items.x7rca}?a={items.dead})\n\n{quote}',
            parse_mode="markdown")
    if chain == "optimism" or chain == "arb":
        burnurl = items.tokenbalanceapibsc + items.x7rca + '&address=' + items.dead + '&tag=latest' + keys.opti
        burnresponse = requests.get(burnurl)
        burndata = burnresponse.json()
        burndata["result"] = int(burndata["result"][:-18])
        result = round(((burndata["result"] / items.supply) * 100), 6)
        await update.message.reply_photo(
            photo=open(items.x7rlogo, 'rb'),
            caption=f'\n\nX7R (OPTIMISM) Tokens Burned:\nUse `/burn [chain-name]` for other chains\n\n'
                    f'{"{:,}".format(burndata["result"])}\n'
                    f'{result}% of Supply\n\n'
                    f'[Optimism.Etherscan]({items.optitoken}{items.x7rca}?a={items.dead})\n\n{quote}',
            parse_mode="markdown")


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quote = (random.choice(quotedata))
    text = quote["text"]
    author = quote["author"]
    wiki = wikipediaapi.Wikipedia('en')
    keyword = " ".join(context.args)
    page_py = wiki.page(keyword)
    if keyword == "":
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption='Please follow the command with your search')
    if page_py.exists():
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'Your search: {page_py.title}\n\n'
                    f'{(page_py.summary[0:800])}'
                    f'....[continue reading on wiki]({page_py.fullurl})\n\n'
                    f'[Google](https://www.google.com/search?q={keyword})\n'
                    f'[Twitter](https://twitter.com/search?q={keyword}&src=typed_query)\n'
                    f'[Etherscan](https://etherscan.io/search?f=0&q={keyword})\n\n'
                    f'`"{text}"\n\n-{author}`',
            parse_mode="markdown")

    else:
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'Your search: {keyword}\n\nNo description available\n\n'
                    f'[Google](https://www.google.com/search?q={keyword})\n'
                    f'[Twitter](https://twitter.com/search?q={keyword}&src=typed_query)\n'
                    f'[Etherscan](https://etherscan.io/search?f=0&q={keyword})\n\n'
                    f'`"{text}"\n\n-{author}`',
            parse_mode="markdown")


async def pool_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    ethurl = items.ethpriceapi + keys.ether
    ethresponse = requests.get(ethurl)
    ethdata = ethresponse.json()
    ethvalue = float(ethdata["result"]["ethusd"])
    if chain == "":
        poolurl = items.ethbalanceapieth + items.lpreserveca + '&tag=latest' + keys.ether
        poolresponse = requests.get(poolurl)
        pooldata = poolresponse.json()
        pool = float(pooldata["result"][0]["balance"])
        poolamount = str(pool / 10 ** 18)
        pooldollar = float(poolamount) * float(ethvalue) / 1 ** 18
        arbpoolurl = items.ethbalanceapiarb + items.lpreserveca + '&tag=latest' + keys.arb
        arbpoolresponse = requests.get(arbpoolurl)
        arbpooldata = arbpoolresponse.json()
        arbpool = float(arbpooldata["result"][0]["balance"])
        arbpoolamount = str(arbpool / 10 ** 18)
        arbpooldollar = float(arbpoolamount) * float(ethvalue) / 1 ** 18
        bscurl = items.bnbpriceapi + keys.bsc
        bscresponse = requests.get(bscurl)
        bscdata = bscresponse.json()
        bscvalue = float(bscdata["result"]["ethusd"])
        bscpoolurl = items.bnbbalanceapi + items.lpreserveca + '&tag=latest' + keys.bsc
        bscpoolresponse = requests.get(bscpoolurl)
        bscpooldata = bscpoolresponse.json()
        bscpool = float(bscpooldata["result"][0]["balance"])
        bscpoolamount = str(bscpool / 10 ** 18)
        bscpooldollar = float(bscpoolamount) * float(bscvalue) / 1 ** 18
        optipoolurl = items.ethbalanceapiopti + items.lpreserveca + '&tag=latest' + keys.opti
        optipoolresponse = requests.get(optipoolurl)
        optipooldata = optipoolresponse.json()
        optipool = float(optipooldata["result"][0]["balance"])
        optipoolamount = str(optipool / 10 ** 18)
        optipooldollar = float(optipoolamount) * float(ethvalue) / 1 ** 18
        polyurl = items.maticpriceapi + keys.poly
        polyresponse = requests.get(polyurl)
        polydata = polyresponse.json()
        polyvalue = float(polydata["result"]["maticusd"])
        polypoolurl = items.maticbalanceapi + items.lpreserveca + '&tag=latest' + keys.poly
        polypoolresponse = requests.get(polypoolurl)
        polypooldata = polypoolresponse.json()
        polypool = float(polypooldata["result"][0]["balance"])
        polypoolamount = str(polypool / 10 ** 18)
        polypooldollar = float(polypoolamount) * float(polyvalue) / 1 ** 18
        totaldollar = polypooldollar + bscpooldollar + optipooldollar + arbpooldollar + pooldollar
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'*X7 Finance Lending Pool Info *\nUse `/pool [chain-name]` for individual contracts\n\n'
                    f'ETH: {poolamount[:5]} ETH (${"{:0,.0f}".format(pooldollar)})\n\n'
                    f'ARB: {arbpoolamount[:4]} ETH (${"{:0,.0f}".format(arbpooldollar)})\n\n'
                    f'OPTI: {optipoolamount[:5]} ETH (${"{:0,.0f}".format(optipooldollar)})\n\n'
                    f'BSC: {bscpoolamount[:4]} BNB (${"{:0,.0f}".format(bscpooldollar)})\n\n'
                    f'POLY: {polypoolamount[:4]} MATIC (${"{:0,.0f}".format(polypooldollar)})\n\n'
                    f'TOTAL: ${"{:0,.0f}".format(totaldollar)}\n\n'
                    f'{quote}', parse_mode='Markdown')

    if chain == "eth":
        poolurl = items.ethbalanceapieth + items.lpreserveca + '&tag=latest' + keys.ether
        poolresponse = requests.get(poolurl)
        pooldata = poolresponse.json()
        pool = float(pooldata["result"][0]["balance"])
        poolamount = str(pool / 10 ** 18)
        pooldollar = float(poolamount) * float(ethvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'*X7 Finance Lending Pool Info (ETH)*\nUse `/pool [chain-name]` for other chains\n\n'
                    f'{poolamount[:4]} ETH (${"{:0,.0f}".format(pooldollar)})\n\n'
                    f'{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='Lending Pool Reserve Contract',
                                       url=f'{items.etheraddress}{items.lpreserveca}')],
                 [InlineKeyboardButton(text='X7 Deposit Contract',
                                       url=f'{items.etheraddress}{items.x7dca}#code')], ]))
    if chain == "bsc":
        bscurl = items.bnbpriceapi + keys.bsc
        bscresponse = requests.get(bscurl)
        bscdata = bscresponse.json()
        bscvalue = float(bscdata["result"]["ethusd"])
        bscpoolurl = items.bnbbalanceapi + items.lpreserveca + '&tag=latest' + keys.bsc
        bscpoolresponse = requests.get(bscpoolurl)
        bscpooldata = bscpoolresponse.json()
        bscpool = float(bscpooldata["result"][0]["balance"])
        bscpoolamount = str(bscpool / 10 ** 18)
        bscpooldollar = float(bscpoolamount) * float(bscvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'*X7 Finance Lending Pool Info (BSC)*\nUse `/pool [chain-name]` for other chains\n\n'
                    f'{bscpoolamount[:4]} BNB (${"{:0,.0f}".format(bscpooldollar)})\n\n'
                    f'{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='Lending Pool Reserve Contract',
                                       url=f'{items.bscaddress}{items.lpreserveca}')],
                 [InlineKeyboardButton(text='X7 Deposit Contract',
                                       url=f'{items.bscaddress}{items.x7dca}#code')], ]))
    if chain == "arbitrum" or chain == "arb":
        arbpoolurl = items.ethbalanceapiarb + items.lpreserveca + '&tag=latest' + keys.arb
        arbpoolresponse = requests.get(arbpoolurl)
        arbpooldata = arbpoolresponse.json()
        arbpool = float(arbpooldata["result"][0]["balance"])
        arbpoolamount = str(arbpool / 10 ** 18)
        arbpooldollar = float(arbpoolamount) * float(ethvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'*X7 Finance Lending Pool Info (ARB)*\nUse `/pool [chain-name]` for other chains\n\n'
                    f'{arbpoolamount[:4]} ETH (${"{:0,.0f}".format(arbpooldollar)})\n\n'
                    f'{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='Lending Pool Reserve Contract',
                                       url=f'{items.arbaddress}{items.lpreserveca}')],
                 [InlineKeyboardButton(text='X7 Deposit Contract',
                                       url=f'{items.arbaddress}{items.x7dca}#code')], ]))
    if chain == "optimism" or chain == "opti":
        optipoolurl = items.ethbalanceapiopti + items.lpreserveca + '&tag=latest' + keys.opti
        optipoolresponse = requests.get(optipoolurl)
        optipooldata = optipoolresponse.json()
        optipool = float(optipooldata["result"][0]["balance"])
        optipoolamount = str(optipool / 10 ** 18)
        optipooldollar = float(optipoolamount) * float(ethvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'*X7 Finance Lending Pool Info (OPTIMISM)*\nUse `/pool [chain-name]` for other chains\n\n'
                    f'{optipoolamount[:4]} ETH (${"{:0,.0f}".format(optipooldollar)})\n\n'
                    f'{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='Lending Pool Reserve Contract',
                                       url=f'{items.optiaddress}{items.lpreserveca}')],
                 [InlineKeyboardButton(text='X7 Deposit Contract',
                                       url=f'{items.optiaddress}{items.x7dca}#code')], ]))
    if chain == "polygon" or chain == "poly":
        polyurl = items.maticpriceapi + keys.poly
        polyresponse = requests.get(polyurl)
        polydata = polyresponse.json()
        polyvalue = float(polydata["result"]["maticusd"])
        polypoolurl = items.maticbalanceapi + items.lpreserveca + '&tag=latest' + keys.poly
        polypoolresponse = requests.get(polypoolurl)
        polypooldata = polypoolresponse.json()
        polypool = float(polypooldata["result"][0]["balance"])
        polypoolamount = str(polypool / 10 ** 18)
        polypooldollar = float(polypoolamount) * float(polyvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'*X7 Finance Lending Pool Info (POLYGON)*\nUse `/pool [chain-name]` for other chains\n\n'
                    f'{polypoolamount[:4]} MATIC (${"{:0,.0f}".format(polypooldollar)})\n\n'
                    f'{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='Lending Pool Reserve Contract',
                                       url=f'{items.polyaddress}{items.lpreserveca}')],
                 [InlineKeyboardButton(text='X7 Deposit Contract',
                                       url=f'{items.polyaddress}{items.x7dca}#code')], ]))


async def listings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    await update.message.reply_photo(
        photo=open((random.choice(items.logos)), 'rb'),
        caption=f'*X7 Finance Listings*\n\n'
                f'*X7R*\nhttps://coinmarketcap.com/currencies/x7r/\n'
                f'https://www.coingecko.com/en/coins/x7r\n'
                f'https://tokeninsight.com/en/coins/x7r/overview\n'
                f'https://coinbazooka.com/coin/X7R\n\n'
                f'*X7DAO*\n'
                f'https://coinmarketcap.com/currencies/x7dao/\n'
                f'https://www.coingecko.com/en/coins/x7dao\n'
                f'https://tokeninsight.com/en/coins/x7dao/overview\n'
                f'https://coinbazooka.com/coin/X7dao\n\n'
                f'*Constellations*\n'
                f'https://www.coingecko.com/en/coins/x7101\n'
                f'https://www.coingecko.com/en/coins/x7102\n'
                f'https://www.coingecko.com/en/coins/x7103\n'
                f'https://www.coingecko.com/en/coins/x7104\n'
                f'https://www.coingecko.com/en/coins/x7105\n\n'
                f'*NFTs*\n'
                f'https://www.coingecko.com/en/nft/x7-pioneer\n\n{quote}',
        parse_mode='Markdown')


async def ebb_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    await update.message.reply_photo(
        photo=open(items.ebblogo, 'rb'),
        caption=f'*\'Ebb\'*\n\nThis is the liquidity hub, moving liquidity around the ecosystem.\n\n'
                f'A DexTools bug is showing the hub address rather than the sell address.\n\n{quote}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Liquidity Hub Contract',
                                   url=f'{items.etheraddress}{items.rliqhubca}#internaltx')], ]))


async def tax_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    await update.message.reply_photo(
        photo=open((random.choice(items.logos)), 'rb'),
        caption=f'*X7 Finance Tax Info*\n\n'
                f'X7R: 6%\nX7DAO: 6%\n'
                f'X7101-X7105: 2%\n\n'
                f'*Tax with NFTs*\n'
                f'Liquidity Maxi:\nX7R: 4.50%\n7DAO: 5.10%\nX7101-X7105: 1.00%\n\n'
                f'Ecosystem Maxi:\nX7R: 5.40%\nX7DAO: 5.40%\nX7101-X7105: 1.50%\n\n'
                f'Magister:\nX7R: 4.50%\nX7DAO: 6.00%\nX7101-X7105: 1.50%\n\n{quote}',
        parse_mode='Markdown')


async def swap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_sticker(
        sticker=items.swap,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Xchange', url='https://app.x7.finance/#/swap')],
             [InlineKeyboardButton(text='Feedback', url='https://discord.com/channels/101665704'
                                                        '4553617428/1053206402065256498')], ]))


async def spaces_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    then = variables.spacestime
    now = datetime.now()
    duration = then - now
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    seconds = divmod(minutes[1], 1)
    if duration < timedelta(0):
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'X7 Finance Twitter space\n\nPlease check back for more details'
            f'\n\n{quote}', parse_mode="Markdown")
    else:
        await update.message.reply_sticker(sticker=items.twittersticker)
        await update.message.reply_text(
            text=f'Next X7 Finance Twitter space is:\n\n{then} (UTC)\n\n'
                 f'%d days, %d hours, %d minutes and %d seconds\n\n'
                 f'[Click here]({variables.spaceslink}) to set a reminder!'
                 f'\n\n{quote}'
                 % (days[0], hours[0], minutes[0], seconds[0]), parse_mode="Markdown")


async def roadmap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    await update.message.reply_text(
        f'Devs are making incremental final progress against all ecosystem deliverables, we expect the '
        f'following order of delivery:\n\n'
        f'1. Whitepaper ✅\n'
        f'2. Pioneer NFT & Reward Pool ✅\n'
        f'3. DEX and Leveraged Initial Liquidity:\n'
        f'3.1. X7D token contract ✅\n'
        f'3.2. A gnosis multisig wallet that will be used to manage the X7D token ownership prior to DAO '
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
        f'> Open sourced testing and development tooling\n\n{quote}',
        parse_mode="Markdown")


async def giveaway_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    ext = " ".join(context.args)
    excel = r"addresses.csv"
    df = pd.read_csv(excel)
    addresses = list(df.Holders)
    last5 = [entry[-5:] for entry in addresses]
    then = variables.giveawaytime
    now = datetime.now()
    duration = then - now
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    seconds = divmod(minutes[1], 1)
    if duration < timedelta(0):
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'X7 Finance Giveaway is now closed\n\nPlease check back for more details'
            f'\n\n{quote}', parse_mode="Markdown")
    else:
        if ext == "":
            await update.message.reply_photo(
                photo=open((random.choice(items.logos)), 'rb'),
                caption=f'*{variables.giveawaytitle}*\n\n'
                        f'X7 Finance Giveaway ends:\n\n{then} (UTC)\n\n'
                        f'%d days, %d hours, %d minutes and %d seconds\n\n'
                        f'{variables.giveawayinfo}'
                        f'\n\n{quote}'
                        % (days[0], hours[0], minutes[0], seconds[0]), parse_mode="Markdown")
        if ext == "entries":
            await update.message.reply_photo(
                photo=open((random.choice(items.logos)), 'rb'),
                caption=f'The following addresses are in the draw, weighted by minted amount'
                        f' (last 5 digits only):\n\n{last5}\n\n'
                        f'{quote}',
                parse_mode="Markdown")
        if ext == "run":
            chat_admins = await update.effective_chat.get_administrators()
            if update.effective_user in (admin.user for admin in chat_admins):
                await update.message.reply_photo(
                    photo=open((random.choice(items.logos)), 'rb'),
                    caption=f'*{variables.giveawaytitle}*\n\n'
                            f'The winner of the {variables.giveawaytitle} is:\n\n'
                            f'{random.choice(last5)} (last 5 digits only)\n'
                            f'Trust no one, trust code. Long live Defi!\n\n{quote}',
                    parse_mode="Markdown")
            else:
                await update.message.reply_text(f'{variables.modsonly}')


async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jokeresponse = requests.get(items.jokeapi)
    joke = jokeresponse.json()
    if joke["type"] == "single":  # Print the joke
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'`{joke["joke"]}`',
            parse_mode="Markdown")
    else:
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'`{joke["setup"]}\n\n{joke["delivery"]}`',
            parse_mode="Markdown")


async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currentday = str(datetime.now().day)
    currentmonth = str(datetime.now().month)
    todayurl = f'{items.todayapi}{currentmonth}/{currentday}'
    todayresponse = requests.get(todayurl)
    todaydata = todayresponse.json()
    today = (random.choice(todaydata["data"]["Events"]))
    await update.message.reply_photo(
        photo=open((random.choice(items.logos)), 'rb'),
        caption=f'`On this day in {today["year"]}:\n\n{today["text"]}`',
        parse_mode="Markdown")


async def fg_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    fearresponse = requests.get(items.fearapi)
    feardata = fearresponse.json()
    timestamp = float(feardata["data"][0]["timestamp"])
    localtime = datetime.fromtimestamp(timestamp)
    timestamp = float(feardata["data"][1]["timestamp"])
    localtime1 = datetime.fromtimestamp(timestamp)
    timestamp = float(feardata["data"][2]["timestamp"])
    localtime2 = datetime.fromtimestamp(timestamp)
    timestamp = float(feardata["data"][3]["timestamp"])
    localtime3 = datetime.fromtimestamp(timestamp)
    timestamp = float(feardata["data"][4]["timestamp"])
    localtime4 = datetime.fromtimestamp(timestamp)
    timestamp = float(feardata["data"][5]["timestamp"])
    localtime5 = datetime.fromtimestamp(timestamp)
    timestamp = float(feardata["data"][6]["timestamp"])
    localtime6 = datetime.fromtimestamp(timestamp)
    duration_in_s = float(feardata["data"][0]["time_until_update"])
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    seconds = divmod(minutes[1], 1)
    await update.message.reply_photo(
        photo=open((random.choice(items.logos)), 'rb'),
        caption=f'*Market Fear and Greed Index*\n\n'
                f'{feardata["data"][0]["value"]} - {feardata["data"][0]["value_classification"]} - {localtime} \n\n'
                f'Change:\n'
                f'{feardata["data"][1]["value"]} - {feardata["data"][1]["value_classification"]} - {localtime1}\n'
                f'{feardata["data"][2]["value"]} - {feardata["data"][2]["value_classification"]} - {localtime2}\n'
                f'{feardata["data"][3]["value"]} - {feardata["data"][3]["value_classification"]} - {localtime3}\n'
                f'{feardata["data"][4]["value"]} - {feardata["data"][4]["value_classification"]} - {localtime4}\n'
                f'{feardata["data"][5]["value"]} - {feardata["data"][5]["value_classification"]} - {localtime5}\n'
                f'{feardata["data"][6]["value"]} - {feardata["data"][6]["value_classification"]} - {localtime6}\n\n'
                f'Next Update:\n'
                f'%d hours, %d minutes and %d seconds\n\n{quote}'
                % (hours[0], minutes[0], seconds[0]), parse_mode='Markdown')


async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quote = (random.choice(quotedata))
    text = quote["text"]
    author = quote["author"]
    await update.message.reply_photo(
        photo=open((random.choice(items.logos)), 'rb'),
        caption=f'`"{text}"\n\n-{author}`',
        parse_mode="Markdown")


async def loans_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loantype = " ".join(context.args).lower()
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    if loantype == "":
        await update.message.reply_text(
            '*X7 Finance Loan Terms*\n\n'
            f'Use `/loans ill001 - ill003` for more details on individual loan contrats\n\n'
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
            f'{quote}',
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='X7 Finance Whitepaper', url=f'{items.wplink}')], ]))
    if loantype == "ill001":
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'{items.ill001name}\n\n'
                    f'{items.ill001terms}\n\n',
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text=f'Ethereum', url=f'{items.etheraddress}{items.ill001ca}')],
                 [InlineKeyboardButton(text=f'BSC', url=f'{items.bscaddress}{items.ill001ca}')],
                 [InlineKeyboardButton(text=f'Polygon', url=f'{items.polyaddress}{items.ill001ca}')],
                 [InlineKeyboardButton(text=f'Arbitrum', url=f'{items.arbaddress}{items.ill001ca}')],
                 [InlineKeyboardButton(text=f'Optimism', url=f'{items.optiaddress}{items.ill001ca}')],
                 ]))
    if loantype == "ill002":
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'{items.ill002name}\n\n'
                    f'{items.ill002terms}\n\n',
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text=f'Ethereum', url=f'{items.etheraddress}{items.ill002ca}')],
                 [InlineKeyboardButton(text=f'BSC', url=f'{items.bscaddress}{items.ill002ca}')],
                 [InlineKeyboardButton(text=f'Polygon', url=f'{items.polyaddress}{items.ill002ca}')],
                 [InlineKeyboardButton(text=f'Arbitrum', url=f'{items.arbaddress}{items.ill002ca}')],
                 [InlineKeyboardButton(text=f'Optimism', url=f'{items.optiaddress}{items.ill002ca}')],
                 ]))
    if loantype == "ill003":
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'{items.ill003name}\n\n'
                    f'{items.ill003terms}\n\n',
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text=f'Ethereum', url=f'{items.etheraddress}{items.ill003ca}')],
                 [InlineKeyboardButton(text=f'BSC', url=f'{items.bscaddress}{items.ill003ca}')],
                 [InlineKeyboardButton(text=f'Polygon', url=f'{items.polyaddress}{items.ill003ca}')],
                 [InlineKeyboardButton(text=f'Arbitrum', url=f'{items.arbaddress}{items.ill003ca}')],
                 [InlineKeyboardButton(text=f'Optimism', url=f'{items.optiaddress}{items.ill003ca}')],
                 ]))


async def twitter_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ext = " ".join(context.args)
    auth = tweepy.OAuthHandler(keys.twitterapi, keys.secret)
    auth.set_access_token(keys.access, keys.accesssecret)
    username = '@x7_finance'
    client = tweepy.API(auth)
    tweet = client.user_timeline(screen_name=username, count=1)
    if ext == "":
        await update.message.reply_text(f'Latest X7 Finance Tweet\n\n{tweet[0].text}\n\n'
                                        f'https://twitter.com/X7_Finance/status/{tweet[0].id}\n\n'
                                        f'{random.choice(items.twitterresp)}',
                                        reply_markup=InlineKeyboardMarkup(
                                            [[InlineKeyboardButton(text='X7 Finance Twitter',
                                                                   url='https://twitter.com/x7_finance')], ]))
    if ext == "count":
        chat_admins = await update.effective_chat.get_administrators()
        if update.effective_user in (admin.user for admin in chat_admins):
            client = tweepy.Client(keys.bearer)
            auth = tweepy.OAuthHandler(keys.twitterapi, keys.secret)
            auth.set_access_token(keys.access, keys.accesssecret)
            api = tweepy.API(auth)
            response = client.get_retweeters(variables.tweetid)
            status = api.get_status(variables.tweetid)
            retweet_count = status.retweet_count
            await update.message.reply_photo(
                photo=open((random.choice(items.logos)), 'rb'),
                caption=f'X7 Finance Twitter\n\n{variables.tweetlink}\n\n'
                        f'Retweeted {retweet_count} times, by the following members:')
            await update.message.reply_text('\n'.join(str(p) for p in response.data))
        else:
            await update.message.reply_text(f'{variables.modsonly}')


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
            [[InlineKeyboardButton(text='Discount Application', url=items.dac)],
             [InlineKeyboardButton(text='X7 Lending Discount Contract',
                                   url=f'{items.etheraddress}{items.lendingdisca}#code')], ]))


async def say_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    engine = pyttsx3.init()
    engine.save_to_file(" ".join(context.args), 'media/voicenote.mp3')
    engine.runAndWait()
    await update.message.reply_audio(audio=open('media/voicenote.mp3', 'rb'))


async def announcements_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open((random.choice(items.logos)), 'rb'),
        caption='Check out the link below for the announcement channel',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='X7 Announcement Channel', url="https://t.me/X7announcements")], ]))


async def voting_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    await update.message.reply_text(
        '*Proposals and Voting*\n\nVoting will occur in multiple phases, each of which has either a minimum or maximum'
        ' time phase duration.\n\n*Phase 1: Quorum-seeking*\nX7DAO token holders will be able to stake their tokens as '
        'X7sDAO, a non-transferrable staked version of X7DAO.\n\nA quorum is reached when more than 50% of circulating '
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
        f'must be executed before a new Quorum Seeking phase may commence.\n\n{quote}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url='https://x7.finance')],
            [InlineKeyboardButton(text='X7 Finance Whitepaper', url='https://x7.finance/whitepaper')], ]))


async def snapshot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    await update.message.reply_sticker(sticker=items.chains)
    await update.message.reply_text(
        f'*X7 Finance Snapshot Information*\n\nThe rollout of the Ecosystem Contracts on BNB Smart Chain, Polygon ' 
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
        f'{quote}', parse_mode='Markdown')


async def liquidity_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    if chain == "":
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'To show initial liquidity, Please choose desired chain with \n`/liquidity [chain-name]`'
                    f'\n\n{quote}', parse_mode='Markdown')
    if chain == "bsc":
        liqurl = \
            items.bnbbalanceapi + items.daoliq + ',' + items.x7rliq + ',' + items.consliq + '&tag=latest' \
            + keys.bsc
        response = requests.get(liqurl)
        data = response.json()
        x7dao = float(data["result"][0]["balance"])
        x7daoamount = str(x7dao / 10 ** 18)
        x7r = float(data["result"][1]["balance"])
        x7ramount = str(x7r / 10 ** 18)
        x7cons = float(data["result"][2]["balance"])
        x7consamount = str(x7cons / 10 ** 18)
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        x7daodollar = float(x7daoamount) * float(ethvalue) / 1 ** 18
        x7rdollar = float(x7ramount) * float(ethvalue) / 1 ** 18
        x7consdollar = float(x7consamount) * float(ethvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption='*X7 Finance Initial Liquidity (BSC)*\nUse /liquidity [chian-name] for other chains\n\n'
                    f'X7R:\n{x7ramount} BNB (${"{:0,.0f}".format(x7rdollar)})\n\n'
                    f'X7DAO:\n{x7dao} BNB (${"{:0,.0f}".format(x7daodollar)})\n\n'
                    f'X7100:\n{x7cons} BNB (${"{:0,.0f}".format(x7consdollar)})\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R Initial Liquidity',
                                      url=f'{items.bscaddress}{items.x7rliq}')],
                [InlineKeyboardButton(text='X7DAO Initial Liquidity',
                                      url=f'{items.bscaddress}{items.daoliq}')],
                [InlineKeyboardButton(text='X7100 Initial Liquidity',
                                      url=f'{items.bscaddress}{items.consliq}')],
            ]))
    if chain == "arbitrum":
        liqurl = \
            items.ethbalanceapiarb + items.daoliq + ',' + items.x7rliq + ',' + items.consliq + '&tag=latest' \
            + keys.arb
        response = requests.get(liqurl)
        data = response.json()
        x7dao = float(data["result"][0]["balance"])
        x7daoamount = str(x7dao / 10 ** 18)
        x7r = float(data["result"][1]["balance"])
        x7ramount = str(x7r / 10 ** 18)
        x7cons = float(data["result"][2]["balance"])
        x7rconsamount = str(x7cons / 10 ** 18)
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        x7daodollar = float(x7daoamount) * float(ethvalue) / 1 ** 18
        x7rdollar = float(x7ramount) * float(ethvalue) / 1 ** 18
        x7consdollar = float(x7rconsamount) * float(ethvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption='*X7 Finance Initial Liquidity (ARBITRUM)*\n\n'
                    f'X7R:\n{x7ramount} ETH (${"{:0,.0f}".format(x7rdollar)})\n\n'
                    f'X7DAO:\n{x7dao} ETH (${"{:0,.0f}".format(x7daodollar)})\n\n'
                    f'X7100:\n{x7cons} ETH (${"{:0,.0f}".format(x7consdollar)})\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R Initial Liquidity',
                                      url=f'{items.arbaddress}{items.x7rliq}')],
                [InlineKeyboardButton(text='X7DAO Initial Liquidity',
                                      url=f'{items.arbaddress}{items.daoliq}')],
                [InlineKeyboardButton(text='X7100 Initial Liquidity',
                                      url=f'{items.arbaddress}{items.consliq}')],
            ]))
    if chain == "optimism":
        liqurl = \
            items.ethbalanceapiarb + items.daoliq + ',' + items.x7rliq + ',' + items.consliq + '&tag=latest' \
            + keys.arb
        response = requests.get(liqurl)
        data = response.json()
        x7dao = float(data["result"][0]["balance"])
        x7daoamount = str(x7dao / 10 ** 18)
        x7r = float(data["result"][1]["balance"])
        x7ramount = str(x7r / 10 ** 18)
        x7cons = float(data["result"][2]["balance"])
        x7consamount = str(x7cons / 10 ** 18)
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        x7daodollar = float(x7daoamount) * float(ethvalue) / 1 ** 18
        x7rdollar = float(x7ramount) * float(ethvalue) / 1 ** 18
        x7consdollar = float(x7consamount) * float(ethvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption='*X7 Finance Initial Liquidity (OPTIMISM)*\n\n'
                    f'X7R:\n{x7ramount} ETH (${"{:0,.0f}".format(x7rdollar)})\n\n'
                    f'X7DAO:\n{x7dao} ETH (${"{:0,.0f}".format(x7daodollar)})\n\n'
                    f'X7100:\n{x7cons} ETH (${"{:0,.0f}".format(x7consdollar)})\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R Initial Liquidity',
                                      url=f'{items.optiaddress}{items.x7rliq}')],
                [InlineKeyboardButton(text='X7DAO Initial Liquidity',
                                      url=f'{items.optiaddress}{items.daoliq}')],
                [InlineKeyboardButton(text='X7100 Initial Liquidity',
                                      url=f'{items.optiaddress}{items.consliq}')],
            ]))
    if chain == "polygon":
        liqurl = \
            items.maticbalanceapi + items.daoliq + ',' + items.x7rliq + ',' + items.consliq + '&tag=latest' \
            + keys.poly
        response = requests.get(liqurl)
        data = response.json()
        x7dao = float(data["result"][0]["balance"])
        x7daoamount = str(x7dao / 10 ** 18)
        x7r = float(data["result"][1]["balance"])
        x7ramount = str(x7r / 10 ** 18)
        x7cons = float(data["result"][2]["balance"])
        x7consamount = str(x7cons / 10 ** 18)
        ethurl = items.maticpriceapi + keys.poly
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["maticusd"])
        x7daodollar = float(x7daoamount) * float(ethvalue) / 1 ** 18
        x7rdollar = float(x7ramount) * float(ethvalue) / 1 ** 18
        x7consdollar = float(x7consamount) * float(ethvalue) / 1 ** 18
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption='*X7 Finance Initial Liquidity (POLYGON)*\n\n'
                    f'X7R:\n{x7ramount} MATIC (${"{:0,.0f}".format(x7rdollar)})\n\n'
                    f'X7DAO:\n{x7dao} MATIC (${"{:0,.0f}".format(x7daodollar)})\n\n'
                    f'X7100:\n{x7cons} MATIC (${"{:0,.0f}".format(x7consdollar)})\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='X7R Initial Liquidity',
                                      url=f'{items.polyaddress}{items.x7rliq}')],
                [InlineKeyboardButton(text='X7DAO Initial Liquidity',
                                      url=f'{items.polyaddress}{items.daoliq}')],
                [InlineKeyboardButton(text='X7100 Initial Liquidity',
                                      url=f'{items.polyaddress}{items.consliq}')],
            ]))


# CG COMMANDS
async def x7r_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    chain = " ".join(context.args).lower()
    dollar = chain.startswith("$")
    cg = CoinGeckoAPI()
    cgx7rprice = (cg.get_price(ids='x7r', vs_currencies='usd', include_24hr_change='true',
                               include_24hr_vol='true', include_last_updated_at="true"))
    x7rprice = (cgx7rprice["x7r"]["usd"])
    burnurl = items.tokenbalanceapieth + items.x7rca + '&address=' + items.dead + '&tag=latest' + keys.ether
    burnresponse = requests.get(burnurl)
    burndata = burnresponse.json()
    burndata["result"] = int(burndata["result"][:-18])
    burnresult = round(((burndata["result"] / items.supply) * 100), 6)
    uniurl = items.tokenbalanceapieth + items.x7rca + '&address=' + items.x7rpaireth + '&tag=latest' + keys.ether
    uniresponse = requests.get(uniurl)
    unidata = uniresponse.json()
    unidata["result"] = int(unidata["result"][:-18])
    uniresult = round(((unidata["result"] / items.supply) * 100), 6)
    x7rholdersurl = items.holdersapi + items.x7rca + keys.holders
    x7rholdersresponse = requests.get(x7rholdersurl)
    x7rholdersdata = x7rholdersresponse.json()
    x7rholders = x7rholdersdata["holdersCount"]
    if dollar:
        amount = round(float(chain[1:]) / float(x7rprice), 2)
        await update.message.reply_photo(
            photo=open(items.x7rlogo, 'rb'),
            caption=f'{chain} will currently buy:\n\n{"{:0,.0f}".format(amount)} '
                    f'X7R (ETH) Tokens (Before Tax)\n\n{quote}',
            parse_mode='Markdown')
    if chain.isdigit():
        amount = round(float(chain) * float(x7rprice), 2)
        await update.message.reply_photo(
            photo=open(items.x7rlogo, 'rb'),
            caption=f'{chain} X7R (ETH) Currently Costs:\n\n${"{:0,.0f}".format(amount)}'
                    f'\n\n{quote}',
            parse_mode='Markdown')
    if chain == "":
        await update.message.reply_photo(
            photo=open(items.x7rlogo, 'rb'),
            caption=f'*X7R Info (ETH)*\nUse `/x7r [chain-name]` for other chains\n\n'
                    f'X7R Price: ${cgx7rprice["x7r"]["usd"]}\n'
                    f'24 Hour Change: {round(cgx7rprice["x7r"]["usd_24h_change"], 1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(x7rprice*items.supply)}\n'
                    f'24 Hour Volume: ${"{:0,.0f}".format(cgx7rprice["x7r"]["usd_24h_vol"])}\n'
                    f'Holders: {x7rholders}\n\n'
                    f'X7R Tokens Burned:\n'
                    f'{"{:,}".format(burndata["result"])}\n'
                    f'{burnresult}% of Supply\n\n'
                    f'Uniswap Supply:\n{"{:,}".format(unidata["result"])}\n{round(uniresult, 2)}% of Supply\n\n'
                    f'Contract Address:\n`{items.x7rca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{items.ethertoken}{items.x7rca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolseth}{items.x7rpaireth}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7rca}')], ]))
    if chain == "arb" or chain == "arbitrum":
        await update.message.reply_photo(
            photo=open(items.x7rlogo, 'rb'),
            caption=f'*X7R Info (ARBITRUM)*\nUse `/x7r [chain-name]` for other chains\n\n'
                    f'Contract Address:\n`{items.x7rca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Arbiscan', url=f'{items.arbtoken}{items.x7rca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsarb}{items.x7rpairarb}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7rca}')], ]))
    if chain == "poly" or chain == "polygon":
        await update.message.reply_photo(
            photo=open(items.x7rlogo, 'rb'),
            caption=f'*X7R Info (POLYGON)*\nUse `/x7r [chain-name]` for other chains\n\n'
                    f'Contract Address:\n`{items.x7rca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Polygonscan', url=f'{items.polytoken}{items.x7rca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolspoly}{items.x7rpairpoly}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7rca}')], ]))
    if chain == "bsc":
        await update.message.reply_photo(
            photo=open(items.x7rlogo, 'rb'),
            caption=f'*X7R Info (BSC)*\nUse `/x7r [chain-name]` for other chains\n\n'
                    f'Contract Address:\n`{items.x7rca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Bscscan', url=f'{items.bsctoken}{items.x7rca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsbsc}{items.x7rpairbsc}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7rca}')], ]))
    if chain == "opti" or chain == "optimism":
        await update.message.reply_photo(
            photo=open(items.x7rlogo, 'rb'),
            caption=f'*X7R Info (OPTIMISM)*\nUse `/x7r [chain-name]` for other chains\n\n'
                    f'Contract Address:\n`{items.x7rca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Optimistic.etherscan', url=f'{items.optitoken}{items.x7rca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsopti}{items.x7rpairopti}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7rca}')], ]))


async def x7dao_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    chain = " ".join(context.args).lower()
    dollar = chain.startswith("$")
    cg = CoinGeckoAPI()
    cgx7daoprice = (cg.get_price(ids='x7dao', vs_currencies='usd', include_24hr_change='true',
                                 include_24hr_vol='true', include_last_updated_at="true"))
    daoprice = (cgx7daoprice["x7dao"]["usd"])
    uniurl = items.tokenbalanceapieth + items.x7daoca + '&address=' + items.x7daopaireth + '&tag=latest' + keys.ether
    uniresponse = requests.get(uniurl)
    unidata = uniresponse.json()
    unidata["result"] = int(unidata["result"][:-18])
    uniresult = round(((unidata["result"] / items.supply) * 100), 6)
    x7daoholdersurl = items.holdersapi + items.x7daoca + keys.holders
    x7daoholdersresponse = requests.get(x7daoholdersurl)
    x7daoholdersdata = x7daoholdersresponse.json()
    x7daoholders = x7daoholdersdata["holdersCount"]
    if dollar:
        amount = round(float(chain[1:]) / float(daoprice), 2)
        await update.message.reply_photo(
            photo=open(items.x7daologo, 'rb'),
            caption=f'{chain} Will currently buy:\n\n{"{:0,.0f}".format(amount)}'
                    f' X7DAO (ETH) Tokens (Before Tax)\n\n{quote}',
            parse_mode='Markdown')
    if chain == "500000":
        amount = round(float(chain) * float(daoprice), 2)
        await update.message.reply_photo(
            photo=open(items.x7daologo, 'rb'),
            caption=f'{chain} X7DAO (ETH) Currently Costs:\n\n${"{:0,.0f}".format(amount)}\n\n'
                    f'Holding {chain} X7DAO Tokens'
                    f' will earn you the right to make proposals on X7 DAO dApp\n\n{quote}',
            parse_mode='Markdown')
        return
    if chain.isdigit():
        amount = round(float(chain)*float(daoprice), 2)
        await update.message.reply_photo(
            photo=open(items.x7daologo, 'rb'),
            caption=f'{chain} X7DAO (ETH) Currently Costs:\n\n${amount}\n\n{quote}',
            parse_mode='Markdown')
    if chain == "":
        await update.message.reply_photo(
            photo=open(items.x7daologo, 'rb'),
            caption=f'*X7DAO (ETH) Info*\n\n'
            f'X7DAO Price: ${cgx7daoprice["x7dao"]["usd"]}\n'
            f'24 Hour Change: {round(cgx7daoprice["x7dao"]["usd_24h_change"],1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(daoprice*items.supply)}\n'
            f'24 Hour Volume: ${"{:0,.0f}".format(cgx7daoprice["x7dao"]["usd_24h_vol"])}\n'
            f'Holders: {x7daoholders}\n\n'
            f'Uniswap Supply:\n{"{:,}".format(unidata["result"])}\n{round(uniresult,2)}% of Supply\n\n'
            f'Contract Address:\n`{items.x7daoca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{items.ethertoken}{items.x7daoca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolseth}{items.x7daopaireth}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7daoca}')], ]))
    if chain == "bsc":
        await update.message.reply_photo(
            photo=open(items.x7daologo, 'rb'),
            caption=f'*X7DAO (BSC) Info*\nUse `/x7dao [chain-name]` for other chains\n\n'
            f'Contract Address:\n`{items.x7daoca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='BSCscan', url=f'{items.bsctoken}{items.x7daoca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsbsc}{items.x7daopairbsc}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7daoca}')], ]))
    if chain == "opti" or chain == "optimism":
        await update.message.reply_photo(
            photo=open(items.x7daologo, 'rb'),
            caption=f'*X7DAO (OPTIMISM) Info*\nUse `/x7dao [chain-name]` for other chains\n\n'
            f'Contract Address:\n`{items.x7daoca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Optimistic.etherscan', url=f'{items.optitoken}{items.x7daoca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsopti}{items.x7daopairopti}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7daoca}')], ]))
    if chain == "arb" or chain == "arbitrum":
        await update.message.reply_photo(
            photo=open(items.x7daologo, 'rb'),
            caption=f'*X7DAO (ARBITRUM) Info*\nUse `/x7dao [chain-name]` for other chains\n\n'
            f'Contract Address:\n`{items.x7daoca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Arbiscan', url=f'{items.arbtoken}{items.x7daoca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsarb}{items.x7daopairarb}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7daoca}')], ]))
    if chain == "poly" or chain == "polygon":
        await update.message.reply_photo(
            photo=open(items.x7daologo, 'rb'),
            caption=f'*X7DAO (POLYGON) Info*\nUse `/x7dao [chain-name]` for other chains\n\n'
            f'Contract Address:\n`{items.x7daoca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Polygonscan', url=f'{items.polytoken}{items.x7daoca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolspoly}{items.x7daopairpoly}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7daoca}')], ]))


async def x7101_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    chain = " ".join(context.args).lower()
    dollar = chain.startswith("$")
    cg = CoinGeckoAPI()
    cgx7101price = (cg.get_price(ids='x7101', vs_currencies='usd', include_24hr_change='true',
                                 include_24hr_vol='true', include_last_updated_at="true"))
    x7101price = (cgx7101price["x7101"]["usd"])
    x7101holdersurl = items.holdersapi + items.x7101ca + keys.holders
    x7101holdersresponse = requests.get(x7101holdersurl)
    x7101holdersdata = x7101holdersresponse.json()
    x7101holders = x7101holdersdata["holdersCount"]
    if dollar:
        amount = round(float(chain[1:]) / float(x7101price), 2)
        await update.message.reply_photo(
            photo=open(items.x7101logo, 'rb'),
            caption=f'{chain} Will currently buy:\n\n{"{:0,.0f}".format(amount)}' 
                    f' X7101 (ETH) Tokens (Before Tax)\n\n{quote}', parse_mode='Markdown')
    if chain.isdigit():
        amount = round(float(chain)*float(x7101price), 2)
        await update.message.reply_photo(
            photo=open(items.x7101logo, 'rb'),
            caption=f'{chain} X7101 (ETH) Currently Costs:\n\n${"{:0,.0f}".format(amount)}\n\n{quote}',
            parse_mode='Markdown')
    if chain == "":
        await update.message.reply_photo(
            photo=open(items.x7101logo, 'rb'),
            caption=f'*X7101 (ETH) Info*\nUse `/X7101 [chain-name]` for other chains\n\n'
            f'X7101 Price: ${cgx7101price["x7101"]["usd"]}\n'
            f'24 Hour Change: ${"{:0,.0f}".format(cgx7101price["x7101"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(x7101price*items.supply)}\n'
            f'24 Hour Volume: ${round(cgx7101price["x7101"]["usd_24h_vol"])}\n'
            f'Holders: {x7101holders}\n\n'
            f'*X7101 Contract*\n`{items.x7101ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{items.ethertoken}{items.x7101ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolseth}{items.x7101paireth}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7101ca}')], ]))
    if chain == "arb" or chain == "arbitrum":
        await update.message.reply_photo(
            photo=open(items.x7101logo, 'rb'),
            caption=f'*X7101 (ARBITRUM) Info*\nUse `/X7101 [chain-name]` for other chains\n\n'
            f'*X7101 Contract*\n`{items.x7101ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Arbiscan', url=f'{items.arbtoken}{items.x7101ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsarb}{items.x7101pairarb}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7101ca}')], ]))
    if chain == "poly" or chain == "polygon":
        await update.message.reply_photo(
            photo=open(items.x7101logo, 'rb'),
            caption=f'*X7101 (POLYGON) Info*\nUse `/X7101 [chain-name]` for other chains\n\n'
            f'*X7101 Contract*\n`{items.x7101ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Polyscan', url=f'{items.polytoken}{items.x7101ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolspoly}{items.x7101pairpoly}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7101ca}')], ]))
    if chain == "bsc":
        await update.message.reply_photo(
            photo=open(items.x7101logo, 'rb'),
            caption=f'*X7101 (BSC) Info*\nUse `/X7101 [chain-name]` for other chains\n\n'
            f'*X7101 Contract*\n`{items.x7101ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='BSCscan', url=f'{items.bsctoken}{items.x7101ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsbsc}{items.x7101pairbsc}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7101ca}')], ]))
    if chain == "opti" or chain == "optimism":
        await update.message.reply_photo(
            photo=open(items.x7101logo, 'rb'),
            caption=f'*X7101 (OPTIMISM) Info*\nUse `/X7101 [chain-name]` for other chains\n\n'
            f'*X7101 Contract*\n`{items.x7101ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Optimistic.etherscan', url=f'{items.optitoken}{items.x7101ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsopti}{items.x7101pairopti}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7101ca}')], ]))


async def x7102_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    chain = " ".join(context.args).lower()
    dollar = chain.startswith("$")
    cg = CoinGeckoAPI()
    cgx7102price = (cg.get_price(ids='x7102', vs_currencies='usd', include_24hr_change='true',
                                 include_24hr_vol='true', include_last_updated_at="true"))
    x7102price = (cgx7102price["x7102"]["usd"])
    x7102holdersurl = items.holdersapi + items.x7102ca + keys.holders
    x7102holdersresponse = requests.get(x7102holdersurl)
    x7102holdersdata = x7102holdersresponse.json()
    x7102holders = x7102holdersdata["holdersCount"]
    if dollar:
        amount = round(float(chain[1:]) / float(x7102price), 2)
        await update.message.reply_photo(
            photo=open(items.x7102logo, 'rb'),
            caption=f'{chain} Will currently buy:\n\n{"{:0,.0f}".format(amount)}'
                    f' X7102 (ETH) Tokens (Before Tax)\n\n{quote}',
            parse_mode='Markdown')
    if chain.isdigit():
        amount = round(float(chain) * float(x7102price), 2)
        await update.message.reply_photo(
            photo=open(items.x7102logo, 'rb'),
            caption=f'{chain} X7102 (ETH) Currently Costs:\n\n${"{:0,.0f}".format(amount)}\n\n{quote}',
            parse_mode='Markdown')
    if chain == "":
        await update.message.reply_photo(
            photo=open(items.x7102logo, 'rb'),
            caption=f'*X7102 (ETH) Info*\nUse `/x7102 [chain-name]` for other chains\n\n'
                    f'X7102 Price: ${cgx7102price["x7102"]["usd"]}\n'
                    f'24 Hour Change: {round(cgx7102price["x7102"]["usd_24h_change"], 1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(x7102price*items.supply)}\n'
                    f'24 Hour Volume: ${"{:0,.0f}".format(cgx7102price["x7102"]["usd_24h_vol"])}\n'
                    f'Holders: {x7102holders}\n\n'
                    f'*X7102 Contract*\n`{items.x7102ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{items.ethertoken}{items.x7102ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolseth}{items.x7102paireth}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7102ca}')], ]))
    if chain == "bsc":
        await update.message.reply_photo(
            photo=open(items.x7102logo, 'rb'),
            caption=f'*X7102 (BSC) Info*\nUse `/x7102 [chain-name]` for other chains\n\n'
                    f'*X7102 Contract*\n`{items.x7102ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='BSCscan', url=f'{items.bsctoken}{items.x7102ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsbsc}{items.x7102pairbsc}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7102ca}')], ]))
    if chain == "opti" or chain == "optimism":
        await update.message.reply_photo(
            photo=open(items.x7102logo, 'rb'),
            caption=f'*X7102 (OPTIMISM) Info*\nUse `/x7102 [chain-name]` for other chains\n\n'
                    f'*X7102 Contract*\n`{items.x7102ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Optimistic.etherscan', url=f'{items.optitoken}{items.x7102ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsopti}{items.x7102pairopti}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7102ca}')], ]))
    if chain == "poly" or chain == "polygon":
        await update.message.reply_photo(
            photo=open(items.x7102logo, 'rb'),
            caption=f'*X7102 (POLYGON) Info*\nUse `/x7102 [chain-name]` for other chains\n\n'
                    f'*X7102 Contract*\n`{items.x7102ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Polygonscan', url=f'{items.polytoken}{items.x7102ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolspoly}{items.x7102pairpoly}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7102ca}')], ]))
    if chain == "arb" or chain == "arbitrum":
        await update.message.reply_photo(
            photo=open(items.x7102logo, 'rb'),
            caption=f'*X7102 (ARBITRUM) Info*\nUse `/x7102 [chain-name]` for other chains\n\n'
                    f'*X7102 Contract*\n`{items.x7102ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Arbiscan', url=f'{items.arbtoken}{items.x7102ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsarb}{items.x7102pairarb}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7102ca}')], ]))


async def x7103_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    chain = " ".join(context.args).lower()
    dollar = chain.startswith("$")
    cg = CoinGeckoAPI()
    cgx7103price = (cg.get_price(ids='x7103', vs_currencies='usd', include_24hr_change='true',
                                 include_24hr_vol='true', include_last_updated_at="true"))
    x7103price = (cgx7103price["x7103"]["usd"])
    x7103holdersurl = items.holdersapi + items.x7103ca + keys.holders
    x7103holdersresponse = requests.get(x7103holdersurl)
    x7103holdersdata = x7103holdersresponse.json()
    x7103holders = x7103holdersdata["holdersCount"]
    if dollar:
        amount = round(float(chain[1:]) / float(x7103price), 2)
        await update.message.reply_photo(
            photo=open(items.x7103logo, 'rb'),
            caption=f'{chain} Will currently buy:\n\n{"{:0,.0f}".format(amount)}'
                    f' X7103 (ETH) Tokens (Before Tax)\n\n{quote}',
            parse_mode='Markdown')
    if chain.isdigit():
        amount = round(float(chain) * float(x7103price), 2)
        await update.message.reply_photo(
            photo=open(items.x7103logo, 'rb'),
            caption=f'{chain} X7103 (ETH) Currently Costs:\n\n${"{:0,.0f}".format(amount)}\n\n{quote}',
            parse_mode='Markdown')
    if chain == "":
        await update.message.reply_photo(
            photo=open(items.x7103logo, 'rb'),
            caption=f'*X7103 (ETH) Info*\nUse `/x7103` [chain-name] for other chains\n\n'
                    f'X7103 Price: ${cgx7103price["x7103"]["usd"]}\n'
                    f'24 Hour Change: {round(cgx7103price["x7103"]["usd_24h_change"], 1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(x7103price*items.supply)}\n'
                    f'24 Hour Volume: ${"{:0,.0f}".format(cgx7103price["x7103"]["usd_24h_vol"])}\n'
                    f'Holders: {x7103holders}\n\n'
                    f'*X7103 Contract*\n`{items.x7103ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{items.ethertoken}{items.x7103ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolseth}{items.x7103paireth}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7103ca}')], ]))
    if chain == "bsc":
        await update.message.reply_photo(
            photo=open(items.x7103logo, 'rb'),
            caption=f'*X7103 (BSC) Info*\nUse `/x7103` [chain-name] for other chains\n\n'
                    f'*X7103 Contract*\n`{items.x7103ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='BSCscan', url=f'{items.bsctoken}{items.x7103ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsbsc}{items.x7103pairbsc}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7103ca}')], ]))
    if chain == "polygon" or chain == "poly":
        await update.message.reply_photo(
            photo=open(items.x7103logo, 'rb'),
            caption=f'*X7103 (POLYGON) Info*\nUse `/x7103` [chain-name] for other chains\n\n'
                    f'*X7103 Contract*\n`{items.x7103ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Polygonscan', url=f'{items.polytoken}{items.x7103ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolspoly}{items.x7103pairpoly}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7103ca}')], ]))
    if chain == "arb" or chain == "arbitrum":
        await update.message.reply_photo(
            photo=open(items.x7103logo, 'rb'),
            caption=f'*X7103 (ARBITRUM) Info*\nUse `/x7103` [chain-name] for other chains\n\n'
                    f'*X7103 Contract*\n`{items.x7103ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Arbiscan', url=f'{items.arbtoken}{items.x7103ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsarb}{items.x7103pairarb}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7103ca}')], ]))
    if chain == "opti" or chain == "optimism":
        await update.message.reply_photo(
            photo=open(items.x7103logo, 'rb'),
            caption=f'*X7103 (OPTIMISM) Info*\nUse `/x7103` [chain-name] for other chains\n\n'
                    f'*X7103 Contract*\n`{items.x7103ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Optimistic.etherscan', url=f'{items.optitoken}{items.x7103ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsopti}{items.x7103pairopti}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7103ca}')], ]))


async def x7104_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    chain = " ".join(context.args).lower()
    dollar = chain.startswith("$")
    cg = CoinGeckoAPI()
    cgx7104price = (cg.get_price(ids='x7104', vs_currencies='usd', include_24hr_change='true',
                                 include_24hr_vol='true', include_last_updated_at="true"))
    x7104price = (cgx7104price["x7104"]["usd"])
    x7104holdersurl = items.holdersapi + items.x7104ca + keys.holders
    x7104holdersresponse = requests.get(x7104holdersurl)
    x7104holdersdata = x7104holdersresponse.json()
    x7104holders = x7104holdersdata["holdersCount"]
    if dollar:
        amount = round(float(chain[1:]) / float(x7104price), 2)
        await update.message.reply_photo(
            photo=open(items.x7104logo, 'rb'),
            caption=f'{chain} Will currently buy:\n\n{"{:0,.0f}".format(amount)}'
                    f' X7104 (ETH) Tokens (Before Tax)\n\n{quote}',
            parse_mode='Markdown')
    if chain.isdigit():
        amount = round(float(chain) * float(x7104price), 2)
        await update.message.reply_photo(
            photo=open(items.x7104logo, 'rb'),
            caption=f'{chain} X7104 (ETH) Currently Costs:\n\n${"{:0,.0f}".format(amount)}\n\n{quote}',
            parse_mode='Markdown')
    if chain == "":
        await update.message.reply_photo(
            photo=open(items.x7104logo, 'rb'),
            caption=f'*X7104 (ETH) Info*\n`Use /x7104 [chain-name]` for other chains\n\n'
                    f'X7104 Price: ${cgx7104price["x7104"]["usd"]}\n'
                    f'24 Hour Change: {round(cgx7104price["x7104"]["usd_24h_change"], 1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(x7104price*items.supply)}\n'
                    f'24 Hour Volume: ${"{:0,.0f}".format(cgx7104price["x7104"]["usd_24h_vol"])}\n'
                    f'Holders: {x7104holders}\n\n'
                    f'*X7104 Contract*\n`{items.x7104ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{items.ethertoken}{items.x7104ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolseth}{items.x7104paireth}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7104ca}')], ]))
    if chain == "bsc":
        await update.message.reply_photo(
            photo=open(items.x7104logo, 'rb'),
            caption=f'*X7104 (BSC) Info*\n`Use /x7104 [chain-name]` for other chains\n\n'
                    f'*X7104 Contract*\n`{items.x7104ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='BSCscan', url=f'{items.bsctoken}{items.x7104ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsbsc}{items.x7104pairbsc}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7104ca}')], ]))
    if chain == "poly" or chain == "polygon":
        await update.message.reply_photo(
            photo=open(items.x7104logo, 'rb'),
            caption=f'*X7104 (POLYGON) Info*\n`Use /x7104 [chain-name]` for other chains\n\n'
                    f'*X7104 Contract*\n`{items.x7104ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Polygonscan', url=f'{items.polytoken}{items.x7104ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolspoly}{items.x7104pairpoly}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7104ca}')], ]))
    if chain == "arb" or chain == "arbitrum":
        await update.message.reply_photo(
            photo=open(items.x7104logo, 'rb'),
            caption=f'*X7104 (ARBITRUM) Info*\n`Use /x7104 [chain-name]` for other chains\n\n'
                    f'*X7104 Contract*\n`{items.x7104ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Arbiscan', url=f'{items.arbtoken}{items.x7104ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsarb}{items.x7104pairarb}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7104ca}')], ]))
    if chain == "opti" or chain == "optimism":
        await update.message.reply_photo(
            photo=open(items.x7104logo, 'rb'),
            caption=f'*X7104 (OPTIMISM) Info*\n`Use /x7104 [chain-name]` for other chains\n\n'
                    f'*X7104 Contract*\n`{items.x7104ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Optimistic.etherscan', url=f'{items.optitoken}{items.x7104ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsopti}{items.x7104pairopti}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7104ca}')], ]))


async def x7105_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    chain = " ".join(context.args).lower()
    dollar = chain.startswith("$")
    cg = CoinGeckoAPI()
    cgx7105price = (cg.get_price(ids='x7105', vs_currencies='usd', include_24hr_change='true',
                                 include_24hr_vol='true', include_last_updated_at="true"))
    x7105price = (cgx7105price["x7105"]["usd"])
    x7105holdersurl = items.holdersapi + items.x7105ca + keys.holders
    x7105holdersresponse = requests.get(x7105holdersurl)
    x7105holdersdata = x7105holdersresponse.json()
    x7105holders = x7105holdersdata["holdersCount"]
    if dollar:
        amount = round(float(chain[1:]) / float(x7105price), 2)
        await update.message.reply_photo(
            photo=open(items.x7105logo, 'rb'),
            caption=f'{chain} Will currently buy:\n\n{"{:0,.0f}".format(amount)}'
                    f' X7105 (ETH) Tokens (Before Tax)\n\n{quote}',
            parse_mode='Markdown')
    if chain.isdigit():
        amount = round(float(chain) * float(x7105price), 2)
        await update.message.reply_photo(
            photo=open(items.x7105logo, 'rb'),
            caption=f'{chain} X7105 (ETH) Currently Costs:\n\n${"{:0,.0f}".format(amount)}\n\n{quote}',
            parse_mode='Markdown')
    if chain == "":
        await update.message.reply_photo(
            photo=open(items.x7105logo, 'rb'),
            caption=f'*X7105 (ETH) Info*\nUse `/x7105 [chain-name]` for other chains\n'
                    f'X7105 Price: ${cgx7105price["x7105"]["usd"]}\n'
                    f'24 Hour Change: {round(cgx7105price["x7105"]["usd_24h_change"], 1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(x7105price*items.supply)}\n'
                    f'24 Hour Volume: ${"{:0,.0f}".format(cgx7105price["x7105"]["usd_24h_vol"])}\n'
                    f'Holders: {x7105holders}\n\n'
                    f'*X7105 Contract*\n`{items.x7105ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Etherscan', url=f'{items.ethertoken}{items.x7105ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolseth}{items.x7105paireth}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7105ca}')], ]))
    if chain == "bsc":
        await update.message.reply_photo(
            photo=open(items.x7105logo, 'rb'),
            caption=f'*X7105 (BSC) Info*\nUse `/x7105 [chain-name]` for other chains\n'
                    f'X7105 Price: ${cgx7105price["x7105"]["usd"]}\n'
                    f'24 Hour Change: {round(cgx7105price["x7105"]["usd_24h_change"], 1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(x7105price*items.supply)}\n'
                    f'24 Hour Volume: ${"{:0,.0f}".format(cgx7105price["x7105"]["usd_24h_vol"])}\n'
                    f'Holders: {x7105holders}\n\n'
                    f'*X7105 Contract*\n`{items.x7105ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='BSCscan', url=f'{items.bsctoken}{items.x7105ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsbsc}{items.x7105pairbsc}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7105ca}')], ]))
    if chain == "poly" or chain == "polygon":
        await update.message.reply_photo(
            photo=open(items.x7105logo, 'rb'),
            caption=f'*X7105 (POLYGON) Info*\nUse `/x7105 [chain-name]` for other chains\n'
                    f'X7105 Price: ${cgx7105price["x7105"]["usd"]}\n'
                    f'24 Hour Change: {round(cgx7105price["x7105"]["usd_24h_change"], 1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(x7105price*items.supply)}\n'
                    f'24 Hour Volume: ${"{:0,.0f}".format(cgx7105price["x7105"]["usd_24h_vol"])}\n'
                    f'Holders: {x7105holders}\n\n'
                    f'*X7105 Contract*\n`{items.x7105ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Polygonscan', url=f'{items.polytoken}{items.x7105ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolspoly}{items.x7105pairpoly}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7105ca}')], ]))
    if chain == "arb" or chain == "arbitrum":
        await update.message.reply_photo(
            photo=open(items.x7105logo, 'rb'),
            caption=f'*X7105 (ARBITRUM) Info*\nUse `/x7105 [chain-name]` for other chains\n'
                    f'X7105 Price: ${cgx7105price["x7105"]["usd"]}\n'
                    f'24 Hour Change: {round(cgx7105price["x7105"]["usd_24h_change"], 1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(x7105price*items.supply)}\n'
                    f'24 Hour Volume: ${"{:0,.0f}".format(cgx7105price["x7105"]["usd_24h_vol"])}\n'
                    f'Holders: {x7105holders}\n\n'
                    f'*X7105 Contract*\n`{items.x7105ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Arbiscan', url=f'{items.arbtoken}{items.x7105ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsarb}{items.x7105pairarb}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7105ca}')], ]))
    if chain == "opti" or chain == "optimism":
        await update.message.reply_photo(
            photo=open(items.x7105logo, 'rb'),
            caption=f'*X7105 (OPTIMISM) Info*\nUse `/x7105 [chain-name]` for other chains\n'
                    f'X7105 Price: ${cgx7105price["x7105"]["usd"]}\n'
                    f'24 Hour Change: {round(cgx7105price["x7105"]["usd_24h_change"], 1)}%\n'
                    f'Market Cap:  ${"{:0,.0f}".format(x7105price*items.supply)}\n'
                    f'24 Hour Volume: ${"{:0,.0f}".format(cgx7105price["x7105"]["usd_24h_vol"])}\n'
                    f'Holders: {x7105holders}\n\n'
                    f'*X7105 Contract*\n`{items.x7105ca}`\n\n{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Optimistic.etherscan', url=f'{items.optitoken}{items.x7105ca}')],
                [InlineKeyboardButton(text='Chart', url=f'{items.dextoolsopti}{items.x7105pairopti}')],
                [InlineKeyboardButton(text='Buy', url=f'{items.xchangebuy}{items.x7105ca}')], ]))


async def mcap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    cg = CoinGeckoAPI()
    cgx7rprice = (cg.get_price(ids='x7r', vs_currencies='usd'))
    x7rprice = (cgx7rprice["x7r"]["usd"]) * items.supply
    cgx7daoprice = (cg.get_price(ids='x7dao', vs_currencies='usd'))
    x7daoprice = (cgx7daoprice["x7dao"]["usd"]) * items.supply
    cgx7101price = (cg.get_price(ids='x7101', vs_currencies='usd'))
    x7101price = (cgx7101price["x7101"]["usd"]) * items.supply
    cgx7102price = (cg.get_price(ids='x7102', vs_currencies='usd'))
    x7102price = (cgx7102price["x7102"]["usd"]) * items.supply
    cgx7103price = (cg.get_price(ids='x7103', vs_currencies='usd'))
    x7103price = (cgx7103price["x7103"]["usd"]) * items.supply
    cgx7104price = (cg.get_price(ids='x7104', vs_currencies='usd'))
    x7104price = (cgx7104price["x7104"]["usd"]) * items.supply
    cgx7105price = (cg.get_price(ids='x7105', vs_currencies='usd'))
    x7105price = (cgx7105price["x7105"]["usd"]) * items.supply
    await update.message.reply_photo(
        photo=open((random.choice(items.logos)), 'rb'),
        caption=f'*X7 Finance Market Cap Info (ETH)*\n\n'
                f'X7R:           ${"{:0,.0f}".format(x7rprice)}\n'
                f'X7DAO:      ${"{:0,.0f}".format(x7daoprice)}\n'     
                f'X7101:       ${"{:0,.0f}".format(x7101price)}\n'
                f'X7102:       ${"{:0,.0f}".format(x7102price)}\n'
                f'X7103:       ${"{:0,.0f}".format(x7103price)}\n'
                f'X7104:       ${"{:0,.0f}".format(x7104price)}\n'
                f'X7105:       ${"{:0,.0f}".format(x7105price)}\n\n'
                f'Constellations Combined:\n'
                f'${"{:0,.0f}".format(x7101price+x7102price+x7103price+x7104price+x7105price)}\n\n'
                f'Total Token Marketcap:\n'
                f'${"{:0,.0f}".format(x7rprice+x7daoprice+x7101price+x7102price+x7103price+x7104price+x7105price)}'
                f'\n\n{quote}',
        parse_mode="Markdown")


async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    search = " ".join(context.args).lower()
    basetokenurl = 'https://api.coingecko.com/api/v3/search?query='
    tokenurl = basetokenurl + search
    tokenresponse = requests.get(tokenurl)
    token = tokenresponse.json()
    tokenid = token["coins"][0]["api_symbol"]
    tokenlogo = token["coins"][0]["large"]
    symbol = token["coins"][0]["symbol"]
    cg = CoinGeckoAPI()
    tokenprice = (cg.get_price(ids=tokenid, vs_currencies='usd', include_24hr_change='true',
                               include_24hr_vol='true', include_market_cap="true"))
    cgtogetherprice = (cg.get_price(ids='x7r,x7dao', vs_currencies='usd', include_24hr_change='true',
                                    include_24hr_vol='true'))
    if search == "":
        await update.message.reply_photo(
            photo=open((random.choice(items.logos)), 'rb'),
            caption=f'*X7 Finance Token Price Info (ETH)*\n'
                    f'Use `/x7tokenname` for all other details\n'
                    f'Use `/constellations` for constellations\n\n'
                    f'X7R:      ${cgtogetherprice["x7r"]["usd"]}\n'
                    f'24 Hour Change: {round(cgtogetherprice["x7r"]["usd_24h_change"], 1)}%\n\n'
                    f'X7DAO:  ${cgtogetherprice["x7dao"]["usd"]}\n'
                    f'24 Hour Change: {round(cgtogetherprice["x7dao"]["usd_24h_change"], 0)}%\n\n'
                    f'{quote}',
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='X7R Chart', url=f'{items.dextoolseth}{items.x7rpaireth}')],
                 [InlineKeyboardButton(text='X7DAO Chart', url=f'{items.dextoolseth}{items.x7daopaireth}')], ]))
        return
    if search == "eth":
        quoteresponse = requests.get(items.quoteapi)
        quotedata = quoteresponse.json()
        quoteraw = (random.choice(quotedata))
        quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
        cg = CoinGeckoAPI()
        eth = (cg.get_price(ids='ethereum', vs_currencies='usd', include_24hr_change='true', include_market_cap="true"))
        gasurl = items.ethgasapi + keys.ether
        gasresponse = requests.get(gasurl)
        gasdata = gasresponse.json()
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        await update.message.reply_photo(
            photo=tokenlogo,
            caption=f'*{symbol} price*\n\n'
                    f'Price: ${ethdata["result"]["ethusd"]}\n'
                    f'24 Hour Change: {round(eth["ethereum"]["usd_24h_change"], 1)}%\n'
                    f'Market Cap: ${"{:0,.0f}".format(eth["ethereum"]["usd_market_cap"])}\n\n'
                    f'Gas Prices:\n'
                    f'Low: {gasdata["result"]["SafeGasPrice"]} Gwei\n'
                    f'Average: {gasdata["result"]["ProposeGasPrice"]} Gwei\n'
                    f'High: {gasdata["result"]["FastGasPrice"]} Gwei\n\n'
                    f'{quote}',
            parse_mode='Markdown')
    else:
        await update.message.reply_photo(
            photo=tokenlogo,
            caption=f'*{symbol} price*\n\n'
                    f'Price: ${tokenprice[tokenid]["usd"]}\n'
                    f'24 Hour Change: {round(tokenprice[tokenid]["usd_24h_change"], 1)}%\n'
                    f'Market Cap: ${"{:0,.0f}".format(tokenprice[tokenid]["usd_market_cap"])}\n\n'
                    f'{quote}',
            parse_mode='Markdown')


async def holders_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    x7rholdersurl = items.holdersapi + items.x7rca + keys.holders
    x7rholdersresponse = requests.get(x7rholdersurl)
    x7rholdersdata = x7rholdersresponse.json()
    x7rholders = x7rholdersdata["holdersCount"]
    x7daoholdersurl = items.holdersapi + items.x7daoca + keys.holders
    x7daoholdersresponse = requests.get(x7daoholdersurl)
    x7daoholdersdata = x7daoholdersresponse.json()
    x7daoholders = x7daoholdersdata["holdersCount"]
    await update.message.reply_photo(
        photo=open((random.choice(items.logos)), 'rb'),
        caption=f'*X7 Finance Token Holders (ETH)*\n\n'
                f'X7R Holders: {x7rholders}\n'
                f'X7DAO Holders: {x7daoholders}\n\n'
                f'{quote}',
        parse_mode='Markdown')


async def constellations_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    cg = CoinGeckoAPI()
    cgconstellationprice = (cg.get_price(ids='x7101,x7102,x7103,x7104,x7105', vs_currencies='usd',
                                         include_24hr_change='true'))
    x7101mc = cgconstellationprice["x7101"]["usd"] * items.supply
    x7102mc = cgconstellationprice["x7102"]["usd"] * items.supply
    x7103mc = cgconstellationprice["x7103"]["usd"] * items.supply
    x7104mc = cgconstellationprice["x7104"]["usd"] * items.supply
    x7105mc = cgconstellationprice["x7105"]["usd"] * items.supply
    constmc = x7101mc + x7102mc + x7103mc + x7104mc + x7105mc
    await update.message.reply_video(
        video=open(items.constellationlogo, 'rb'),
        caption=f'*X7 Finance Constellation Token Prices (ETH)*\n\n'
                f'For more info use `/x7tokenname`\n\n'
                f'X7101:      ${cgconstellationprice["x7101"]["usd"]}\n'
                f'24 Hour Change: {round(cgconstellationprice["x7101"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(x7101mc)}\n'
                f'CA: `{items.x7101ca}\n\n`'
                f'X7102:      ${cgconstellationprice["x7102"]["usd"]}\n'
                f'24 Hour Change: {round(cgconstellationprice["x7102"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(x7102mc)}\n'
                f'CA: `{items.x7102ca}\n\n`'
                f'X7103:      ${cgconstellationprice["x7103"]["usd"]}\n'
                f'24 Hour Change: {round(cgconstellationprice["x7103"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(x7103mc)}\n'
                f'CA: `{items.x7103ca}\n\n`'
                f'X7104:      ${cgconstellationprice["x7104"]["usd"]}\n'
                f'24 Hour Change: {round(cgconstellationprice["x7104"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(x7104mc)}\n'
                f'CA: `{items.x7104ca}\n\n`'
                f'X7105:      ${cgconstellationprice["x7105"]["usd"]}\n'
                f'24 Hour Change: {round(cgconstellationprice["x7105"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(x7105mc)}\n'
                f'CA: `{items.x7105ca}\n\n`'
                f'Combined Market Cap: ${"{:0,.0f}".format(constmc)}\n\n'
                f'{quote}', parse_mode="Markdown")


# HARD AUTO MESSAGES
async def wp_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.send_message(
        job.chat_id,
        text=f'*X7 Finance Whitepaper Quote*\n\n{random.choice(items.quotes)}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url=f'{items.website}')],
            [InlineKeyboardButton(text='Whitepaper', url=f'{items.wplink}')], ]))


async def twitter_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    await context.bot.send_sticker(chat_id=job.chat.id, sticker=items.twittersticker)
    await context.bot.send_text(
        chat_id=job.chat_id,
        caption=f'{variables.automessage}\n\n{quote}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Twitter Raid!', url=f'{variables.automessagelink}')], ]))


# AUTO MESSAGES
async def auto_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.send_photo(
        job.chat_id,
        photo=open((random.choice(items.logos)), 'rb'),
        caption=f"{job.data}")


async def show_auto_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_admins = await update.effective_chat.get_administrators()
    job_names = [job.name for job in context.job_queue.jobs()]
    if update.effective_user in (admin.user for admin in chat_admins):
        await update.message.reply_text(f'X7 Finance Auto Messages set:\n\n{job_names}\n\nUse /stop_auto "name" '
                                        f'to stop')
    else:
        await update.message.reply_text(f'{variables.modsonly}')


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
        context.job_queue.run_repeating(auto_message, due*60, chat_id=chat_id, name=name, data=message)
        await update.effective_message.reply_text(f"X7 Finance Auto Message: '{name}'\n\nSet every {due} "
                                                  f"minutes\n\n{message}\n\nby {user}")
    else:
        await update.message.reply_text(f'{variables.modsonly}')


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
        await update.message.reply_text(f'{variables.modsonly}')


# GENERAL MESSAGES
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = str(update.effective_message.text).lower()
    print(f'{update.effective_message.from_user.username} says "{message}" in: '
          f'{update.effective_message.chat.title}')
    if "trust no one, trust code" in message:
        await update.message.reply_text('Long live Defi!')
    if "patience" in message:
        await update.message.reply_text('`Patience is bitter, but its fruit is sweet.\n\n- Aristotle`',
                                        parse_mode="markdown")
    if "https://twitter" in message:
        await update.message.reply_text(f'{random.choice(items.twitterresp)}')
    if message.startswith("gm"):
        await update.message.reply_sticker(sticker=items.gm)
    if "new on chain message" in message:
        await update.message.reply_sticker(sticker=items.chain)
    if "lfg" in message:
        await update.message.reply_sticker(sticker=items.lfg)
    if "goat" in message:
        await update.message.reply_sticker(sticker=items.goat)
    if "smashed" in message:
        await update.message.reply_sticker(sticker=items.smashed)
    if "wagmi" in message:
        await update.message.reply_sticker(sticker=items.wagmi)
    if "slapped" in message:
        await update.message.reply_sticker(sticker=items.slapped)


async def admincommands_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        await update.message.reply_text(
            f'{variables.admincommands}',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Rose Bot Antiflood', url='https://missrose.org/guide/antiflood/')], ]))
    else:
        await update.message.reply_text(f'{variables.modsonly}')


async def everyone_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('@robthebank44 @Adz1doubleD @DallasX7 @CoastCorn @cryptod0c @Phlux '
                                    '@shillingtonlevy @SlumdOg_shillionaire2022 @Zaratustra @WoxieX @CallMeLandlord '
                                    '@gazuga @Gavalars\n\n'
                                    'MODS ASSEMBLE!')


async def error(update, context):
    print(f'Update {update} caused error: {context.error}')


# RUN
if __name__ == '__main__':
    application = ApplicationBuilder().token(keys.token).build()
    job_queue = application.job_queue
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    application.add_error_handler(error)
    application.add_handler(CommandHandler('links', links_command))
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
    application.add_handler(CommandHandler(['price', 'prices'], price_command))
    application.add_handler(CommandHandler(['ecosystem', 'tokens'], ecosystem_command))
    application.add_handler(CommandHandler('media', media_command))
    application.add_handler(CommandHandler('buyevenly', buyevenly_command))
    application.add_handler(CommandHandler(['bot', 'start', 'filters'], bot_command))
    application.add_handler(CommandHandler('channels', channels_command))
    application.add_handler(CommandHandler('pioneer', pioneer_command))
    application.add_handler(CommandHandler(['spaces', 'space'], spaces_command))
    application.add_handler(CommandHandler('burn', burn_command))
    application.add_handler(CommandHandler('search', search_command))
    application.add_handler(CommandHandler(['pool', 'lpool', 'lendingpool'], pool_command))
    application.add_handler(CommandHandler('listings', listings_command))
    application.add_handler(CommandHandler(['tax', 'slippage'], tax_command))
    application.add_handler(CommandHandler(['swap', 'xchange', 'dex'], swap_command))
    application.add_handler(CommandHandler('giveaway', giveaway_command))
    application.add_handler(CommandHandler(['mcap', 'marketcap'], mcap_command))
    application.add_handler(CommandHandler('roadmap', roadmap_command))
    application.add_handler(CommandHandler('joke', joke_command))
    application.add_handler(CommandHandler('quote', quote_command))
    application.add_handler(CommandHandler(['ebb', '6ebb'], ebb_command))
    application.add_handler(CommandHandler('today', today_command))
    application.add_handler(CommandHandler('holders', holders_command))
    application.add_handler(CommandHandler(['fg', 'feargreed'], fg_command))
    application.add_handler(CommandHandler('x7d', x7d_command))
    application.add_handler(CommandHandler(['constellations', 'constellation', 'quints'], constellations_command))
    application.add_handler(CommandHandler(['loans', 'borrow'], loans_command))
    application.add_handler(CommandHandler('start_auto', auto_command))
    application.add_handler(CommandHandler('stop_auto', stop_auto_command))
    application.add_handler(CommandHandler('show_auto', show_auto_command))
    application.add_handler(CommandHandler('twitter', twitter_command))
    application.add_handler(CommandHandler('announcements', announcements_command))
    application.add_handler(CommandHandler('say', say_command))
    application.add_handler(CommandHandler('liquidity', liquidity_command))
    application.add_handler(CommandHandler('everyone', everyone_command))
    application.add_handler(CommandHandler('voting', voting_command))
    application.add_handler(CommandHandler(['snapshot', 'rollout', 'multichain', 'airdrop'], snapshot_command))
    application.add_handler(CommandHandler(['discount', 'dsc', 'dac'], discount_command))
    application.add_handler(CommandHandler(['admin_commands', 'admin', 'admincommands'], admincommands_command))
    application.job_queue.run_repeating(
        wp_message, variables.wptime*60*60,
        chat_id=items.main_id,
        name=str('WP Message'),
        data=variables.wptime*60*60)
    application.job_queue.run_repeating(
        twitter_message, variables.twittertime*60*60,
        chat_id=items.main_id,
        name=str('Twitter Message'),
        data=variables.twittertime*60*60)

    application.run_polling()
