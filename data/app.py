import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
from dash.dependencies import Output, Input

# Load the data from the CSV file
df = pd.read_csv(
    "C:\\users\\Sushmitha\\Desktop\\MY_SPACE\\FORGE TASKS\\quantium-starter-repo\\data\\pink_morsel_sales.csv")

# Sort the data by date
df['date'] = pd.to_datetime(df['date'])  # Convert date column to datetime format
df.sort_values('date', inplace=True)

# Create the Dash app layout
app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1('Pink Morsel Sales Visualizer'),
        html.Div(
            children=[
                dcc.DatePickerRange(
                    id='date-filter',
                    min_date_allowed=df['date'].min(),
                    max_date_allowed=df['date'].max(),
                    initial_visible_month=df['date'].min(),
                    start_date=df['date'].min(),
                    end_date=df['date'].max()
                )
            ]
        ),
        dcc.Graph(id='sales-chart'),
    ]
)


# Update the line chart based on the selected date range
@app.callback(
    Output('sales-chart', 'figure'),
    Input('date-filter', 'start_date'),
    Input('date-filter', 'end_date')
)
def update_line_chart(start_date, end_date):
    filtered_data = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=filtered_data['date'],
            y=filtered_data['sales'],
            mode='lines'
        )
    )
    fig.update_layout(
        title='Sales Data',
        xaxis={'title': 'Date'},
        yaxis={'title': 'Sales'}
    )

    return fig


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
