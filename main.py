from fastapi import FastAPI, BackgroundTasks
import torch
from KGAT import main_kgat
import boto3
import os
import datasets.preprocessing as preprocessing
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import pytz

load_dotenv()

service_name = 's3'
endpoint_url = 'https://kr.object.ncloudstorage.com'
region_name = 'kr-standard'
access_key = os.getenv('NCLOUD_ACCESS_KEY')
secret_key = os.getenv('NCLOUD_SECRET_KEY')
slack_token = os.getenv('SLACK_TOKEN')
slack_channel = os.getenv('SLACK_CHANNEL')

client = WebClient(token=slack_token)

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
n_items = None

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

async def train():
	# await data_preprocessing()
	await alert_slack_channel("Data Preprocessing Completed! Starting Model Training...")
	await model_training()
	try:
		url = await save_model_to_cloud_storage()
		await alert_slack_channel(f"Model Training Completed! Training Report URL: {url}")
	except Exception as e:
		await alert_slack_channel(f"Model Training Completed! But an error occurred while saving the model to cloud storage. Error: {e}")
	await start_model()

@app.get('/predict')
async def get_predict(user_id: int):
	global n_items
	top500 = main_kgat.predict_top500(model, user_id, n_items)
	top500 = top500.tolist()
	print(top500)

	await save_predictions_to_redis_cache(user_id, top500)

	return top500

async def data_preprocessing():
	preprocessing.data_preprocessing()

async def model_training():
	main_kgat.train()
	
async def save_model_to_cloud_storage():
	destination_blob_name = "rec_models/" + str(datetime.now(pytz.timezone('Asia/Seoul')).date())
	bucket_name = "geport"  # 네이버 클라우드 버킷 이름

	with open("trained_model/model_epoch1.pth", 'rb') as model_file:
		s3_client.put_object(
            Bucket=bucket_name,
            Key=destination_blob_name + "/model_epoch.pth",
            Body=model_file,
            ACL='public-read',
        )

	with open("trained_model/log.log", 'rb') as model_file:
		s3_client.put_object(
            Bucket=bucket_name,
            Key=destination_blob_name + "/log.log",
            Body=model_file,
            ACL='public-read',
        )

	with open("trained_model/metrics.tsv", 'rb') as metrics_file:
		s3_client.put_object(
			Bucket=bucket_name,
			Key=destination_blob_name + "/metrics.tsv",
			Body=metrics_file,
			ACL='public-read',
		)

	return f"{endpoint_url}/{bucket_name}/{destination_blob_name}/metrics.tsv"

async def alert_slack_channel(text: str):
	try:
		response = client.chat_postMessage(
			channel=slack_channel,
			text=text,
		)
	except SlackApiError as e:
		assert e.response["error"]

async def save_predictions_to_redis_cache(user_id: int, top500: list):
	'''
	생성된 예측값을 redis cache에 저장
	key: user_id
	value: top500
	'''
	pass

async def start_model():
	# 기존 모델 삭제
	global model, n_items
	del model
	torch.cuda.empty_cache()

	# 최신 모델 로드
	model, n_items = main_kgat.load_new_model()
	model.eval()
	