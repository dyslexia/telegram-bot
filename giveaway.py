from datetime import datetime, timezone
import pytz
import api
import random

header = ("BUY THE X”7s”R CONTEST!!")

text = ('Buy X7R in any of the following increments of 7 to enter:\n\n🔵 777 = 1 entry\n'
'🟣 7,777 = 10 entries\n'
'🟤 77,777 = 30 entries\n' 
'🚨 MUST buy on Xchange:\n\n'
'https://app.x7.finance/#/swap\n\n'
'3 winners will be randomly drawn on our “Wheel of Misfortune” app 🎉\n\n'
'🥇1st prize = Ecosystem Maxi NFT (currently .33 ETH/$620)\n'
'🥈 2nd prize = 10,000 X7R (currently $250)\n'
'🥉3rd prize = 5,000 X7R (currently $125)\n\n'
'📌Content ends 0:00 EST, Sunday July 23rd!\n\n'
'X7R: `0x70008F18Fc58928dcE982b0A69C2c21ff80Dca54`')

# GIVEAWAY            Y   M   D   H   M  S
time_raw = datetime(2023, 7, 24, 5, 00, 00)
update_raw = datetime(2023, 7, 21, 21, 30, 00)

time = time_raw.astimezone(pytz.utc)
update = update_raw.astimezone(pytz.utc)

def calculate_duration(giveaway_time):
    now = datetime.now(timezone.utc)
    duration = giveaway_time - now
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    return int(days[0]), int(hours[0]), int(minutes[0])

def last5():
    filename = 'raffle.csv'
    column_index = 0
    selected_column = api.read_csv_column(filename, column_index)
    list = [entry[-5:] for entry in selected_column]
    return list


def countdown():                 
    countdown_days, countdown_hours, countdown_minutes = calculate_duration(time)
    return f'{header} ends:\n\n{time.strftime("%A %B %d %Y %I:%M %p")} (UTC)\n\n{countdown_days} days, {countdown_hours} hours and {countdown_minutes} minutes'

def entries():
    return f"Entries for the {header} are: (last 5 digits only):\n\n{last5()}"


def updated():
    return f'{update.strftime("%A %B %d %Y %I:%M %p")} (UTC)'


def run():
    return f"The winner of the {header} is: (last 5 digits only)\n\n{random.choice(last5())}\n\nTrust no one, trust code. Long live Defi!"