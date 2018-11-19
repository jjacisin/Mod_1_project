from dash_package.dash_queries import *
import dash
from dash.dependencies import Input, Output
# from folium import Iframe
# from dash_package.robbery_locations_1K import *




initial_display = open('dash_package/map_storage/initial_map.html', 'r').read()

app.layout = html.Div([
    html.H1('NYC Crime Data - 1H 2018'),
    html.Div([
        html.H2('Crime by Level of Offense'),
        dcc.Tabs(id="tabs", children=[
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
                dcc.Graph(figure=
                {'data': level_graph_creator_all("Felony")+level_graph_all_boroughs(boroughs,month_names,"Felony"),
                'layout': {'title':'Felonies'}})
                ]
            ),
            dcc.Tab(id='Misdemeanor', label='Misdemeanor Complaints',
                children=[
                dcc.Graph(figure=
                {'data': level_graph_creator_all("Misdemeanor")+level_graph_all_boroughs(boroughs,month_names,"Misdemeanor"),
                'layout': {'title':'Misdemeanors'}})
                ]
            ),
            dcc.Tab(id='Violation', label='Violation Complaints',
                children=[
                dcc.Graph(figure=
                {'data': level_graph_creator_all("Violation")+level_graph_all_boroughs(boroughs,month_names,"Violation"),
                'layout': {'title':'Violations'}})
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


#
# app.layout = html.Div(
#     children=[
#     dcc.Tabs(id="tabs", children=[
#         dcc.Tab(id='NYC', label='Crimes by Borough',
#             children=[
#             dcc.Graph(figure=
#             {'data': crime_graph_creator()+crime_graph_all_boroughs(boroughs,month_names),
#             'layout': {'title':'All Complaints'},
#             })
#             ]
#         ),
#         dcc.Tab(id='Felony', label='Felony Complaints',
#             children=[
#             dcc.Graph(figure=
#             {'data': level_graph_creator_all("Felony")+level_graph_all_boroughs(boroughs,month_names,"Felony"),
#             'layout': {'title':'Felonies'}})
#             ]
#         ),
#         dcc.Tab(id='Misdemeanor', label='Misdemeanor Complaints',
#             children=[
#             dcc.Graph(figure=
#             {'data': level_graph_creator_all("Misdemeanor")+level_graph_all_boroughs(boroughs,month_names,"Misdemeanor"),
#             'layout': {'title':'Misdemeanors'}})
#             ]
#         ),
#         dcc.Tab(id='Violation', label='Violation Complaints',
#             children=[
#             dcc.Graph(figure=
#             {'data': level_graph_creator_all("Violation")+level_graph_all_boroughs(boroughs,month_names,"Violation"),
#             'layout': {'title':'Violations'}})
#             ]
#         ),
#         ])
#     ]
# )
