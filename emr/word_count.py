from pyspark.sql import SparkSession
import argparse
from pyspark.sql.functions import explode, split, lower, regexp_replace, col, input_file_name


def process_texts(input_path, output_path):
    spark = SparkSession.builder.appName("WordCount").getOrCreate()

    text_files = spark.read.text(f"{input_path}/*.txt").withColumn("filename", input_file_name())

    words_df = text_files \
        .select(input_file_name().alias("filename"), lower(col("value")).alias("text")) \
        .select(col("filename"), regexp_replace(col("text"), "[^a-zA-Z\\s]", "").alias("text")) \
        .select(col("filename"), explode(split(col("text"), "\\s+")).alias("word")) \
        .filter(col("word") != "") \
        .groupBy("filename", "word") \
        .count()

    words_df.orderBy("filename", "word").write.mode("overwrite").csv(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="S3 input path (e.g. s3://bucket/input)")
    parser.add_argument("--output", required=True, help="S3 output path (e.g. s3://bucket/output)")
    args = parser.parse_args()

    process_texts(args.input, args.output)
