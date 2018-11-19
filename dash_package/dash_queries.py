from dash_package import app
import dash_core_components as dcc
import dash_html_components as html
from dash_package.dash_crime_models import *
import folium
from folium import plugins
from folium.plugins import MarkerCluster
import plotly.graph_objs as go
import pandas as pd
import datetime
import calendar


########Level of Offense Graphs/Queries

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

######## Offense Description Map Functions

##Initial Map

def return_len_of_all_crimes():
    return len(db.session.query(Crime_Event.crime_completed_y_n).all())

total_crimes = return_len_of_all_crimes()

def setlist_of_crime_event_objects():
    return list(set(db.session.query(Crime_Event.offense_descr).all()))

def fulllist_of_crime_event_objects():
    return list(db.session.query(Crime_Event.offense_descr).all())

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

option_values = list(map(lambda x: x['key'],ofns_occurances))

def option_creator(opt_vals):
    s_vals = sorted(opt_vals)
    oc_list = []
    for val in s_vals:
        if val != "SEX CRIMES":
            oc_dict = {}
            oc_dict['label'] = val.title()
            oc_dict['value'] = val
            oc_list.append(oc_dict)
    return oc_list

drop_down_options = option_creator(option_values)

# new_list = [expression(i) for i in old_list if filter(i)]

other_ofns = count_function_sorted_most_least_w_removal(setlist_of_crime_event_objects(),fulllist_of_crime_event_objects())[1]

#returns "OTHER" cluster; Defined by ofns_type that makes up > 5% of all crime; BUG: drops 'nan'/'None' values;
def return_other_ofn_locations():
    return db.session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.offense_descr.in_(other_ofns)).all()

def return_ofns_type_locs(type):
    return db.session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.offense_descr==type.upper()).all()

#tri-boro bridge coordinates
NY_COORDINATES = (40.7797, -73.9266)
#inital map creation
ny_map = folium.Map(location=NY_COORDINATES,tiles='Stamen Terrain',zoom_start=11)
initial_display = ny_map.save('dash_package/map_storage/initial_map.html')
#insert

def map_ofns_coord(coord_list):
    marker_cluster = plugins.MarkerCluster(name=None).add_to(ny_map)
    for item in coord_list:
        folium.Marker([item.latitude,item.longitude]).add_to(marker_cluster)
    return ny_map

def map_html_creator(value):
    if value == "OTHER":
        location_map = map_ofns_coord(return_other_ofn_locations())
        location_map.save('dash_package/map_storage/"{}".html'.format(value))
        # location_map.save('dash_package/map_storage/"{}".html').format(value)
    else:
        location_map = map_ofns_coord(return_ofns_type_locs(value))
        location_map.save('dash_package/map_storage/"{}".html'.format(value))

#create_all_html_maps
#only need to run once to initialize
# for value in option_values:
#     if value != "SEX CRIMES":
#         print(".....NOW PROCESSING....."+str(value))
#         map_html_creator(value)
