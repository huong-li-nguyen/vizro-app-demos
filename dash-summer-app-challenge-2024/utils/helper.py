"""Contains helper functions to tidy/format data and refactor bigger components on screen."""

import pandas as pd
import vizro.models as vm
from vizro.figures import kpi_card_reference

from .config import NULL_VALUE, REGION_MAPPING, SELECTED_CUSTOMER_COLUMNS


def shorten_product_name(name, n_words=4):
    """Shortens product labels by reducing it to the first n words."""
    words = str(name).split()
    return " ".join(words[:n_words])


def tidy_orders_data(orders: pd.DataFrame):
    """Tidies and filters the data frame and creates additional columns."""
    # Remove rows where 'Category' is missing
    orders = orders[orders["Category"].notna()]
    orders = orders.dropna(subset=["Order Date"])

    # Convert to correct data types
    orders["Order Date"] = pd.to_datetime(orders["Order Date"], format="%Y-%m-%d", errors="coerce")

    # Create new columns
    orders = orders.assign(
        Region=orders["Shipping Address State"].map(REGION_MAPPING).fillna(NULL_VALUE),
        Order_Value=orders["Purchase Price Per Unit"] * orders["Quantity"],
        Short_Title=orders["Title"].apply(shorten_product_name),
        Year=orders["Order Date"].dt.year.astype(str),
        Month_Day=orders["Order Date"].dt.strftime("%b-%d"),
        Month=orders["Order Date"].dt.month,
    )

    # Fill null values
    orders["Shipping Address State"] = orders["Shipping Address State"].fillna(NULL_VALUE)
    return orders


def create_kpi_data(orders):
    """Calculate KPIs and create correct data format."""
    df_kpi = (
        orders.groupby("Year")
        .agg({"Order_Value": "sum", "Survey ResponseID": pd.Series.nunique, "Quantity": "sum"})
        .reset_index()
    )

    df_kpi = df_kpi.rename(
        columns={
            "Order_Value": "Total order value",
            "Survey ResponseID": "Number of customers",
            "Quantity": "Total units ordered",
        }
    )

    df_kpi["Avg product unit price"] = df_kpi["Total order value"] / df_kpi["Total units ordered"]
    df_kpi["Total order value mil"] = df_kpi["Total order value"] / 1000000

    df_kpi["index"] = 0
    df_kpi = df_kpi.pivot(
        index="index",
        columns="Year",
        values=[
            "Total order value mil",
            "Number of customers",
            "Total units ordered",
            "Avg product unit price",
        ],
    )
    df_kpi.columns = [f"{kpi}_{year}" for kpi, year in df_kpi.columns]
    return df_kpi


def create_kpi_container(data_frame: pd.DataFrame, id: str, layout: vm.Layout):
    """Creates reusable KPI container configuration."""
    container = vm.Container(
        id=f"kpi-container-{id}",
        title="",
        layout=layout if layout else None,
        components=[
            vm.Figure(
                figure=kpi_card_reference(
                    data_frame,
                    value_column="Total order value mil_2021",
                    reference_column="Total order value mil_2020",
                    title="Total order value",
                    value_format="${value:.2f}M",
                    reference_format="{delta_relative:+.1%} vs. LY (${reference:.2f}M)",
                    icon="payments",
                ),
            ),
            vm.Figure(
                figure=kpi_card_reference(
                    data_frame,
                    value_column="Number of customers_2021",
                    reference_column="Number of customers_2020",
                    title="No. of customers",
                    value_format="{value:,.0f}",
                    reference_format="{delta_relative:+.1%} vs. LY ({reference:,.0f})",
                    icon="groups",
                )
            ),
            vm.Figure(
                figure=kpi_card_reference(
                    data_frame,
                    value_column="Total units ordered_2021",
                    reference_column="Total units ordered_2020",
                    title="Total units ordered",
                    value_format="{value:,.0f}",
                    reference_format="{delta_relative:+.1%} vs. LY ({reference:,.0f})",
                    icon="production_quantity_limits",
                )
            ),
            vm.Figure(
                figure=kpi_card_reference(
                    data_frame,
                    value_column="Avg product unit price_2021",
                    reference_column="Avg product unit price_2020",
                    title="Avg. unit price",
                    value_format="${value:.2f}",
                    reference_format="{delta_relative:+.1%} vs. LY (${reference:.2f})",
                    icon="price_change",
                )
            ),
        ],
    )
    return container


def create_customer_df(orders_cy: pd.DataFrame, survey: pd.DataFrame):
    """Creates aggregated customer dataframe with socioeconomic columns added."""
    df_customer = (
        orders_cy.groupby(["Year", "Survey ResponseID", "Region", "Shipping Address State"])
        .agg(
            {
                "Order_Value": "sum",
                "Category": pd.Series.nunique,
                "ASIN/ISBN (Product Code)": pd.Series.nunique,
                "Order Date": pd.Series.nunique,
                "Quantity": "sum",
            }
        )
        .reset_index()
    )
    df_customer = df_customer.merge(survey, on="Survey ResponseID", how="left")

    # Filter and rename columns for better understanding
    df_customer = df_customer[SELECTED_CUSTOMER_COLUMNS]
    df_customer = df_customer.rename(
        columns={
            "Order_Value": "Total order value",
            "Category": "Number of unique categories",
            "ASIN/ISBN (Product Code)": "Number of unique products",
            "Order Date": "Number of unique order dates",
            "Quantity": "Total units ordered",
        }
    )

    # Create new metrics
    df_customer["Avg unit price"] = df_customer["Total order value"] / df_customer["Total units ordered"]
    df_customer["Avg order value"] = df_customer["Total order value"] / df_customer["Number of unique order dates"]
    df_customer["Quintiles"] = pd.qcut(df_customer["Total order value"], 5, labels=False)
    return df_customer
