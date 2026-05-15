from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

print("🔥 RUNNING SIGNAL LAB BACKEND")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AudioChunk(BaseModel):
    samples: list

# ✅ global LMS parameters
w = np.zeros(8)
mu = 0.01

@app.options("/process")
def options_handler(request: Request):
    return {}

@app.post("/process")
def process_audio(chunk: AudioChunk):
    global w

    x = np.array(chunk.samples)
    N = len(x)

    y = np.zeros(N)

    for n in range(8, N):
        x_vec = x[n-8:n][::-1]

        y[n] = np.dot(w, x_vec)

        e = x[n] - y[n]

        w = w + mu * e * x_vec

    print("🔥 PROCESS HIT:", N)

    return {"filtered": y.tolist()}

@app.get("/check")
def check():
    return {"msg": "THIS IS MY SIGNAL LAB BACKEND"}