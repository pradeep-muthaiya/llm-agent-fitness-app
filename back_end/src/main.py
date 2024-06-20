from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:8080",
]

sys.path.insert(0, "")
from routers.router import router as router

app = FastAPI(title="AI Fitness Application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix='/aifitnessapp')

if __name__ == '__main__':
    #uvicorn.run("main:app", host="127.0.0.1", port=8001)
    uvicorn.run("main:app", host="0.0.0.0", port=8001)