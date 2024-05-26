# Telegram Bot Signal Copier to MT4 / MT5  💻💸

This Telegram bot allows users to enter trades directly from Telegram and provides detailed risk-to-reward ratios, profit, loss, and calculated lot sizes. Customize settings such as allowed symbols and risk factors through your personalized Python script and environment variables.

The FX Signal Copier Telegram Bot uses the MetaAPI cloud forex trading API for MetaTrader 4 and MetaTrader 5 to connect to your MetaTrader account, providing access to account balance, open positions, and trading permissions. The API supports both live and demo accounts.

Official REST and WebSocket API documentation for MetaAPI: [MetaAPI Docs](https://metaapi.cloud/docs/client/)

This bot is deployed using Render.

# Features 💡
- Copy trades directly from signal providers or personal analysis.
- Retrieve MT4/MT5 account information (Balance, Equity, Open Positions) via MetaAPI.
- Place all six order types from Telegram bot (Market Buy/Sell, Limit Buy/Sell, Buy/Sell Stop).
- Calculate risk-to-reward using stop loss and take profit, displaying size in pips and profit/loss (USD).
- Place up to two take profits, using half position size for each to maintain the risk-to-reward ratio.
- Future feature: Trailing stop loss.

# Demonstration 🎥

![Demo GIF](https://user-images.githubusercontent.com/54332223/180027398-36ddf07b-0f22-4589-9e02-8bd4031dc27b.gif)

# Installation ⚒️

Prerequisites:
- Telegram Account 
- MetaAPI Account: [Sign up here](https://app.metaapi.cloud/sign-up)
- Render Account: [Sign up here](https://dashboard.render.com/)

I have created a YouTube video showcasing how to install and run this bot.

***YouTube Demonstration:*** [Watch Here](https://youtu.be/oMsuAA9N3U4)

**1. Create a Telegram Bot**

Start a conversation with @BotFather on Telegram and create a new bot with a unique name. Save the given API token.

**2. Navigate to Your Render Dashboard**

**3. Create a new web service application**

**4. Scroll down to 'Public Git repository' and paste the following URL:**
```
https://github.com/ehijiele1/Telegram-Signal-Copier-to-MT4-MT5/
```

**5. Set up Render Application**

- Create a unique name for your application, e.g., mt4tradingbot.
- Ensure build command is `pip install -r requirements.txt`.
- Change start command to `python run.py`.
- Select "create web service."

**6. Set Up Application Environment Variables**

After creating your web service, navigate to the environment tab and set the following:

| Key  | Value |
| ------------- | ------------- |
| PYTHON_VERSION | 3.8.2 |
| TOKEN | "INSERT TELEGRAM BOT API TOKEN HERE" |
| APP_URL | "https://[INSERT NAME OF APP HERE].onrender.com/" |
| TELEGRAM_USER | "INSERT TELEGRAM USERNAME HERE" |
| API_KEY | "INSERT META API TOKEN HERE" ([Get Token](https://app.metaapi.cloud/token)) |
| ACCOUNT_ID | "INSERT META API ACCOUNT ID HERE" ([Get Account ID](https://app.metaapi.cloud/accounts)) |
| RISK_FACTOR | "INSERT PERCENTAGE OF RISK PER TRADE HERE IN DECIMAL FORM, e.g., 5% = 0.05" |

**7. Ensure That App Has Been Deployed**

Navigate to the events tab and view logs for deployment. If there are no errors with the environment variables you set, your bot should now be running.

If you need to change any environment variables, navigate to the Render web app and edit the value. After saving, the application will automatically deploy with the new changes.

**Congratulations!** 🥳 You should now be able to open a conversation with your bot on Telegram, calculate trade risk-to-reward, and place trades. For help, send the /help command for instructions and example trades.

# License 📝
&copy; 2024 Ehijie Ibadin. All rights reserved.

Licensed under the MIT license.
