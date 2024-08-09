"""Dev app to try things out."""

from typing import List, Optional

import pandas as pd
import vizro.models as vm
import vizro.plotly.express as px
from helper import tidy_df
from vizro import Vizro
from vizro.actions import filter_interaction
from vizro.models.types import capture

df = pd.read_csv("survey_results_public.csv")
df = tidy_df(df)


@capture("graph")
def bar_dev_type(data_frame, top_n: int = 15, custom_data: Optional[List[str]] = None):
    df_median = data_frame.groupby("DevType")["ConvertedCompYearly"].median().reset_index()
    df_median = df_median.nlargest(top_n, "ConvertedCompYearly").sort_values(by="ConvertedCompYearly")

    fig = px.bar(
        df_median,
        y="DevType",
        x="ConvertedCompYearly",
        orientation="h",
        text="ConvertedCompYearly",
        text_auto=True,
        custom_data=custom_data,
    )
    fig.update_layout(
        title=f"Top {top_n} developer types by median yearly salary (USD)"
        f"<br><sup> ⤵ Click on bar to filter charts on the right. Refresh the page to deselect.</sup>",
        xaxis_title="Median yearly salary (USD)",
        yaxis_title="Developer Type",
        title_pad_t=24,
    )
    return fig


@capture("graph")
def bar_experience(data_frame):
    df_median = data_frame.groupby("WorkExp_cat")["ConvertedCompYearly"].median().reset_index()
    fig = px.bar(df_median, x="WorkExp_cat", y="ConvertedCompYearly")
    fig.update_layout(
        title="Median yearly salary (USD) by experience",
        yaxis_title="Median yearly salary (USD)",
        xaxis_title="Work experience",
        legend_title=None,
    )
    return fig


@capture("graph")
def xy_heatmap(data_frame):
    fig = px.density_heatmap(data_frame, x="WorkExp", y="ConvertedCompYearly", text_auto=True)
    fig.update_layout(
        title="Frequency count by yearly salary (USD) and experience",
        yaxis_title="Yearly salary (USD)",
        xaxis_title="Work Experience",
        legend_title=None,
    )
    fig.update_traces(xbins=dict(start=0.0, end=30.0, size=2))
    return fig


page = vm.Page(
    title="Week 31 - Stackoverflow Developer Survey 2023 💻",
    layout=vm.Layout(grid=[[0, 0, 0, 1, 1], [0, 0, 0, 2, 2]]),
    components=[
        vm.Graph(
            figure=bar_dev_type(df, custom_data=["DevType"]),
            id="bar-chart",
            actions=[vm.Action(function=filter_interaction(targets=["grouped-bar", "xy-heatmap"]))],
        ),
        vm.Graph(figure=xy_heatmap(df), id="xy-heatmap"),
        vm.Graph(figure=bar_experience(df), id="grouped-bar"),
    ],
    controls=[
        vm.Filter(column="Country", selector=vm.Dropdown(multi=False, value="United States of America")),
        vm.Parameter(
            targets=["bar-chart.top_n"],
            selector=vm.Slider(min=0, max=30, step=5, value=20, title="Show top-n developer types:"),
        ),
    ],
)
dashboard = vm.Dashboard(pages=[page], title="Figure Friday")

if __name__ == "__main__":
    Vizro().build(dashboard).run()
