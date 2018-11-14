import pandas as pd
import datetime
import calendar

def return_all_crime_objects_in_month(month_input):
    year = 2018
    month = month_input
    num_days = calendar.monthrange(year, month)[1]
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, num_days)
    return session.query(Crime_Event).filter(Crime_Event.date_of_occurance >= start_date, Crime_Event.date_of_occurance <= end_date,Crime_Event.precinct<=34).order_by(Crime_Event.date_of_occurance).all()

def return_lvl_of_offense_objects_in_month(month_input,type):
    all_month_data = return_all_crime_objects_in_month(month_input)
    return list(filter(lambda event: event.level_of_offense==type,all_month_data))
