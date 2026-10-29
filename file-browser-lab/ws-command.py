#!/usr/bin/env python3
"""Drive File Browser's interactive command runner over its websocket.

Usage: ws_command.py <token-file> <command>
Prints every message the server sends back, then closes.
"""
import sys
import websocket

token = open(sys.argv[1]).read().strip()
command = sys.argv[2]

url = "ws://127.0.0.1:18080/api/command/"
ws = websocket.create_connection(url, timeout=10, header={"X-Auth": token})
print(f"connected: {url} (token sent in the X-Auth header)")
ws.send(command)
print(f"sent: {command}")
try:
    while True:
        msg = ws.recv()
        if msg == "":
            break
        print(f"received: {msg}")
except websocket.WebSocketConnectionClosedException:
    print("server closed the connection")
finally:
    ws.close()
