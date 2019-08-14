import dash
from dash_package.flask_init import *

app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

from dash_package.dash_dashboard import *
import webbrowser
