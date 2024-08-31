"""Contains Vizro app configuration."""

import dash_bootstrap_components as dbc
import pandas as pd
import vizro.models as vm
from dash import html
from utils.charts import COLUMNDEFS, FlexContainer, bar_avg, bar_top_n, choropleth, line, product_seasonality_heatmap
from utils.config import CURRENT_YEAR, LAST_YEAR, ORANGE_SEQUENTIAL_PALETTE
from utils.helper import create_customer_df, create_kpi_container, create_kpi_data, tidy_orders_data
from vizro import Vizro
from vizro.actions import filter_interaction
from vizro.tables import dash_ag_grid

# TIDY AND CREATE RELEVANT DATA SETS ---------------------
# Data set below was created by loading original `amazon-purchases.csv` and filtering data on CURRENT_YEAR and LAST_YEAR
orders = pd.read_csv(f"data/amazon-purchases-{CURRENT_YEAR}-{LAST_YEAR}.csv")
survey = pd.read_csv("data/survey.csv")
orders = tidy_orders_data(orders)
orders_cy = orders[orders["Year"] == str(CURRENT_YEAR)]
kpi_overall_df = create_kpi_data(orders)
kpi_midwest_df = create_kpi_data(orders.query("Region=='Midwest'"))
kpi_northeast_df = create_kpi_data(orders.query("Region=='Northeast'"))
kpi_south_df = create_kpi_data(orders.query("Region=='South'"))
kpi_west_df = create_kpi_data(orders.query("Region=='West'"))
customer_df = create_customer_df(orders_cy, survey)

# CONFIGURE BIGGER COMPONENTS FOR PAGES -------------------
kpi_overall = create_kpi_container(kpi_overall_df, "overall", vm.Layout(grid=[[0, 1], [2, 3]]))
kpi_northeast = create_kpi_container(
    kpi_northeast_df,
    "northeast",
    vm.Layout(grid=[[0], [1], [2], [3]], row_gap="8px", col_gap="8px"),
)
kpi_midwest = create_kpi_container(
    kpi_midwest_df,
    "midwest",
    vm.Layout(grid=[[0], [1], [2], [3]], row_gap="8px", col_gap="8px"),
)
kpi_south = create_kpi_container(
    kpi_south_df,
    "south",
    vm.Layout(grid=[[0], [1], [2], [3]], row_gap="8px", col_gap="8px"),
)
kpi_west = create_kpi_container(
    kpi_west_df,
    "west",
    vm.Layout(grid=[[0], [1], [2], [3]], row_gap="8px", col_gap="8px"),
)


tabs_overall = vm.Tabs(
    tabs=[
        vm.Container(
            title="By Category",
            components=[
                vm.Graph(
                    figure=bar_top_n(
                        data_frame=orders_cy,
                        y="Category",
                        x="Order_Value",
                    ),
                )
            ],
        ),
        vm.Container(
            title="By Product",
            components=[
                vm.Graph(
                    figure=bar_top_n(
                        data_frame=orders_cy,
                        y="Short_Title",
                        x="Order_Value",
                    ),
                )
            ],
        ),
        vm.Container(
            title="By Region",
            components=[
                vm.Graph(
                    figure=bar_top_n(
                        data_frame=orders_cy,
                        y="Region",
                        x="Order_Value",
                    ),
                )
            ],
        ),
        vm.Container(
            title="By State",
            components=[
                vm.Graph(
                    figure=bar_top_n(
                        data_frame=orders_cy,
                        y="Shipping Address State",
                        x="Order_Value",
                    ),
                )
            ],
        ),
    ],
)


# CONFIGURE PAGES -------------------
page_orders = vm.Page(
    title="Order summary",
    layout=vm.Layout(grid=[[0, 1], [2, 1]], col_gap="40px", row_gap="40px"),
    components=[
        kpi_overall,
        vm.Container(title="Top performers 🚀", components=[tabs_overall]),
        vm.Graph(
            figure=line(
                data_frame=orders,
                x="Month_Day",
                y="Order_Value",
                color="Year",
                title="Performance vs. last year (LY) ⏳",
            )
        ),
    ],
)

