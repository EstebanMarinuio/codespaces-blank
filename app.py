import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

# Load data
df = pd.read_csv('db/Voga_ventas.csv')

# Convert 'fecha_movimiento' to datetime
df['fecha_movimiento'] = pd.to_datetime(df['fecha_movimiento'])

# Extract year, month, and week
df['year'] = df['fecha_movimiento'].dt.year
df['month'] = df['fecha_movimiento'].dt.month
df['week'] = df['fecha_movimiento'].dt.isocalendar().week

# Group the data by year, month, and week
df_grouped = df.groupby(['year', 'month', 'week'], as_index=False)['count_items'].sum()

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Dashboard de Ventas de Joyería"),

    # Line chart
    html.Div([
        html.H2("Línea de Tiempo de Ventas (por Año, Mes y Semana)"),
        dcc.Graph(id='line-chart')
    ]),

    # Pie chart
    html.Div([
        html.H2("Distribución por Categoría"),
        dcc.Graph(id='pie-chart')
    ]),

    # Bar chart
    html.Div([
        html.H2("Ventas por Tipo de Producto"),
        dcc.Graph(id='bar-chart')
    ]),
])

# Callback to update graphs
@app.callback(
    [Output('line-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('line-chart', 'id')]  # Dummy input to trigger the update
)
def update_graphs(_):
    # Line chart: Sales over time (by year, month, week)
    line_fig = px.line(df_grouped, x='week', y='count_items', color='year',
                       title='Ventas por Semana', labels={'count_items': 'Cantidad de Ítems', 'week': 'Semana'})

    # Pie chart: Sales distribution by category
    pie_fig = px.pie(df, names='CATEGORY', title='Distribución por Categoría')

    # Bar chart: Sales by product type
    bar_fig = px.bar(df, x='tipo', y='count_items', title='Ventas por Tipo de Producto',
                     labels={'count_items': 'Cantidad de Ítems'})

    return line_fig, pie_fig, bar_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
