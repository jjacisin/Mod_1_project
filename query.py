from crime_models import *
from sqlalchemy import create_engine
import pandas as pd
import csv
import datetime
import calendar

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
#     return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.date_of_occurance=="2018-01").all()

def all_crime_dates():
    return session.query(Crime_Event.date_of_occurance).all()

def return_all_crime_objects_in_month(month_input):
    year = 2018
    month = month_input
    num_days = calendar.monthrange(year, month)[1]
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, num_days)
    return session.query(Crime_Event).filter(Crime_Event.date_of_occurance >= start_date, Crime_Event.date_of_occurance <= end_date).order_by(Crime_Event.date_of_occurance).all()

def return_lvl_of_offense_objects_in_month(month_input,type):
    all_month_data = return_all_crime_objects_in_month(month_input)
    return list(filter(lambda event: event.level_of_offense==type,all_month_data))
