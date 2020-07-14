## User settings
# API keys. Use read-only API keys for more security:
API_key = 'm5gNycphXSKHEUT3yCOs875VqXzEGSudt1RGpML9O3PkxVCVNUODIUMiBe8PaTTi '
API_secret = 'PRgpBJLfzWgnuyZ9OjfA2ODJk8v0YLyhyANXgtzYeud4b6dBGjMzM7EQDK4b5g0o'

# Market. Use dash '-' between base and quote assets.
market = 'MFT-ETH' 
 
# Start and end date (UTC). Note, that end_date is used for getting final prices. P&L greatly depends on this date!
start_date = '2020-06-01' 
end_date = '2020-06-30' 

## Calculations
import sys
import time
import calendar
import pandas as pd
import binance_api
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
pd.set_option('display.max_rows', None)

try:
    asset_base = market.split('-')[0]
    asset_quote = market.split('-')[1]
except IndexError:
    raise Exception(f"!!! Warning: Use dash '-' to split base and quote assets for {market}!")

symbol = asset_base + asset_quote

# Connect to Binance
binance = binance_api.Binance(API_key, API_secret)
try:
    trades = binance.myTrades(symbol = symbol)
    print(f"INFO: Exchange is successfully connected.")
except:
    raise Exception(f"!!! Warning: Can't get orders for {symbol}! Read message above.")    

# Create DataFrame 
df = pd.DataFrame(trades, columns = ['time', 'symbol', 'isBuyer', 'price', 'qty', 'quoteQty', 'commission', 'commissionAsset'])
qty_base = 'qty_' + asset_base
qty_quote = 'qty_' + asset_quote
df.columns = ['time', 'symbol', 'side', 'price', qty_base, qty_quote, 'fee', 'fee_coin']
df.side = df.side.replace([True, False], [1, -1])
df = df.astype({'price': 'float', qty_base: 'float', qty_quote: 'float', 'fee': 'float'})

# Start from time
time_format = '%Y-%m-%d'
start_date_ms = int(calendar.timegm(time.strptime(start_date, time_format)) * 1000)
end_date_ms = int((calendar.timegm(time.strptime(end_date, time_format))) * 1000)
df = df[(df.time >= start_date_ms) & (df.time <= end_date_ms + 86_400_000)]
df.time = pd.to_datetime(df.time, unit='ms')

# Find time for getting market prices
time_now = time.gmtime(time.time())
day_now_ms = calendar.timegm((time_now.tm_year, time_now.tm_mon, time_now.tm_mday, 0, 0, 0, 0, 0, 0)) * 1000
prices_time = min(day_now_ms, end_date_ms)

# Get symbol price
try:
    symbol_price  = float(binance.klines(symbol = symbol, interval = '1m', startTime = prices_time, limit = 1)[0][1])
except:
    print(f"Something wrong with request of {symbol} price. Please try again.")

# Get quote-USD price
if asset_quote == 'USDC' or asset_quote == 'USDT' or asset_quote == 'BUSD':
    usd_price = 1
else:
    try:
        usd_price  = float(binance.klines(symbol = asset_quote + 'USDT', interval = '1m', startTime = prices_time, limit = 1)[0][1])
    except:
        print(f"Something wrong with the request of {asset_quote}USDT price. Please try again.")

# Get BNB-quote price
if asset_quote == 'BNB':
    bnb_price = 1
else:
    try:
        bnb_price = float(binance.klines(symbol = 'BNB' + asset_quote, interval = '1m', startTime = prices_time, limit = 1)[0][1])
    except:
        print(f"Something wrong with the request of BNB{asset_quote} price. Please try again.")

# Summary
days = int((prices_time - start_date_ms)/(1000 * 86400)) + 1
average_buy = df[df.side == 1][qty_quote].sum()/df[df.side == 1][qty_base].sum()
average_sell = df[df.side == -1][qty_quote].sum()/df[df.side == -1][qty_base].sum()
total_volume = df[qty_quote].sum()

# Delta
delta_base = (df[qty_base] * df.side).sum()
delta_quote = - (df[qty_quote] * df.side).sum()

# Fees
fee_bnb = df[df.fee_coin == 'BNB'].fee.sum()
fee_base = df[df.fee_coin == asset_base].fee.sum()
fee_quote = df[df.fee_coin == asset_quote].fee.sum()

# Totals
total_quote = (delta_base - fee_base) * symbol_price + (delta_quote - fee_quote) - fee_bnb * bnb_price
total_usd = total_quote * usd_price
prices_time_utc = time.strftime(time_format, time.gmtime(prices_time/1000))

## Trades
if df.empty:
    print(f"No trades found for {symbol} from {start_date} till {end_date}")
else: 
    print(f"\nTrades gathered for {symbol}:")
    df.side = df.side.replace([1, -1], ['BUY', 'SELL'])
    print(df)

## Summary output
print(f"Summary for {symbol} for period [{start_date} - {end_date}]:")
print(f"   Days: {days}")
print(f"   Trades executed: {df.time.count()}")
print(f"   Total volume traded ({asset_quote}): {round(total_volume, 8)}")
print(f"   Average buy price: {round(average_buy, 8)}")
print(f"   Average sell price: {round(average_sell, 8)}")
print(f"\nTrading delta:")
print(f"   Delta {asset_base}: {round(delta_base, 8)}")
print(f"   Delta {asset_quote}: {round(delta_quote, 8)}")
print(f"\nFees:")
print(f"   Fees BNB: {round(fee_bnb, 8)}")
print(f"   Fees {asset_base}: {round(fee_base, 8)}")
print(f"   Fees {asset_quote}: {round(fee_quote, 8)}")
print(f"\nPrices at the end of the period [{prices_time_utc}]:")
print(f"   Price {symbol}: {symbol_price}")
print(f"   Price {asset_quote}USDT: {usd_price}")
print(f"   Price BNB{asset_quote}: {bnb_price}")
print(f"\nTotal profit:")
print(f"   Total profit ({asset_quote}): {round(total_quote, 8)}")
print(f"   Total profit (USDT): {round(total_usd, 8)}")
