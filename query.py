from crime_models import *
from sqlalchemy import create_engine

engine = create_engine('sqlite:///crime_data.db')

Session = sessionmaker(bind=engine)
session = Session()


def return_len_of_all_crimes():
    return len(session.query(Crime_Event.crime_completed_y_n).all())

def return_len_of_all_crimes_completed():
    return len(session.query(Crime_Event.crime_completed_y_n).filter(Crime_Event.crime_completed_y_n=="COMPLETED").all())

def percent_of_reported_incompetent_criminals():
    return round(1-(return_len_of_all_crimes_completed()/return_len_of_all_crimes()),4)*100

def all_latitudes():
    return session.query(Location.latitude).all()

def all_location_pairs():
    return session.query(Location.latitude, Location.longitude).all()

def felony_locations():
    return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.level_of_offense=="Felony").all()

def set_list_of_precincts():
    return sorted(list(set(session.query(Crime_Event.precinct).all())))

def crimes_in_manhattan():
    return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.precinct<=34).all()

def crimes_in_bronx():
    return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.precinct>=35,Crime_Event.precinct<=52).all()

def crimes_in_brooklyn():
    return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.precinct>=53,Crime_Event.precinct<=94).all()

def crimes_in_queens():
    return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.precinct>=95,Crime_Event.precinct<=115).all()

def crimes_in_staten_island():
    return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.precinct>=116).all()



# def january_crime_locations():
#     return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.date_of_occurance.split(":")[1]).all()
#
# def Locations_by_date():
#     return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.level_of_offense=="Felony").all()
