from telegram.ext import *
from telegram import *
import api
import ca
import commands
import keys
import logging
import media
import random
import text
import times
import url

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
print('Bot Restarted')

async def auto_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = str(update.effective_message.text).lower()
    print(f'{update.effective_message.from_user.username} says "{message}" in: '
          f'{update.effective_message.chat.title}')
    if "@devs" in message:
        result = round(((api.get_token_balance(ca.dead, ca.x7r, "eth") / ca.supply) * 100), 6)
        await update.message.reply_text(f'Please send 1000 X7R to the burn wallet:\n\n'
                                        f'`0x000000000000000000000000000000000000dEaD`\n\nThank you for your '
                                        f'contribution {update.message.from_user.username}\n\n'
                                        f'X7R (ETH) Tokens Burned:\n'
                                        f'{"{:,}".format(api.get_token_balance(ca.dead, ca.x7r, "eth"))}\n'
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

async def error(update, context):
    print(f'Update {update} caused error: {context.error}')

async def wp_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.send_message(
        job.chat_id,
        text=f'*X7 Finance Whitepaper Quote*\n\n{random.choice(text.quotes)}',
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Website', url=f'{url.website}')],
            [InlineKeyboardButton(text='Whitepaper', url=f'{url.wp_link}')], ]))

async def raid_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
#    username = random.choice(text.usernamelist)
    username = '@x7_finance'
    tweet = api.twitter.user_timeline(screen_name=username, count=1, include_rts="false", exclude_replies="true")
    await context.bot.send_sticker(job.chat_id, sticker=media.twitter_sticker)
    await context.bot.send_message(
        job.chat_id,
        f'🚨🚨 Raid {username} 🚨🚨\n\n'
        f'{tweet[0].text}\n\n'
        f'https://twitter.com/intent/'
        f'tweet?text=@X7_Finance&hashtags=X7Finance%2CLongLiveDefi&in_reply_to={tweet[0].id}\n\n'
        f'{random.choice(text.twitter_replies)}', disable_web_page_preview=True)

async def alert_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.send_photo(
        job.chat_id,
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f'*X7 Finance*\n\n{random.choice(text.quotes)}\n\n{api.get_quote()}\n\n'
                f'🏠 [X7.Finance](http://x7.finance) ┃ 🔗 [X7finance.org](http://x7finance.org)\n'
                f'💬 [Telegram](t.me/x7m105portal)   ┃ 💰 [Donate]({url.ether_address}'
                f'0x89eE55b32B0E463C27508669fcFCf43D18e9833E)',
        parse_mode='Markdown')

async def auto_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.send_photo(
        job.chat_id,
        photo=open((random.choice(media.logos)), 'rb'),
        caption=f"{job.data}")