page_region_comparison = vm.Page(
    title="Regional comparison",
    layout=vm.Layout(grid=[[0, 1, 2, 3]], row_min_height="800px"),
    components=[
        FlexContainer(
            title="Midwest",
            components=[
                vm.Graph(
                    figure=choropleth(
                        data_frame=orders_cy.query('Region=="Midwest"'),
                        locations="Shipping Address State",
                        color="Order_Value",
                        custom_data=["Shipping Address State"],
                        color_continuous_scale=ORANGE_SEQUENTIAL_PALETTE,
                        show_region_only=True,
                    ),
                ),
                kpi_midwest,
                vm.Graph(
                    id="midwest-bar",
                    figure=bar_top_n(
                        data_frame=orders_cy.query('Region=="Midwest"'),
                        y="Short_Title",
                        x="Order_Value",
                        top_n=6,
                        x_visible=False,
                        title="Top performers 🚀",
                    ),
                ),
            ],
            classname="flex-container-regional",
        ),
        FlexContainer(
            title="Northeast",
            components=[
                vm.Graph(
                    figure=choropleth(
                        data_frame=orders_cy.query('Region=="Northeast"'),
                        locations="Shipping Address State",
                        color="Order_Value",
                        custom_data=["Shipping Address State"],
                        color_continuous_scale=ORANGE_SEQUENTIAL_PALETTE,
                        show_region_only=True,
                    ),
                ),
                kpi_northeast,
                vm.Graph(
                    id="northeast-bar",
                    figure=bar_top_n(
                        data_frame=orders_cy.query('Region=="Northeast"'),
                        y="Short_Title",
                        x="Order_Value",
                        top_n=6,
                        x_visible=False,
                        title="Top performers 🚀",
                    ),
                ),
            ],
            classname="flex-container-regional",
        ),
        FlexContainer(
            title="South",
            components=[
                vm.Graph(
                    figure=choropleth(
                        data_frame=orders_cy.query('Region=="South"'),
                        locations="Shipping Address State",
                        color="Order_Value",
                        custom_data=["Shipping Address State"],
                        color_continuous_scale=ORANGE_SEQUENTIAL_PALETTE,
                        show_region_only=True,
                    ),
                ),
                kpi_south,
                vm.Graph(
                    id="south-bar",
                    figure=bar_top_n(
                        data_frame=orders_cy.query('Region=="South"'),
                        y="Short_Title",
                        x="Order_Value",
                        top_n=6,
                        x_visible=False,
                        title="Top performers 🚀",
                    ),
                ),
            ],
            classname="flex-container-regional",
        ),
        FlexContainer(
            title="West",
            components=[
                vm.Graph(
                    figure=choropleth(
                        data_frame=orders_cy.query('Region=="West"'),
                        locations="Shipping Address State",
                        color="Order_Value",
                        custom_data=["Shipping Address State"],
                        color_continuous_scale=ORANGE_SEQUENTIAL_PALETTE,
                        show_region_only=True,
                    ),
                ),
                kpi_west,
                vm.Graph(
                    id="west-bar",
                    figure=bar_top_n(
                        data_frame=orders_cy.query('Region=="West"'),
                        y="Short_Title",
                        x="Order_Value",
                        top_n=6,
                        x_visible=False,
                        title="Top performers 🚀",
                    ),
                ),
            ],
            classname="flex-container-regional",
        ),
    ],
    controls=[
        vm.Parameter(
            targets=["south-bar.y", "northeast-bar.y", "west-bar.y", "midwest-bar.y"],
            selector=vm.Dropdown(
                options=[
                    {"value": "Shipping Address State", "label": "State"},
                    {"value": "Category", "label": "Category"},
                    {"value": "Short_Title", "label": "Product item"},
                ],
                title="Change y-axis on top performers:",
                multi=False,
                value="Shipping Address State",
            ),
        ),
    ],
)

page_region_map = vm.Page(
    title="Regional map",
    layout=vm.Layout(grid=[[0, 1]]),
    components=[
        vm.Graph(
            figure=choropleth(
                data_frame=orders_cy,
                locations="Shipping Address State",
                color="Order_Value",
                title="Total order value by shipping state <br><sup> ⤵ Click on a state to filter the "
                "charts on the right. Refresh the page to deselect.</sup>",
                custom_data=["Shipping Address State"],
                color_continuous_scale=ORANGE_SEQUENTIAL_PALETTE,
            ),
            actions=[
                vm.Action(
                    function=filter_interaction(targets=["regional-bar"]),
                )
            ],
        ),
        vm.Graph(
            id="regional-bar",
            figure=bar_top_n(data_frame=orders_cy, y="Category", x="Order_Value", title="Top performers 🚀"),
        ),
    ],
    controls=[
        vm.Filter(column="Region"),
        vm.Filter(column="Shipping Address State"),
        vm.Filter(column="Category"),
        vm.Parameter(
            targets=["regional-bar.y"],
            selector=vm.Dropdown(
                options=[
                    {"value": "Shipping Address State", "label": "State"},
                    {"value": "Category", "label": "Category"},
                    {"value": "Short_Title", "label": "Product item"},
                ],
                title="Change y-axis on bar chart:",
                multi=False,
                value="Category",
            ),
        ),
        vm.Parameter(
            targets=["regional-bar.top_n"],
            selector=vm.Slider(min=10, max=35, step=5, value=15, title="Display top N:"),
        ),
    ],
)

