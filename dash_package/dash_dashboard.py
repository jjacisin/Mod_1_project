from dash_package import app
import dash_core_components as dcc
import dash_html_components as html
# from dash_package.dash_queries import *
from dash_package.dash_crime_models import *
from dash_package import *
import datetime
import calendar

month_range = list(range(1,7))
month_names = ['January','February','March','April','May','June']

def return_all_crime_instances_in_month(month_input):
    year = 2018
    month = month_input
    num_days = calendar.monthrange(year, month)[1]
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, num_days)
    return len(db.session.query(Crime_Event.report_date).filter(Crime_Event.report_date >= start_date, Crime_Event.report_date <= end_date).all())

def return_manhattan_crime_instances_in_month(month_input):
    year = 2018
    month = month_input
    num_days = calendar.monthrange(year, month)[1]
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, num_days)
    return len(db.session.query(Crime_Event.report_date).filter(Crime_Event.report_date >= start_date, Crime_Event.report_date <= end_date,Crime_Event.precinct<=34).all())

def crime_graph_creator():
    month_crime_totals = list(map(lambda month:return_all_crime_objects_in_month(month),month_range))
    return {'x':month_names,'y':month_crime_totals}

def crime_graph_creator():
    month_crime_totals = list(map(lambda month:return_all_crime_objects_in_month(month),month_range))
    return {'x':month_names,'y':month_crime_totals}



def listing_prices():
    listing_titles = ['bk', 'queens', 'manhattan']
    listing_prices = [4, 10, 20]
    return {'x': listing_titles, 'y': listing_prices}


app.layout = html.Div(
    children=[
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(id='NYC', label='Crimes by Borough',
            children=[
            dcc.Graph(figure=
            {'data': [crime_graph_creator()],
            'layout': {},
            'name':'Overall'})
            ]
        ),
        dcc.Tab(id='something', label='apartments',
            children=[
            dcc.Graph(figure=
            {'data': [listing_prices()],
            'layout': {}})
            ]
        )

        ])
    ]
)
