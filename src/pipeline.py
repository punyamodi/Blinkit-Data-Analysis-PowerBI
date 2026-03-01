from pathlib import Path

import numpy as np
import pandas as pd

DATA_PATH = Path(__file__).parent.parent / "data" / "blinkit_grocery_data.xlsx"

FAT_NORMALISATION_MAP = {
    "LF": "Low Fat",
    "low fat": "Low Fat",
    "reg": "Regular",
    "Regular": "Regular",
    "Low Fat": "Low Fat",
}


def load_raw() -> pd.DataFrame:
    return pd.read_excel(DATA_PATH, engine="openpyxl")


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = [
        "item_fat_content",
        "item_identifier",
        "item_type",
        "outlet_establishment_year",
        "outlet_identifier",
        "outlet_location_type",
        "outlet_size",
        "outlet_type",
        "item_visibility",
        "item_weight",
        "sales",
        "rating",
    ]

    df["item_fat_content"] = df["item_fat_content"].map(FAT_NORMALISATION_MAP)

    weight_means = df.groupby("item_type")["item_weight"].transform("mean")
    df["item_weight"] = df["item_weight"].fillna(weight_means)

    df["item_visibility"] = df["item_visibility"].replace(0, np.nan)
    visibility_means = df.groupby("item_type")["item_visibility"].transform("mean")
    df["item_visibility"] = df["item_visibility"].fillna(visibility_means)

    df["outlet_age"] = 2024 - df["outlet_establishment_year"]

    df["sales"] = df["sales"].round(2)
    df["rating"] = df["rating"].round(1)

    return df


def load() -> pd.DataFrame:
    return clean(load_raw())
