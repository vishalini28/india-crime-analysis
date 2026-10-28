from pyspark.sql import SparkSession

# 1. Start Spark
spark = SparkSession.builder.master("local[*]").appName("IndiaCrime").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# 2. Load the two CSV files
ipc = spark.read.csv("1_datasets/processed/ipc_city_2021_2023.csv", header=True, inferSchema=True)
violent = spark.read.csv("1_datasets/processed/violent_city_2021_2023.csv", header=True, inferSchema=True)

# 3. Register them as SQL tables
ipc.createOrReplaceTempView("ipc")
violent.createOrReplaceTempView("violent")

# 4. Join both tables and add two new columns using SQL
crime = spark.sql("""
    SELECT i.city,
           CAST(i.ipc_2021 AS INT) AS ipc_2021,
           CAST(i.ipc_2022 AS INT) AS ipc_2022,
           CAST(i.ipc_2023 AS INT) AS ipc_2023,
           i.ipc_rate_2023,
           CAST(v.violent_2023 AS INT) AS violent_2023,
           ROUND((i.ipc_2023 - i.ipc_2021) * 100.0 / i.ipc_2021, 1) AS growth_pct,
           ROUND(v.violent_2023 * 100.0 / i.ipc_2023, 1) AS violent_share_pct
    FROM ipc i
    JOIN violent v ON i.city = v.city
""")

print("Rows after join:", crime.count())

# 5. Save the clean data as Parquet
crime.write.mode("overwrite").parquet("1_datasets/processed/crime_clean.parquet")
crime.createOrReplaceTempView("crime")

# 6. Answer the questions with SQL
print("Q1. Top 5 cities by crime rate (2023)")
spark.sql("SELECT city, ipc_rate_2023 FROM crime ORDER BY ipc_rate_2023 DESC LIMIT 5").show()

print("Q2. Fastest growing cities, 2021 to 2023")
spark.sql("SELECT city, ipc_2021, ipc_2023, growth_pct FROM crime ORDER BY growth_pct DESC LIMIT 5").show()

print("Q3. Total crimes by year")
spark.sql("SELECT SUM(ipc_2021) AS y2021, SUM(ipc_2022) AS y2022, SUM(ipc_2023) AS y2023 FROM crime").show()

print("Q4. Cities with highest violent crime share (2023)")
spark.sql("SELECT city, violent_share_pct FROM crime ORDER BY violent_share_pct DESC LIMIT 5").show()

print("Q5. Bengaluru, Chennai, Hyderabad")
spark.sql("SELECT * FROM crime WHERE city IN ('Bengaluru', 'Chennai', 'Hyderabad')").show()

spark.stop()
