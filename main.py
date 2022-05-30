import dash
import dash_bootstrap_components as dbc
import nav as nav
import pandas as pd
import numpy as np
import plotly.express as px

from dash.dependencies import Output, Input
from IPython.display import display
from dash import html
from dash import dcc
from random import randint

# settings
from matplotlib import pyplot as plt

pd.options.plotting.backend = "plotly"

# # stack makes the table taller by grouping certain datas
# # reset_index shifts the index to the dataframe as a separate column
# df = df.stack().reset_index()
# print(df[:15])
#
# read from CSV file
df = pd.read_excel("mystocks.xlsx")

# to print first 15 entries of data
# print(df[:15])

# convert date to format
df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')

# initial dataframe for ball contacts
dates = [x for x in sorted(df['Date'].unique())]
default_ball_contact_data = {'Date': [], 'Total Contact': []}
for date in dates:
    df1 = df.copy()
    df1 = df1[df1['Date'] == date]
    totalContact = 0
    for index, row in df1.iterrows():
        totalContact += int(row['Total Contacts'])
    default_ball_contact_data['Date'].append(date)
    default_ball_contact_data['Total Contact'].append(totalContact)
y_mean = [np.mean(default_ball_contact_data['Total Contact'])] * len(default_ball_contact_data['Date'])
df_ball_contacts = pd.DataFrame(default_ball_contact_data)
fig, ax = plt.subplots()

# Plot the data
data_line = ax.plot(df_ball_contacts['Date'], df_ball_contacts['Total Contact'], label='Data', marker='o')

# Plot the average line
mean_line = ax.plot(df_ball_contacts['Date'], y_mean, label='Mean', linestyle='--')

# Make a legend
legend = ax.legend(loc='upper right')
ball_contact_graph = df_ball_contacts.plot(x='Date', y='Total Contact', title="Total ball contacts of players by date")
ball_contact_graph.add_scatter(x=default_ball_contact_data['Date'], y=y_mean, name='Average')

# card for ball contacts graph
card_ball_contacts = dbc.Card([
    dbc.CardBody([
        html.H6("Select date to get detailed view of player contacts on that date", className="card-subtitle"),
        html.Br(),
        dcc.Dropdown(id="fst-dpdn", multi=False, value='',
                     options=[{'label': x, 'value': x}
                              for x in dates]),
        dcc.Graph(id='ball-contact-fig', figure={})
    ])
],
    className="card bg-light mb-3"
)

# Getting unique names in dataset
names = [x for x in df['Player Name'].unique()]

# dataframe for left contacts
data_for_left_right_contacts = []
for name in names:
    left_contacts = 0
    right_contacts = 0
    totalContact = 0
    df_name = df[df['Player Name'] == name]
    for value in df_name['Left Contacts'].values:
        left_contacts += int(value)
    for value in df_name['Right Contacts'].values:
        right_contacts += int(value)
    totalContact = left_contacts + totalContact
    new_entry = [name, left_contacts, right_contacts, totalContact]
    data_for_left_right_contacts.append(new_entry)

df_ball_contacts_left_right = pd.DataFrame(data_for_left_right_contacts,
                                           columns=['Player Name', 'Left', 'Right', 'Total Contact'])
df_ball_contacts_left_right = df_ball_contacts_left_right.sort_values(by='Total Contact', ascending=False)
most_contacts_array = [x for x in df_ball_contacts_left_right['Player Name']]

# Card for left and right contacts
card_ball_contacts_left_right = dbc.Card([
    dbc.CardBody([
        html.H6("Use dropdown to add players to the graph", className="card-subtitle"),
        html.Br(),
        dcc.Dropdown(id="snd-dpdn", multi=True, value=[x for x in most_contacts_array[:5]],
                     options=[{'label': x, 'value': x}
                              for x in most_contacts_array]),
        dcc.Graph(id='ball-contact-left-right-fig', figure={})
    ])
],
    className="card bg-light mb-3"
)

# dataframe for frequency of names appearing in dataset
data_for_frequency = []
for name in names:
    df_copy = df[df['Player Name'] == name]
    freq = df_copy.count()[0]
    avg_time_use = np.mean(df_copy['Time spent (mins)'])
    new_entry = [name, freq, np.round(avg_time_use, 2)]
    data_for_frequency.append(new_entry)

