from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from import_and_clean_data import  cleaned_data_all #clean_data_test
from crime_models import Crime_Event, Suspect, Victim, Location

# Base = declarative_base()
engine = create_engine('sqlite:///crime_data.db')
Session = sessionmaker(bind=engine)
# session.configure(bind=engine)
# Base.metadata.bind = engine

session = Session()

#functions to create crime_data objects
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



def convert_to_classes_single(element):
    crime_event = Crime_Event(complaint_num=element['cmplnt_num'],date_of_occurance=element['cmplnt_fr_dt'],time_of_occurance=element['cmplnt_fr_tm'],crime_completed_y_n=element['crm_atpt_cptd_cd'],jurisdiction_code=element['jurisdiction_code'],jurisdiction_desc=element['juris_desc'],report_date=element['rpt_dt'],level_of_offense=element['law_cat_cd'],offense_descr=element['ofns_desc'],locations=Location(latitude=element['latitude'],longitude=element['longitude'],precinct=element['addr_pct_cd'],borough=borough_finder(element['addr_pct_cd'],)),suspects = Suspect(age_group=element['susp_age_group'],race=element['susp_race'],gender=element['susp_sex']),victims = Victim(age_group=element['vic_age_group'],race=element['vic_race'],gender=element['vic_sex']))
    return crime_event

def create_classes(data_set):
    new_list = []
    for i,value in enumerate(data_set):
        new_list.append(convert_to_classes_single(value))
        if i % 50000 == 0:
            print("seed value "+str(i))
    return new_list

list_of_crime_event_objects = create_classes(cleaned_data_all)


session.add_all(list_of_crime_event_objects)
session.commit()
