import sys
sys.dont_write_bytecode = True

import discord, os, inspect, importlib
from datetime import datetime
from discord.ext import commands
from types import FunctionType
from typing import Any, Callable, List, Tuple, Union
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

isCallable: Callable[[Any], bool] = lambda v: isinstance(v, Callable)
isCommand: Callable[[Any], bool] = lambda v: isinstance(v, commands.core.Command)
isGroup: Callable[[Any], bool] = lambda v: isinstance(v, commands.core.Group)
isFunction: Callable[[Any], bool] = lambda v: isinstance(v, FunctionType)
filterFunction: Callable[[Union[List, Tuple]], Union[FunctionType, None]] = lambda v: list(filter(isFunction, list(map(lambda x: x[1] or None, list(v)))))[0] or None
filterGroup: Callable[[Union[List, Tuple]], Union[commands.core.Group, None]] = lambda v: list(filter(isGroup, list(map(lambda x: x[1] or None, list(v)))))[0] or None

class CustomBot(commands.Bot):
	async def setup_hook(self):
		for file in os.listdir('./commands/'):
			if file.endswith('.py'):
				filename = os.path.basename(file).split('.')[0]
				time = datetime.now().strftime('%I:%M:%S %p')
				cmds = list(inspect.getmembers(importlib.import_module(f'commands.{filename}'), predicate=isCommand))
				if len(cmds) > 1 or any(isGroup(cmd) for cmd in cmds):
					main = filterGroup(cmds)
					if main is None:
						continue
					self.add_command(main)
				else:
					self.add_command(cmds[0][1])
				print(f'{time} || Loaded command {filename}')

		for file in os.listdir('./events/'):
			if file.endswith('.py'):
				evname = os.path.basename(file).split('.')[0]
				time = datetime.now().strftime('%I:%M:%S %p')
				listn = filterFunction(list(inspect.getmembers(importlib.import_module(f'events.{evname}'), predicate=isCallable)))
				if listn is None:
					continue
				self.add_listener(listn)
				print(f'{time} || Loaded event {evname}')

client = CustomBot(command_prefix='.', help_command = None, intents=intents, heartbeat_timeout=60000)
client.run(format(os.environ.get('TOKEN')))