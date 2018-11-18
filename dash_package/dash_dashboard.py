from dash_package.dash_queries import *
# from folium import Iframe
# from dash_package.robbery_locations_1K import *






app.layout = html.Div([
    html.H1('NYC Crime Clusters'),
    dcc.Dropdown(
        id='my-dropdown',
        options=drop_down_options,
        placeholder = "Select an Offense"
        # value=drop_down_options[0]['value']
    ),
    html.Div(id='output-container'),
    html.Iframe(id='output-container',srcDoc = open('ROBBERY.html', 'r').read(), width = '100%', height = '600')])

@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


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
