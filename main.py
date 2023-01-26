import json
import requests
from telegram import Bot
from telegram.ext import ApplicationBuilder, Updater, CommandHandler, MessageHandler
import telegram.ext.filters as Filters
from datetime import datetime
from itertools import islice
import asyncio

# import logging

# logging.basicConfig(level=logging.ERROR,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Telegram bot token
token='5409758372:AAGCPq3_S0oCLIwS8oCVME5DBJ7ThZCIH68'
# bot = Bot(token)


def sample_responses(input_text):
    address = str(input_text).lower()
    print(details(address))
    return details(address)

def start_command(update, context):
    update.message.reply_text('Type in your wallet address to get started!')

def help_command(update, context):
    help_text = "This bot sends you the recent 10 BSC tokens received in your wallet"
    update.message.reply_text(help_text)


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = sample_responses(text)
    update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} caused error {context.error}")


async def main():
    # async with ApplicationBuilder().token(token).build() as app:
    # updater = Updater(token, update_queue=Queue())
    try:
        app = ApplicationBuilder().token(token).build()
        await app.initialize()

        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("help", help_command))

        app.add_handler(MessageHandler(Filters.Text, handle_message))

        app.add_error_handler(error)

        # updater.start_polling()
        # updater.idle()
        await app.run_polling()
        await app.start()
    finally:
        await app.shutdown()

def details(address):
    API_KEY = "D3XPR53MHTF8YI3W71YHI923V9MC4HW4XM"

    url = f'https://api.bscscan.com/api?module=account&action=tokentx&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={API_KEY}'
    response = requests.get(url)
    data = json.loads(response.text)
    all_details = ""
    # Check for new transactions
    for tx in islice(data['result'], 10):
        if tx['to'] == address:
            BASE_CONVERT_RATE = 10 ** 18
            value = int(tx['value'])  / BASE_CONVERT_RATE
            token_name = tx['tokenName']
            timestamp = int(tx['timeStamp'])

            # convert timestamp to datetime object
            date_time = datetime.fromtimestamp(timestamp)

            # print the date
            token_date = str(date_time.strftime("%Y-%m-%d %H:%M:%S"))

            details = f'Token: {token_name}\nValue: {value}\nDate received: {token_date}'
            all_details += "Transaction details!\n" + details + "\n\n"
    # Send message to Telegram user
    # bot.send_message(chat_id=chat_id, text=all_details)
    return all_details
if __name__ == '__main__':
    print("Bot started...")
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
