from datetime import datetime, timezone
import pytz
import api
import random

header = ("X7DAO BUY PARTY")

text = ('One buyer that bought X7DAO in increments of 7 (777, 7,777, 77,7777 etc) will be eligble to with 7,777 X7R!\n\n use /giveaway entries to view entries')

# GIVEAWAY            Y   M   D   H   M  S
time_raw = datetime(2023, 6, 23, 4, 00, 00)
update_raw = datetime(2023, 3, 29, 21, 30, 00)

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