page_product = vm.Page(
    title="Product overview",
    layout=vm.Layout(grid=[[0, 0, 1, 1, 1]], col_gap="0px"),
    components=[
        vm.Graph(
            id="product-bar",
            figure=bar_top_n(
                data_frame=orders_cy,
                y="Category",
                x="Order_Value",
                title="Top categories / product items by total order value",
            ),
        ),
        vm.Graph(
            id="product-heatmap",
            figure=product_seasonality_heatmap(
                orders_cy, x="Month", y="Category", z="Order_Value", color_continuous_scale=ORANGE_SEQUENTIAL_PALETTE
            ),
        ),
    ],
    controls=[
        vm.Filter(column="Category"),
        vm.Parameter(
            targets=["product-bar.y", "product-heatmap.y"],
            selector=vm.Dropdown(
                options=[{"value": "Category", "label": "Category"}, {"value": "Short_Title", "label": "Product item"}],
                title="Change product level:",
                multi=False,
                value="Category",
            ),
        ),
        vm.Parameter(
            targets=["product-bar.top_n", "product-heatmap.top_n"],
            selector=vm.Slider(min=10, max=35, step=5, value=15, title="Display top N:"),
        ),
        vm.Filter(column="Region"),
        vm.Filter(column="Shipping Address State"),
    ],
)


page_customer = vm.Page(
    title="Customer overview",
    components=[
        vm.Graph(
            id="average-bar",
            figure=bar_avg(
                customer_df,
                x="Q-demos-age",
                y="Total order value",
                title="Average KPI numbers across selected categories 📊",
            ),
        ),
        vm.AgGrid(figure=dash_ag_grid(customer_df, columnDefs=COLUMNDEFS, dashGridOptions={"pagination": True})),
    ],
    controls=[
        vm.Parameter(
            targets=["average-bar.x"],
            selector=vm.Dropdown(
                options=[
                    {"value": "Q-demos-age", "label": "Age group"},
                    {"value": "Q-demos-education", "label": "Education level"},
                    {"value": "Q-demos-income", "label": "Income group"},
                    {"value": "Q-demos-gender", "label": "Gender"},
                ],
                title="Change category on x-axis",
                multi=False,
                value="Q-demos-age",
            ),
        ),
        vm.Parameter(
            targets=["average-bar.y"],
            selector=vm.Dropdown(
                options=[
                    "Total order value",
                    "Number of unique categories",
                    "Number of unique products",
                    "Number of unique order dates",
                    "Total units ordered",
                    "Avg. unit price",
                    "Avg. order value",
                ],
                title="Change KPI on y-axis",
                multi=False,
                value="Total order value",
            ),
        ),
    ],
)

# CONFIGURE DASHBOARD WITH PAGES AND NAVIGATION -------------------
dashboard = vm.Dashboard(
    pages=[page_orders, page_product, page_region_comparison, page_region_map, page_customer],
    navigation=vm.Navigation(
        nav_selector=vm.NavBar(
            items=[
                vm.NavLink(label="Order summary", pages=["Order summary"], icon="Home"),
                vm.NavLink(
                    label="Product overview",
                    pages=["Product overview"],
                    icon="Shopping Cart",
                ),
                vm.NavLink(
                    label="Regional overview",
                    pages=["Regional comparison", "Regional map"],
                    icon="South America",
                ),
                vm.NavLink(
                    label="Customer overview",
                    pages=["Customer overview"],
                    icon="Groups",
                ),
            ]
        )
    ),
    title=f"Purchase history dashboard: {CURRENT_YEAR}",
)

app = Vizro().build(dashboard)

# Add footer
app.dash.layout.children.append(
    html.Div(
        [
            dbc.NavLink("🌸 Created by Li Nguyen", href="https://github.com/huong-li-nguyen"),
            dbc.NavLink("💻 Code", href=""),
            dbc.NavLink(
                "💾 Data", href="https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/YGLYDY"
            ),
        ],
        className="anchor-container",
    )
)


if __name__ == "__main__":
    app.run()
