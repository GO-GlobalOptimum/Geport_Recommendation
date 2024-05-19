from fastapi import FastAPI

app = FastAPI()

@app.get('/train')
async def train():
	'''
	Background Task
	
	1. Data Preprocessing
	2. Model Training
	3. Model Evaluation
	4. Model Saving
	5. Save Model to Cloud Storage

	retrun: wandb run url
	'''
	
	return {"message": "Started Training!", "wandb_url": "https://wandb.ai/username/project/runs/run_id"}

@app.get('/predict')
async def predict(user_id: int):

	return {"message": "Welcome Home!"}

@app.get('/start')
async def start():
	'''
	Start Model REST API Server

	1. Load Model from Cloud Storage
	2. Start Model REST API Server

	'''
	return {"message": "Model REST API Server Started!"}

@app.get('/stop')
async def stop():
	'''
	Stop Model REST API Server

	1. Stop Model REST API Server(Stop model serving, kill the process)

	'''
	return {"message": "Model REST API Server Stopped!"}