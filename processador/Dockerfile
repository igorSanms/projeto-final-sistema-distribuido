FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY alerta.proto .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. alerta.proto

COPY processador.py .

CMD ["python", "-u", "processador.py"]