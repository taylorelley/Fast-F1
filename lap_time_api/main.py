from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import fastf1
import json
from pathlib import Path

app = FastAPI()


def get_practice_laps(season: int, round_: int, session: int) -> list[dict]:
    """Load lap times for a practice session."""
    ses = fastf1.get_session(season, round_, f"FP{session}")
    ses.load()
    laps = ses.laps.fillna("").astype(str)
    return laps.to_dict(orient="records")


def save_practice_laps(data: list[dict], season: int, round_: int, session: int) -> None:
    """Persist lap times to disk as JSON."""
    out_dir = Path(__file__).resolve().parent / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{season}_{round_}_FP{session}.json"
    with out_file.open("w", encoding="utf-8") as f:
        json.dump(data, f)


def load_saved_practice_laps(season: int, round_: int, session: int) -> list[dict] | None:
    """Load cached lap times if available."""
    out_dir = Path(__file__).resolve().parent / "data"
    out_file = out_dir / f"{season}_{round_}_FP{session}.json"
    if out_file.exists():
        with out_file.open("r", encoding="utf-8") as f:
            return json.load(f)
    return None


@app.get("/practice-laps")
async def practice_laps(season: int, round: int, session: int = 1):
    saved = load_saved_practice_laps(season, round, session)
    if saved is None:
        saved = get_practice_laps(season, round, session)
        save_practice_laps(saved, season, round, session)
    return jsonable_encoder(saved)

