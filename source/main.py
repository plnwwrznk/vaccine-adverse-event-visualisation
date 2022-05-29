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

VAERSVAX = (
    pd.concat(
        map(read_w_parameters, glob.glob("data/*VAERSVAX.csv"), repeat(columns_vax)),
        ignore_index=True,
    )
    .replace({"VAX_NAME": r"\(SEASONAL\)"}, {"VAX_NAME": "SEASONAL"}, regex=True)
    .replace({"VAX_NAME": r"\(H1N1\)"}, {"VAX_NAME": "H1N1"}, regex=True)
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

app = Dash(__name__, assets_folder="../assets", suppress_callback_exceptions=True)

df2 = (
    VAERSDATA.round(0).groupby(["AGE_YRS"])["AGE_YRS"].size().reset_index(name="ilosc")
)

df3 = (
    DATA_VAX[DATA_VAX["ER_VISIT"] == "Y"]
    .groupby(["VAX_NAME"])
    .size()
    .reset_index(name="ilosc")
    .sort_values(by="ilosc")
)
vax_names = pd.unique(DATA_VAX["VAX_NAME"].replace(regex={r" \(.*\)$": ""}))
app.layout = html.Div(
    className="grid-wrapper",
    children=[
        html.Div(
            children=[
                html.H1(children="Vaccine adverse events", className="header-title"),
                html.H2(
                    children="Visualize the adverse event reactions"
                    " to vaccines in US"
                    " between 2015 and 2020",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                dcc.Tabs(
                    id="tabs-with-classes",
                    value="tab-1",
                    parent_className="custom-tabs",
                    className="custom-tabs-container",
                    children=[
                        dcc.Tab(
                            label="Age influence",
                            value="tab-1",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                        dcc.Tab(
                            label="Doctor graph",
                            value="tab-2",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                        dcc.Tab(
                            label="Tab three, multiline",
                            value="tab-3",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                        dcc.Tab(
                            label="Tab four",
                            value="tab-4",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                    ],
                ),
                html.Div(id="tabs-content-classes"),
            ],
            className="graphs",
        ),
    ],
)


@app.callback(
    Output("tabs-content-classes", "children"), Input("tabs-with-classes", "value")
)
def render_content(tab):
    """updating tabs selection"""
    if tab == "tab-1":
        return html.Div(
            [
                html.Div(
                    className="graphs-selection",
                    children=[
                        html.Label("Select age"),
                        dcc.RangeSlider(
                            0, 120, 5, value=[10, 50], id="my-range-slider"
                        ),
                    ],
                ),
                dcc.Graph(id="graph-with-slider"),
            ]
        )
    if tab == "tab-2":
        return html.Div(
            [
                html.Div(
                    className="graphs-selection",
                    children=[
                        html.Label("Wybierz szczepionke"),
                        dcc.Dropdown(
                            vax_names, "INFLUENZA SEASONAL", id="wybierz-szczepionke"
                        ),
                    ],
                ),
                html.Div(
                    className="doctors_graph",
                    children=[
                        dcc.Graph(id="doctor-graph"),
                    ],
                ),
            ]
        )
    if tab == "tab-3":
        return html.Div([html.H3("Tab content 3")])
    if tab == "tab-4":
        return html.Div([html.H3("Tab content 4")])
    return html.Div([html.H3("NO TAB SELECTED")])


@app.callback(
    Output("graph-with-slider", "figure"), [Input("my-range-slider", "value")]
)
def update_slider(value):
    """updating line graph based on the slider value"""
    mask = (df2["AGE_YRS"] > value[0]) & (df2["AGE_YRS"] < value[1])
    fig = px.line(df2[mask], x="AGE_YRS", y="ilosc", template="ggplot2")
    fig.update_layout(transition_duration=500)
    fig.update_layout(plot_bgcolor="#f6f6f2")

    return fig


@app.callback(Output("doctor-graph", "figure"), [Input("wybierz-szczepionke", "value")])
def update_graph(value):
    """updating bar graph"""
    mask = df3["VAX_NAME"].replace(regex={r" \(.*\)$": ""}) == value
    fig2 = px.bar(
        df3[mask],
        x="VAX_NAME",
        y="ilosc",
        labels={
            "VAX_NAME": "Vaccine for disease: " + value,
            "ilosc": "Number of ER visits",
        },
        template="ggplot2",
    )
    fig2.update_layout(plot_bgcolor="#f6f6f2")
    fig2.update_layout()

    return fig2


if __name__ == "__main__":
    app.run_server(debug=True)
