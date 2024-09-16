"""App configuration."""

from typing import Literal

import pandas as pd
import plotly.express as px
import vizro.models as vm
import vizro.plotly.express as px
from vizro import Vizro
from vizro.models.types import capture

# Load the data
df = pd.read_csv("https://raw.githubusercontent.com/plotly/Figure-Friday/main/2024/week-29/ewf_standings.csv")


@capture("graph")
def stacked_bar(data_frame, baseline_category: Literal["wins", "draws", "losses"] = "wins"):
    """Create a stacked 100% bar chart for the selected team."""
    # Change default order based on chosen baseline_category
    default_order = ["wins", "draws", "losses"]
    x_order = [baseline_category] + [item for item in default_order if item != baseline_category]

    # Create stacked 100% bar chart
    fig = px.histogram(
        data_frame,
        y="season",
        x=x_order,
        barnorm="fraction",
        text_auto=".0%",
        color_discrete_map={"wins": "#625AD8", "draws": "#d4d4d4", "losses": "#97dffc"},
    )

    fig.update_layout(
        xaxis=dict(
            title="Share of Total Matches",
            tickmode="array",
            tickvals=[0, 0.2, 0.4, 0.6, 0.8, 1],
            ticktext=["0%", "20%", "40%", "60%", "80%", "100%"],
        ),
        yaxis_title="Season",
        legend_title=None,
        hovermode=False,
        # Make title dynamic (reactive to controls)
        title=f"Seasonal Win, Draw, Loss Distribution for <b>{data_frame['team_name'].iloc[0]}<b>",
    )
    return fig


page = vm.Page(
    title="Week 29 - English Women's Football ⚽",
    components=[
        vm.Graph(figure=stacked_bar(data_frame=df), id="stacked-bar"),
    ],
    controls=[
        vm.Filter(
            column="team_name", selector=vm.Dropdown(multi=False, title="Select a team:", value="Manchester City Women")
        ),
        vm.Parameter(
            targets=["stacked-bar.baseline_category"],
            selector=vm.RadioItems(
                options=["wins", "draws", "losses"], value="wins", title="Select baseline category:"
            ),
        ),
    ],
)

dashboard = vm.Dashboard(pages=[page], theme="vizro_light", title="Figure Friday")


if __name__ == "__main__":
    Vizro().build(dashboard).run()
