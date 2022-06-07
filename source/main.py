"""layout file"""
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from source import readdata
from source import parsesymptoms

app = Dash(__name__, assets_folder="../assets")

DATA_VAX = readdata.read_vax_data()

app.layout = html.Div(
    className="grid-wrapper",
    children=[
        html.Div(
            children=[
                html.H1(children="Vaccine adverse events", className="header-title"),
                html.H2(
                    children="Visualization of the adverse event reactions"
                    " to vaccines in US between 2015 and 2020",
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
                            label="Age and sex influence",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                            children=[
                                html.Div(
                                    className="graphs-selection",
                                    children=[
                                        html.H3("Select age range"),
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
                            label="Number of ER, hospital visits and deaths",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                            children=[
                                html.Div(
                                    className="tab_grid",
                                    children=[
                                        html.Div(
                                            className="graphs-selection",
                                            children=[
                                                html.H3("Select Vaccine type"),
                                                dcc.Dropdown(
                                                    sorted(
                                                        pd.unique(DATA_VAX["VAX_TYPE"])
                                                    ),
                                                    "RABIES",
                                                    id="wybierz-szczepionke",
                                                ),
                                                html.H3("Select event"),
                                                dcc.Checklist(
                                                    options={
                                                        "ER_VISITS": "ER visit",
                                                        "HOSPITAL_VISITS": "Hospital visit",
                                                        "DEATHS": "Death",
                                                    },
                                                    value=[],
                                                    id="wybierz-akcje",
                                                    className="checklist",
                                                    labelClassName="checklist-option",
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
                            ],
                        ),
                        dcc.Tab(
                            label="Most frequent symptoms",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                            children=[
                                html.Div(
                                    className="tab_grid",
                                    children=[
                                        html.Div(
                                            className="graphs-selection",
                                            children=[
                                                html.H3("Select Vaccine type"),
                                                dcc.Dropdown(
                                                    sorted(
                                                        pd.unique(DATA_VAX["VAX_TYPE"])
                                                    ),
                                                    "INFLUENZA SEASONAL",
                                                    id="wybierz-szczepionke2",
                                                ),
                                                html.H3("Select Brand"),
                                                dcc.Dropdown(
                                                    id="wybierz-brand",
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="symptoms_graph",
                                            children=[
                                                dcc.Graph(id="symptom-graph"),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
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
def update_age_slider(value):
    """updating line graph based on the slider value"""
    df1 = (
        DATA_VAX.round(0)
        .groupby(["SEX", "AGE_YRS"])[["SEX", "AGE_YRS"]]
        .size()
        .reset_index(name="ilosc")
    )
    mask = (df1["AGE_YRS"] >= value[0]) & (df1["AGE_YRS"] <= value[1])
    colors = ["#ed5d53", "#BEBBBB", "#444054"]
    fig = px.bar(
        df1[mask],
        x="AGE_YRS",
        y="ilosc",
        barmode="group",
        color="SEX",
        template="ggplot2",
        color_discrete_sequence=colors,
        labels={
            "AGE_YRS": "Patient's age",
            "ilosc": "Number of adverse events",
            "SEX": "Patient's sex",
        },
    )
    fig.update_layout(plot_bgcolor="#f6f6f2")
    for i, new_name in enumerate(["Female", "Male", "Undefined"]):
        fig.data[i].name = new_name
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output("doctor-graph", "figure"),
    [Input("wybierz-szczepionke", "value"), Input("wybierz-akcje", "value")],
)
def update_action_graph(szczepionka, akcja):
    """updating bar graph based on the dropdown and checklist"""
    df2 = (
        DATA_VAX.groupby(["VAX_NAME", "BRAND"])
        .agg(
            ER_VISITS=("ER_VISIT", "count"),
            HOSPITAL_VISITS=("HOSPITAL", "count"),
            DEATHS=("DIED", "count"),
        )
        .reset_index()
    )
    mask = df2["VAX_NAME"].replace(regex={r" \(.*\)$": ""}) == szczepionka
    if not akcja:
        akcja = ["ER_VISITS", "HOSPITAL_VISITS", "DEATHS"]
    colors = ["#ed5d53", "#BEBBBB", "#444054"]
    fig2 = px.bar(
        df2[mask].sort_values(akcja, ascending=False),
        y="BRAND",
        x=akcja,
        barmode="stack",
        orientation="h",
        labels={
            "BRAND": "Available vaccines",
            "value": "Number of events",
            "variable": "Event type",
        },
        template="ggplot2",
        color_discrete_sequence=colors,
    )
    fig2.update_layout(plot_bgcolor="#f6f6f2")
    fig2.update_layout()

    return fig2


@app.callback(
    Output("wybierz-brand", "options"), [Input("wybierz-szczepionke2", "value")]
)
def set_brands_options(szczepionka):
    """update brand dropdown based on vaccine type"""
    df_brands = DATA_VAX[["BRAND", "VAX_TYPE"]]
    mask = df_brands["VAX_TYPE"] == szczepionka
    unique_brands = df_brands[mask]["BRAND"].unique()
    return [{"label": "All brands", "value": "all_values"}] + [
        {"label": x, "value": x} for x in unique_brands
    ]


@app.callback(Output("wybierz-brand", "value"), [Input("wybierz-brand", "options")])
def set_brands_value(available_options):  # pylint: disable=W0613
    """set default value of brand dropdown"""
    return "all_values"


@app.callback(
    Output("symptom-graph", "figure"),
    [Input("wybierz-szczepionke2", "value"), Input("wybierz-brand", "value")],
)
def update_symptoms_graph(szczepionka, brand):
    """updating symptoms graph based on the dropdown values"""
    df3 = DATA_VAX[["SYMPTOMS", "VAX_TYPE", "BRAND"]]
    if not brand or brand == "all_values":
        mask = df3["VAX_TYPE"] == szczepionka
    else:
        mask = (df3["VAX_TYPE"] == szczepionka) & (df3["BRAND"] == brand)
    df4 = parsesymptoms.find_most_frequent_symptoms(df3[mask], 15)
    if not szczepionka:
        df4 = parsesymptoms.find_most_frequent_symptoms(df3, 15)
    colors = ["#ed5d53", "#BEBBBB", "#444054"]
    fig3 = px.bar(
        df4.sort_values("count", ascending=True),
        x="count",
        y="symptom",
        orientation="h",
        labels={
            "symptom": "Top symptoms",
            "count": "Number of occurences",
        },
        template="ggplot2",
        color_discrete_sequence=colors,
    )
    fig3.update_layout(plot_bgcolor="#f6f6f2")
    fig3.update_layout()

    return fig3


if __name__ == "__main__":
    app.run_server(debug=True)
