# Import required libraries
import csv
import pickle
import copy
import pathlib
import re
import urllib.request
import dash
import math
import numpy as np
import datetime
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State, ClientsideFunction
from data_pre_treat import *
import dash_core_components as dcc
import dash_html_components as html

from dateutil.relativedelta import relativedelta

# config
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Google Play Store"
server = app.server

# pre -- treat
category_list, android_ver_list = pre_treat_ori_csv()

# Create global chart template
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Google Play Apps Overview",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=7,
    ),
)

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("google_play.png"),
                            id="plotly-image",
                            style={
                                "height": "100px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Google Play Store",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Apps Overview", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="two-third column",
                    id="title", ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H5(
                            "Filter by Last Updated time",
                            className="control_label",
                            style={"margin-top": "20px", "margin-bottom": "40px"},
                        ),
                        dcc.RangeSlider(
                            id="year_month_slider",
                            min=2010.0,
                            max=2019.0,
                            step=1 / 12,
                            value=[2012.0, 2017.0],
                            className="dcc_control",
                        ),
                        html.H5("Filter by category:", className="control_label",
                                style={"margin-top": "20px", "margin-bottom": "20px"}),
                        dcc.Dropdown(
                            id="category_selector",
                            multi=True,
                            options=[{"label": now, "value": now} for now in category_list],
                            value=["ALL"],
                            className="dcc_control",
                        ),

                    ],
                    className="pretty_container three columns",
                    id="cross-filter-options",
                    style={"height": "600px"}
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="appsText"), html.P("No. of Apps")],
                                    id="apps",
                                    className="mini_container four columns",
                                ),
                                html.Div(
                                    [html.H6(id="reviewText"), html.P("Reviews")],
                                    id="review",
                                    className="mini_container four columns",
                                ),
                                html.Div(
                                    [html.H6(id="installText"), html.P("Installs")],
                                    id="installs",
                                    className="mini_container four columns",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="count_graph")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="nine columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="main_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="reviews_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="pie_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="installs_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

# Create callbacks
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("count_graph", "figure")],
)


@app.callback(
    Output("aggregate_data", "data"),
    [
        Input("category_selector", "value"),
        Input("year_month_slider", "value"),
    ],
)
def update_production_text(category_selector, year_month_slider):
    new_csv_reader = load_new_csv()
    apps, reviews, installs = cnt_aggregate(new_csv_reader, category_selector, year_month_slider)
    return [human_format(apps), human_format(reviews), human_format(installs)]


# Selectors,slider -> count graph
@app.callback(
    Output("count_graph", "figure"),
    [
        Input("category_selector", "value"),
        Input("year_month_slider", "value"),
    ],
)
def make_count_figure(category_selector, year_month_slider):
    new_csv_reader = load_new_csv()
    _, res = get_data_by_categoryandlastupdated(new_csv_reader, category_selector, year_month_slider)

    Count = {}

    for now_res in res:
        now_y_d_str = now_res[10].rsplit("-", 1)[0]
        if now_y_d_str in Count:
            Count[now_y_d_str] += 1
        else:
            Count[now_y_d_str] = 1

    Count = dict(sorted(Count.items(), key=lambda x: x[0]))

    data = [
        dict(
            type="scatter",
            mode="markers",
            x=list(Count.keys()),
            y=list(Count.values()),
            opacity=0,
            name="counts",
            hoverinfo="skip",
        ),
        dict(
            type="bar",
            x=list(Count.keys()),
            y=list(Count.values()),
            name="counts",
            marker=dict(color="rgb(123, 199, 255)"),
        ),
    ]

    layout = {}

    layout["title"] = "Last Updated / Count"
    layout["dragmode"] = "select"
    layout["showlegend"] = False
    layout["autosize"] = True

    figure = dict(data=data, layout=layout)
    return figure


# aggregate_date -> show text
@app.callback(
    [
        Output("appsText", "children"),
        Output("reviewText", "children"),
        Output("installText", "children"),
    ],
    [Input("aggregate_data", "data")],
)
def update_text(data):
    return data[0] + " apps", data[1] + " + reviews", data[2] + " + installs"


# Selectors,slider -> main graph
@app.callback(
    Output("main_graph", "figure"),
    [
        Input("category_selector", "value"),
        Input("year_month_slider", "value"),
    ],
)
def update_main_figure(category_selector, year_month_slider):
    new_csv_reader = load_new_csv()
    _, res = get_data_by_categoryandlastupdated(new_csv_reader, category_selector, year_month_slider)

    map = {}
    Ratings = []
    Prices = []

    for line in res:
        now_map_cord = line[2] + "-" + line[7]
        if now_map_cord in map:
            map[now_map_cord] += 1
        else:
            map[now_map_cord] = 1

    for key in map.keys():
        Ratings.append(key.split("-")[0])
        Prices.append(key.split("-")[1])

    return {
        'data': [
            go.Scatter(
                x=Ratings,  # x轴为评分
                y=Prices,  # y轴为价格
                mode='markers',
                marker={
                    'size': 8,
                    'opacity': 0.6,
                    'line': {
                        'width': 0.5,
                        'color': 'white'
                    }
                })],
        'layout':
            go.Layout(
                xaxis={
                    'title': 'Rating',
                },
                yaxis={
                    'title': 'Price',
                },
                margin={
                    'l': 40,
                    'b': 30,
                    't': 10,
                    'r': 0
                },
                height=450,
                hovermode='closest')
    }


