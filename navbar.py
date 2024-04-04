# %%
#import dependencies
import pandas as pd
import dash
from dash import dcc, html, Input, Output

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
#define external stylesheet
external_stylesheets = ['https://bootswatch.com/5/quartz/bootstrap.css', '/Users/ciarafasullo/Desktop/DS4003/APP/assets/app_style.css']

# %%
#initialize the dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#connect the server for Render
server=app.server

# %%
#define layout
app.layout = html.Div([
    html.Nav(
        className="navbar navbar-dark bg-primary",
        children=[
            html.A("Movie Search", className="navbar-brand"),
        ]
    ),
    html.Div([
        html.H1("Movie Information"),
        dcc.Dropdown(
            id='movie-dropdown',
            options=[],
            placeholder='Enter movie title...',
            style={'width': '50%'}
        ),
        html.Div(id='movie-info')
    ])
])

# %%
#define callback to update movie dropdown options
@app.callback(
    Output('movie-dropdown', 'options'),
    [Input('movie-dropdown', 'search_value')]
)
def update_dropdown_options(search_value):
    if search_value is None:
        return []
    else:
        filtered_options = df[df['title'].str.contains(search_value, case=False)]['title'].tolist()
        return [{'label': option, 'value': option} for option in filtered_options]


# %%
#define callback to update movie information
@app.callback(
    Output('movie-info', 'children'),
    [Input('movie-dropdown', 'value')]
)
def update_movie_info(selected_movie):
    if selected_movie is None:
        return html.Div()
    else:
        movie_data = df[df['title'] == selected_movie].iloc[0]
        movie_title = movie_data['title']
        movie_year = movie_data['year']
        movie_genre = movie_data['genre']
        movie_description = movie_data['description']
        
        return html.Div([
            html.H2(movie_title),
            html.H3(f"Year: {movie_year}"),
            html.H3(f"Genre: {movie_genre}"),
            html.P(f"Description: {movie_description}")
        ])


# %%
#run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)


