
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "raw" / "Online Retail.xlsx"
OUTPUT = ROOT / "data" / "processed" / "sales_clean.csv"


def transform_data():
    df = pd.read_excel(SOURCE)

    # Padronizar nomes das colunas
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
    )

    # Converter tipos
    df["invoicedate"] = pd.to_datetime(
        df["invoicedate"], errors="coerce"
    )
    df["quantity"] = pd.to_numeric(
        df["quantity"], errors="coerce"
    )
    df["unitprice"] = pd.to_numeric(
        df["unitprice"], errors="coerce"
    )

    # Remover registros sem informações essenciais
    df = df.dropna(
        subset=["invoicedate", "quantity", "unitprice"]
    )

    # Excluir registros com quantidade ou preço inválidos
    df = df[
        (df["quantity"] > 0) &
        (df["unitprice"] > 0)
    ].copy()

    # Calcular valor bruto dos itens
    df["revenue"] = df["quantity"] * df["unitprice"]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")

    print(f"Registros após tratamento: {len(df):,}")
    print(f"Arquivo gerado: {OUTPUT}")
    print(f"Faturamento bruto analisado: {df['revenue'].sum():,.2f}")

    return df


if __name__ == "__main__":
    transform_data()
