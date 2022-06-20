import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np
import logging


path = r'DatasetAtp.xlsx'

df = pd.read_excel(path)


player_options = [dict(label=player, value=player) for player in df['Winner'].unique()]
player_options2 = [dict(label=player, value=player) for player in df['Winner'].unique()]


app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    html.Div(
        className='h1_title',
        children=html.Div([
            html.H2('Professional Tennis Players Analysis from \n2015 to 2021'),
        ])
    ),

    html.Div(
        className='pies_row',
        children=html.Div([
            html.Div(
            className='pie_player1',
            children=html.Div([
                html.Label('Choose Player 1:'),
                html.Br(),
                dcc.Dropdown(options=player_options,
                            value='Nadal R.',
                            id='drop'),
                html.Br(),
                dcc.Graph(
                    id='pie_player_1'
                ),
            ])
        ),

        html.Div(
            className='pie_player2',
            children=html.Div([
                html.Label('Choose Player 2:'),
                html.Br(),
                dcc.Dropdown(options=player_options,
                            value='Djokovic N.',
                            id='drop2'),
                html.Br(),
                dcc.Graph(
                    id='pie_player_2'
                ),
            ])
        ),
        ])
    ),

    html.Br(),

    html.Div(
        className='evo_1v1_row',
        children=html.Div([
            html.Div(
                className='graph_player_evolution',
                children=html.Div([
                    html.H2('Check the win evolution of each player'),
                    dcc.Graph(
                        id='PlayerEvolution'
                    ),
                ])
            ),

            html.Div(
                className='1v1',
                children=html.Div([
                    html.H2(
                        'H2H'
                    ),
                    html.Div(id='div')
                ])
            )
        ])
    ),

])

@app.callback(
    Output(component_id='pie_player_1', component_property='figure'),
    [Input(component_id='drop', component_property='value')]
)
def callback_1(input1):
    pielabels = ['Wins', 'Defeats']
    pievalues2 = df['Winner'][(df['Winner'] == input1)].count(), df['Loser'][(df['Loser'] == input1)].count()
    colors = ['lightgreen','tomato']

    pie_chart = dict(type='pie',
                     labels=pielabels,
                     values=pievalues2,
                     name='Pie Chart',
                     )

    pie_chart_layout = dict(title=dict(text='Wins vs Defeats'))


    fig = go.Figure(data=pie_chart, layout=pie_chart_layout)

    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                         marker=dict(colors=colors, line=dict(color='#000000', width=2)))

    return fig

@app.callback(
    Output(component_id='pie_player_2', component_property='figure'),
    [Input(component_id='drop2', component_property='value')]
)
def callback_2(input2):
    pie2labels = ['Wins', 'Defeats']
    pie2values2 = df['Winner'][(df['Winner'] == input2)].count(), df['Loser'][(df['Loser'] == input2)].count()
    colors = ['lightgreen','tomato']


    pie_chart2 = dict(type='pie',
                     labels=pie2labels,
                     values=pie2values2,
                     name='Pie Chart')

    pie_chart_layout2 = dict(title=dict(text='Wins vs Defeats'))

    fig = go.Figure(data=pie_chart2, layout=pie_chart_layout2)

    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                         marker=dict(colors=colors, line=dict(color='#000000', width=2)))

    return fig

@app.callback(
    Output('PlayerEvolution', 'figure'),
    [Input('drop', 'value'),
     Input('drop2', 'value')]
)

def update_graph(input1, input2):

    for x in [df['Winner'] == input1]:
        v = 0
        int_list = [v := v + b for b in x]

    for x in [df['Winner'] == input2]:
        v = 0
        int_list2 = [v := v + b for b in x]



    #fig = px.line(df, x="Date", y=[int_list,int_list2])

    fig = px.line(df, x="Date", y=[])

    fig.add_trace(go.Scatter(x=df['Date'], y=int_list, name=input1,
                             line=dict(color='black', width=4, dash='dot')))
    fig.add_trace(go.Scatter(x=df['Date'], y=int_list2, name=input2,
                             line=dict(color='darkblue', width=4, dash='dot')))


    fig.update_layout(title='Comparison of victories between players',
                      xaxis_title='Date',
                      yaxis_title='Total of Wins')

    return fig

@app.callback(
    Output(component_id='div', component_property='children'),
    [Input(component_id='drop', component_property='value')],
    [Input(component_id='drop2', component_property='value')]
)

#def update_output_div(input_value1, input_value2):

#    for ind in df.index:
#        if df['Winner'][ind] == input_value1 and df['Loser'][ind] == input_value2:
#            return df.iloc[ind]['Location'], ': ', df.iloc[ind]['Wsets'], '-', df.iloc[ind]['Lsets']

def update_output_div(input_value1, input_value2):
    res = []
    for ind in df.index:
        if df['Winner'][ind] == input_value1 and df['Loser'][ind] == input_value2:
            res.append("{}/{}/{} {}: {}-{}".format(df.iloc[ind]['Day'],df.iloc[ind]['Month'],df.iloc[ind]['Year'],df.iloc[ind]['Location'], round(df.iloc[ind]['Wsets']),
                                            round(df.iloc[ind]['Lsets']))+"\n")

            #res.append(f"\r\n{df.iloc[ind]['Location']}: {round(df.iloc[ind]['Wsets'])}-{round(df.iloc[ind]['Lsets'])}" + "\n")
    return res




if __name__ == '__main__':
    app.run_server(debug=True)




