from datetime import datetime
import sys
from typing import Any, Dict, List, cast
sys.dont_write_bytecode = True
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from schemas.tutorial_schema import Tutorial, TutorialField, TutorialPage
import json

engine = create_engine("sqlite:///database.db", future=True)
with Session(engine) as session:
	tut = Tutorial(
		pages = json.dumps([TutorialPage(
			content='Banana',
			fields=[
				TutorialField(title='What is a banana?', content='It is a fruit!', pos=0),
				TutorialField(title='What is the color of a banana', content='It is a fruit!', pos=0)
			]
		)]),
		created_at = datetime.now(),
		author_id = 1
	)

	session.add(tut)
	session.commit()

session = Session(engine)

tuts: List[Tutorial] = session.query(Tutorial).all()
if len(tuts) > 0:
	for tutorial in tuts:
		if int(str(tutorial.tut_id)) != tuts.index(tutorial) + 1:
			values: Dict[str, Any] = {"id": tuts.index(tutorial) + 1}
			if str(tutorial.name).startswith('Tutorial #'):
				id_ = values['id']
				values["name"] = f"Tutorial #{id_}"
			session.query(Tutorial).filter(Tutorial.tut_id == tutorial.tut_id).update(values, synchronize_session=False)

		elif str(tutorial.name).startswith('Tutorial #') and str(tutorial.name).split('#')[1] != str(tuts.index(tutorial) + 1):
			session.query(Tutorial).filter(Tutorial.tut_id == tutorial.tut_id).update({"name": f"Tutorial #{tuts.index(tutorial) + 1}"}, synchronize_session=False)
		
		print(str(tutorial.name).split('#')[1])
		print(str(tuts.index(tutorial) + 1))
		print(str(tutorial.name).split('#')[1] != str(tuts.index(tutorial) + 1))
		session.commit()