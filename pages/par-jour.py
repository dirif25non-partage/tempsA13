import dash,os,flask
from dash import dcc,dash_table,html,callback
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
import gunicorn   
import plotly.graph_objects as go
dash.register_page(__name__,name='Temps de parcours, du 4 au 17 juin',order=0)

dg0=pd.read_csv('./pages/data.csv')
lstOD=list(dg0['od'].unique())
def generate_graph(od):
  dg=dg0[dg0['od']==od]
  x=list(range(4,18))    
  fig = go.Figure()
  for k in range(3):
    y=dg[dg['prd']==k].groupby('d')['dit'].mean()
    fig.add_trace(go.Scatter(x= x, y= y,mode='markers',hoverinfo='none',
    marker=dict(
       color=['#f99','#9f9','#99f'][k],
       size=20,
      ),
     name=['HPM-6:10h','HC-10:16h','HPS-16:20h'][k]))
    fig.update_layout(
    margin=dict(l=20, r=0, t=0, b=0),
    autosize=True,
    height=600,
    yaxis = dict(title='Minutes', 
                 fixedrange=True),
    xaxis = dict(
        title='Jours du mois de juin',
        tickmode = 'array',
        tickvals = x,
    )
  )
  return dcc.Graph(figure=fig,config={'displayModeBar': False })

layout = html.Div([
        html.P("""On a enregistré les temps de parcours sur 8 relations Origine / Destination concernées par la fermeture de l'A13.
        Les graphiques permettent de visualiser les temps moyens pour 3 périodes horaires, 6-10h, 10-16h & 16-20h.
        """, 
        style={'marginLeft': 90,'marginRight': 150, 'marginTop': 0}),        
        dbc.Row([
            dbc.Col( '  ' , width=1),
            dbc.Col(html.Label('OD:', style={'text-align': 'center' }), width=1),
            dbc.Col(dcc.Dropdown(
            id='od-dropdown',
            options=[{'label': k, 'value': k} for k in lstOD],
            value='Versailles-Cht-PtAuteuil'
            ), width=3),  
                   ]),    

        dbc.Row(id='display-gr', children=[generate_graph('Versailles-Cht-PtAuteuil')]),
        html.Hr(),
        dbc.Row(html.Img(src=r'assets/point5_A13.jpg', alt='image',
                 style={'height':'50%', 'width':'50%'}),
                   justify='center', align='center'),
])

@callback( Output('display-gr', 'children'),
    Input('od-dropdown', 'value'),prevent_initial_callbacks=True)
def met_a_jour(od):
    return html.Div(children=[generate_graph(od)])

