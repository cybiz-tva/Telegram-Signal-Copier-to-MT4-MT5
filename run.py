import os
import csv
import math
import logging
import asyncio
from metaapi_cloud_sdk import MetaApi
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# MetaAPI credentials
API_KEY = os.getenv('API_KEY')
ACCOUNT_ID = os.getenv('ACCOUNT_ID')

# Telegram credentials
TOKEN = os.getenv('TOKEN')
TELEGRAM_USER_ID = int(os.getenv('TELEGRAM_USER_ID'))

# Risk factor
RISK_FACTOR = float(os.getenv('RISK_FACTOR', 0.01))

# Allowed symbols
SYMBOLS = ['AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADCHF', 'CADJPY', 'CHFJPY', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'EURNZD', 'EURUSD', 'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPNZD', 'GBPUSD', 'NOW', 'NZDCAD', 'NZDCHF', 'NZDJPY', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY', 'XAGUSD', 'XAUUSD']

def parse_csv(file_path):
    trades = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            trade = {
                'Symbol': row['instrument'].upper(),
                'Entry': float(row['entry']) if row['entry'].upper() != 'NOW' else 'NOW',
                'StopLoss': float(row['sl']),
                'TP': [float(row['tp1'])],
                'OrderType': 'Buy' if float(row['entry']) < float(row['tp1']) else 'Sell',
                'RiskFactor': RISK_FACTOR
            }
            if 'tp2' in row and row['tp2']:
                trade['TP'].append(float(row['tp2']))
            trades.append(trade)
    return trades

async def execute_trades_from_csv(api, account_id, trades, context):
    try:
        account = await api.metatrader_account_api.get_account(account_id)
        if account.state not in ['DEPLOYED', 'DEPLOYING']:
            await account.deploy()
        await account.wait_connected()
        
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()

        account_info = await connection.get_account_information()
        balance = account_info['balance']

        for trade in trades:
            if trade['Symbol'] not in SYMBOLS:
                context.bot.send_message(TELEGRAM_USER_ID, f"Invalid symbol: {trade['Symbol']}")
                continue
            
            if trade['Entry'] == 'NOW':
                price = await connection.get_symbol_price(trade['Symbol'])
                trade['Entry'] = float(price['bid']) if trade['OrderType'] == 'Buy' else float(price['ask'])
            
            stop_loss_pips = abs(trade['StopLoss'] - trade['Entry']) / (0.01 if len(trade['Symbol']) >= 6 else 0.0001)
            trade['PositionSize'] = math.floor(((balance * trade['RiskFactor']) / stop_loss_pips) / 10 * 100) / 100

            for tp in trade['TP']:
                if trade['OrderType'] == 'Buy':
                    await connection.create_market_buy_order(trade['Symbol'], trade['PositionSize'], trade['StopLoss'], tp)
                elif trade['OrderType'] == 'Sell':
                    await connection.create_market_sell_order(trade['Symbol'], trade['PositionSize'], trade['StopLoss'], tp)

            context.bot.send_message(TELEGRAM_USER_ID, f"Executed trade for {trade['Symbol']} at {trade['Entry']} with SL {trade['StopLoss']} and TP {trade['TP']}")

    except Exception as e:
        logger.error(f"Error executing trades: {e}")
        context.bot.send_message(TELEGRAM_USER_ID, f"Error executing trades: {e}")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hi! Use /upload to upload a CSV file with trade signals.")

def upload(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Please upload the CSV file.")

def handle_csv(update: Update, context: CallbackContext) -> None:
    file = context.bot.get_file(update.message.document)
    file_path = "trades.csv"
    file.download(file_path)
    trades = parse_csv(file_path)
    
    api = MetaApi(API_KEY)
    asyncio.run(execute_trades_from_csv(api, ACCOUNT_ID, trades, context))

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("upload", upload))
    dp.add_handler(MessageHandler(Filters.document.mime_type("text/csv"), handle_csv))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
