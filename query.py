from crime_models import *
from sqlalchemy import create_engine
import folium
from folium import plugins
from folium.plugins import MarkerCluster
import pandas as pd
import pandas as pd
import csv
import datetime
import calendar
import re
import pdb

engine = create_engine('sqlite:///crime_data.db')

Session = sessionmaker(bind=engine)
session = Session()

month_range = list(range(1,11))
month_names = ['January','February','March','April','May','June']


###############################################



def SQLresListToStrList(SQLresList):
    return [str(x) for x in SQLresList]

def stringListSorter(stringList, startTrim, endTrim):
    newList = list()

    for x in stringList:
        newList.append((re.search('%s(.*)%s'%(startTrim,endTrim), x)).group(2))
    return newList

def resultListFromDescr(resultList):
    newList = list()
    for x in resultList:
        newList.append(x.offense_descr)
        #pdb.set_trace()
    return newList

def setList1Count(inputList):
    newDatDict = dict()
    #pdb.set_trace()
    listKeys = list(set(inputList))

    #'Initialize '
    for a in listKeys:
        newDatDict[a] = 0
        #'Fill'
        for b in inputList:
            if a == b:
                newDatDict[a] += 1

    return newDatDict

def dictToDash(inputDict):
    listX = list()
    listY = list()

    for a,b in inputDict.items():
        listX.append(a)
        listY.append(b)
    return {'x': listX, 'y': listY}

def SQLresListToStrList(SQLresList):
    return [str(x) for x in SQLresList]

####

def return_crime_types_overall():
    allOffensesList = session.query(Crime_Event.offense_descr).order_by(Crime_Event.date_of_occurance).all()
    return allOffensesList

####

def crimeTypeQueryToDash(crimeTypeQuery):
    return dictToDash(setList1Count(resultListFromDescr(crimeTypeQuery)))


###############################################


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

def crime_in_manhattan():
    return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Location.borough=="Manhattan").all()
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
    return session.query(Crime_Event).filter(Crime_Event.date_of_occurance >= start_date, Crime_Event.date_of_occurance <= end_date).order_by(Crime_Event.date_of_occurance).all()

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

month_names = ['January','February','March','April','May','June']
boroughs = ['Manhattan',"Brooklyn",'Bronx',"Queens",'Staten Island']

def return_all_crime_instances_in_month(month_input):
    year = 2018
    month = month_input
    num_days = calendar.monthrange(year, month)[1]
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, num_days)
    return len(session.query(Crime_Event.report_date).filter(Crime_Event.report_date >= start_date, Crime_Event.report_date <= end_date).all())

def crime_graph_creator():
    month_crime_totals = list(map(lambda month:return_all_crime_instances_in_month(month),month_range))
    return {'x':month_names,'y':month_crime_totals,'name':'Overall'}


def return_all_crime_instances_in_month_for_boro(boro_input,month_input):
    year = 2018
    month = month_input
    num_days = calendar.monthrange(year, month)[1]
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, num_days)
    return len(session.query(Crime_Event.report_date).join(Location).filter(Crime_Event.report_date >= start_date, Crime_Event.report_date <= end_date,Location.borough==boro_input).all())

def crime_graph_all_boroughs(boros,months):
    output = []
    for boro in boroughs:
        total_list = []
        for month in list(range(1,len(months)+1)):
            month_total = return_all_crime_instances_in_month_for_boro(boro,month)
            total_list.append(month_total)
        output.append({'x':months,'y':total_list,'name':boro})
    return output

def return_felony_instances_in_month(month_input):
    year = 2018
    month = month_input
    num_days = calendar.monthrange(year, month)[1]
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, num_days)
    return len(session.query(Crime_Event.report_date).filter(Crime_Event.report_date >= start_date, Crime_Event.report_date <= end_date,Crime_Event.level_of_offense=="Felony").all())

def felony_graph_creator():
    month_crime_totals = list(map(lambda month:return_felony_instances_in_month(month),list(range(1,len(month_names)+1))))
    return {'x':month_names,'y':month_crime_totals,'name':'Overall'}

def off_desc_return():
    return session.query(Crime_Event.offense_descr).all()

def robbery_locations():
    return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.offense_descr=="ROBBERY").all()

##List of objects that includes the lat/lng of each crime_event
##if list is less than 2000 elements group as other (i.e. <1%)

def return_len_of_all_crimes():
    return len(session.query(Crime_Event.crime_completed_y_n).all())

total_crimes = return_len_of_all_crimes()

def setlist_of_crime_event_objects():
    return list(set(session.query(Crime_Event.offense_descr).all()))

def fulllist_of_crime_event_objects():
    return list(session.query(Crime_Event.offense_descr).all())

def count_function_sorted_most_least_w_removal(unique_list, full_list):
    CF=[]
    CF_other = []
    CF_other_names = []
    for list_item in unique_list:
        CF_dict = {}
        CF_dict['key'] = list_item.offense_descr
        CF_dict['count'] = full_list.count(list_item)
        if full_list.count(list_item) > total_crimes*.005:
            CF.append(CF_dict)
        else:
            CF_other.append(full_list.count(list_item))
            CF_other_names.append(list_item.offense_descr)
    CF.append({'key':'OTHER','count':sum(CF_other)})
    #return CF_dict
    return [sorted(CF, key=lambda k:k['count'],reverse=True),CF_other_names]

ofns_occurances = count_function_sorted_most_least_w_removal(setlist_of_crime_event_objects(),fulllist_of_crime_event_objects())[0]

drop_down_options = list(map(lambda x: x['key'],ofns_occurances))+['OTHER']

other_ofns = count_function_sorted_most_least_w_removal(setlist_of_crime_event_objects(),fulllist_of_crime_event_objects())[1]

#returns "OTHER" cluster; Defined by ofns_type that makes up > 5% of all crime; BUG: drops 'nan'/'None' values;
def return_other_ofn_locations():
    return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.offense_descr.in_(other_ofns)).all()

def return_ofns_type_locs(type):
    return session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.offense_descr==type.upper()).all()

#tri-boro bridge coordinates
NY_COORDINATES = (40.7797, -73.9266)
#inital map creation
ny_map = folium.Map(location=NY_COORDINATES,tiles='Stamen Terrain',zoom_start=11)
#insert

def map_ofns_coord(coord_list):
    marker_cluster = plugins.MarkerCluster(name=None).add_to(ny_map)
    for item in coord_list:
        folium.Marker([item.latitude,item.longitude]).add_to(marker_cluster)
    return ny_map
