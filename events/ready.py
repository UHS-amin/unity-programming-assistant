from datetime import datetime
from discord import Client, ClientUser

async def on_ready(client=Client):
	time = datetime.now().strftime('%I:%M:%S %p')
	print(f'Logged in{" as " + client.user.name if isinstance(client.user, ClientUser) else ""} at {time}')