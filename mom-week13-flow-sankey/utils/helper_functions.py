"""Utils file that contains helper functions."""
import pandas as pd
from typing import List


def get_cleaned_df(df_original: pd.DataFrame) -> pd.DataFrame:
    """Get cleaned dataframe."""
    df = df_original.map(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.drop(columns="Total Tons")
    return df


def transform_data_for_sankey(df: pd.DataFrame, labels: List[str]) -> pd.DataFrame:
    """Transform data for sankey chart."""
    link_mappings = {value: index for index, value in enumerate(labels)}
    df_indexed = df.replace(link_mappings)
    df_melted = pd.melt(df_indexed, id_vars=["Source", "Destination"], var_name="Variable", value_name="Value")
    return df_melted
