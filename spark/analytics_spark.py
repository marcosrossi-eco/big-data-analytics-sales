from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "processed" / "sales_clean.csv"
OUTPUT = ROOT / "reports" / "spark"


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {SOURCE}. "
            "Execute primeiro python src/transform.py."
        )

    spark = (
        SparkSession.builder
        .appName("BigDataAnalyticsSales")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    try:
        df = (
            spark.read
            .option("header", True)
            .option("inferSchema", True)
            .csv(str(SOURCE))
        )

        df = df.withColumn(
            "revenue",
            F.col("revenue").cast("double"),
        )

        OUTPUT.mkdir(parents=True, exist_ok=True)

        print("\nTotal de registros:")
        print(df.count())

        print("\nTop 10 países por faturamento — PySpark:")
        by_country = (
            df.groupBy("country")
            .agg(F.sum("revenue").alias("revenue"))
            .orderBy(F.desc("revenue"))
        )
        by_country.show(10, truncate=False)

        print("\nTop 10 produtos por quantidade — PySpark:")
        by_product = (
            df.groupBy("description")
            .agg(F.sum("quantity").alias("quantity"))
            .orderBy(F.desc("quantity"))
        )
        by_product.show(10, truncate=False)

        print("\nFaturamento por mês — PySpark:")
        by_month = (
            df.withColumn(
                "month",
                F.date_format(
                    F.to_timestamp("invoicedate"),
                    "yyyy-MM",
                ),
            )
            .groupBy("month")
            .agg(F.sum("revenue").alias("revenue"))
            .orderBy("month")
        )
        by_month.show(100, truncate=False)

        by_country.toPandas().to_csv(
            OUTPUT / "sales_by_country_spark.csv",
            index=False,
        )
        by_product.toPandas().to_csv(
            OUTPUT / "top_products_spark.csv",
            index=False,
        )
        by_month.toPandas().to_csv(
            OUTPUT / "sales_by_month_spark.csv",
            index=False,
        )

        print(f"\nRelatórios PySpark salvos em: {OUTPUT}")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
