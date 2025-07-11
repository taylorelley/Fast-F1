# Lap Time API

This directory contains a small FastAPI service that exposes lap time data.

The service depends on the `fastf1` package from this repository. To run it
locally you can use `uvicorn`:

```bash
uvicorn lap_time_api.main:app --reload
```

The service saves every response under `lap_time_api/data` for future use.

A Dockerfile is provided. You can start the API using `docker compose`:

```bash
docker compose up --build lap-time-api
```

which will run the service on port 8001.

## Practice Laps API

The service exposes a single endpoint that returns lap times for practice
sessions.

### `GET /practice-laps`

Load lap timing data for a chosen practice session.

**Query Parameters**

| name     | type | description                                   |
|----------|------|-----------------------------------------------|
|`season`  | int  | **Required.** Season year to load.            |
|`round`   | int  | **Required.** Championship round number.      |
|`session` | int  | Practice session number (1-3). Defaults to `1`.|

**Response**

Returns status `200` with a JSON array where each element represents one lap.
Every object contains the following keys:

| field           | type   | description                                         |
|-----------------|-------|-----------------------------------------------------|
|`date_start`     | string | ISO 8601 timestamp of the lap start.                |
|`driver_number`  | int    | Driver number.                                      |
|`is_pit_out_lap` | bool   | `true` if the lap started with a pit exit.          |
|`lap_duration`   | float  | Lap time in seconds or `null` for incomplete laps.  |
|`lap_number`     | int    | Lap counter within the session.                     |
Responses are cached under `lap_time_api/data/{season}_{round}_FP{session}.json`
and served from disk on subsequent requests.

**Example**

```http
GET /practice-laps?season=2023&round=1&session=1
```

```json
[
  {
    "date_start": "2023-03-03T10:00:15+00:00",
    "driver_number": 44,
    "is_pit_out_lap": true,
    "lap_duration": 93.482,
    "lap_number": 1
  }
]
```
