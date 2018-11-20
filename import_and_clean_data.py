import pandas as pd


records = pd.read_json("https://data.cityofnewyork.us/resource/7x9x-zpz6.json?$limit=300000")
crime_data = records.to_dict('records')

#clean functions are below

def clean_crime_data_master(data):
    print("pre-age-check")
    bad_ages = bad_ages_finder(data)
    print("pre-cleaned checked")
    cleaned_data = data.copy()
    for i, x in enumerate(cleaned_data):
        x['cmplnt_fr_dt'] = x['cmplnt_fr_dt'].split("T",1)[0]
        x['rpt_dt'] = x['rpt_dt'].split("T",1)[0]
        x['law_cat_cd'] = x['law_cat_cd'].title()
        x['susp_age_group'] = clean_susp_age(x,bad_ages)
        x['vic_age_group'] = clean_vic_age(x,bad_ages)
        if i % 100000 == 0:
            print("clean value "+str(i))
    return cleaned_data

def bad_ages_finder(data):
    vic_bad_values = list(set(list(map(lambda x: x['vic_age_group'],data))))
    susp_bad_values = list(set(list(map(lambda x: x['susp_age_group'],data))))
    all_age_values = set(vic_bad_values+susp_bad_values)
    bad_ages_1 = list(filter(lambda x:x!=('<18'),all_age_values))
    bad_ages_2 = list(filter(lambda x:x!=('18-24'),bad_ages_1))
    bad_ages_3 = list(filter(lambda x:x!=('25-44'),bad_ages_2))
    bad_ages_4 = list(filter(lambda x:x!=('45-64'),bad_ages_3))
    bad_ages = list(filter(lambda x:x!=('65+'),bad_ages_4))
    return bad_ages

def clean_susp_age(element,remove_list):
    for bad in remove_list:
        if element['susp_age_group'] == bad:
            return 'Not Available'
    return element['susp_age_group']

def clean_vic_age(element,remove_list):
    for bad in remove_list:
        if element['vic_age_group'] == bad:
            return 'Not Available'
    return element['vic_age_group']

cleaned_data_all = clean_crime_data_master(crime_data)


# clean_data_test = clean_crime_data_master(crime_data[0:201])
