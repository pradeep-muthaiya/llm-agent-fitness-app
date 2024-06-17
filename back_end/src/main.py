from fastapi import FastAPI
import uvicorn
import sys

sys.path.insert(0, "")
from routers.router import router as router

app = FastAPI(title="AI Fitness Application")

app.include_router(router, prefix='/aifitnessapp')

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8001)