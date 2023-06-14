from telegram.ext import *
from telegram import *
import api
import commands
import logging
import media
import random
import text
import times
import url
from dotenv import load_dotenv
import os
import subprocess
import sys

load_dotenv()

print("Bot Restarted")


async def auto_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_message.from_user.username
    message = str(update.effective_message.text)
    chat_title = update.effective_message.chat.title
    lower_message = message.lower()
    keyword_to_response = {
        "rob the bank": {"text": text.rob, "mode": "Markdown"},
        "delay": {"text": text.delay, "mode": "Markdown"},
        "patience": {"text": text.patience, "mode": "Markdown"},
        "https://twitter": {
            "text": random.choice(text.twitter_replies),
            "mode": None,
        },
        "gm": {"sticker": media.gm},
        "new on chain message": {"sticker": media.chain},
        "lfg": {"sticker": media.lfg},
        "goat": {"sticker": media.goat},
        "smashed": {"sticker": media.smashed},
        "wagmi": {"sticker": media.wagmi},
        "slapped": {"sticker": media.slapped},
    }

    for keyword, response in keyword_to_response.items():
        target_message = message if "https://" in keyword else lower_message

        if keyword in target_message:
            if "text" in response:
                await update.message.reply_text(
                    response["text"], parse_mode=response["mode"]
                )
            elif "sticker" in response:
                await update.message.reply_sticker(sticker=response["sticker"])


async def error(update, context):
    print(f"Update {update} caused error: {context.error}")


async def send_endorsement_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    photo_url = f"{url.pioneers}{api.get_random_pioneer_number()}.png"
    caption_text = f"*X7 Finance Xchange Pairs*\n\n{text.endorse}"
    keyboard_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Xchange Alerts", url=f"{url.tg_alerts}")]]
    )
    await context.bot.send_photo(
        chat_id=job.chat_id,
        photo=photo_url,
        caption=caption_text,
        parse_mode="Markdown",
        reply_markup=keyboard_markup,
    )


async def send_referral_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    photo_url = f"{url.pioneers}{api.get_random_pioneer_number()}.png"
    caption_text = f"*X7 Finance Referral Scheme*\n\n{text.referral}"
    keyboard_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Application", url=f"{url.referral}")]]
    )
    await context.bot.send_photo(
        chat_id=job.chat_id,
        photo=photo_url,
        caption=caption_text,
        parse_mode="Markdown",
        reply_markup=keyboard_markup,
    )


