import pandas as pd

COLUMNS = [
    "Country",
    "DevType",
    "Age",
    "Employment",
    "WorkExp",
    "YearsCode",
    "ConvertedCompYearly",
]

AGE_MAPPING = {
    "Under 18 years old": "<18y",
    "18-24 years old": "18-24y",
    "25-34 years old": "25-34y",
    "35-44 years old": "35-44y",
    "45-54 years old": "45-54y",
    "55-64 years old": "55-64y",
    "65 years or older": "65+",
    "Prefer not to say": "N/A",
}


def tidy_df(df):
    # Filter data
    df = df[COLUMNS]
    df = df.dropna()

    # Tidy columns
    df["Age"] = df["Age"].map(AGE_MAPPING)
    df["WorkExp"] = pd.to_numeric(df["WorkExp"], errors="coerce")

    # Create bins for WorkExp and YearsCode
    bins = [-float("inf"), 2, 5, 8, 11, 13, 15, 20, 30, float("inf")]
    labels = ["<=2y", "3-5y", "6-8y", "9-11y", "12-13y", "13-15y", "16-20y", "21-30y", ">30y"]
    df["WorkExp_cat"] = pd.cut(df["WorkExp"], bins=bins, labels=labels, right=True)
    return df
