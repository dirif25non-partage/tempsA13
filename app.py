import dash,os,flask
from dash import dcc,dash_table,html
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

server = flask.Flask(__name__)
app = dash.Dash(    __name__,    server=server, routes_pathname_prefix='/',
          external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
app.title = "Temps de parcours A13"

app.layout = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col(  dcc.Link(f"{page['name']}", href=page["relative_path"]) , width=6)        
         for page in dash.page_registry.values()])
    ]),
    dash.page_container
])

if __name__ == '__main__':
   app.run_server(debug=True)

