from fastapi import FastAPI, BackgroundTasks
import torch
from KGAT import main_kgat

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
	# with torch.no_grad():
	# 	batch_scores = model(user_id, item_ids, mode='predict')
	# batch_scores = batch_scores.cpu()
	pass

async def train():
	data = await data_preprocessing()
	model, report = await model_training(data)
	model_url = await save_model_to_cloud_storage(model)
	await alert_slack_channel(model_url, report)

async def data_preprocessing():
	'''
	database에서 데이터를 가져와서 학습에 적합한 형태로 변환
	'''
	pass

async def model_training(data):
	'''
	전처리 시킨 데이터를 이용하여 모델을 학습
	'''
	main_kgat.train()
	pass

async def save_model_to_cloud_storage(model):
	'''
	학습된 모델을 클라우드 스토리지에 저장
	'''
	pass

async def alert_slack_channel():
	'''
	학습이 완료되었음을 slack 채널에 알림
	학습 보고서 전송
	'''
	pass

async def generate_predictions_top_500(model):
	'''
	학습된 모델을 이용하여 모든 유저의 상위 500개의 예측값을 생성
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
	model = torch.load('model.pth')
	model.to('cuda')
	model.eval()