"""Example for MakeOverMonday - Week 14."""

import os
from itertools import cycle
from typing import List, Optional

import pandas as pd
import plotly.graph_objects as go
import vizro.models as vm
from plotly.subplots import make_subplots
from vizro import Vizro
from vizro.models.types import capture

# Get and transform dataframe
df = pd.read_excel(
    f"{os.path.dirname(os.path.abspath(__file__))}/data/awareness_of_whether_viral_infection_cured_by_antibiotics.xlsx"
)
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
df_long = pd.melt(df, id_vars=["Category", "Sub-category"], var_name="Opinion", value_name="Percentage")


@capture("graph")
def multi_cat_bar(
    data_frame: pd.DataFrame,
    x: str,
    y: str,
    y2: str,
    color: str,
    color_discrete_sequence: List[str],
    color_category_order: List[str],
    title: Optional[str] = None,
):
    colors = cycle(color_discrete_sequence)

    fig = go.Figure()
    for color_cat in color_category_order:
        tmp_df = data_frame.query(f'{color} == "{color_cat}"')
        fig.add_trace(
            go.Bar(
                x=tmp_df[x],
                y=[tmp_df[y2], tmp_df[y]],
                name=color_cat,
                orientation="h",
                text=tmp_df[x],
                textposition="inside",
                marker_color=next(colors),
            )
        )

    fig.update_layout(
        barmode="relative",
        title=title,
        title_pad_l=8,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="left", x=-0.6),
    )
    return fig


@capture("graph")
def multi_cat_faceted_bar(
    data_frame: pd.DataFrame,
    x: str,
    y: str,
    y2: str,
    color: str,
    color_discrete_sequence: List[str],
    color_category_order: List[str],
    title: Optional[str] = None,
):
    colors = cycle(color_discrete_sequence)

    fig = make_subplots(rows=1, cols=3, shared_yaxes=True, vertical_spacing=0.04)
    for i, color_cat in enumerate(color_category_order):
        tmp_df = data_frame.query(f'{color} == "{color_cat}"')
        fig.add_trace(
            go.Bar(
                x=tmp_df[x],
                y=[tmp_df[y2], tmp_df[y]],
                name=color_cat,
                orientation="h",
                text=tmp_df[x],
                textposition="inside",
                marker_color=next(colors),
            ),
            row=1,
            col=i + 1,
        )

    fig.update_layout(
        title=title, title_pad_l=8, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="left", x=-0.6)
    )
    return fig


page = vm.Page(
    title="Can viral infections be cured with antibiotics?",
    layout=vm.Layout(grid=[[0, 0]] + [[1, 2]] * 8, col_gap="40px"),
    components=[
        vm.Card(
            id="card-insight",
            text="""
            #### Accordion to a KFF poll in 2019, the public's knowledge on antibiotic resistance varies by demographic characteristics. Women, adults ages 18-64, adults with higher income and higher levels of education are more likely to be aware that antibiotics are not effective at treating viral infections.
        """,
        ),
        vm.Graph(
            figure=multi_cat_bar(
                data_frame=df_long,
                x="Percentage",
                y="Sub-category",
                y2="Category",
                color="Opinion",
                color_discrete_sequence=["#04247d", "#5861c7", "#a7a7ff"],
                color_category_order=["Cannot be cured (correct)", "Don't know enough to say", "Can usually be cured"],
                title="Stacked Bar Chart",
            )
        ),
        vm.Graph(
            figure=multi_cat_faceted_bar(
                data_frame=df_long,
                x="Percentage",
                y="Sub-category",
                y2="Category",
                color="Opinion",
                color_discrete_sequence=["#04247d", "#5861c7", "#a7a7ff"],
                color_category_order=["Cannot be cured (correct)", "Don't know enough to say", "Can usually be cured"],
                title="Unstacked Bar Chart",
            )
        ),
    ],
)


dashboard = vm.Dashboard(pages=[page], theme="vizro_light")

if __name__ == "__main__":
    Vizro().build(dashboard).run()
