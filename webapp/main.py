import asyncio
from pathlib import Path

from fastapi import (
    FastAPI,
    Request,
    WebSocket
)
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

import fastf1


stream_task = None
stream_enabled = False

app = FastAPI()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/historical")
async def historical(season: int, round: int):
    session = fastf1.get_session(season, round, "R")
    session.load()
    results = session.results.fillna("").astype(str)
    return jsonable_encoder(results.to_dict(orient="records"))


@app.post("/admin/start")
async def admin_start():
    global stream_enabled
    stream_enabled = True
    return {"status": "started"}


@app.post("/admin/stop")
async def admin_stop():
    global stream_enabled
    stream_enabled = False
    return {"status": "stopped"}

# Simple websocket streaming from example data
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    # Stream from a sample live data file as demonstration
    path = "fastf1/testing/reference_data/livedata/2021_1_FP3.txt"
    with open(path) as f:
        for line in f:
            if not stream_enabled:
                break
            await ws.send_text(line.strip())
            await asyncio.sleep(0.05)
    await ws.send_text("[stream ended]")
    await ws.close()
