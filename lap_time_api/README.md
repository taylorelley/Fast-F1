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
