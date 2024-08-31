"""Contains configuration constants to be reused inside dashboard."""

PRIMARY_COLOR = "#FF9900"
SECONDARY_COLOR = "#bfbdc1"
CURRENT_YEAR = 2021
LAST_YEAR = CURRENT_YEAR - 1
REGION_MAPPING = {
    **dict.fromkeys(["CT", "ME", "MA", "NH", "RI", "VT", "NJ", "NY", "PA"], "Northeast"),
    **dict.fromkeys(["IL", "IN", "MI", "OH", "WI", "IA", "KS", "MN", "MO", "NE", "ND", "SD"], "Midwest"),
    **dict.fromkeys(
        ["DE", "FL", "GA", "MD", "NC", "SC", "VA", "WV", "DC", "AL", "KY", "MS", "TN", "AR", "LA", "TX", "OK"], "South"
    ),
    **dict.fromkeys(["AZ", "NM", "CO", "ID", "MT", "NV", "UT", "WY", "CA", "OR", "WA"], "West"),
    **dict.fromkeys(["UM", "PR", "AP", "VI", "AE", "AS", "GU", "FM", "PW", "MP"], "Other"),
}
NULL_VALUE = "Unknown"
ORANGE_SEQUENTIAL_PALETTE = ["#ffffff", "#dedce0", "#f0c8aa", "#f9b578", "#fca14b", "#fb8e22", "#f77a00"]
SELECTED_CUSTOMER_COLUMNS = [
    "Survey ResponseID",
    "Q-demos-age",
    "Q-demos-education",
    "Q-demos-income",
    "Q-demos-gender",
    "Order_Value",
    "Category",
    "ASIN/ISBN (Product Code)",
    "Order Date",
    "Quantity",
]
