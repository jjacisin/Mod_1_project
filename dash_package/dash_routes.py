from flask import render_template

from dash_package.dash_crime_models import Crime_Event, Victim, Suspect,Location
import pdb
from dash_package import server

#JJ: decorators are for Flask, so 'server' is referenced rather than 'app'
@server.route('/first_complaint')
def render_apartments():
    crime = Crime_Event.query.first()
    return str(crime.complaint_num)

@server.route('/test')
def render_apartments_2():
    crime = Crime_Event.query.first()
    return str(crime.complaint_num)
