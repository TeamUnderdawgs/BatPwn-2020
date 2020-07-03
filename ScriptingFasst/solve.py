import asyncio,websockets,time
from datetime import datetime, timedelta

url = "ws://127.0.0.1:8000/ws/kiraak"

async def main():
	async with websockets.connect(url) as websocket:
		inp_msg = input("[INPUT] ==> ")
		send_msg =  await websocket.send(inp_msg)
		recv_msg = await websocket.recv()
		print(f"[RECIEVED] : {recv_msg}")
		inp_msg = input("[INPUT] ==> ")
		send_msg =  await websocket.send(inp_msg)
		while True:
			recv_msg = await websocket.recv()
			print(f"[RECIEVED] : {recv_msg}")
			datetime_object = datetime.strptime(str(recv_msg), '%Y-%m-%d %H:%M:%S')
			timestamp = int(datetime.timestamp(datetime_object))
			print(f"[SENDING] : {timestamp}")
			send_msg =  await websocket.send(str(timestamp))
			time.sleep(1)

asyncio.get_event_loop().run_until_complete(main())
