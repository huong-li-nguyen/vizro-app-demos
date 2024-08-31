"""Contains code for custom charts and table configurations."""

from typing import List, Literal, Optional

import pandas as pd
import vizro.models as vm
import vizro.plotly.express as px
from dash import html
from vizro.models.types import capture

from .config import PRIMARY_COLOR, SECONDARY_COLOR
from .helper import shorten_product_name


# CUSTOM CHARTS ---------------
@capture("graph")
def bar_top_n(
    data_frame: pd.DataFrame,
    x: str,
    y: str,
    top_n: int = 15,
    custom_data: Optional[List[str]] = None,
    title: Optional[str] = None,
    x_visible: bool = True,
):
    """Custom bar chart implementation.

    Based on [px.bar](https://plotly.com/python-api-reference/generated/plotly.express.bar).
    """
    df_agg = data_frame.groupby(y).agg({x: "sum"}).sort_values(by=x, ascending=False).reset_index()
    fig = px.bar(
        data_frame=df_agg.head(top_n),
        x=x,
        y=y,
        orientation="h",
        text_auto=".3s",
        color_discrete_sequence=[SECONDARY_COLOR],
        custom_data=custom_data,
    )
    fig.update_layout(
        title=title,
        xaxis={"title": "Total order value in USD", "visible": x_visible},
        yaxis={"title": "", "autorange": "reversed"},
        margin={"r": 0, "b": 16, "t": 32},
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
    )
    return fig


@capture("graph")
def line(data_frame: pd.DataFrame, x: str, y: str, color: str, title: Optional[str] = None):
    """Custom line chart implementation.

    Based on [px.line](https://plotly.com/python-api-reference/generated/plotly.express.line).
    """
    df_agg = data_frame.groupby([x, color]).agg({y: "sum"}).reset_index()

    # Create full order date for correct sorting
    df_agg["order_date_sort"] = pd.to_datetime(df_agg[x] + "-" + df_agg[color], format="%b-%d-%Y")
    df_agg = df_agg.sort_values(by="order_date_sort")

    fig = px.line(
        data_frame=df_agg,
        x=x,
        y=y,
        color=color,
        color_discrete_sequence=[SECONDARY_COLOR, PRIMARY_COLOR],
    )
    fig.update_layout(
        title=title,
        xaxis={"title": "", "nticks": 12, "showgrid": False},
        yaxis_title="Total order value in USD",
        legend_title="",
    )
    return fig


@capture("graph")
def product_seasonality_heatmap(
    data_frame: pd.DataFrame,
    x: str,
    y: str,
    z: str,
    top_n: int = 15,
    color_continuous_scale: Optional[List[str]] = None,
):
    """Custom density heatmap implementation.

    Based on [px.density_heatmap](https://plotly.com/python-api-reference/generated/plotly.express.density_heatmap).
    """
    # Filter for top n categories
    top_products = (
        data_frame.groupby([y]).agg({z: "sum"}).sort_values(by=z, ascending=False).reset_index().head(top_n)[y]
    )
    df_filtered = data_frame[data_frame[y].isin(top_products)]

    # Get average order value per category and month
    df_agg = df_filtered.groupby([x, y]).agg({z: "sum"}).sort_values(by=z, ascending=False).reset_index()

    fig = px.density_heatmap(
        data_frame=df_agg,
        x=x,
        y=y,
        z=z,
        text_auto=".2s",
        nbinsx=12,
        color_continuous_scale=color_continuous_scale,
    )

    fig.update_coloraxes(colorbar_title="")
    fig.update_yaxes(categoryorder="array", categoryarray=top_products)
    fig.update_layout(
        title={"text": f"Seasonality of {top_n} categories / products", "pad_l": 0, "pad_r": 0},
        yaxis={"title": "", "autorange": "reversed", "visible": False},
        xaxis={
            "title": "",
            "showgrid": False,
            "tickmode": "array",
            "tickvals": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "ticktext": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        },
        margin={"l": 0, "r": 0, "t": 32, "b": 0},
    )
    return fig


