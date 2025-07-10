FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir . && \
    pip install --no-cache-dir -r lap_time_api/requirements.txt
CMD ["uvicorn", "lap_time_api.main:app", "--host", "0.0.0.0", "--port", "8001"]
