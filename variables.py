from datetime import datetime
# VARIABLES

# AUTO TIMES HOURS
wptime = 1
twittertime = 6
airdroptime = 1

# AUTO MESSAGE
automessage = "**X7 Finance Twitter Raid**\n\nClick the link below and like and RT everything you see!"
automessagelink = "https://twitter.com/search?q=%23x7finance&src=typed_query"

# SPACES                Y   M   D   H   M  S
spacestime = datetime(2023, 3, 1, 23, 00, 00)
spaceslink = "https://twitter.com/i/spaces/1MYxNgLLvdXKw?s=20"


# GIVEAWAY               Y   M   D   H   M  S
giveawaytime = datetime(2023, 3, 10, 20, 30, 00)
snapshot1 = datetime(2023, 2, 9, 20, 30, 00)
snapshot2 = datetime(2023, 3, 9, 20, 30, 00)
giveawaytitle = "X7 Finance 20,000 X7R Giveaway!"
giveawayinfo = "For every 0.1 X7D minted,1 entry into the draw was generated!\n\n" \
               f"A Snapshot of minters was taken at {snapshot1} (UTC) and a second will be at {snapshot2} (UTC)\n\n" \
               f"The Diamond hands that have held for the entire duration will be in the draw! The more minted," \
               " the better the chance!\n\n" \
               "Any withdrawals will be deducted from the entries at the second snapshot.\n\n" \
               f"The draw will be made at {giveawaytime} (UTC)\n\nCredit: Defi Dipper!\n\nUse `/giveaway entries`" \
               f" to see last 5 of every address in the draw"

# TWITTER
tweetid = 1625541579074158607
tweetlink = "https://twitter.com/X7_Finance/status/1625541579074158607?s=20&t=h25BT4ivN34G70MIZCrHVQ"

# COMMANDS
modsonly = "You do not have permission from the X7 Mods to do this. #trustnoone"

commands = f'Available @X7Finance_bot Commands:\n\n/about - Welcome to X7 Finance\n' \
           f'/ecosystem - Token Overview\n' \
           f'/swap - Xchange Info\n' \
           f'/roadmap - wen?\n' \
           f'/links - Official Links\n' \
           f'/website - Official Website\n' \
           f'/channels - List of X7 Finance TG Channels\n' \
           f'/discount - Discount Launch NFT Info\n' \
           f'/contract - Token Contract Addresses\n' \
           f'/chart - Chart Links\n' \
           f'/price - /price [anytoken] - Price Info\n' \
           f'/buy - Buy Links\n' \
           f'/wp - Whitepaper Links\n' \
           f'/x7r - X7R Info\n' \
           f'/x7dao - X7DAO Info\n' \
           f'/x7101 - X7101 Info\n' \
           f'/x7102 - X7102 Info\n' \
           f'/x7103 - X7103 Info\n' \
           f'/x7104 - X7104 Info\n' \
           f'/x7105 - X7105 Info\n' \
           f'/constellations - X7 Constellation Info\n' \
           f'/x7d - X7Deposit Info\n' \
           f'/buyevenly - A Guide to buying constellation series evenly\n' \
           f'/tax - Token Tax Info\n' \
           f'/ebb - DexTools help\n' \
           f'/mcap - Market Cap Info\n' \
           f'/spaces - Twitter Space Info\n' \
           f'/listings - Token Listing Info\n' \
           f'/nft - NFT Info\n' \
           f'/opensea - Opensea Links\n' \
           f'/pioneer - Pioneer NFT Details (can be used as /pioneer #)\n' \
           f'/treasury - Treasury Info\n' \
           f'/pool - Lending Pool Info\n' \
           f'/loans - Loan Term Info\n' \
           f'/burn - Burnt Tokens Info\n' \
           f'/holders - Token Holder Info\n' \
           f'/smart - Smart Contract Info\n' \
           f'/voting - DAO Voting Info\n' \
           f'/media - TG Stickers and Emojis\n' \
           f'/giveaway - Current Giveaway Info\n' \
           f'/search - Search the web\n\n'

admincommands = 'To be run in main chat\n\n' \
                '/settings - Open the setting menu\n' \
                '/setup - Setup the portal\n' \
                '/difficulty - Set the CAPTCHA difficulty\n' \
                '/antiflood - (Dis)Enable antiflood mode\n' \
                '/lock all - mutes chat\n' \
                '/unlock all - unmute chat\n' \
                '/start_auto [name_oneword] [time_in_minutes] [message] \n' \
                '/stop_auto [name]\n' \
                '/view_auto\n\n' \
                f'wp quote will trigger every {wptime} hour\n' \
                f'twitter "RT everything" message will trigger every {twittertime}'
