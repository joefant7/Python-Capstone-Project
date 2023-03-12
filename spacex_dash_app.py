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

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div(),
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label':'All','value':'All'},
                                    {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                    {'label':'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                    {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'}],

                                value='All',
                                placeholder='Select Launch Site using Dropdown',
                                searchable=True),
                                html.Br(),
                                html.Div(id='message_launches'),


                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(min=0, max=10000, step=1000,marks={
                                    0:'0',2500:'2500',
                                    5000:'5000',
                                    7500:'7500'},
                                value=[min_payload, max_payload], id='payload-slider'),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart',component_property='figure'),
              Input(component_id='site-dropdown',component_property='value')
              )
def plot_chart(site_selection):
    #print('running callback')
    if site_selection=='All':
        outcomes=spacex_df.loc[spacex_df['class']==1,'Launch Site']
        nums=outcomes.value_counts()
        fig=px.pie(spacex_df['class'],values=nums,names=outcomes.unique())
    else:
        #print('recognizing that this is not all')
        df=spacex_df.loc[spacex_df['Launch Site']==site_selection]
        fig=px.pie(df['class'],values=df['class'].value_counts(),names=['Failure','Success'])        
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart',component_property='figure'),
    Output(component_id='message_launches',component_property='children'),
    [Input(component_id='site-dropdown',component_property='value'),Input(component_id='payload-slider',
                                                                        component_property='value')])
def scatterplot(site,slider_range):
    if site == 'All':
        df=spacex_df
        df2=df.loc[df['Payload Mass (kg)']>=slider_range[0]]
        df3=df2.loc[df2['Payload Mass (kg)']<=slider_range[1]]
        fig2=px.scatter(data_frame=df3, x='Payload Mass (kg)',y='class',color='Booster Version Category')
        message="Total successful launches by site."
    else:
        df=spacex_df.loc[spacex_df['Launch Site']==site]
        df2=df.loc[df['Payload Mass (kg)']>=slider_range[0]]
        df3=df2.loc[df2['Payload Mass (kg)']<=slider_range[1]]
        fig2=px.scatter(data_frame=df3,x='Payload Mass (kg)', y='class',color='Booster Version Category')
        message="Total successful lauches for "+site
        
        
    return fig2,message
# Run the app
if __name__ == '__main__':
    app.run_server()