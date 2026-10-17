
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    explode,
    count,
    avg,
    round,
    current_timestamp,
)

def main():
    # 1. Start a local Spark session
    spark = (
        SparkSession.builder
        .appName("EcommerceDataPipeline")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    # 2. Find the most recent raw JSON file
    raw_files = sorted(
        Path("data/raw").glob("products_*.json")
    )

    if not raw_files:
        raise FileNotFoundError(
            "No raw JSON files found. Run src/extract.py first."
        )

    latest_file = str(raw_files[-1])
    print(f"Reading: {latest_file}")

    # 3. Read JSON into a Spark DataFrame
    raw_df = (
    spark.read
    .option("multiLine", "true")
    .json(latest_file)
)

    # The API response contains a list named "products".
    products_df = (
        raw_df
        .select(explode(col("products")).alias("p"))
        .select(
            col("p.id").alias("product_id"),
            col("p.title").alias("title"),
            col("p.category").alias("category"),
            col("p.price").alias("price"),
            col("p.rating").alias("rating"),
            col("p.stock").alias("stock"),
        )
    )

    print("\n--- Product schema ---")
    products_df.printSchema()

    print("\n--- Sample products ---")
    products_df.show(10, truncate=False)

    # 4. Clean data: remove invalid records
    silver_df = (
        products_df
        .filter(col("product_id").isNotNull())
        .filter(col("title").isNotNull())
        .filter(col("price") >= 0)
        .filter(col("rating").between(0, 5))
        .filter(col("stock") >= 0)
        .withColumn("processed_at", current_timestamp())
    )

    print("Valid product count:", silver_df.count())

    # 5. Save cleaned records as Parquet
    silver_path = "data/processed/silver/products"

    (
        silver_df.write
        .mode("overwrite")
        .parquet(silver_path)
    )

    # 6. Create analytics-ready category summaries
    gold_df = (
        silver_df
        .groupBy("category")
        .agg(
            count("*").alias("product_count"),
            round(avg("price"), 2).alias("average_price"),
        )
        .orderBy(col("average_price").desc_nulls_last())
    )

    print("\n--- Average price by category ---")
    gold_df.show(truncate=False)

    gold_path = "data/processed/gold/category_summary"

    (
        gold_df.write
        .mode("overwrite")
        .parquet(gold_path)
    )

    print("\nPipeline completed successfully!")
    print(f"Silver output: {silver_path}")
    print(f"Gold output: {gold_path}")

    spark.stop()


if __name__ == "__main__":
    main()
