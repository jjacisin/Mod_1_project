local_server_ip = '127.0.0.1'
port = '8050'
from dash_package import *

app.run_server(debug = True,host=local_server_ip,port=port)

webbrowser.open_new('{}:{}/dashboard/'.format(local_server_ip,port))
