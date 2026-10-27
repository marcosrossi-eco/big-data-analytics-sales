
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "raw" / "Online Retail.xlsx"


def load_data():
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {SOURCE}\n"
            "Baixe o conjunto Online Retail do UCI "
            "e coloque-o em data/raw/."
        )

    df = pd.read_excel(SOURCE)

    print(f"Total de registros: {len(df):,}")
    print(f"Total de colunas: {len(df.columns)}")
    print("\nColunas encontradas:")
    print(df.columns.tolist())

    print("\nAmostra dos dados:")
    print(df.head())

    return df


if __name__ == "__main__":
    load_data()