df_frequency = pd.DataFrame(data_for_frequency, columns=['Player Name', 'Frequency', 'Average Time Spent(mins)'])
df_frequency = df_frequency.sort_values(by='Frequency', ascending=False)
freq_array_names = [x for x in df_frequency['Player Name']]

# Card for frequency of use
card_frequency = dbc.Card([
    dbc.CardBody([
        html.H6("Use dropdown to add players to the graph", className="card-subtitle"),
        html.Br(),
        dcc.Dropdown(id="thrd-dpdn", multi=True, value=[x for x in freq_array_names[:5]],
                     options=[{'label': x, 'value': x}
                              for x in freq_array_names]),
        dcc.Graph(id='freq-fig', figure={})
    ])
],
    className="card bg-light mb-3"
)

# data for player in format (player, date)
data_for_player_date = []
for name in names:
    df_name_date = df[df['Player Name'] == name]
    new_entry = [name, [x for x in df_name_date['Date']]]
    data_for_player_date.append(new_entry)
array_player_date = []
for i in range(0, len(data_for_player_date)):
    for date in data_for_player_date[i][1]:
        entry = [data_for_player_date[i][0], date]
        array_player_date.append(entry)

# Card for video
card_video = dbc.Card([
    dbc.CardBody([
        html.H6("Select player and date to view training video", className="card-subtitle"),
        html.Br(),
        dcc.Dropdown(id="fifth-dpdn", multi=False, value=index,
                     options=[{'label': x[0] + " " + x[1], 'value': index}
                              for index, x in enumerate(array_player_date)]),
        html.Br(),
        html.Center([html.Div(id="vid-div")])
    ])
],
    className="card bg-light mb-3"
)

# Data for ball speed and rotation
data_for_ball_speed_rotation = []
for name in names:
    df_speed = df[df['Player Name'] == name]
    avg_ball_speed = np.mean(df_speed['Average Ball Speed(mph)'])
    avg_ball_rotation = np.mean(df_speed['Average Ball Rotation(rpm)'])
    new_entry = [name, np.round(avg_ball_speed, 2), np.round(avg_ball_rotation, 2)]
    data_for_ball_speed_rotation.append(new_entry)

df_ball_speed_rotation = pd.DataFrame(data_for_ball_speed_rotation,
                                      columns=['Player Name', 'Average Ball Speed(mph)', 'Average Ball Rotation(rpm)'])

# dataframe for speed
df_speed = df_ball_speed_rotation.copy()
df_speed = df_speed.sort_values(by='Average Ball Speed(mph)', ascending=False)
array_name_speed = [x for x in df_speed['Player Name']]

# dataframe for rotation
df_rotation = df_ball_speed_rotation.copy()
df_rotation = df_rotation.sort_values(by='Average Ball Rotation(rpm)', ascending=False)
array_name_rotation = [x for x in df_rotation['Player Name']]

# card for ball speed and rotation
card_speed_rotation = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Ball Speed", tab_id="tab-speed"),
                    dbc.Tab(label="Ball Rotation", tab_id="tab-rotation"),
                ],
                id="card-tabs",
                active_tab="tab-speed",
            )
        ),
        dbc.CardBody([
            html.H6("Use dropdown to add players to the graph", className="card-subtitle"),
            dcc.Dropdown(id="frth-dpdn", multi=True),
            dcc.Graph(id='speed-rotation-fig', figure={}, className="h-100")
        ],
            className="card bg-light mb-3"
        )
    ], style={'margin-left': '20px'}
)

# card group
cards = dbc.CardGroup([card_frequency, card_speed_rotation])

# meta_tags is for mobile scaling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# Layout section: BootStrap
# ----------------------------------------------------

# dbc.Row for how each row and dbc.Col for each column
# for className, consult the cheatsheet in Google Docs
# fluid=False means got space on right & left, if True means you stretch all the way
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div([html.H1("MiniSoccerBal 3.0 Dashboard", className="text-center mb-4")],
                         className="p-3 mb-2 bg-secondary text-white"), width=12)
    ]),
    # using for loop to populate options for dropdown based on Excel column 'Symbols'
    dbc.Row([
        dbc.Col([
            card_ball_contacts
        ], width={'size': 6}),
        dbc.Col([
            card_ball_contacts_left_right
        ], width={'size': 6})
    ]),
    dbc.Row([cards]),
    dbc.Row([
        dbc.Col([
            card_video
        ], width={'size': 6})
    ], align="center",
        justify="center", )
], fluid=False)


