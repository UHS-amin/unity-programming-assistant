from sqlalchemy import JSON, DateTime, Identity, String, create_engine, Column, Integer
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Mapper, declarative_base
from typing import Optional, List, Union
from sqlalchemy.orm.events import event
import random, string

engine = create_engine("sqlite:///database.db", future=True)
class TutorialField:
	pos: Optional[int]
	title: str = 'Field'
	content: str

	def __init__(self, title: str, content: str, pos: int = 0):
		self.pos = pos or 0
		if len(title) > 125:
			raise ValueError('Title is greater than 125 characters in length.')
		self.title = title
		self.content = content

class TutorialPage:
	pos: int
	content: str
	fields: List
	image: Optional[str]

	def __new__(cls, content: str, pos: int = 0, fields: List[TutorialField] = [], image: Union[str, None] = None):
		cls.image = image
		cls.content = content
		cls.pos = pos
		if fields:
			non_pos_fields = list(filter(lambda f: f.pos == None, fields))
			if len(non_pos_fields) > 0:
				for non_pos in non_pos_fields:
					non_pos.pos = non_pos_fields.index(non_pos) or 0
		
			for field in fields:
				if len(list(filter(lambda f: f.pos == field.pos, fields))) > 1:
					list(filter(lambda f: f.pos == field.pos, fields))[1].pos = fields.index(list(filter(lambda f: f.pos == field.pos, fields))[1]) or 1

		cls.fields = list(map(lambda f: f.__dict__, fields))
		iters = dict((x, y) for x, y in TutorialPage.__dict__.items() if x[:2] != '__')
		return iters		
	
Base = declarative_base()
class Tutorial(Base):
	__tablename__ = 'tutorial'

	tut_id = Column('id', Integer, Identity(start=1, cycle=True, order=True), primary_key=True)
	category = Column(String, default='Tutorial Category')
	name = Column(String(250), unique=True, default=''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=8)))
	pages = Column(JSON, nullable=False)
	read_page_index = Column(Integer, default=-1)
	author_id = Column(Integer, nullable=False)
	created_at = Column(DateTime, nullable=False)
	edited_at = Column(DateTime)

	@staticmethod
	def fill_ref(mapper: Mapper, connection: Connection, target):
		connection.execute(mapper.mapped_table.update().values(name=f'Tutorial #{target.tut_id}').where(mapper.mapped_table.c['id'] == target.tut_id))

event.listen(Tutorial, 'after_insert', Tutorial.fill_ref)

Base.metadata.create_all(engine)
