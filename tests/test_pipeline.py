from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
PROCESSED = ROOT / "data" / "processed" / "sales_clean.csv"


def test_processed_dataset_exists():
    assert PROCESSED.exists(), "Execute primeiro o pipeline de transformação."


def test_processed_dataset_has_required_columns():
    df = pd.read_csv(PROCESSED, nrows=5)

    assert not df.empty
    assert {"quantity", "revenue", "country"}.issubset(df.columns)


def test_reports_exist_and_are_not_empty():
    files = [
        "sales_by_country.csv",
        "top_products.csv",
        "sales_by_month.csv",
        "sales_by_country.png",
        "top_products.png",
        "sales_by_month.png",
    ]

    for filename in files:
        path = REPORTS / filename
        assert path.exists(), f"Relatório ausente: {filename}"
        assert path.stat().st_size > 0, f"Relatório vazio: {filename}"


def test_country_report():
    df = pd.read_csv(REPORTS / "sales_by_country.csv")

    assert {"country", "revenue"}.issubset(df.columns)
    assert not df.empty
    assert df["revenue"].notna().all()
    assert (df["revenue"] >= 0).all()
    assert df.iloc[0]["country"] == "United Kingdom"


def test_product_report():
    df = pd.read_csv(REPORTS / "top_products.csv")

    assert {"description", "quantity"}.issubset(df.columns)
    assert not df.empty
    assert df["description"].notna().all()
    assert (df["quantity"] > 0).all()


def test_monthly_report():
    df = pd.read_csv(REPORTS / "sales_by_month.csv")

    assert {"month", "revenue"}.issubset(df.columns)
    assert not df.empty
    assert df["month"].is_monotonic_increasing
    assert df["revenue"].notna().all()