@capture("graph")
def choropleth(
    locations: str,
    color: str,
    data_frame: pd.DataFrame = None,
    title: Optional[str] = None,
    custom_data: Optional[List[str]] = None,
    color_continuous_scale: Optional[List[str]] = None,
    show_region_only: bool = False,
):
    """Custom choropleth implementation.

    Based on [px.choropleth](https://plotly.com/python-api-reference/generated/plotly.express.choropleth).
    """
    df_agg = data_frame.groupby(locations).agg({color: "sum"}).reset_index()
    fig = px.choropleth(
        data_frame=df_agg,
        locations=locations,
        color=color,
        color_continuous_scale=color_continuous_scale,
        scope="usa",
        locationmode="USA-states",
        title=title,
        custom_data=custom_data,
    )
    fig.update_coloraxes(colorbar={"thickness": 10, "title": ""})
    fig.update_layout(geo_bgcolor="rgba(0,0,0,0)")

    if show_region_only:
        fig.update_geos(
            fitbounds="locations",
            visible=False,
            projection_scale=10,
        )
        fig.update_layout(
            {
                "coloraxis_showscale": False,
                "margin": {"t": 0, "b": 0, "r": 0, "l": 0},
                "title_pad": {"t": 0, "b": 0, "r": 0, "l": 0},
                "height": 160,
            }
        )
    return fig


@capture("graph")
def bar_avg(data_frame: pd.DataFrame, x: str, y: str, title: Optional[str] = None):
    """Custom bar chart implementation.

    Based on [px.bar](https://plotly.com/python-api-reference/generated/plotly.express.bar).
    """
    df_agg = data_frame.groupby(x).agg({y: "mean"}).sort_values(by=y, ascending=False).reset_index()
    df_agg[x] = df_agg[x].apply(shorten_product_name)
    fig = px.bar(
        data_frame=df_agg,
        x=x,
        y=y,
        text_auto=".0f",
        color_discrete_sequence=[SECONDARY_COLOR],
    )
    fig.update_layout(
        title=title,
        xaxis={"title": ""},
        yaxis={"title": f"{y}"},
    )
    if x == "Q-demos-income":
        fig.update_xaxes(
            categoryorder="array",
            categoryarray=[
                "Less than $25,000",
                "$25,000 - $49,999",
                "$50,000 - $74,999",
                "$75,000 - $99,999",
                "$100,000 - $149,999",
                "$150,000 or more",
                "Prefer not to say",
            ],
        )
    else:
        fig.update_xaxes(categoryorder="category ascending")
    return fig


# CUSTOM COMPONENTS -----------
class FlexContainer(vm.Container):
    """Custom flex `Container`."""

    type: Literal["flex_container"] = "flex_container"
    classname: Optional[str] = "d-flex"

    def build(self):
        """Returns a flex container."""
        components_container = [component.build() for component in self.components]

        return html.Div(
            id=self.id,
            children=[html.H3(children=self.title, className="container__title"), *components_container],
            className=self.classname,
        )


vm.Page.add_type("components", FlexContainer)


# TABLE SPECIFICATIONS ----
CELL_STYLE = {
    "styleConditions": [
        {
            "condition": "params.data.Quintiles == 0",
            "style": {"backgroundColor": "#ffc495"},
        },
        {
            "condition": "params.data.Quintiles == 1",
            "style": {"backgroundColor": "#ffb276"},
        },
        {
            "condition": "params.data.Quintiles == 2",
            "style": {"backgroundColor": "#fe9f56"},
        },
        {
            "condition": "params.data.Quintiles == 3",
            "style": {"backgroundColor": "#fb8d35"},
        },
        {
            "condition": "params.data.Quintiles == 4",
            "style": {"backgroundColor": "#f77a00"},
        },
    ],
}

COLUMNDEFS = [
    {"field": "Survey ResponseID", "cellDataType": "text"},
    {"field": "Q-demos-age", "cellDataType": "text"},
    {"field": "Q-demos-education", "cellDataType": "text"},
    {"field": "Q-demos-income", "cellDataType": "text"},
    {"field": "Q-demos-gender", "cellDataType": "text"},
    {"field": "Total order value", "cellDataType": "dollar", "cellStyle": CELL_STYLE},
    {"field": "Quintiles"},
    {"field": "Avg unit price", "cellDataType": "dollar"},
    {"field": "Avg order value", "cellDataType": "dollar"},
    {"field": "Total units ordered"},
    {"field": "Number of unique categories"},
    {"field": "Number of unique products"},
    {"field": "Number of unique order dates"},
    {"field": "pop", "flex": 3},
]