# App callbacks
# ----------------------------------------------------

# Ball contact callback
@app.callback(
    Output("ball-contact-fig", component_property="figure"),
    Input("fst-dpdn", component_property="value")
)
def update_ball_contact_graph(date):
    if date == '' or date is None:
        return ball_contact_graph
    else:
        dff = df.copy()
        dff = dff[dff['Date'] == date]
        names = dff['Player Name'].unique()
        data = []
        for name in names:
            totalContact = 0
            dff_name = dff[dff['Player Name'] == name]
            for index, row in dff_name.iterrows():
                totalContact += int(row['Total Contacts'])
            new_entry = [name, totalContact]
            data.append(new_entry)
        df_contacts_by_date = pd.DataFrame(data, columns=['Player Name', 'Total Contacts'])
        df_contacts_by_date = df_contacts_by_date.sort_values(by='Total Contacts', ascending=True)
        fig = df_contacts_by_date.plot(x="Player Name", y="Total Contacts")
        return fig


# Left right contact callbacks
@app.callback(
    Output('ball-contact-left-right-fig', component_property="figure"),
    Input("snd-dpdn", component_property="value")
)
def update_left_right_graph(names):
    df_copy = df_ball_contacts_left_right.copy()
    df_copy = df_copy[df_copy['Player Name'].isin(names)]
    bar_chart_left_right = df_copy.plot.bar(x='Player Name', y=['Left', 'Right'], labels={'value': 'Contacts'},
                                            title="Top 5 players in terms of ball contacts and their distribution",
                                            text_auto=True, )
    return bar_chart_left_right


# Frequency callbacks
@app.callback(
    Output('freq-fig', component_property="figure"),
    Input("thrd-dpdn", component_property="value")
)
def update_freq_graph(names):
    df_copy = df_frequency.copy()
    df_copy = df_copy[df_copy['Player Name'].isin(names)]
    bar = px.bar(df_copy, x='Player Name', y='Frequency', text_auto=True,
                 title="Top 5 frequency of players using the ball",
                 hover_data=[df_copy['Average Time Spent(mins)']])
    return bar


# Speed & Rotation card content callback
@app.callback(
    Output("frth-dpdn", "value"), Output("frth-dpdn", "options"), [Input("card-tabs", "active_tab")]
)
def update_card_body(tab_name):
    if tab_name == "tab-speed":
        return [x for x in array_name_speed[:5]], [{'label': x, 'value': x} for x in array_name_speed]
    else:
        return [x for x in array_name_rotation[:5]], [{'label': x, 'value': x} for x in array_name_rotation]


# Speed & Rotation callback
@app.callback(
    Output('speed-rotation-fig', component_property="figure"),
    Input("frth-dpdn", component_property="value"), [Input("card-tabs", "active_tab")]
)
def update_speed_rot_graph(names, tab):
    if tab == "tab-speed":
        df_copy = df_speed.copy()
        df_copy = df_copy[df_copy['Player Name'].isin(names)]
        bar = px.bar(df_copy, x='Player Name', y='Average Ball Speed(mph)', text_auto=True,
                     title="Top 5 players with highest average ball speed(mph)")
        return bar
    else:
        df_copy = df_rotation.copy()
        df_copy = df_copy[df_copy['Player Name'].isin(names)]
        bar = px.bar(df_copy, x='Player Name', y='Average Ball Rotation(rpm)', text_auto=True,
                     title="Top 5 players with highest average ball rotation(rpm)")
        return bar


@app.callback(
    Output('vid-div', component_property="children"),
    Input("fifth-dpdn", component_property="value")
)
def update_video_div(name):
    value = randint(0, 10)
    if (value % 2) == 0:
        return [html.Iframe(src='https://www.youtube.com/embed/zrgwuNoqexw', className="responsive-iframe")]
    else:
        return [html.Iframe(src='https://www.youtube.com/embed/L1QxOgvnEao', className="responsive-iframe")]


# run the application
if __name__ == '__main__':
    app.run_server(debug=True)
