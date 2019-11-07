import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go



app = dash.Dash(__name__)

df = pd.read_csv('DV_data.csv')
available_indicators = df.columns

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='total'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Waste (MtCO2e)'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style=dict(width='48%', float='right', display='inline-block'))
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    )
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    filtered_df = df[df['Year'] == year_value]

    data = [go.Scatter(dict(
        y=filtered_df.loc[filtered_df['region-wb'] == i][yaxis_column_name],
        x=filtered_df.loc[filtered_df['region-wb'] == i][xaxis_column_name],
        text=filtered_df.loc[df['region-wb'] == i]['Country'],
        mode='markers',
        marker=dict(size=15, opacity=0.5, line=dict(width=0.5, color='white')),
        name=i
    )) for i in filtered_df['region-wb'].unique()]

    fig = go.Figure(data=data,
                    layout_xaxis=dict(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log'),
                    layout_yaxis=dict(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log'),
                    layout_margin=dict(l=40, b=40, t=10, r=0),
                    layout_hovermode='closest')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
