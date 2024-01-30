# Develoment Note

## `Constants.py`

## Stage 1 - Preparation

### Connect to DYDX

`func_connections.py` - `connect_dydx()`

### Place Maket Order

`func_private.py` - `place_market_order()`

- Get Position Id

- Get expiraion time

- Place an order

### Abort All Open Orders & Positions

For testing the code repetitively

`func_private.py` - `abort_all_positions()`

- Cancel all orders

- Cancel all positions

  - Get "markets" to access "tickSize" to find out correct decimals lateron

  - Get all open positions

  - Loop through each position

    - Determine the crypto (market), side, worst price, decimals (`func_utils.py` - `format_number()`)

    - Place order to close: `place_market_order()`

    - Append the result

## Stage 2 - Find Co-integration

Trigger by `FIND_COINTEGRATED` in `constants.py`
Stage 2 is only done once a day.

### Construct Market Prices

Build a table with all of the prices across all the cryptos

Functions:

- Get ISO Times

  We can get market candles at max. 100 on time, but we will need 300 or 400 in total.
  So we will make separate requests with different "timeframes" and join them together.

  `get_ISO_times()` in `func_utils.py`

- Get Historical Candles

  `get_candles_historical()` in `func_public.py`

- Construct Market Prices

  `construct_market_prices()` in `func_public.py`

### Store Cointegrated Pairs

- Write Cointegration Functions in `func_cointegration.py`

  - `calculate_half_lif()`

  - `calculate_zscore()` -> Will be used in Stage 3

  - `calculate_cointegration()`

- Find and Store Cointegrated Pairs

  We don't need to run "Stage 2" everytime. Instead, we just refer to a csv file.

  - `store_cointegration_result()` in `func_cointegration.py`

## Stage 3 - Execution

While True + CRON

### Open Positions (3a)

- Create BotAgent Class

  we are going to opening potentially many positions in one go, so use Python class.

  `func_bot_agent.py`:

  - Attributes

  - order_dict

  - `check_order_status_by_id()`

    we will need to check order status before opening trades -> create `check_order_status()` in `func_private.py`

  - `open_trades()`

- Get Recent Candles (close prices)

  Decide when to enter and exit -> `get_candles_recent()` in `func_public.py`

- Check Open Positions

  Avoild double orders -> `is_open_positions()` in `func_private.py`

- Place and Save Trades

  `open_positions()` in `func_entry_pairs.py`

  - Load cointegrated pairs from csv

  - Use the market pairs in csv to get recent prices

  - Use the prices to calculate Z-score

  - If z-score > THRESHOLD

  - check if base or quote is already open

  - Determine all the args for placing order

  - Create Bot Agent

  - Open trades

    Call `open_trades()` on the instance of BotAgent

  - Save the dicts to a csv

### Manage Existing Trades (3b)

`manage_trade_exits()` in `func_exit_pairs.py`

- Open JSON file

- Get all open positions per trading platform -> market_live

- Check all saved positions in saved cvs match order record on DYDX as well as in market_live

- Get price for series_1 and series_2

- Determine all the args

- CLOSE_AT_ZSCORE_CROSS (Trigger) -> calculate current z-score -> is_close

- is_close (Trigger) -> determine args -> place opposite order

## Stage 4 - Telegram

1. Create a bot @BotFather

- Get token of the created bot (save to .env)

- Get your personal ChatID (save to .env)

- Send 3 test messages in the bot

- Send a mesage through API via the url: "https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"

2. Send message from Python

- pip3 install requests