# Main graph -> reviews graph
@app.callback(Output("reviews_graph", "figure"),
              [Input("main_graph", "hoverData"),
               ])
def make_reviews_figure(main_graph_hover):
    layout_individual = copy.deepcopy(layout)

    if main_graph_hover is None:
        main_graph_hover = {
            "points": [
                {"x": 4.1, "y": 0}
            ]
        }

    points = [point for point in main_graph_hover["points"]]

    new_rcsv = load_new_csv()
    res = get_data_by_priceandrating(new_rcsv, points[0]["y"], points[0]["x"])
    reviews, _ = get_data_by_android_ver(res)

    if len(reviews) == 0:
        annotation = dict(
            text="No data available",
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper",
        )
        layout_individual["annotations"] = [annotation]
        data = []
    else:
        data = [
            dict(
                type="scatter",
                mode="lines+markers",
                name="reviews",
                x=list(reviews.keys()),
                y=list(reviews.values()),
                line=dict(shape="spline", smoothing=2, width=1, color="#fac1b7"),
                marker=dict(symbol="diamond-open"),
            ),
        ]
    layout_individual["title"] = "Reviews -- Android_ver —— Price: $"+format(points[0]["y"],'.2f')+" Rating:"+format(points[0]["x"],'.1f')

    figure = dict(data=data, layout=layout_individual)
    return figure


# main graph -> installs graph
@app.callback(
    Output("installs_graph", "figure"),
    [Input("main_graph", "hoverData"),
     ], )
def make_installs_figure(main_graph_hover):
    layout_aggregate = copy.deepcopy(layout)

    if main_graph_hover is None:
        main_graph_hover = {
            "points": [
                {"x": 4.1, "y": 0}
            ]
        }

    points = [point for point in main_graph_hover["points"]]

    new_rcsv = load_new_csv()
    res = get_data_by_priceandrating(new_rcsv, points[0]["y"], points[0]["x"])
    _, installs = get_data_by_android_ver(res)

    if len(installs) == 0:
        annotation = dict(
            text="No data available",
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper",
        )
        layout_aggregate["annotations"] = [annotation]
        data = []
    else:
        data = [
            dict(
                type="scatter",
                mode="lines+markers",
                # mode="lines",
                name=" installs",
                x=list(installs.keys()),
                y=list(installs.values()),
                line=dict(shape="spline", smoothing="2", color="#F9ADA0"),
            ),
        ]
    layout_aggregate["title"] = "Installs -- Android_ver —— Price: $"+format(points[0]["y"],'.2f')+" Rating:"+format(points[0]["x"],'.1f')

    figure = dict(data=data, layout=layout_aggregate)
    return figure


# Selectors -> pie graph
@app.callback(
    Output("pie_graph", "figure"),
    [
        Input("category_selector", "value"),
        Input("year_month_slider", "value"),
    ],
)
def make_pie_figure(category_selector, year_month_slider):
    layout_pie = copy.deepcopy(layout)

    new_csv_reader = load_new_csv()
    _, res = get_data_by_categoryandlastupdated(new_csv_reader, category_selector, year_month_slider)

    Type = {}
    Content_Rating = {}

    for line in res:
        type = line[6]
        content_rating = line[8]
        if type in Type:
            Type[type] += 1
        else:
            Type[type] = 1
        if content_rating in Content_Rating:
            Content_Rating[content_rating] += 1
        else:
            Content_Rating[content_rating] = 1

    if len(Type) == 0 or len(Content_Rating) == 0:
        annotation = dict(
            text="No data available",
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper",
        )
        layout_pie["annotations"] = [annotation]
        data = []
    else:
        data = [
            dict(
                type="pie",
                labels=list(Type.keys()),
                values=list(Type.values()),
                name="Type",
                text=[
                    "Free",
                    "Paid",
                ],
                hoverinfo="text+value+percent",
                textinfo="label+percent+name",
                hole=0.5,
                marker=dict(colors=["#fac1b7", "#a9bb95"]),
                domain={"x": [0, 0.45], "y": [0.2, 0.8]},
            ),
            dict(
                type="pie",
                labels=list(Content_Rating.keys()),
                values=list(Content_Rating.values()),
                name="Content Rating",
                hoverinfo="label+text+value+percent",
                textinfo="label+percent+name",
                hole=0.5,
                marker=dict(
                    colors=[Content_Rating_COLORS[index] for index, key in enumerate(Content_Rating.keys())]),
                domain={"x": [0.55, 1], "y": [0.2, 0.8]},
            ),
        ]

    left_y_m = str(round((year_month_slider[0] * 12 + 1) // 12)) + "-" + str(
        round((year_month_slider[0] * 12 + 1) % 12))
    right_y_m = str(round((year_month_slider[1] * 12 + 1) // 12)) + "-" + str(
        round((year_month_slider[1] * 12 + 1) % 12))

    layout_pie["title"] = "Apps Type and Content Rating Summary: {} to {}".format(
        left_y_m, right_y_m
    )
    layout_pie["font"] = dict(color="#777777")
    layout_pie["legend"] = dict(
        font=dict(color="#CCCCCC", size="10"), orientation="h", bgcolor="rgba(0,0,0,0)"
    )

    figure = dict(data=data, layout=layout_pie)
    return figure


# Main
if __name__ == "__main__":
    app.run_server(debug=True)
