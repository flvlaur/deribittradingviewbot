"""
This program is a webhook reader which waits for messages that come on the localhost.

Components:
1. Ngrok redirects webhook messages to localhost and must be opened like: ngrok http 6969.
2. Alerts set up on TradingView must have the ngrok forward address as webhook.
3. TradingView alerts must be set up for a Strategy() and must contain the message:
{{time}}-{{strategy.order.action}}-{{strategy.order.contracts}}-{{ticker}}-{{strategy.order.price}}

"""



# Dependencies
from flask import Flask, request, abort
from path_manager import path
import subprocess
import threading
import json
import os



# Load & define configs
# TODO: move to path_manager and import port directly as int.
with open(path("/config.json")) as config_json:
    configs = json.load(config_json)

port = configs["network"]["port"]



# Starting Ngrok
def start_ngrok():
    ngrok_executable = path("ngrok/ngrok.exe")
    command = f"{ngrok_executable} http {port}"
    subprocess.Popen(command, shell=True)



# Starting Flask
app = Flask(__name__)



# Defining alert log folder
tv_alert_msg_dir = path("tradingview_alerts")
if not os.path.exists(tv_alert_msg_dir):
    os.makedirs(tv_alert_msg_dir)

# Start webhook listener and reader. Actions:
# 1. Requests "POST" methods. If present, msg is decoded as utf-8.
# 2. Splits msg into:
#    a. timestamp at entry (date and time)
#    b. trade action (buy or sell)
#    c. ticker
#    d. Price at entry
# 3. Writes .txt in folder from msg components, later to be used for deribit actions.
@app.route("/", methods=["POST"])
def webhook_master():
    if request.method == "POST":

        msg = request.data.decode("utf-8")
        msg_comps = msg.split("_")

        timestamp = msg_comps[0]
        date_part, time_part = timestamp.split("T", 1)
        date_at_entry = date_part  # Format eg: 2023-12-28
        time_at_entry = time_part.replace("Z", "").replace(":", "-")  # Format eg: 15-33-00

        trade_action = msg_comps[1]
        position_size = msg_comps[2]
        trade_ticker = msg_comps[3]
        price_at_entry = msg_comps[4]

        # Construct the filename
        msg_file = os.path.join(tv_alert_msg_dir, f"{date_at_entry}-"
                                                    f"{time_at_entry}-"
                                                    f"{position_size}-"
                                                    f"{trade_action}-"
                                                    f"{trade_ticker}-"
                                                    f"{price_at_entry}.txt")
    
        # Write the message to the file
        with open(msg_file, "w") as f:
            f.write("")

        print(msg_file)
    
        return "Success", 200

    else:
        abort(400)



# Start Ngrok in a seaparate thread
thread = threading.Thread(target=start_ngrok)
thread.start()


if __name__ == "__main__":
    app.run(port=int(port))