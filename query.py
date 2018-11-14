from crime_models import *
from sqlalchemy import create_engine
import pandas as pd
import csv
import datetime
import calendar

engine = create_engine('sqlite:///crime_data.db')

Session = sessionmaker(bind=engine)
session = Session()

month_range = list(range(1,11))
month_names = ['January','February','March','April','May','June','July','August','September','October']



def return_len_of_all_crimes():
    return len(session.query(Crime_Event.crime_completed_y_n).all())

def return_all_crime_objects():
    return session.query(Crime_Event).all()

def borough_objects_check(boro_input): #this works; checked:"Manhattan"
    boro_check = session.query(Crime_Event).join(Location).filter(Location.borough==boro_input).all()
    truth_status = []
    for x in boro_check:
        if x.locations.borough == boro_input:
            truth_status.append("True")
        else:
            truth_status.appen("False")
    return set(truth_status)

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

# def set_list_of_precincts():
#     return sorted(list(set(session.query(Crime_Event.precinct).all())))

# def crime_in_manhattan():
#     return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.precinct<=34).all()
#
# def crimes_in_bronx():
#     return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.precinct>=35,Crime_Event.precinct<=52).all()
#
# def crimes_in_brooklyn():
#     return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.precinct>=53,Crime_Event.precinct<=94).all()
#
# def crimes_in_queens():
#     return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.precinct>=95,Crime_Event.precinct<=115).all()
#
# def crimes_in_staten_island():
#     return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.precinct>=116).all()

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
    return session.query(Crime_Event.date_of_occurance).filter(Crime_Event.date_of_occurance >= start_date, Crime_Event.date_of_occurance <= end_date).order_by(Crime_Event.date_of_occurance).all()

def return_lvl_of_offense_objects_in_month(month_input,type):
    all_month_data = return_all_crime_objects_in_month(month_input)
    return list(filter(lambda event: event.level_of_offense==type,all_month_data))

def num_of_crimes_in_manhattan_w_month(month_input):
    year = 2018
    month = month_input
    num_days = calendar.monthrange(year, month)[1]
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, num_days)
    return session.query(func.count(Crime_Event.complaint_num)).filter(Crime_Event.precinct<=34,Crime_Event.date_of_occurance >= start_date, Crime_Event.date_of_occurance <= end_date).first()[0]

def return_len_of_crimes_in_month(month_input):
    year = 2018
    month = month_input
    num_days = calendar.monthrange(year, month)[1]
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, num_days)
    return len(db.session.query(Crime_Event.date_of_occurance).filter(Crime_Event.date_of_occurance >= start_date, Crime_Event.date_of_occurance <= end_date).all())

def crime_graph_creator():
    month_crime_totals = list(map(lambda month:return_all_crime_objects_in_month(month),month_range))
    return {'x':month_names,'y':month_crime_totals}

def borough_finder(prct_num):
    if prct_num <= 34:
        return "Manhattan"
    elif prct_num>=35 and prct_num<=52:
        return "Bronx"
    elif prct_num>=53 and prct_num<=94:
        return "Brooklyn"
    elif prct_num>=95 and prct_num<=115:
        return "Queens"
    elif prct_num>=116:
        return "Staten Island"

# def return_all_crime_objects_in_manhattan_in_month(month_input):
#     all_month_data = return_all_crime_objects_in_month(month_input)
#     return list(filter(lambda event: event.pre))
