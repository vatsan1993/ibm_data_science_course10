# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create a dash application
app = dash.Dash(__name__)
# print(spacex_df.columns)
launch_sites = set(spacex_df['Launch Site'])

options = [{'label': 'All Sites', 'value': 'ALL'}]
options.extend([{'label':site, 'value': site} for site in launch_sites])
# print(options)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                    options = options,
                                    value='ALL',
                                    placeholder="Select a launch site",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range

                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(0, 10000, 1000, value = [min_payload, max_payload], id='payload-slider'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# # Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@dash.callback(
    Output(component_id = 'success-pie-chart', component_property = 'figure'),
    Input(component_id = 'site-dropdown', component_property = 'value')
)
def update_pie_chart(site_value):
    print(site_value)
    if site_value in launch_sites:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site_value]
        success_counts = filtered_df['class'].value_counts()
        print(success_counts.head())
        pie_chart = px.pie(success_counts, values=success_counts.values, names=success_counts.index, title='Success vs. Failed Counts for'+ site_value)
        return pie_chart
    elif site_value == 'ALL':
        success_counts = spacex_df['Launch Site'].value_counts()
        print(success_counts)
        pie_chart = px.pie(success_counts, values=success_counts.values, names=success_counts.index, title='Success vs. Failed Counts for All Sites')
        return pie_chart



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@dash.callback(
    Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
    [
        Input(component_id = 'site-dropdown', component_property = 'value'),
        Input(component_id = 'payload-slider', component_property = 'value')
    ]
)
def update_scatter_chart(site_value, slider_value):
    print(slider_value)
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= slider_value[0]) & (spacex_df['Payload Mass (kg)'] <= slider_value[1])]
    if site_value != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == site_value]
    scatter_chart = px.scatter(filtered_df, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category', title = f'Correlation between Payload and Success for {site_value}')

    return scatter_chart


# Run the app
if __name__ == '__main__':
    app.run_server(debug = True)
