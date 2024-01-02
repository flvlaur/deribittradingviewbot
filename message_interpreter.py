from path_manager import path
import re
import os

# TODO: while loop to constantly reiterate over tradingview_alerts folder
def message_interpreter():
    # Assuming necessary imports and 'path' definition

    directory = path("tradingview_alerts")

    # List all .txt files in the directory
    file_names = [f for f in os.listdir(directory) if f.endswith('.txt')]

    trade_data = []

    for index, file_name in enumerate(file_names, start=1):
        match = re.search(r'(\d{4}-\d{2}-\d{2})-(\d{2}-\d{2}-\d{2})-(\d+)-(buy|sell)-([A-Z]+)-(\d+\.?\d*)', file_name)
        if match:
            date, time, size, action, symbol, price = match.groups()
            time = time.replace('-', ':')  # Format time correctly

            if all([date, time, size, action, symbol, price]):
                trade_data.append((index, date, time, size, action, symbol, price))
            else:
                print(f"Data not available for {file_name}")
        else:
            print(f"Data not available for {file_name}")

    return trade_data




def filter_trades(dates=None, times=None, symbols=None, actions=None, price_range=None):
    all_trade_data = message_interpreter()

    filtered_trades = []

    for trade in all_trade_data:
        index, date, time, size, action, symbol, price = trade
        price = float(price)  # Convert price to float for comparison

        # Check each criterion
        date_match = (dates is None or date in dates)
        time_match = (times is None or time in times)
        symbol_match = (symbols is None or symbol in symbols)
        action_match = (actions is None or action in actions)
        price_match = (price_range is None or price_range[0] <= price <= price_range[1])

        if date_match and time_match and symbol_match and action_match and price_match:
            filtered_trades.append(trade)

    return filtered_trades

# Usage examples:

# Example criteria
dates = ["2023-12-28", "2023-12-29"]
times = ["19:14:00", "19:23:00"]
symbols = ["BTCUSD"]
actions = ["buy", "sell"]
price_range = (42500, 43000)

# Get trades matching specific criteria
# matching_trades = filter_trades(dates, times, symbols, actions, price_range)
# for trade in matching_trades:
#     print(trade)

# Get all trades

index_array = []
dates_array = []
times_array = []
symbols_array = []
actions_array = []
price_array = []

all_trades = filter_trades()
for trade in all_trades:
    index, date, time, size, action, symbol, price = trade

    index_array.append(index)
    dates_array.append(date)
    times_array.append(time)
    symbols_array.append(symbol)
    actions_array.append(action)
    price_array.append(price)


print(filter_trades())