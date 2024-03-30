"""Example for MakeOverMonday - Week 13."""
import os
from typing import List, Optional

import pandas as pd
import plotly.graph_objects as go
import vizro.models as vm
from vizro import Vizro
from vizro.models.types import capture
from vizro.tables import dash_ag_grid
from utils.helper_functions import transform_data_for_sankey, get_cleaned_df

# Get dataframe and relevant labels for sankey
df_original = pd.read_excel(f"{os.path.dirname(os.path.abspath(__file__))}/data/Amsterdam_Material Flow Diagram Data_2019_.xlsx")
df_clean = get_cleaned_df(df_original)
labels = set(list(df_clean["Source"]) + list(df_clean["Destination"]))
df_transformed = transform_data_for_sankey(df_clean, labels)


# Create custom chart
@capture("graph")
def sankey(
    data_frame: pd.DataFrame, labels: List[str], source: str, target: str, value: str, title: Optional[str] = None
):
    # Aggregate dataframe for sankey chart (relevant for filtering)
    df_agg = data_frame.groupby([source, target]).aggregate({value: "sum"}).reset_index()

    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=16,
                    thickness=16,
                    label=labels,
                ),
                link=dict(
                    source=df_agg[source],
                    target=df_agg[target],
                    value=df_agg[value],
                    label=labels,
                    color="rgba(205, 209, 228, 0.4)",
                ),
            )
        ]
    )
    fig.update_layout(title=title)
    return fig


page_context = vm.Page(
    title="Context: EU cohesion funds",
    components=[
        vm.Container(
            title="The 5 Policy Objectives - how does this look in practice?",
            components=[
                vm.Card(
                    id="card-1",
                    text="""
                        # SMARTER

                        #### A more competitive and smarter Europe
                        """,
                ),
                vm.Card(
                    id="card-2",
                    text="""
                        # SOCIAL

                        #### A more social and inclusive Europe
                        """,
                ),
                vm.Card(
                    id="card-3",
                    text="""
                        # CONNECTED

                        #### A more connected Europe by enhancing mobility
                        """,
                ),
                vm.Card(
                    id="card-4",
                    text="""
                        # GREENER

                        #### A greener, low carbon transitioning towards a net zero carbon economy
                        """,
                ),
                vm.Card(
                    id="card-5",
                    text="""
                        # CLOSER TO CITIZENS

                        #### Europe closer to citizens by fostering the sustainable and integrated development of all types of territories.
                        """,
                ),
            ],
        )
    ],
)


page_with_table = vm.Page(
    title="Raw Data (in tons)",
    components=[
        vm.AgGrid(
            figure=dash_ag_grid(
                data_frame=df_original,
                columnDefs=[
                    {"field": "Source"},
                    {"field": "Destination"},
                    {"field": "Biomass", "cellDataType": "numeric"},
                    {"field": "Fossil", "cellDataType": "numeric"},
                    {"field": "Metals", "cellDataType": "numeric"},
                    {"field": "Minerals", "cellDataType": "numeric"},
                    {"field": "Unknown/Mixed", "cellDataType": "numeric"},
                    {"field": "Total Tons", "cellDataType": "numeric"},
                ],
            )
        )
    ],
)


page_with_sankey = vm.Page(
    title="Material Flow (in tons)",
    layout=vm.Layout(grid=[[0]] + [[1]] * 8),
    components=[
        vm.Card(
            id="card-material-flow",
            text="""
            In 2019, the City of Amsterdam processed 75.3 billion kilos of raw materials. 
            At the end of the life cycle, the resulting materials are mainly exported (74% of the total).
        """
        ),
        vm.Graph(
            figure=sankey(
                df_transformed,
                labels=list(labels),
                source="Source",
                target="Destination",
                value="Value",
            ),
        ),
    ],
    controls=[vm.Filter(column="Variable", selector=vm.Dropdown(title="Select measure for sankey:", value="Minerals"))],
)


dashboard = vm.Dashboard(
    pages=[page_context, page_with_table, page_with_sankey],
    title="The Life of Raw Materials",
    navigation=vm.Navigation(
        nav_selector=vm.NavBar(
            items=[
                vm.NavLink(
                    label="Context",
                    icon="Policy",
                    pages=["Context: EU cohesion funds"],
                ),
                vm.NavLink(
                    label="Example",
                    icon="Network Node",
                    pages={"Example 1: Amsterdam": ["Raw Data (in tons)", "Material Flow (in tons)"]},
                ),
            ]
        )
    ),
)

if __name__ == "__main__":
    Vizro().build(dashboard).run()
