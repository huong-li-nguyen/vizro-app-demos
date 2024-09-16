"""App configuration."""

import pandas as pd
import vizro.models as vm
from charts import COLUMN_DEFS, scatter_with_quadrants
from vizro import Vizro
from vizro.actions import export_data, filter_interaction
from vizro.tables import dash_ag_grid

# TIDY DATA
df = pd.read_excel("https://raw.githubusercontent.com/plotly/Figure-Friday/main/2024/week-28/Sample%20-%20Superstore.xls")
df["Category / Sub-Category"] = df["Category"] + " / " + df["Sub-Category"]
df = df.groupby(["Category / Sub-Category", "Product Name"]).agg({"Sales": "sum", "Profit": "sum"}).reset_index()
df["Profit Margin"] = df["Profit"] / df["Sales"]
df["Profit Absolute"] = abs(df["Profit"])  # For size in px.scatter (cannot be negative)


# DEFINE PAGE AND DASHBOARD
page = vm.Page(
    title="Week 28 - Sales vs. Profit 📈",
    id="page-id",
    layout=vm.Layout(grid=[[0, 1]] * 6 + [[2, -1]]),
    components=[
        vm.Graph(
            id="scatter",
            figure=scatter_with_quadrants(data_frame=df, x="Sales", y="Profit", custom_data=["Product Name", "Profit Margin"]),
            actions=[vm.Action(function=filter_interaction(targets=["table"]))],
        ),
        vm.AgGrid(id="table", figure=dash_ag_grid(df, columnDefs=COLUMN_DEFS)),
        vm.Button(
            text="Export data",
            actions=[
                vm.Action(function=export_data()),
            ],
        ),
    ],
    controls=[
        vm.Filter(column="Category / Sub-Category", selector=vm.Dropdown(multi=False, value="Technology / Phones")),
        vm.Parameter(
            targets=["scatter.x_ref_quantile"],
            selector=vm.Slider(min=0, max=1, step=0.2, value=0.8, title="X-reference line (quantile)"),
        ),
        vm.Parameter(
            targets=["scatter.y_ref_quantile"],
            selector=vm.Slider(min=0, max=1, step=0.2, value=0.2, title="Y-reference line (quantile)"),
        ),
    ],
)

dashboard = vm.Dashboard(pages=[page], title="Figure Friday", theme="vizro_light")


if __name__ == "__main__":
    Vizro().build(dashboard).run()
