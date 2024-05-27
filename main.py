from fastapi import FastAPI, BackgroundTasks
import torch
from KGAT import main_kgat
import boto3
import os
from datetime import datetime
from dotenv import load_dotenv
import pytz

load_dotenv()

service_name = 's3'
endpoint_url = 'https://kr.object.ncloudstorage.com'
region_name = 'kr-standard'
access_key = os.getenv('NCLOUD_ACCESS_KEY')
secret_key = os.getenv('NCLOUD_SECRET_KEY')

# boto3 클라이언트 생성
s3_client = boto3.client(
    service_name,
    endpoint_url=endpoint_url,
    region_name=region_name,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

app = FastAPI()

model = None

@app.get('/train')
async def get_train(background_tasks: BackgroundTasks):
	'''
	Background Task

	1. Data Preprocessing
	2. Model Training: Alert Slack Channel
	3. Save Model to Cloud Storage
	4. Alert Slack Channel: Report Training Status
	5. Start Model
	'''
	background_tasks.add_task(train)

	return {"message": "Started Training!"}

@app.get('/predict')
async def get_predict(user_id: int):
	'''
	1. Generate Predictions top 500
	2. Save Predictions to Redis Cache

	return: dict
	'''
	top500 = main_kgat.predict_top500(model, user_id)
	print(top500)
	await save_predictions_to_redis_cache()

	return top500

async def train():
	await data_preprocessing()
	# report = await model_training()
	# print(report)
	# model_url = await save_model_to_cloud_storage()
	# print(model_url)
	# await alert_slack_channel(model_url, report)
	await start_model()

async def data_preprocessing():
	'''
	database에서 데이터를 가져와서 학습에 적합한 형태로 변환
	test_datasets에 저장 + object storage에 저장
	'''
	pass

async def model_training():
	'''
	전처리 시킨 데이터를 이용하여 모델을 학습
	'''
	return main_kgat.train()
	

async def save_model_to_cloud_storage():
	'''
	학습된 모델을 클라우드 스토리지에 저장
	'''
	destination_blob_name = "rec_models/" + str(datetime.now(pytz.timezone('Asia/Seoul'))) + ".pth"
	bucket_name = "geport"  # 네이버 클라우드 버킷 이름

    # 이미지를 BytesIO 객체로 변환
	with open("trained_model/model_epoch1.pth", 'rb') as model_file:
		s3_client.put_object(
            Bucket=bucket_name,
            Key=destination_blob_name,
            Body=model_file,
            ACL='public-read'  # public 접근 가능하도록 설정
        )
	return f"{endpoint_url}/{bucket_name}/{destination_blob_name}"

async def alert_slack_channel():
	'''
	학습이 완료되었음을 slack 채널에 알림
	학습 보고서 전송
	'''
	pass


async def save_predictions_to_redis_cache():
	'''
	생성된 예측값을 redis cache에 저장
	'''
	pass

async def start_model():
	'''
	학습된 모델을 서비스에 적용
	'''

	# 기존 모델 삭제
	global model
	del model
	torch.cuda.empty_cache()

	# 최신 모델 로드
	model = main_kgat.load_new_model()
	model.eval()
	print("Model Started!")