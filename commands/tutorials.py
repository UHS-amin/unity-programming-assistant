from typing import Any, Dict, Optional, List, Sequence, cast
import discord, json
from discord.ext import commands, menus
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from schemas.tutorial_schema import Tutorial
engine = create_engine("sqlite:///database.db")

COLOUR = 0x3772a2
class TutorialsSource(menus.ListPageSource):
	def __init__(self, entries, results, *, per_page):
		self.entries = entries
		self.per_page = per_page
		self.results = results

		pages, left_over = divmod(len(entries), per_page)
		if left_over:
			pages += 1

		self._max_pages = pages

	async def format_page(self, menu, page):
		if isinstance(page, discord.Embed):
			return page
		elif isinstance(page, str):
			embed = discord.Embed(
				colour=COLOUR,
				description=page,
				title='Tutorials Index'
			)
			entries = cast(Sequence, self.entries)
			embed.set_footer(text=f'({self.results / (entries.index(page) or 0) + 1}/{self.results or 0}) Results | Page ({(entries.index(page) or 0) + 1/len(entries)})')

class MyMenuPages(menus.MenuPages):
    def __init__(self, source):
        self._source = source
        self.current_page = 0
        self.ctx = None
        self.message = None

    async def start(self, ctx):
        await self._source._prepare_once()
        self.ctx = ctx
        page = await self._source.get_page(0)
        kwargs = cast(Dict[str, Any], await self._get_kwargs_from_page(page))
        self.message = await cast(commands.Context, self.ctx).reply(**kwargs)

@commands.group(invoke_without_command=True)
async def tutorials(ctx: commands.Context):
	embed = discord.Embed(
		colour=COLOUR,
		title='Tutorials Guide',
		description='This command is the main functionality of UPA! These tutorials help you learn progressively the basises and extensions of their topics, and there are dedicated subcommands for each functionality of the `tutorials` command!'
	)
	cmd = ctx.command
	if isinstance(cmd, commands.Group):
		subs = [sub for sub in cmd.walk_commands() if sub.parents[0] == cmd]
		if len(subs) > 0:
			cont = []
			for sub in subs:
				desc = sub.description or 'N/A'
				if sub.aliases:
					arr = [sub.name]
					cont.append(f'`{"|".join(arr)}: {desc}`')

			if len(cont) > 0: 
				embed.add_field(name='Subcommands', value='\n'.join(cont))

	await ctx.reply(embed=embed)


@tutorials.command(aliases=['search'], description='List/search all tutorials, including with or without a specified topic.')
async def list(ctx: commands.Context, topic: Optional[str] = None):
	session = Session(engine)
	query = session.query(Tutorial)
	if topic:
		query = query.filter(str(Tutorial.name).lower() == topic.lower())
	res = query.all()
	if len(res) <= 0:
		embed = discord.Embed(
			colour=discord.Colour.red(),
			title='Tutorials Index',
			description=f'No tutorials{" regarding " + f"`{topic}`"} were found.'
		)
		embed.set_footer(text='(0/0) Results | Page (1/1)')
		return await ctx.reply(embed=embed)
	else:
		if len(res) > 10:
			res = [res[i:i+10] for i in range(0, len(res), 10)]
		else:
			cont = ''
			for tut in res:
				page_length = len(cast(List, json.loads(str(tut.pages)))) or 0
				tut = cast(Tutorial, tut)
				name = str(tut.name)
				category = str(tut.category)
				rpi = int(str(tut.read_page_index))
				_id = int(str(tut.tut_id))

				read_status = "⚫" if rpi == -1 else "🔵" if rpi == 1 else "🟡" if rpi == round((rpi/page_length) * 100) >= 25 else "🟠" if rpi == round((rpi/page_length) * 100) >= 50 else "🔴" if rpi == round((rpi/page_length) * 100) >= 75 else "🟢" if round((rpi/page_length) * 100) == 100 or rpi + 1 == page_length else "❓"

				cont += f'{"*" if read_status == "🟢" else ""}{read_status} `[{_id}] {category}`/{name} ({page_length} pages, read {rpi + 1}){"*" if read_status == "🟢" else ""}\n'

			if len(cont) > 0:
				splitted = cont.split('\n')
				if len(splitted) > 8:
					splitted = [splitted[i:i+8] for i in range(0, len(splitted), 8)]
					Pagin
