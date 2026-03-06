#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv')

# Initialize Dash app
app = dash.Dash(__name__)

# Dropdown options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [i for i in range(1980, 2014)]

# Layout
app.layout = html.Div([
    html.H1('Automobile Sales Statistics Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),

    # Dropdown 1
    html.Div([
        html.Label("Select Report Type:"),
        dcc.Dropdown(
            id='select-stat',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a report type'
        )
    ]),

    # Dropdown 2
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=1980
        )
    ]),

    # Output container
    html.Div(id='output-container', className='chart-grid', style={'padding': '20px'})
])

# -----------------------------------------------------------
# CALLBACK 1 — Enable/Disable Year Dropdown
@app.callback(
    Output('select-year', 'disabled'),
    Input('select-stat', 'value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# -----------------------------------------------------------
# CALLBACK 2 — Update Graphs
@app.callback(
    Output('output-container', 'children'),
    [Input('select-stat', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):

    # -------------------------------------------------------
    # RECESSION REPORT
    if selected_statistics == 'Recession Period Statistics':

        recession_data = data[data['Recession'] == 1]

        # Plot 1 — Yearly recession sales
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec,
                           x='Year',
                           y='Automobile_Sales',
                           title="Average Automobile Sales Fluctuation During Recession")
        )

        # Plot 2 — Avg vehicles sold by type
        avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(avg_sales,
                          x='Vehicle_Type',
                          y='Automobile_Sales',
                          title="Average Vehicles Sold by Vehicle Type During Recession")
        )

        # Plot 3 — Pie chart expenditure share
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
                          names='Vehicle_Type',
                          values='Advertising_Expenditure',
                          title="Advertising Expenditure Share by Vehicle Type During Recession")
        )

        # Plot 4 — Effect of unemployment rate
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data,
                          x='unemployment_rate',
                          y='Automobile_Sales',
                          color='Vehicle_Type',
                          labels={'unemployment_rate': 'Unemployment Rate',
                                  'Automobile_Sales': 'Average Automobile Sales'},
                          title='Effect of Unemployment Rate on Vehicle Type and Sales')
        )

        return [
            html.Div(className='chart-item',
                     children=[html.Div(R_chart1), html.Div(R_chart2)],
                     style={'display': 'flex'}),

            html.Div(className='chart-item',
                     children=[html.Div(R_chart3), html.Div(R_chart4)],
                     style={'display': 'flex'})
        ]

    # -------------------------------------------------------
    # YEARLY REPORT
    elif input_year and selected_statistics == 'Yearly Statistics':

        yearly_data = data[data['Year'] == input_year]

        # Plot 1 — Yearly sales (whole period)
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas,
                           x='Year',
                           y='Automobile_Sales',
                           title='Yearly Automobile Sales (1980–2013)')
        )

        # Plot 2 — Monthly sales for selected year
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas,
                           x='Month',
                           y='Automobile_Sales',
                           title='Total Monthly Automobile Sales')
        )

        # Plot 3 — Avg vehicles sold by type
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata,
                          x='Vehicle_Type',
                          y='Automobile_Sales',
                          title=f'Average Vehicles Sold by Vehicle Type in {input_year}')
        )

        # Plot 4 — Pie chart advertising expenditure
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data,
                          names='Vehicle_Type',
                          values='Advertising_Expenditure',
                          title=f'Advertising Expenditure by Vehicle Type in {input_year}')
        )

        return [
            html.Div(className='chart-item',
                     children=[html.Div(Y_chart1), html.Div(Y_chart2)],
                     style={'display': 'flex'}),

            html.Div(className='chart-item',
                     children=[html.Div(Y_chart3), html.Div(Y_chart4)],
                     style={'display': 'flex'})
        ]

    else:
        return None

# Run app
if __name__ == '__main__':
    app.run(debug=True)