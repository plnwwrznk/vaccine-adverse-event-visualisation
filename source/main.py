"""test file"""
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        html.Div(
            children="""
        Dash: A web application framework for your data.
    """
        ),
        dcc.Graph(id="example-graph", figure=fig),
        dcc.Slider(0, 20, 2, value=10, id="my-slider"),
        html.Div(id="slider-output-container"),
    ]
)


@app.callback(
    Output("slider-output-container", "children"), Input("my-slider", "value")
)
def update_output(value):
    """zwraca napis z wartością ze slidera"""
    return f'You have selected "{value}"'


if __name__ == "__main__":
    app.run_server(debug=True)
