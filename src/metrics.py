import pandas as pd


def kpis(df: pd.DataFrame) -> dict:
    return {
        "total_sales": df["sales"].sum(),
        "average_sales": df["sales"].mean(),
        "item_count": len(df),
        "average_rating": df["rating"].mean(),
    }


def sales_by_fat_content(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("item_fat_content")["sales"]
        .sum()
        .reset_index()
        .rename(columns={"item_fat_content": "fat_content", "sales": "total_sales"})
        .sort_values("total_sales", ascending=False)
    )


def sales_by_item_type(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("item_type")["sales"]
        .sum()
        .reset_index()
        .rename(columns={"item_type": "category", "sales": "total_sales"})
        .sort_values("total_sales", ascending=False)
    )


def sales_by_outlet_size(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("outlet_size")["sales"]
        .sum()
        .reset_index()
        .rename(columns={"outlet_size": "size", "sales": "total_sales"})
        .sort_values("total_sales", ascending=False)
    )


def sales_by_location_type(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("outlet_location_type")["sales"]
        .sum()
        .reset_index()
        .rename(columns={"outlet_location_type": "location", "sales": "total_sales"})
        .sort_values("total_sales", ascending=False)
    )


def outlet_establishment_trend(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("outlet_establishment_year")["sales"]
        .agg(total_sales="sum", outlet_count="nunique")
        .reset_index()
        .rename(columns={"outlet_establishment_year": "year"})
    )


def outlet_type_comparison(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("outlet_type")
        .agg(
            total_sales=("sales", "sum"),
            item_count=("item_identifier", "count"),
            average_sales=("sales", "mean"),
            average_rating=("rating", "mean"),
            average_visibility=("item_visibility", "mean"),
        )
        .reset_index()
        .rename(columns={"outlet_type": "type"})
        .round(2)
    )


def sales_by_fat_and_location(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["outlet_location_type", "item_fat_content"])["sales"]
        .sum()
        .reset_index()
        .rename(
            columns={
                "outlet_location_type": "location",
                "item_fat_content": "fat_content",
                "sales": "total_sales",
            }
        )
    )


def top_items_by_sales(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return (
        df.groupby("item_identifier")
        .agg(total_sales=("sales", "sum"), item_type=("item_type", "first"))
        .reset_index()
        .sort_values("total_sales", ascending=False)
        .head(n)
    )


def sales_by_outlet_age_band(df: pd.DataFrame) -> pd.DataFrame:
    bins = [0, 5, 10, 15, 20, 100]
    labels = ["0-5 yrs", "6-10 yrs", "11-15 yrs", "16-20 yrs", "20+ yrs"]
    df = df.copy()
    df["age_band"] = pd.cut(df["outlet_age"], bins=bins, labels=labels, right=True)
    return (
        df.groupby("age_band", observed=True)["sales"]
        .sum()
        .reset_index()
        .rename(columns={"age_band": "age_band", "sales": "total_sales"})
    )


def rating_distribution(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df["rating"]
        .value_counts()
        .sort_index()
        .reset_index()
        .rename(columns={"rating": "rating", "count": "count"})
    )
