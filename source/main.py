"""test file"""
import glob
from itertools import repeat
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd


def read_w_parameters(file, fields):
    """function to read from multiple csv files with parameters"""
    return pd.read_csv(file, encoding="iso-8859-1", usecols=fields, low_memory=False)


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
    map(read_w_parameters, glob.glob("data/*VAERSDATA.csv"), repeat(columns_data)),
    ignore_index=True,
)

VAERSVAX = pd.concat(
    map(read_w_parameters, glob.glob("data/*VAERSVAX.csv"), repeat(columns_vax)),
    ignore_index=True,
)

VAERSSYMPTOMS = pd.concat(
    map(
        read_w_parameters,
        glob.glob("data/*VAERSSYMPTOMS.csv"),
        repeat(columns_symptoms),
    ),
    ignore_index=True,
)

DATA_VAX = pd.merge(VAERSDATA, VAERSVAX, on="VAERS_ID")

app = Dash(__name__)

df2 = (
    VAERSDATA.round(0).groupby(["AGE_YRS"])["AGE_YRS"].size().reset_index(name="ilosc")
)

df3 = pd.DataFrame(
    {
        "Amount_doctor": DATA_VAX.notnull().groupby(["ER_VISIT"])["ER_VISIT"].count(),
        "Vaccine": DATA_VAX["VAX_NAME"],
    }
)


fig2 = px.bar(df3, x="Vaccine", y="Amount_doctor")

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        html.Div(
            children="""
        Dash: A web application framework for your data.
    """
        ),
        dcc.Graph(id="graph-with-slider"),
        dcc.RangeSlider(0, 120, 1, value=[10, 50], id="my-range-slider"),
        html.Div(id="slider-output-container"),
        html.Div(
            [
                html.Div(
                    children=[
                        dcc.Graph(id="doctor-graph", figure=fig2),
                        html.Label("Wybierz szczepionke"),
                        dcc.Dropdown(df3.Vaccine, id="wybierz-szczepionke"),
                    ],
                    style={"padding": 10, "flex": 1},
                ),
            ]
        ),
    ]
)


@app.callback(
    Output("graph-with-slider", "figure"), [Input("my-range-slider", "value")]
)
@app.callback(
    Output("doctor-graph", "figure"), [Input("wybierz-szczepionke", "options")]
)
def update_figure(value):
    """zwraca napis z wartością ze slidera"""
    filtered_df = df2[(df2["AGE_YRS"] > value[0]) & (df2["AGE_YRS"] < value[1])]
    fig = px.line(filtered_df, x="AGE_YRS", y="ilosc")
    fig.update_layout(transition_duration=500)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