# RUN
if __name__ == '__main__':
    application = ApplicationBuilder().token(keys.token).build()
    job_queue = application.job_queue
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_replies))
    application.add_error_handler(error)
    application.add_handler(CommandHandler('about', commands.about))
    application.add_handler(CommandHandler(['admin_commands', 'admin', 'admincommands'], commands.admin))
    application.add_handler(CommandHandler('alerts', commands.alerts))
    application.add_handler(CommandHandler(['rollout', 'multichain', 'airdrop'], commands.airdrop))
    application.add_handler(CommandHandler('alumni', commands.alumni))
    application.add_handler(CommandHandler('announcements', commands.announcements))
    application.add_handler(CommandHandler('ath', commands.ath))
    application.add_handler(CommandHandler(['bot', 'start', 'filters'], commands.bot))
    application.add_handler(CommandHandler('burn', commands.burn))
    application.add_handler(CommandHandler('buy', commands.buy))
    application.add_handler(CommandHandler(['buybots', 'bobby', 'buybot'], commands.buy_bots))
    application.add_handler(CommandHandler(['buyevenly', 'quintsevenly'], commands.buy_evenly))
    application.add_handler(CommandHandler('channels', commands.channels))
    application.add_handler(CommandHandler(['chart', 'charts'], commands.chart))
    application.add_handler(CommandHandler(['constellations', 'constellation', 'quints'], commands.constellations))
    application.add_handler(CommandHandler(['ca', 'contract', 'contracts'], commands.contracts))
    application.add_handler(CommandHandler('community', commands.community))
    application.add_handler(CommandHandler('count', commands.count))
    application.add_handler(CommandHandler([f'{times.countdown_command}'], commands.countdown))
    application.add_handler(CommandHandler(['docs', 'dashboard'], commands.dashboard))
    application.add_handler(CommandHandler(['deployer', 'devs'], commands.deployer))
    application.add_handler(CommandHandler(['discount', 'dsc', 'dac'], commands.discount))
    application.add_handler(CommandHandler('draw', commands.draw))
    application.add_handler(CommandHandler(['ebb', 'buybacks'], commands.ebb))
    application.add_handler(CommandHandler(['ecosystem', 'tokens'], commands.ecosystem))
    application.add_handler(CommandHandler('factory', commands.factory))
    application.add_handler(CommandHandler('faq', commands.faq))
    application.add_handler(CommandHandler(['fg', 'feargreed'], commands.fg))
    application.add_handler(CommandHandler('gas', commands.gas))
    application.add_handler(CommandHandler('german', commands.german))
    application.add_handler(CommandHandler('giveaway', commands.giveaway))
    application.add_handler(CommandHandler('holders', commands.holders))
    application.add_handler(CommandHandler('image', commands.image))
    application.add_handler(CommandHandler('joke', commands.joke))
    application.add_handler(CommandHandler('launch', commands.launch))
    application.add_handler(CommandHandler(['links', 'socials'], commands.links))
    application.add_handler(CommandHandler('liquidity', commands.liquidity))
    application.add_handler(CommandHandler('loan', commands.loan))
    application.add_handler(CommandHandler(['loans', 'borrow'], commands.loans_command))
    application.add_handler(CommandHandler('magisters', commands.magisters))
    application.add_handler(CommandHandler(['mcap', 'marketcap', 'cap'], commands.mcap))
    application.add_handler(CommandHandler('media', commands.media_command))
    application.add_handler(CommandHandler('mods', commands.mods))
    application.add_handler(CommandHandler(['nft', 'nfts'], commands.nft))
    application.add_handler(CommandHandler(['on_chain', 'onchain', 'message'], commands.on_chain))
    application.add_handler(CommandHandler(['opensea',  'os'], commands.opensea))
    application.add_handler(CommandHandler('pair', commands.pair))
    application.add_handler(CommandHandler('pioneer', commands.pioneer))
    application.add_handler(CommandHandler('proposal', commands.proposal))
    application.add_handler(CommandHandler(['pool', 'lpool', 'lendingpool'], commands.pool))
    application.add_handler(CommandHandler('potw', commands.potw))
    application.add_handler(CommandHandler(['price', 'prices'], commands.price))
    application.add_handler(CommandHandler('question', commands.question))
    application.add_handler(CommandHandler('quote', commands.quote))
    application.add_handler(CommandHandler('raid', commands.raid))
    application.add_handler(CommandHandler(['referral', 'refer'], commands.refer))
    application.add_handler(CommandHandler('roadmap', commands.roadmap))
    application.add_handler(CommandHandler('router', commands.router))
    application.add_handler(CommandHandler('say', commands.say))
    application.add_handler(CommandHandler('search', commands.search))
    application.add_handler(CommandHandler('show_auto', commands.show_auto))
    application.add_handler(CommandHandler('signers', commands.signers))
    application.add_handler(CommandHandler('smart', commands.smart))
    application.add_handler(CommandHandler('snapshot', commands.snapshot))
    application.add_handler(CommandHandler(['spaces', 'space'], commands.spaces))
    application.add_handler(CommandHandler('supply', commands.supply))
    application.add_handler(CommandHandler('start_auto', commands.start_auto))
    application.add_handler(CommandHandler('stop_auto', commands.stop_auto))
    application.add_handler(CommandHandler(['swap', 'xchange', 'dex'], commands.swap))
    application.add_handler(CommandHandler(['tax', 'slippage'], commands.tax_command))
    application.add_handler(CommandHandler('test', commands.test))
    application.add_handler(CommandHandler(['time', 'clock'], commands.time))
    application.add_handler(CommandHandler('today', commands.today))
    application.add_handler(CommandHandler('token', commands.token))
    application.add_handler(CommandHandler('treasury', commands.treasury))
    application.add_handler(CommandHandler('twitter', commands.twitter))
    application.add_handler(CommandHandler('volume', commands.volume))
    application.add_handler(CommandHandler('x7r', commands.x7r))
    application.add_handler(CommandHandler('x7d', commands.x7d))
    application.add_handler(CommandHandler(['x7dao', 'dao'], commands.x7dao))
    application.add_handler(CommandHandler(['x7101', '101'], commands.x7101))
    application.add_handler(CommandHandler(['x7102', '102'], commands.x7102))
    application.add_handler(CommandHandler(['x7103', '103'], commands.x7103))
    application.add_handler(CommandHandler(['x7104', '104'], commands.x7104))
    application.add_handler(CommandHandler(['x7105', '105'], commands.x7105))
    application.add_handler(CommandHandler('voting', commands.voting))
    application.add_handler(CommandHandler('wei', commands.wei))
    application.add_handler(CommandHandler(['website', 'site'], commands.website))
    application.add_handler(CommandHandler(['whitepaper', 'wp', 'wpquote'], commands.wp))
    application.job_queue.run_repeating(
        wp_message, times.wp_time * 60 * 60,
        chat_id=keys.main_id,
        name=str('WP Message'),
        data=times.wp_time * 60 * 60)
    application.job_queue.run_repeating(
        alert_message, times.alert_time * 60 * 60,
        chat_id=keys.alerts_id,
        name=str('Alert Message'),
        data=times.alert_time * 60 * 60)
    application.job_queue.run_repeating(
        raid_message, times.raid_time * 60 * 60,
        chat_id=keys.main_id,
        first=1800,
        name=str('Raid Message'),
        data=times.raid_time * 60 * 60)
    application.run_polling()
