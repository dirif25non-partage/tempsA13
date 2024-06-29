import dash,os,flask
from dash import dcc,dash_table,html,callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import datetime,timedelta
import gunicorn   
import plotly.graph_objects as go
from google.cloud import bigquery
dash.register_page(__name__,name='Dernières 24 heures',order=1)
          
client = bigquery.Client()
table =client.dataset("temps_google").table("A13-2024")
query = "SELECT * from `tempsparcours.temps_google.A13-2024` "
rows=client.query(query).result()
rowsTab=[list(row) for row in rows]
df=pd.DataFrame(rowsTab)
df.columns=['od','date','temp' ]
df['dt']= pd.to_datetime('24'+ df['date'],format='%y%m%d%H%M')
df['od']=df['od'].str.split('-t').apply(lambda x:x[0])
df['temp']=df['temp'].astype(int)
ods={
    "odsY":['PtChatillon-Versailles-Cht',  'PtAuteuil-Versailles-Cht', 'PontNeuilly-StGermainLay','PtAuteuil-StGermainLay'],
    "odsW":['Versailles-Cht-PtChatillon', 'Versailles-Cht-PtAuteuil', 'StGermainLay-PontNeuilly', 'StGermainLay-PtAuteuil']
}
dateNow=datetime.now().replace( minute=0)
d24=dateNow-timedelta(1)
dg=df[df['dt']>d24]
dg['tt']=dg['dt']-d24
dg['tt']=(dg['tt'].dt.total_seconds()/60).astype(int)
def generate_gr(sens):
    odsZ=ods[sens]
    heureNow=dateNow.hour+2
    fig = go.Figure()
    for k in range(4):
        od= odsZ[k]
        dgo=dg[dg['od']==od]
        x=dgo['tt']
        y=(dgo['temp']/60)
        fig.add_trace(go.Scatter(x= x, y= y,
                mode='markers',
                hoverinfo='none',
                name=od,
                marker=dict(
                    color=['#f44','#37f','#4a4','#948'][k],
                    size=15,
                )
        ))
    fig.update_layout(
        width=1200,height=600,
        margin=dict(l=20, r=40, t=0, b=0),
        yaxis = dict(title='Minutes',  fixedrange=True),
        xaxis = dict(
            title='Dernières 24 heures',
            tickmode = 'array',
            tickvals = [(i+1)*60 for i in range(24)],
            ticktext=[str(i)+'h' for i in range(heureNow+1,25)]+[str(i)+'h' for i in range(1,heureNow+2)],
            range=[0,25*60]
        )
    )
    return dcc.Graph(figure=fig,config={'displayModeBar': False })

layout = html.Div([
        html.P("""Ce graphique est mis à jour toutes les 15 minutes, de 6h à 22h, avec les dernières estimations
             des temps de parcours point à point.   
                  """, 
        style={'marginLeft': 90,'marginRight': 150, 'marginTop': 0}),        
        dbc.Row([
            dbc.Col( '  ' , width=1),
            dbc.Col(html.Label('Sens:', style={'text-align': 'center' }), width=1),
            dbc.Col(dcc.Dropdown(
            id='sens-dropdown',
            options=[{'label': kL, 'value': kV} for (kL,kV) in [('Province vers Paris','odsW'),('Paris vers Province','odsY')]],
            value='odsW'
            ), width=3),  
                   ]),    

        dbc.Row(id='display-gr2', children=[generate_gr('odsW')]),
        html.Hr(),
        dbc.Row(html.Img(src=r'assets/point5_A13.jpg', alt='image',
                 style={'height':'50%', 'width':'50%'}),
                   justify='center', align='center'),
])


@callback( Output('display-gr2', 'children'),
    Input('sens-dropdown', 'value'),prevent_initial_callbacks=True)
def met_a_jour(sens):
    return html.Div(children=[generate_gr(sens)])
