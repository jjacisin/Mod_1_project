from flask import render_template

from dash_package.dash_crime_models import Crime_Event, Victim, Suspect,Location
import pdb
from dash_package import server

#JJ: decorators are for Flask, so 'server' is referenced rather than 'app'
@server.route('/first_complaint')
def render_apartments():
    crime = Crime_Event.query.first()
    return crime.complaint_num
    # return render_template('index.html', apartments = apartments)
