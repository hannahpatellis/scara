## This file gets called by the home.py file as a QProcess and constantly listens to the server for data
## It's a good idea to assign your ScARA Server a static IP address so you're not constantly changing this file
## Written by Hannah A. Patellis - hannahap.com - @hannahpatellis

import websocket
from threading import Timer

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### open ###")

def establish():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://Your Scara Server IP:8080/", on_message=on_message, on_error=on_error, on_close=on_close,
                                subprotocols=["echo-protocol"])
    t = Timer(300, renew, args=[ws])
    t.start()
    ws.on_open = on_open
    ws.run_forever()

def renew(ws):
    ws.close()
    establish()

if __name__ == "__main__":
    establish()