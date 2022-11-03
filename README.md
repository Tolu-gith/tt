# Telegram Trader
 CCXT and Telegram integration. Based on python telegram bot v20. 
 Deploy it via docker. 


[![donate](https://img.shields.io/badge/donate-kofi-orange)](https://imgur.com/a/WQiZcW0) 
[![donate](https://badgen.net/badge/github/pages/grey?icon=github)](https://github.com/mraniki/tt)   


[![Docker Pulls](https://img.shields.io/docker/pulls/mraniki/tt?style=plastic)](https://hub.docker.com/r/mraniki/tt)  [![Docker](https://github.com/mraniki/tt/actions/workflows/DockerHub.yml/badge.svg)](https://github.com/mraniki/tt/actions/workflows/DockerHub.yml) [![DockerNightly](https://github.com/mraniki/tt/actions/workflows/DockerHub_Dev.yml/badge.svg)](https://github.com/mraniki/tt/actions/workflows/DockerHub_Dev.yml)



[![telegrambot](https://badgen.net/badge/telegrambot/pages/grey?icon=telegram)](https://t.me/pythontelegrambotchannel)
[![ccxt](https://badgen.net/badge/ccxt/pages/grey?icon=bitcoin)](https://github.com/ccxt/ccxt)

## Install
1) Create a bot via [@BotFather ](https://core.telegram.org/bots/tutorial)
2) Create your API Keys supported by CCXT https://github.com/ccxt/ccxt. Use testnet account for testing this tool.
3) Deploy :
- via docker 
  - dockerhub `docker push mraniki/tt:latest` or nightly,
  - or github `docker pull ghcr.io/mraniki/tt:main` or nightly
- or `git clone https://github.com/mraniki/tt:main`
4) Update bot token / API in the .env file in config (container volume /code/config)
5) Start your container
6) Submit order to the bot as per the following Order format DIRECTION SYMBOL STOPLOSS TAKEPROFIT QUANTITY 
  (e.g. `sell BTCUSDT sl=6000 tp=4500 q=1%`) 
  
        ##ENV Variables:
        TG_TOKEN=""
        TG_USER_ID=""

        #CCXTsupported exchange details
        #CCXTSANDBOX details
        TEST_SANDBOX_MODE="True"
        TEST_SANDBOX_EXCHANGE_NAME="binance"
        TEST_SANDBOX_YOUR_API_KEY=""
        TEST_SANDBOX_YOUR_SECRET=""
        TEST_SANDBOX_ORDERTYPE="MARKET" 

        #PROD APIKEY Exchange1
        EXCHANGE1_NAME="binance"
        EXCHANGE1_YOUR_API_KEY=""
        EXCHANGE1_YOUR_SECRET=""
        EXCHANGE1_ORDERTYPE="MARKET" 

        
 ## Use Case
 - Enable bot in pythontelegram v20 and support exchange raw error via telegram
 - Push your signal manually or from system like trading view webhook to submit order to your ccxt exchange and receive confirmation
 - Disable or Enable trading process via /trading command
 - Query balance via /bal command and view it in formatted way
 - Support testnet and prod exchange via variable 
 - Support % of balance for order

![IMG_2517](https://user-images.githubusercontent.com/8766259/199422978-dc3322d9-164b-42af-9cf2-84c6bc3dae29.jpg)

 ## toDo
- formating/handling of response from exchange (opened position, last closed order)
- support futures and margin
- formating/handling of error from bot and from exchange api
- view opened orders/position via /order command 
- handle 2/multi exchanges
- Merge with MQL4 version which integrate with MT4 exchanges (reach out if you are interested)


