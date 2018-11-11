from crime_models import *
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///crime_data.db')

Session = sessionmaker(bind=engine)
session = Session()

records = pd.read_json("https://data.cityofnewyork.us/resource/7x9x-zpz6.json?$limit=300000")
crime_data = records.to_dict('records')

# add and commit the actors and roles below


session.add_all([tom_hanks,gwyneth_paltrow,daniel_craig])
session.commit()
