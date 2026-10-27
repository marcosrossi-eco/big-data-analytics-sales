
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "processed" / "sales_clean.csv"
OUTPUT = ROOT / "reports"


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {SOURCE}. "
            "Execute primeiro python src/transform.py."
        )

    df = pd.read_csv(
        SOURCE,
        parse_dates=["invoicedate"],
        dtype={"invoiceno": "string"},
        low_memory=False,
    )

    # 1. Faturamento por país
    by_country = (
        df.groupby("country", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    # 2. Quantidade vendida por produto
    by_product = (
        df.groupby("description", as_index=False)["quantity"]
        .sum()
        .sort_values("quantity", ascending=False)
    )

    # 3. Faturamento por mês
    df["month"] = df["invoicedate"].dt.to_period("M").astype(str)

    by_month = (
        df.groupby("month", as_index=False)["revenue"]
        .sum()
        .sort_values("month")
    )

    OUTPUT.mkdir(parents=True, exist_ok=True)

    # Exportar relatórios CSV
    by_country.to_csv(
        OUTPUT / "sales_by_country.csv",
        index=False,
        encoding="utf-8-sig",
    )
    by_product.to_csv(
        OUTPUT / "top_products.csv",
        index=False,
        encoding="utf-8-sig",
    )
    by_month.to_csv(
        OUTPUT / "sales_by_month.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Gráfico 1: faturamento por país (top 10)
    top_countries = by_country.head(10).sort_values("revenue")

    plt.figure(figsize=(11, 6))
    plt.barh(top_countries["country"], top_countries["revenue"])
    plt.title("Top 10 países por faturamento")
    plt.xlabel("Faturamento")
    plt.ylabel("País")
    plt.ticklabel_format(axis="x", style="plain")
    plt.tight_layout()
    plt.savefig(OUTPUT / "sales_by_country.png", dpi=150)
    plt.close()

    # Gráfico 2: top 10 produtos por quantidade
    top_products = by_product.head(10).sort_values("quantity")

    plt.figure(figsize=(11, 7))
    plt.barh(top_products["description"], top_products["quantity"])
    plt.title("Top 10 produtos por quantidade vendida")
    plt.xlabel("Quantidade vendida")
    plt.ylabel("Produto")
    plt.tight_layout()
    plt.savefig(OUTPUT / "top_products.png", dpi=150)
    plt.close()

    # Gráfico 3: evolução mensal do faturamento
    plt.figure(figsize=(11, 6))
    plt.plot(
        by_month["month"],
        by_month["revenue"],
        marker="o",
    )
    plt.title("Evolução mensal do faturamento")
    plt.xlabel("Mês")
    plt.ylabel("Faturamento")
    plt.xticks(rotation=45)
    plt.ticklabel_format(axis="y", style="plain")
    plt.tight_layout()
    plt.savefig(OUTPUT / "sales_by_month.png", dpi=150)
    plt.close()

    print("\nTop 10 países por faturamento:")
    print(by_country.head(10).to_string(index=False))

    print("\nTop 10 produtos por quantidade:")
    print(by_product.head(10).to_string(index=False))

    print("\nFaturamento por mês:")
    print(by_month.to_string(index=False))

    print(f"\nRelatórios CSV e gráficos PNG salvos em: {OUTPUT}")


if __name__ == "__main__":
    main()
