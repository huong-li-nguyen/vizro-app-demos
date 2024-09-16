"""Utils file for custom chart code and constants."""

import pandas as pd
import vizro.plotly.express as px
from vizro.models.types import capture


@capture("graph")
def scatter_with_quadrants(
    x: str,
    y: str,
    custom_data: str,
    x_ref_quantile: float = 0.5,
    y_ref_quantile: float = 0.2,
    data_frame: pd.DataFrame = None,
):
    """Custom scatter plot with quadrants made with Plotly."""
    fig = px.scatter(
        data_frame=data_frame,
        x=x,
        y=y,
        custom_data=custom_data,
        color_discrete_sequence=["grey"],
        size="Profit Absolute",
        size_max=20,
        opacity=0.6,
        hover_data=["Product Name", "Profit", "Sales", "Profit Margin"],
        title=f"{data_frame['Category / Sub-Category'].iloc[0]} <br><sup> ⤵ Click on a point to filter the table. Refresh the page to deselect.</sup>",
    )

    # Add reference lines to figure
    x_reference_line = data_frame[x].quantile(x_ref_quantile)
    y_reference_line = data_frame[y].quantile(y_ref_quantile)
    fig.add_hline(y=y_reference_line, line_dash="dash", line_color="grey")
    fig.add_vline(x=x_reference_line, line_dash="dash", line_color="grey")

    # Add quadrants to figure
    fig.add_shape(
        type="rect",
        xref="x",
        yref="y",
        x0=x_reference_line,
        y0=data_frame[y].max() + 700,
        x1=data_frame[x].max() + 700,
        y1=y_reference_line,
        fillcolor="#00b4ff",
        line_width=0,
        opacity=0.4,
        layer="below",
    )
    fig.add_shape(
        type="rect",
        xref="x",
        yref="y",
        x0=data_frame[x].min(),
        y0=y_reference_line,
        x1=x_reference_line,
        y1=data_frame[y].max() + 700,
        fillcolor="#00b4ff",
        line_width=0,
        opacity=0.2,
        layer="below",
    )
    fig.add_shape(
        type="rect",
        xref="x",
        yref="y",
        x0=data_frame[x].min(),
        y0=data_frame[y].min() - 700,
        x1=x_reference_line,
        y1=y_reference_line,
        fillcolor="#ff9222",
        line_width=0,
        opacity=0.4,
        layer="below",
    )
    fig.add_shape(
        type="rect",
        xref="x",
        yref="y",
        x0=x_reference_line,
        y0=data_frame[y].min() - 700,
        x1=data_frame[x].max() + 700,
        y1=y_reference_line,
        fillcolor="#ff9222",
        line_width=0,
        opacity=0.2,
        layer="below",
    )

    # Customize hovertemplate
    fig.update_layout(title_pad_t=24)
    fig.update_traces(
        hovertemplate="<br>".join(
            [
                "%{customdata[0]}",
                "Profit: %{y:$,.2f}",
                "Sales: %{x:$,.2f}",
                "Profit Margin: %{customdata[1]:.0%}",
            ]
        )
        + "<extra></extra>"
    )

    return fig


CELL_STYLE = {
    "styleConditions": [
        {
            "condition": "params.value < -0.1",
            "style": {"backgroundColor": "#ff9222"},
        },
        {
            "condition": "params.value >= -0.1 && params.value <= 0",
            "style": {"backgroundColor": "#ffba7f"},
        },
        {
            "condition": "params.value > 0 && params.value <= 0.05",
            "style": {"backgroundColor": "#e4e4e4"},
        },
        {
            "condition": "params.value > 0.05 && params.value <= 0.15",
            "style": {"backgroundColor": "#b7d4ee"},
        },
        {
            "condition": "params.value > 0.15 && params.value <= 0.20",
            "style": {"backgroundColor": "#80c4f6"},
        },
        {
            "condition": "params.value > 0.20",
            "style": {"backgroundColor": "#00b4ff"},
        },
    ]
}


COLUMN_DEFS = [
    {"field": "Product Name", "cellDataType": "text", "headerName": "Product", "flex": 3},
    {
        "field": "Profit",
        "cellDataType": "number",
        "flex": 2,
        "valueFormatter": {"function": "d3.format('$,.2f')(params.value)"},
    },
    {
        "field": "Sales",
        "cellDataType": "number",
        "flex": 2,
        "valueFormatter": {"function": "d3.format('$,.2f')(params.value)"},
    },
    {
        "field": "Profit Margin",
        "flex": 2,
        "cellDataType": "number",
        "valueFormatter": {"function": "d3.format('.0%')(params.value)"},
        "cellStyle": CELL_STYLE,
    },
]
