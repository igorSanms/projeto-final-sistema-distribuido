FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY alerta.proto .

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. alerta.proto

COPY dashboard.py .
COPY templates/ templates/

# Flask (8080) gRPC (50051)
EXPOSE 8080 50051

CMD ["python", "-u", "dashboard.py"]