import json
import socketio

TOKEN = "You donation alert token" #You donation alert token

sio = socketio.Client()

@sio.on('connect')
def on_connect():
	sio.emit('add-user', {"token": TOKEN, "type": "alert_widget"})

@sio.on('donation')
def on_message(data):
	y = json.loads(data)

	print(y['username'])
	print(y['message'])
	print(y['amount'])
	print(y['currency'])


sio.connect('wss://socket.donationalerts.ru:443',transports='websocket')
