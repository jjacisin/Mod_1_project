from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from import_and_clean_data import  clean_data_test, cleaned_data_all
from crime_models import *

Base = declarative_base()

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.bind = engine

session = session()

#functions to create crime_data objects
def convert_to_classes_single(element):
    crime_event = Crime_Event(complaint_num=element['cmplnt_num'],precinct=element['addr_pct_cd'],date_of_occurance=element['cmplnt_fr_dt'],time_of_occurance=element['cmplnt_fr_tm'],crime_completed_y_n=element['crm_atpt_cptd_cd'],jurisdiction_code=element['jurisdiction_code'],jurisdiction_desc=element['juris_desc'],report_date=element['rpt_dt'],level_of_offense=element['law_cat_cd'],offense_descr=element['ofns_desc'],locations=Location(latitude=element['latitude'],longitude=element['longitude']),suspects = Suspect(age_group=element['susp_age_group'],race=element['susp_race'],gender=element['susp_sex']),victims = Victim(age_group=element['vic_age_group'],race=element['vic_race'],gender=element['vic_sex']))
    return crime_event

def create_classes(data_set):
    new_list = []
    for i,value in enumerate(data_set):
        new_list.append(convert_to_classes_single(value))
        if i % 100 == 0:
            print(i)
    return new_list

list_of_crime_event_objects = create_classes(cleaned_data_all)


session.add_all(list_of_crime_event_objects)
session.commit()
