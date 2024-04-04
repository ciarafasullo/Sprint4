# %% [markdown]
# Scatterplot of Duration vs Average Ratings
# 
# -user can select multiple genres, color coded
# 
# -user can hover to receive more details on each data point such as the title, genre, duration, and average vote

# %%
#import dependencies
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# %%
#define external stylesheet
external_stylesheets = ['https://bootswatch.com/5/quartz/bootstrap.css']

# %%
#read the data from the csv file
df = pd.read_csv('data.csv')

# %%
#data cleaning
columns_to_drop = ['filmtv_id', 'total_votes', 'notes', 'humor', 'rhythm', 'effort', 'tension', 'erotism']
df = df.drop(columns = columns_to_drop)
#drop all rows that include movies from countries outside of the United States
df = df[df['country'] == 'United States']
df

# %%
#define genres and options for dropdown menu
genres = [
    'Animation', 'Drama', 'Romantic', 'Comedy', 'Spy', 'Crime', 'Thriller',
    'Adventure', 'Documentary', 'Horror', 'Action', 'Western', 'Biography',
    'Musical', 'Sci-Fi', 'War', 'Fantasy'
]
genre_options = [{'label': genre, 'value': genre} for genre in genres]

# %%
#initialize dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#connect the server for Render
server = app.server

# %%
app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='/Users/ciarafasullo/Desktop/DS4003/APP/assets/app_style.css'  #path to external stylesheet
    ),
    html.H1("Movie Duration vs Average Ratings"),
    dcc.Dropdown(
        id='genre-dropdown',
        options=genre_options,
        value='Animation', #default value
        multi=True, #allow multiple selections
        style={'width': '50%'}
    ),
    dcc.Graph(id='scatter-plot')
])

# %%
#define callback to update scatterplot
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('genre-dropdown', 'value')]
)    
def update_plot(selected_genres):
    if not isinstance(selected_genres, list):
        selected_genres = [selected_genres]  # Convert single value to list
    filtered_data = df[df['genre'].isin(selected_genres)]
    avg_vote = filtered_data.groupby(['duration', 'genre']).agg({'avg_vote': 'mean', 'title': 'first'}).reset_index()
    fig = px.scatter(avg_vote, x='duration', y='avg_vote', color='genre', hover_data=['title'])
    fig.update_layout(xaxis_title='Duration (minutes)', yaxis_title='Average Rating')
    return fig

# %%
#run the app
if __name__ == '__main__':
    app.run_server(debug=True)


