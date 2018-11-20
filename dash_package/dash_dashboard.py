from dash_package.dash_queries import *
import dash
from dash.dependencies import Input, Output
# from folium import Iframe
# from dash_package.robbery_locations_1K import *



app.layout = html.Div([
    html.H1('NYC Crime Data - 1H 2018'),
    html.Div([
        html.H2('Crime by Level of Offense & Offense Description Graph'),
        dcc.Tabs(id="tabs", children=[
            ############################################################
            ###Common theme identified: calling query via a specific value of a field.
            ####This can be streamlined via automatic key creation and through sets.
            #####All 4 of these tabs can be shortened into a single tab,
            ###### which picks traces based on input from a dropdown list.
            dcc.Tab(id='NYC', label='Crimes by Borough',
                children=[
                dcc.Graph(figure=
                {'data': crime_graph_creator()+crime_graph_all_boroughs(boroughs,month_names),
                'layout': {'title':'All Complaints'},
                })
                ]
            ),
            dcc.Tab(id='Felony', label='Felony Complaints',
                children=[
                dcc.Graph(figure=generalDashWrapper('level','Felony',boroughs,month_names,'Felonies','All Felonies','Felonies','line'))
                ]
            ),
            dcc.Tab(id='Misdemeanor', label='Misdemeanor Complaints',
                children=[
                dcc.Graph(figure=generalDashWrapper('level','Misdemeanor',boroughs,month_names,'Misdemeanors','All Misdemeanors','Misdemeanors','line'))
                ]
            ),
            dcc.Tab(id='Violation', label='Violation Complaints',
                children=[
                dcc.Graph(figure=generalDashWrapper('level','Violation',boroughs,month_names,'Violations','All Violations','Violations','line'))
                ]
            ),
            ###Notes found for the above graphs. See note at top.
            #####################################
            dcc.Tab(id='Types', label='Types of Crime',
                children=[
                dcc.Graph(figure=
                #This input could potentially be improved.
                {'data': [crimeTypeQueryToDash(off_desc_return(), 'bar', 'Types of Crime in New York')],
                'layout': {'title':'Types of Crime'}})
                ]
            ),
            ])
        ]),
    html.H2('Crime Clusters by Primary Description'),
    dcc.Dropdown(
        id='my-dropdown',
        options=drop_down_options,
        placeholder = "Select an Offense"
        # value=drop_down_options[0]['value']
    ),
    html.Iframe(id='output-container',srcDoc = initial_display, width = '100%', height = '600')])

@app.callback(
    dash.dependencies.Output('output-container', 'srcDoc'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_output(value):
    srcDoc = open('dash_package/map_storage/"{}".html'.format(value), 'r').read()
    return srcDoc
