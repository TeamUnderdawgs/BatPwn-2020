import asyncio,websockets,random,logging,time
from datetime import datetime, timedelta

logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def gen_datetime(min_year=2000, max_year=datetime.now().year):
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    fin_date = start + (end - start) * random.random()
    final_date = fin_date.replace(microsecond=0)
    timestamp = int(datetime.timestamp(final_date))
    return final_date,timestamp

async def main(websocket,path):
	remote_ip = websocket.remote_address[0]
	print("[CONNECTED] : ",remote_ip)

	await websocket.send("[+] Please send me the timestamps of upcoming datetimes, Are you ready? [y/Y]")
	
	try:
		agree_term = await asyncio.wait_for(websocket.recv(),timeout=10)
		if str(agree_term) != 'y':
			await websocket.send("Bye!")
			await websocket.close(1000,reason='BYE')
		else:
			for loop in range(30):
				chal,sol = gen_datetime()
				await websocket.send(str(chal))
				try:
					recieve_sol = await asyncio.wait_for(websocket.recv(),timeout=13)
					if int(recieve_sol) != sol:
						await websocket.send("Incorrect ! Closing Connection from our end!")
						await websocket.close(1000,reason='InCorrect')
				except asyncio.exceptions.TimeoutError:
					await websocket.send("[TIMEOUT] Closed connection, Bye!")
					await websocket.close(1000,reason='TIMEOUT')
				except ValueError:
					await websocket.send("[FORMAT] Bad Format, Bye!")
					await websocket.close(1000,reason='BadFormat')
				except Exception as e:
					print("[OTHER-EXCEPTION] SOME OTHER EXCEPTION : {}".format(e))
			try:
				await websocket.send("[=] Your flag is batpwn{1590300735000}")
			except websockets.exceptions.ConnectionClosedOK:
				pass

			except asyncio.exceptions.TimeoutError:
				await websocket.send("[TIMEOUT] Closed connection, Bye!")
				await websocket.close(1000,reason='TIMEOUT')

	except asyncio.exceptions.TimeoutError:
		await websocket.send("[TIMEOUT] Closed connection, Bye!")
		await websocket.close(1000,reason='TIMEOUT')

start_server = websockets.serve(main,'0.0.0.0',8765,close_timeout=10)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()