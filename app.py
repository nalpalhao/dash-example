import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

df_1 = pd.read_csv('DV_data.csv')

app = dash.Dash(__name__)

fig = px.choropleth(df_1, locations='iso-a3', color='total', projection='orthographic', animation_frame='Year', title='El Mundo')

server = app.server

app.layout = html.Div([
    dcc.Graph(
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
