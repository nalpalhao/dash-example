#!/usr/bin/env python
# coding: utf-8

# In[3]:

# In[72]:


import numpy as np 
import pandas as pd 
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash import Dash



# In[73]:


covid_impact = pd.read_csv (r'WHRData2021.csv')
covid_impact.head()


# In[74]:


covid_impact.describe()


# In[75]:


covid_impact.isna().sum()


# In[76]:


covid_impact2= covid_impact.drop(['All-cause death count, 2017','All-cause death count, 2018','All-cause death count, 2019','All-cause death count, 2020','Excess deaths in 2020 per 100,000 population, relative to 2017-2019 average'] , axis=1)

covid_impact2.head()


# In[77]:


covid_impact2.dropna(inplace=True)

covid_impact2.isnull().sum()


# In[78]:


# dar a descobrir algumas variáveis


# In[79]:


#teste


fig = px.scatter(covid_impact2, 
                 x='Median age', 
                 y='Gini coefficient of income', 
                 color='Country name',
                 trendline='ols',
                 trendline_scope='overall',
                 trendline_color_override='black'
                )
fig.show()


# In[80]:


data = covid_impact2.loc[:,['Country name','Population 2020','Population 2019']].sort_values(by='Population 2019',
                                                                                   ascending=False).head(10)

# plotting go figure for grouped bar chart

fig2 = go.Figure(data=[go.Bar(name='Population 2019',x=data['Country name'],y=data['Population 2019']),
                      go.Bar(name='Population 2020',x=data['Country name'],y=data['Population 2020'])
                     ])

fig2.update_layout(barmode='group', title_text='Top10 countries with most population')
fig2.show()


# In[81]:


data = covid_impact2.loc[:,['Country name','Population 2020','COVID-19 deaths per 100,000 population in 2020']].sort_values(by='COVID-19 deaths per 100,000 population in 2020',
                                                                                   ascending=False).head(10)

# plotting go figure for grouped bar chart

fig3 = go.Figure(data=[go.Bar(name='COVID-19 deaths per 100,000 population in 2020',x=data['Country name'],y=data['COVID-19 deaths per 100,000 population in 2020']),
                      go.Bar(name='Population 2020',x=data['Country name'],y=data['Population 2020'])
                     ])

fig3.update_layout(barmode='group', title_text='teste')
fig3.show()


# In[82]:


covid_impact2.info()


# In[83]:


covid_impact2['Female head of government'].value_counts()


# In[84]:


# Pie chart, where the slices will be ordered and plotted counter-clockwise:
#labels = 'Female', 'Male'
#sizes = [23, 140]
#explode = (0, 0)  

#fig1, ax1 = plt.subplots()
#ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
 #       shadow=True, startangle=90)
#ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

#plt.show()


# In[70]:


#plt.figure(figsize=(12,12))
#sns.heatmap(covid_impact2.corr(), 
#            vmin=-1, 
 #           vmax=1, 
  #          annot=True)

#plt.title('correlation matrix of dataset')
#plt.show()


#App itself

app = dash.Dash(__name__)

server = app.server

#test
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











