from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

@app.get('/train')
async def get_train(background_tasks: BackgroundTasks):
	'''
	Background Task

	1. Data Preprocessing
	2. Model Training: Alert Slack Channel
	3. Save Model to Cloud Storage
	4. Generate Predictions top 500
	5. Save Predictions to Redis Cache
	6. Alert Slack Channel: Report Training Status

	'''
	background_tasks.add_task(train)

	return {"message": "Started Training!"}

async def train():
	
	pass


async def data_preprocessing():
	'''
	database에서 데이터를 가져와서 학습에 적합한 형태로 변환
	'''
	pass

async def model_training():
	'''
	전처리 시킨 데이터를 이용하여 모델을 학습
	'''
	pass

async def save_model_to_cloud_storage():
	'''
	학습된 모델을 클라우드 스토리지에 저장
	'''
	pass

async def generate_predictions_top_500():
	'''
	학습된 모델을 이용하여 모든 유저의 상위 500개의 예측값을 생성
	'''
	pass

async def save_predictions_to_redis_cache():
	'''
	생성된 예측값을 redis cache에 저장
	'''
	pass

async def alert_slack_channel():
	'''
	학습이 완료되었음을 slack 채널에 알림
	학습 보고서 전송
	'''
	pass