#!/bin/bash

DATA_DIR=/opt/bitnami/spark/data

API_KEY=""
CHANNEL_ID="UCMki_UkHb4qSc0qyEcOHHJw"
TARGET_DATE=$1  # Airflow에서 전달받는 날짜 (yyyy-mm-dd 형식)
DATA_DIR="/opt/bitnami/spark/data"
OUTPUT_PATH="${DATA_DIR}/${TARGET_DATE}.json"

echo "Fetching YouTube Data for date: $TARGET_DATE..."

# Python 스크립트를 실행하여 YouTube 데이터를 가져옵니다.
python3 /opt/airflow/jobs/fetch_youtube_data.py \
  --api_key "${API_KEY}" \
  --channel_id "${CHANNEL_ID}" \
  --output_path "${OUTPUT_PATH}"

if [ $? -eq 0 ]; then
    echo "Data fetch complete. Output saved in ${OUTPUT_PATH}."
else
    echo "Failed to fetch YouTube data." >&2
    exit 1
fi
