FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY proto ./proto
COPY db ./db
COPY server ./server

ENV GRPC_PORT=50051
EXPOSE 50051

CMD ["python", "server/app.py"]
