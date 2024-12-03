from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType
import pyspark.sql.functions as F
from es import Es

def process_youtube_data(spark, input_path):
    schema = StructType([
        StructField("videoId", StringType(), True),
        StructField("title", StringType(), True),
        StructField("viewCount", StringType(), True),
        StructField("likeCount", StringType(), True),
        StructField("commentCount", StringType(), True),
    ])

    # JSON 데이터 읽기 (multiline 옵션 추가)
    df = spark.read.option("multiline", "true").json(input_path, schema=schema)

    # 데이터 검증
    if df.count() == 0:
        raise ValueError(f"No data found in the file: {input_path}")

    # viewCount, likeCount, commentCount 컬럼을 LongType으로 변환
    for col in ["viewCount", "likeCount", "commentCount"]:
        df = df.withColumn(col, F.col(col).cast(LongType()))

    # 제목에서 특수문자 제거
    df = df.withColumn("cleaned_title", F.regexp_replace(F.col("title"), r"[^\w\s]", ""))

    # 조회수 기준 상위 10개 데이터 선택
    top_10_videos = df.orderBy(F.desc("viewCount")).limit(10)

    # 상위 10개 데이터 출력
    top_10_videos.show(truncate=False)

    return top_10_videos


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--target_date", required=True, help="Target date (yyyy-mm-dd)")
    parser.add_argument("--es_index", default="newjeans-youtube-stats", help="Elasticsearch index name")
    args = parser.parse_args()

    # 입력 파일 경로
    input_path = f"/opt/bitnami/spark/data/{args.target_date}.json"

    # SparkSession 초기화
    spark = (SparkSession
             .builder
             .master("local")
             .appName("youtube-data-pipeline")
             .config("spark.driver.extraClassPath", "/opt/bitnami/spark/resources/elasticsearch-spark-30_2.12-8.4.3.jar")
             .config("spark.jars", "/opt/bitnami/spark/resources/elasticsearch-spark-30_2.12-8.4.3.jar")
             .getOrCreate())

    try:
        # 데이터 처리
        df = process_youtube_data(spark, input_path)

        # Elasticsearch에 데이터 저장
        es_index_name = f"{args.es_index}-{args.target_date}"  # 날짜 포함
        es = Es("http://es:9200")
        print(f"Writing data to Elasticsearch index: {es_index_name}")
        es.write_df(df, es_index_name)

    except Exception as e:
        print(f"Pipeline failed: {e}")
        raise

    finally:
        spark.stop()
