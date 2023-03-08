# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 20:36:04 2023

@author: LeopoldPL
"""

import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
import datetime as dt
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# Read the CSV file
data = pd.read_csv('C:/Users/LeopoldPL/Desktop/testprojet.csv', index_col=0, parse_dates=True,sep=',')
data['price;'] = data['price;'].str.replace(';', '')
data['price;'] = data['price;'].str.replace('?', '')
data['price;'] = pd.to_numeric(data['price;'], errors='coerce') # converting to numeric data
#today = dt.datetime.now().strftime('%Y-%m-%d')
today=dt.datetime(2023, 3, 7).strftime('%Y-%m-%d')
#yesterday
#yesterday = today - dt.timedelta(days=1)

daily_data = data.loc[today]
# Calculate the volatility of the prices
daily_data['volatility'] = daily_data['price;'].pct_change()
daily_data['evolution'] = data['price;'].astype(float).pct_change(periods=1)
# Create the dashboard report
fig = go.Figure()
fig.add_trace(go.Scatter(x=daily_data.index, y=daily_data['price;'], name='Price'))
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=daily_data.index, y=daily_data['volatility'], name='Volatility'))
#fig.add_trace(go.Scatter(x=daily_data.index, y=daily_data['evolution'], name='Evolution'))
fig.update_layout(title='Daily Financial Report', xaxis_title='Date', yaxis_title='price')
fig3.update_layout(xaxis_title='Date', yaxis_title='volatility')


# Create a Plotly figure
fig2 = px.line(data, x=data.index, y='price;') #price graph

# Create the Dash app
app = dash.Dash()


app.layout = html.Div(children=[
    html.H1(children='Price Dashboard'),
    html.Div(children=[
        dcc.Graph(id='daily-report', figure=fig2),
        dcc.Graph(id='graph', figure=fig),
        dcc.Graph(id='',figure=fig3)
    ])
])

# Define the callback function to update the graph with new data
@app.callback(Output('graph', 'figure'), [Input('interval-component', 'n_intervals')])
def update_graph(n):
    # Read the CSV file
    data = pd.read_csv('C:/Users/LeopoldPL/Desktop/testpourprojet.csv', index_col=0, parse_dates=True, sep=';')

    # Create a new Plotly figure
    fig = px.line(data, x=data.index, y='price')

    # Return the updated figure
    return fig

# Start the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

