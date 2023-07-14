import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
from dash.dependencies import Output, Input
import base64

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
        html.H1('Sales Data Visualizer'),
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
        html.A(
            id='download-link',
            children=[
                html.Button('Download CSV')
            ],
            href='',
            download='sales_data.csv',
            target='_blank'
        )
    ]
)


# Update the bar chart and CSV download link based on the selected date range
@app.callback(
    Output('sales-chart', 'figure'),
    Output('download-link', 'href'),
    Input('date-filter', 'start_date'),
    Input('date-filter', 'end_date')
)
def update_bar_chart(start_date, end_date):
    filtered_data = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=filtered_data['date'],
            y=filtered_data['sales'],
            marker={'color': 'red'}  # Specify the desired color here
        )
    )
    fig.update_layout(
        title='Sales Data',
        xaxis={'title': 'Date'},
        yaxis={'title': 'Sales'}
    )

    csv_string = filtered_data.to_csv(index=False, encoding='utf-8-sig')
    csv_string = "data:text/csv;charset=utf-8-sig," + base64.b64encode(csv_string.encode()).decode()

    return fig, csv_string


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
