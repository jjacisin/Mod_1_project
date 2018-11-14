from dash_package import app
import dash_core_components as dcc
import dash_html_components as html
from dash_package.dash_crime_models import *
import pandas as pd
import datetime
import calendar

month_names = ['January','February','March','April','May','June']
boroughs = ['Manhattan',"Brooklyn",'Bronx',"Queens",'Staten Island']

def return_all_crime_instances_in_month(month_input):
    year = 2018
    month = month_input
    num_days = calendar.monthrange(year, month)[1]
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, num_days)
    return len(db.session.query(Crime_Event.report_date).filter(Crime_Event.report_date >= start_date, Crime_Event.report_date <= end_date).all())

def crime_graph_creator():
    month_crime_totals = list(map(lambda month:return_all_crime_instances_in_month(month),list(range(1,len(month_names)+1))))
    return [{'x':month_names,'y':month_crime_totals,'name':'Overall'}]


def return_all_crime_instances_in_month_for_boro(boro_input,month_input):
    year = 2018
    month = month_input
    num_days = calendar.monthrange(year, month)[1]
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, num_days)
    return len(db.session.query(Crime_Event.report_date).join(Location).filter(Crime_Event.report_date >= start_date, Crime_Event.report_date <= end_date,Location.borough==boro_input).all())

def crime_graph_all_boroughs(boros,months):
    output = []
    for boro in boroughs:
        total_list = []
        for month in list(range(1,len(months)+1)):
            month_total = return_all_crime_instances_in_month_for_boro(boro,month)
            total_list.append(month_total)
        output.append({'x':months,'y':total_list,'name':boro})
    return output

def return_felony_instances_in_month(month_input,type):
    year = 2018
    month = month_input
    num_days = calendar.monthrange(year, month)[1]
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, num_days)
    return len(db.session.query(Crime_Event.report_date).filter(Crime_Event.report_date >= start_date, Crime_Event.report_date <= end_date,Crime_Event.level_of_offense==type).all())

def level_graph_creator_all(type):
    month_crime_totals = list(map(lambda month:return_felony_instances_in_month(month,type),list(range(1,len(month_names)+1))))
    return [{'x':month_names,'y':month_crime_totals,'name':'Overall'}]

def return_level_instances_in_month_for_boro(boro_input,month_input,type):
    year = 2018
    month = month_input
    num_days = calendar.monthrange(year, month)[1]
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, num_days)
    return len(db.session.query(Crime_Event.report_date).join(Location).filter(Crime_Event.report_date >= start_date, Crime_Event.report_date <= end_date,Location.borough==boro_input,Crime_Event.level_of_offense==type).all())

def level_graph_all_boroughs(boros,months,type):
    output = []
    for boro in boroughs:
        total_list = []
        for month in list(range(1,len(months)+1)):
            month_total = return_level_instances_in_month_for_boro(boro,month,type)
            total_list.append(month_total)
        output.append({'x':months,'y':total_list,'name':boro})
    return output
