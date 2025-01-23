# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
# import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown'
                                    , options=['All Sites', 'CCAFS LC-40', 'VAFB SLC-4E', 'KSC LC-39A', 'CCAFS SLC-40']
                                    , value='All Sites'
                                    , placeholder='Select a Launch Site here'
                                    , searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks={0:'0', 10000:'10000'},
                                                value=[min_payload, max_payload]
                                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                html.Br(),

                                dcc.Dropdown(
                                    id = 'booster-dropdown'
                                    , options=['v1.0', 'v1.1', 'FT', 'B4', 'B5']
                                    , value='v1.0'
                                ),
                                html.Br(),

                                html.Div(id='output-number'),
                                html.Br(),

                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
)
def get_pie_chart(entered_site, value):
    # return f'you have selected {entered_site}'
    if entered_site in 'All SitesSelect a Launch Site hereAllALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>=value[0]) & (spacex_df['Payload Mass (kg)']<=value[1])]
        fig = px.pie(filtered_df, values='class', names='Launch Site', title='Pie for All')
        return fig
    else:
        filtered_df=spacex_df[spacex_df['Launch Site']==entered_site]
        fig = px.pie(filtered_df, names='class', title='One for Pie')
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_chart(entered_site, value):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>=value[0]) & (spacex_df['Payload Mass (kg)']<=value[1])]
    if entered_site in 'All SitesSelect a Launch Site hereAllALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category'
        )
        return fig
    else:
        filtered_df=filtered_df[filtered_df['Launch Site']==entered_site]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category'
        )
        return fig

# @app.callback(
#     Output(component_id='success-pie-chart-2', component_property='figure'),
#     Input(component_id="payload-slider", component_property="value")
#     )
# def get_pie_chart_2(value):
#     # return f'you have selected {entered_site}'
#     filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>=value[0]) & (spacex_df['Payload Mass (kg)']<=value[1])]
#     fig = px.pie(filtered_df, values='class', names='Payload Mass (kg)', title='Pie for All')
#     return fig

@app.callback(
    Output(component_id='output-number', component_property='children'),
    Input(component_id='booster-dropdown', component_property='value')
)
def get_output_number(value):
    filtered_df = spacex_df[spacex_df['Booster Version Category']==value]
    # print(filtered_df.head())
    # print(filtered_df['class'].mean())
    return filtered_df['class'].mean()

# Run the app
if __name__ == '__main__':
    app.run_server()

'''
Which site has the largest successful launches?
- VAFB SLC-4E Has a successful 9,600kg launch
Which site has the highest launch success rate?
- CCAFS SLC-40 has 42.9% success rate
Which payload range(s) has the highest launch success rate?
- 3000-4000, 72%
Which payload range(s) has the lowest launch success rate?
- 6000-7000, 0%
Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest
launch success rate?
- B5, but only 1 launch

'''
