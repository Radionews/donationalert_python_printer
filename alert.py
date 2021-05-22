import win32print
import win32ui
from PIL import Image, ImageWin
import os
from urllib.request import urlretrieve
import json
import socketio
import requests

TOKEN = "type_your_token" #You donation alert token

white_list = {"jpg","JPG","jpeg","JPEG","png","PNG","bmp","BMP"}

def print_img(url):
	#скачивание файла по ссылке
	typ = url[url.rfind(".")+1:]
	flag = False
	for wh in white_list:
		if wh == typ:
			flag = True
	if flag:
		img = requests.get(url)
		img_file = open('temp.' + typ, 'wb')
		img_file.write(img.content)
		img_file.close()

		#печать файла на принтере по умолчанию
		printer_name = win32print.GetDefaultPrinter ()
		file_name = "temp." + typ

		HORZRES = 8
		VERTRES = 10
		
		LOGPIXELSX = 88
		LOGPIXELSY = 90

		PHYSICALWIDTH = 110
		PHYSICALHEIGHT = 111

		PHYSICALOFFSETX = 112
		PHYSICALOFFSETY = 113

		hDC = win32ui.CreateDC ()
		hDC.CreatePrinterDC (printer_name)
		printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)
		printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)
		printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)

		bmp = Image.open (file_name)
		if bmp.size[1] > bmp.size[0]:
		  bmp = bmp.rotate (90)

		ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
		scale = min (ratios)

		hDC.StartDoc (file_name)
		hDC.StartPage ()

		dib = ImageWin.Dib (bmp)
		scaled_width, scaled_height = [int (scale * i) for i in bmp.size]
		x1 = int ((printer_size[0] - scaled_width) / 2)
		y1 = int ((printer_size[1] - scaled_height) / 2)
		x2 = x1 + scaled_width
		y2 = y1 + scaled_height
		dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))

		hDC.EndPage ()
		hDC.EndDoc ()
		hDC.DeleteDC ()

sio = socketio.Client()

@sio.on('connect')
def on_connect():
	sio.emit('add-user', {"token": TOKEN, "type": "alert_widget"})

@sio.on('donation')
def on_message(data):
	y = json.loads(data)
	if((y['message'].find('IMG:') != -1)):
		url = y['message'].split('IMG:')[1]
		print(y['username'])
		print(y['message'])
		print_img(y['message'].split('IMG:')[1])

sio.connect('wss://socket.donationalerts.ru:443',transports='websocket')