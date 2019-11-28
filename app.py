import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd

# Dataset Processing

df = pd.read_csv('emission_full.csv')
data = df.loc[df['country_name'] == 'Portugal'][['year', 'CO2_emissions']].values
x = data[:, 0]
y = data[:, 1]

# Building our Graphs

data = [dict(type='scatter', x=x, y=y)]

fig = go.Figure(
    data=data,
    layout_title_text="Portugal's Emissions over 25 years",
    layout_xaxis_title='Years',
    layout_yaxis_title='CO2 Emissions'
)

# The App itself

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(children=[
    html.H1(children='My First DashBoard'),

    html.Div(children='''
        Example of html Container
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
