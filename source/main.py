"""test file"""
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from source import readdata

app = Dash(__name__, assets_folder="../assets")

DATA_VAX = readdata.read_vax_data()


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
                            label="Number of adverse events based on age",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                            children=[
                                html.Div(
                                    className="graphs-selection",
                                    children=[
                                        html.Label("Select age"),
                                        dcc.RangeSlider(
                                            0,
                                            120,
                                            5,
                                            value=[10, 50],
                                            id="my-range-slider",
                                        ),
                                    ],
                                ),
                                dcc.Graph(id="graph-with-slider"),
                            ],
                        ),
                        dcc.Tab(
                            label="Number of ER Visits",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                            children=[
                                html.Div(
                                    className="graphs-selection",
                                    children=[
                                        html.Div(
                                            className="dropdown-1",
                                            children=[
                                                html.Label("Select Vaccine type"),
                                                dcc.Dropdown(
                                                    pd.unique(DATA_VAX["VAX_TYPE"]),
                                                    "INFLUENZA SEASONAL",
                                                    id="wybierz-szczepionke",
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="dropdown-2",
                                            children=[
                                                html.Label("Pacient action"),
                                                dcc.Dropdown(
                                                    ["ER visit", "Hospital visit"],
                                                    value="ER visit",
                                                    id="wybierz-akcje",
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="doctors_graph",
                                    children=[
                                        dcc.Graph(id="doctor-graph"),
                                    ],
                                ),
                            ],
                        ),
                        dcc.Tab(
                            label="Tab three, multiline",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                            children=[html.Div([html.H3("Tab content 3")])],
                        ),
                        dcc.Tab(
                            label="Tab four",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                            children=[html.Div([html.H3("Tab content 4")])],
                        ),
                    ],
                )
            ],
            className="graphs",
        ),
    ],
)


@app.callback(
    Output("graph-with-slider", "figure"), [Input("my-range-slider", "value")]
)
def update_slider(value):
    """updating line graph based on the slider value"""
    df2 = (
        DATA_VAX.round(0)
        .groupby(["AGE_YRS", "RECVYEAR"])["AGE_YRS", "RECVYEAR"]
        .size()
        .reset_index(name="ilosc")
    )
    mask = (df2["AGE_YRS"] >= value[0]) & (df2["AGE_YRS"] <= value[1])
    fig = px.bar(
        df2[mask],
        x="AGE_YRS",
        y="ilosc",
        color="RECVYEAR",
        template="ggplot2",
        color_continuous_scale=["#FAC9B8", "#ed5d53"],
    )
    fig.update_layout(plot_bgcolor="#f6f6f2")
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output("doctor-graph", "figure"),
    [Input("wybierz-szczepionke", "value"), Input("wybierz-akcje", "value")],
)
def update_graph(szczepionka, akcja):
    """updating bar graph"""
    if akcja == "ER visit":
        df3 = (
            DATA_VAX[DATA_VAX["ER_VISIT"] == "Y"]
            .groupby(["VAX_NAME", "BRAND"])
            .size()
            .reset_index(name="ilosc")
            .sort_values(by="ilosc")
        )
    else:
        df3 = (
            DATA_VAX[DATA_VAX["HOSPITAL"] == "Y"]
            .groupby(["VAX_NAME", "BRAND"])
            .size()
            .reset_index(name="ilosc")
            .sort_values(by="ilosc")
        )
    mask = df3["VAX_NAME"].replace(regex={r" \(.*\)$": ""}) == szczepionka
    fig2 = px.bar(
        df3[mask],
        x="BRAND",
        y="ilosc",
        labels={
            "BRAND": "Available vaccines",
            "ilosc": "Number of ER visits",
        },
        template="ggplot2",
    )
    fig2.update_layout(plot_bgcolor="#f6f6f2")
    fig2.update_layout()

    return fig2


if __name__ == "__main__":
    app.run_server(debug=True)
