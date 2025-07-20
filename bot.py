import pytesseract
from PIL import Image
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import time
import os

TELEGRAM_BOT_TOKEN = '7699253029:AAG33ai0B-wL_-rzgSvlKW1nwOanVOrRMhU'

def start(update: Update, context: CallbackContext):
    update.message.reply_text("📸 Send me a screenshot of your Brawl Stars account, and I’ll generate a sales title instantly!")

def extract_text(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

def parse_data(text):
    lines = text.lower().splitlines()
    data = {
        'trophies': None,
        'brawlers': None,
        'hypercharge': None,
        'maxed': None,
        'skins': []
    }

    for line in lines:
        if 'troph' in line and not data['trophies']:
            data['trophies'] = ''.join(filter(str.isdigit, line))
        elif 'brawler' in line and not data['brawlers']:
            data['brawlers'] = ''.join(filter(str.isdigit, line))
        elif 'hyper' in line and not data['hypercharge']:
            data['hypercharge'] = ''.join(filter(str.isdigit, line))
        elif 'max' in line and not data['maxed']:
            data['maxed'] = ''.join(filter(str.isdigit, line))
        elif 'kraken' in line or 'cuddly' in line or 'shadow' in line:
            data['skins'].append(line.strip())

    return data

def generate_title(data):
    trophies = data.get('trophies') or '50K+'
    brawlers = data.get('brawlers') or '88'
    hyper = data.get('hypercharge') or '11'
    maxed = data.get('maxed') or '27'
    skins = ', '.join(data.get('skins')) or 'Kraken Surge, Cuddly Kit'

    return (
        f"🔥 STACKED BRAWL STARS ACCOUNT ▣ {trophies} TROPHIES\n"
        f"🎭 RARE SKINS: {skins}\n"
        f"✨ {brawlers} BRAWLERS ▣ {hyper} HYPERCHARGE ▣ {maxed} MAXED POWER 11\n"
        f"❤️‍🔥 FAST DELIVERY ▣ CHEAPEST DEAL ON MARKET 🤑"
    )

def handle_photo(update: Update, context: CallbackContext):
    start_time = time.time()

    photo = update.message.photo[-1].get_file()
    image_path = f"{photo.file_id}.jpg"
    photo.download(image_path)

    text = extract_text(image_path)
    data = parse_data(text)
    title = generate_title(data)

    duration = round(time.time() - start_time, 2)

    update.message.reply_text(f"{title}\n\n⏱️ Title generated in {duration} seconds")

    os.remove(image_path)

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
