
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("VerifyEcommercePipeline")
    .master("local[*]")
    .getOrCreate()
)

silver = spark.read.parquet("data/processed/silver/products")
gold = spark.read.parquet("data/processed/gold/category_summary")

print("Silver record count:", silver.count())
print("Gold category count:", gold.count())

print("\nGold analytics:")
gold.show(truncate=False)

spark.stop()
