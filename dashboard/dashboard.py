import grpc
import threading
from concurrent import futures
from flask import Flask, render_template, jsonify
import alerta_pb2
import alerta_pb2_grpc
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

historico = []

estatisticas = {
    "maior_temp": 0.0,
    "menor_temp": 999.0,
    "soma_temp": 0.0,
    "total_leituras": 0
}

fuso_brasil = timezone(timedelta(hours=-3))

class AlertaServicer(alerta_pb2_grpc.AlertaServiceServicer):
    def Notificar(self, request, context):
        temp = round(request.temperatura, 1)
        agora = datetime.now(fuso_brasil).strftime("%H:%M:%S")
        
        if temp > estatisticas["maior_temp"]: estatisticas["maior_temp"] = temp
        if temp < estatisticas["menor_temp"]: estatisticas["menor_temp"] = temp
        estatisticas["soma_temp"] += temp
        estatisticas["total_leituras"] += 1

        dado = {
            "tempo": agora,
            "temperatura": temp,
            "origem": request.origem,
            "is_alerta": request.is_alerta
        }
        
        historico.append(dado)
        if len(historico) > 20:
            historico.pop(0)
            
        return alerta_pb2.AlertaResponse(sucesso=True)

def iniciar_grpc():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    alerta_pb2_grpc.add_AlertaServiceServicer_to_server(AlertaServicer(), servidor)
    servidor.add_insecure_port('[::]:50051')
    servidor.start()
    servidor.wait_for_termination()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/dados')
def get_dados():
    media = 0.0
    if estatisticas["total_leituras"] > 0:
        media = round(estatisticas["soma_temp"] / estatisticas["total_leituras"], 1)
        
    return jsonify({
        "historico": historico,
        "estatisticas": {
            "maior_temp": estatisticas["maior_temp"],
            "menor_temp": estatisticas["menor_temp"],
            "media_temp": media
        }
    })

if __name__ == "__main__":
    thread_grpc = threading.Thread(target=iniciar_grpc)
    thread_grpc.daemon = True
    thread_grpc.start()
    app.run(host='0.0.0.0', port=8080)