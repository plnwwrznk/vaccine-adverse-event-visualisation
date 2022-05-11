"""test file"""
import glob
from itertools import repeat
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd


def read_w_parameters(file, fields):
    """function to read from multiple csv files with parameters"""
    return pd.read_csv(file, encoding="iso-8859-1", usecols=fields)


columns_data = [
    "VAERS_ID",
    "STATE",
    "AGE_YRS",
    "SEX",
    "DIED",
    "DATEDIED",
    "L_THREAT",
    "ER_VISIT",
    "HOSPITAL",
    "HOSPDAYS",
    "VAX_DATE",
    "ONSET_DATE",
    "NUMDAYS",
    "CUR_ILL",
    "PRIOR_VAX",
    "ALLERGIES",
]
columns_vax = [
    "VAERS_ID",
    "VAX_TYPE",
    "VAX_MANU",
    "VAX_LOT",
    "VAX_DOSE_SERIES",
    "VAX_ROUTE",
    "VAX_SITE",
    "VAX_NAME",
]
columns_symptoms = [
    "VAERS_ID",
    "SYMPTOM1",
    "SYMPTOMVERSION1",
    "SYMPTOM2",
    "SYMPTOMVERSION2",
    "SYMPTOM3",
    "SYMPTOMVERSION3",
    "SYMPTOM4",
    "SYMPTOMVERSION4",
    "SYMPTOM5",
    "SYMPTOMVERSION5",
]

VAERSDATA = pd.concat(
    map(read_w_parameters, glob.glob("data\\*VAERSDATA.csv"), repeat(columns_data)),
    ignore_index=True,
)

VAERSVAX = pd.concat(
    map(read_w_parameters, glob.glob("data\\*VAERSVAX.csv"), repeat(columns_vax)),
    ignore_index=True,
)

VAERSSYMPTOMS = pd.concat(
    map(
        read_w_parameters,
        glob.glob("data\\*VAERSSYMPTOMS.csv"),
        repeat(columns_symptoms),
    ),
    ignore_index=True,
)


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
