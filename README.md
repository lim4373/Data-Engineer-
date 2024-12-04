# 유튜브 NewJeans 영상 분석 프로젝트
![image](https://github.com/user-attachments/assets/07acdf41-d5a2-44c9-a9d4-e250300eae5c)

## 📌 목적
NewJeans 유튜브 채널의 데이터 수집 및 분석을 자동화하여 효율적인 데이터 관리와 시각화를 구현하는 것을 목표로 합니다.

---

## 📂 파이프라인
1. **데이터 추출**:
   - Airflow를 사용하여 NewJeans 유튜브 채널의 영상 데이터를 자동으로 수집합니다.
   - 수집 데이터: 조회수, 좋아요 수, 댓글 수.

2. **데이터 전처리**:
   - Spark를 활용하여 수집된 데이터를 정제하고 필요한 형식으로 변환합니다.

3. **데이터 저장 및 시각화**:
   - 전처리된 데이터를 Elasticsearch에 저장.
   - Kibana를 통해 데이터 트렌드를 시각화하여 유의미한 인사이트를 제공합니다.

---

## 🛠 기술 스택
- **Airflow**: 데이터 수집 및 워크플로 자동화.
- **Spark**: 대규모 데이터 처리 및 전처리.
- **Elasticsearch**: 데이터 저장소로 활용.
- **Kibana**: 데이터 시각화 도구.
- **Docker**: YAML 기반 환경 설정 및 컨테이너화.

---

## ✨ 주요 특징
- **Airflow DAG**을 사용하여 작업 스케줄링을 자동화하여 반복적인 작업을 효율화.
- **YAML 기반 Docker 환경** 설정으로 손쉬운 배포 및 실행 환경 구축.
- **Kibana 시각화**를 통해 조회수, 좋아요 수, 댓글 수 등 주요 지표의 트렌드를 직관적으로 확인 가능.

---




![image](https://github.com/user-attachments/assets/21b6f86b-98a2-4c20-84a1-0e8f6949f191)

### airflow log
![image](https://github.com/user-attachments/assets/9091433b-d2de-4db2-8361-69b9e3e7f702)

### elasticsearch
![image](https://github.com/user-attachments/assets/2d204cd6-0a24-4fdc-b18f-454514209ca0)


### kibana
![image](https://github.com/user-attachments/assets/8c0e23e0-43a6-47c6-84a9-d9def21ab802)
