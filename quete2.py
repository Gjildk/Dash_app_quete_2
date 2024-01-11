from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Lien vers le fichier CSV
url = "https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv"

# Créez un DataFrame en utilisant on_bad_lines
df = pd.read_csv(url, on_bad_lines='skip')

app = Dash(__name__)

# Layout de base
app.layout = html.Div([
    dcc.Dropdown(
        id='book-dropdown',
        options=[{'label': title, 'value': title} for title in df['title']],
        value=df['title'].iloc[0],  # Valeur par défaut
        multi=False
    ),
    dcc.Dropdown(
        id='author-dropdown',
        options=[{'label': author, 'value': author} for author in df['authors']],
        value=df['authors'].iloc[0],  # Valeur par défaut
        multi=False
    ),
    dcc.Input(
        id='page-input',
        type='number',
        value=df['  num_pages'].max(),  # Valeur par défaut
        placeholder='Nombre de pages maximum'
    ),
    dcc.Graph(id='graph-example')
])

# Callback pour mettre à jour le graphique en fonction des filtres sélectionnés
@app.callback(
    Output('graph-example', 'figure'),
    [Input('book-dropdown', 'value'),
     Input('author-dropdown', 'value'),
     Input('page-input', 'value')]
)
def update_graph(selected_book, selected_author, max_pages):
    if selected_book:
        selected_data = df[df['title'] == selected_book]
    elif selected_author:
        selected_data = df[df['authors'] == selected_author]
    else:
        selected_data = df[df['  num_pages'] <= max_pages]

    figure = px.bar(
        selected_data,
        x='title',
        y='  num_pages',  
        labels={'  num_pages': 'Nombre de Pages'}, 
        title=f'Graphique à Barres'
    )
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
