import dash
from dash import dcc, html, Input, Output, State

#def slider_func():
#    """slider_func принимает на вход начальную и конечную дату, а отдает последнюю дату выборки"""
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Slider(
        id='my-slider',
        min=1609459200, # 1 января 2021
        max=1640908800, # 31 декабря 2021
        step=86400,
        value=1636243200,
    ),
    html.Div(id='slider-output-container')
])

@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('my-slider', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)