# RUN
if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    job_queue = application.job_queue
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_replies))
    application.add_error_handler(error)
    application.add_handler(CommandHandler("about", commands.about))
    application.add_handler(CommandHandler(["admin_commands", "admin", "admincommands"], commands.admin))
    application.add_handler(CommandHandler("alerts", commands.alerts))
    application.add_handler(CommandHandler(["rollout", "multichain", "airdrop"], commands.airdrop))
    application.add_handler(CommandHandler("alumni", commands.alumni))
    application.add_handler(CommandHandler("announcements", commands.announcements))
    application.add_handler(CommandHandler("ath", commands.ath))
    application.add_handler(CommandHandler(["bot", "start", "filters"], commands.bot))
    application.add_handler(CommandHandler("burn", commands.burn))
    application.add_handler(CommandHandler("buy", commands.buy))
    application.add_handler(CommandHandler(["buybots", "bobby", "buybot"], commands.buy_bots))
    application.add_handler(CommandHandler(["buyevenly", "quintsevenly"], commands.buy_evenly))
    application.add_handler(CommandHandler("channels", commands.channels))
    application.add_handler(CommandHandler(["chart", "charts"], commands.chart))
    application.add_handler(CommandHandler(["constellations", "constellation", "quints"], commands.constellations))
    application.add_handler(CommandHandler(["ca", "contract", "contracts"], commands.contracts))
    application.add_handler(CommandHandler("community", commands.community))
    application.add_handler(CommandHandler("count", commands.count))
    application.add_handler(CommandHandler([f"{times.countdown_command}"], commands.countdown))
    application.add_handler(CommandHandler(["docs", "dashboard"], commands.dashboard))
    application.add_handler(CommandHandler(["deployer", "devs"], commands.deployer))
    application.add_handler(CommandHandler(["discount", "dsc", "dac"], commands.discount))
    application.add_handler(CommandHandler("draw", commands.draw))
    application.add_handler(CommandHandler(["ebb", "buybacks"], commands.ebb))
    application.add_handler(CommandHandler(["ecosystem", "tokens"], commands.ecosystem))
    application.add_handler(CommandHandler("factory", commands.factory))
    application.add_handler(CommandHandler("faq", commands.faq))
    application.add_handler(CommandHandler(["fg", "feargreed"], commands.fg))
    application.add_handler(CommandHandler("gas", commands.gas))
    application.add_handler(CommandHandler("german", commands.german))
    application.add_handler(CommandHandler("giveaway", commands.giveaway_command))
    application.add_handler(CommandHandler("holders", commands.holders))
    application.add_handler(CommandHandler("image", commands.image))
    application.add_handler(CommandHandler("joke", commands.joke))
    application.add_handler(CommandHandler("launch", commands.launch))
    application.add_handler(CommandHandler(["links", "socials"], commands.links))
    application.add_handler(CommandHandler("liquidity", commands.liquidity))
    application.add_handler(CommandHandler("loan", commands.loan))
    application.add_handler(CommandHandler(["loans", "borrow"], commands.loans_command))
    application.add_handler(CommandHandler("magisters", commands.magisters))
    application.add_handler(CommandHandler(["mcap", "marketcap", "cap"], commands.mcap))
    application.add_handler(CommandHandler("media", commands.media_command))
    application.add_handler(CommandHandler("mods", commands.mods))
    application.add_handler(CommandHandler(["nft", "nfts"], commands.nft))
    application.add_handler(CommandHandler(["on_chain", "onchain", "message"], commands.on_chain))
    application.add_handler(CommandHandler(["opensea", "os"], commands.opensea))
    application.add_handler(CommandHandler("pair", commands.pair))
    application.add_handler(CommandHandler("pioneer", commands.pioneer))
    application.add_handler(CommandHandler("proposal", commands.proposal))
    application.add_handler(CommandHandler(["pool", "lpool", "lendingpool"], commands.pool))
    application.add_handler(CommandHandler("potw", commands.potw))
    application.add_handler(CommandHandler(["price", "prices"], commands.price))
    application.add_handler(CommandHandler("question", commands.question))
    application.add_handler(CommandHandler("quote", commands.quote))
    application.add_handler(CommandHandler("raid", commands.raid))
    application.add_handler(CommandHandler(["referral", "refer"], commands.refer))
    application.add_handler(CommandHandler("roadmap", commands.roadmap))
    application.add_handler(CommandHandler("router", commands.router))
    application.add_handler(CommandHandler("say", commands.say))
    application.add_handler(CommandHandler("search", commands.search))
    application.add_handler(CommandHandler("signers", commands.signers))
    application.add_handler(CommandHandler("smart", commands.smart))
    application.add_handler(CommandHandler("snapshot", commands.snapshot))
    application.add_handler(CommandHandler(["spaces", "space"], commands.spaces))
    application.add_handler(CommandHandler("supply", commands.supply))
    application.add_handler(CommandHandler(["beta", "swap", "xchange", "dex"], commands.swap))
    application.add_handler(CommandHandler(["tax", "slippage"], commands.tax_command))
    application.add_handler(CommandHandler("test", commands.test))
    application.add_handler(CommandHandler(["time", "clock"], commands.time))
    application.add_handler(CommandHandler("today", commands.today))
    application.add_handler(CommandHandler("treasury", commands.treasury))
    application.add_handler(CommandHandler("twitter", commands.twitter))
    application.add_handler(CommandHandler("website", commands.website))
    application.add_handler(CommandHandler("x7r", commands.x7r))
    application.add_handler(CommandHandler("x7d", commands.x7d))
    application.add_handler(CommandHandler(["x7dao", "dao"], commands.x7dao))
    application.add_handler(CommandHandler(["x7101", "101"], commands.x7101))
    application.add_handler(CommandHandler(["x7102", "102"], commands.x7102))
    application.add_handler(CommandHandler(["x7103", "103"], commands.x7103))
    application.add_handler(CommandHandler(["x7104", "104"], commands.x7104))
    application.add_handler(CommandHandler(["x7105", "105"], commands.x7105))
    application.add_handler(CommandHandler("voting", commands.voting))
    application.add_handler(CommandHandler("wei", commands.wei))
    application.add_handler(CommandHandler(["website", "site"], commands.website))
    application.add_handler(CommandHandler(["whitepaper", "wp", "wpquote"], commands.wp))
    application.job_queue.run_repeating(
        send_endorsement_message,
        times.endorse_time * 60 * 60,
        chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        name=str("Endorsement Message"),
        data=times.endorse_time * 60 * 60,
    )
    application.job_queue.run_repeating(
        send_referral_message,
        times.referral_time * 60 * 60,
        chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        first=10800,
        name=str("Referral Message"),
        data=times.referral_time * 60 * 60,
    )
    
    scripts = ['bsc.py', 'eth.py','arb.py', 'poly.py', 'opti.py']
    python_executable = sys.executable
    processes = []
    for script in scripts:
        command = [python_executable, script]
        process = subprocess.Popen(command)
        processes.append(process)
    application.run_polling()

    

    
