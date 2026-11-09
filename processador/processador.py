import socket
import grpc
import os
import alerta_pb2
import alerta_pb2_grpc

DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "localhost")
DASHBOARD_PORT = 50051
SOCKET_PORT = 5000

def notificar_dashboard(temperatura, is_alerta):
    try:
        with grpc.insecure_channel(f"{DASHBOARD_HOST}:{DASHBOARD_PORT}") as canal:
            cliente = alerta_pb2_grpc.AlertaServiceStub(canal)
            requisicao = alerta_pb2.AlertaRequest(
                temperatura=temperatura, 
                origem="Sensor-1",
                is_alerta=is_alerta
            )
            cliente.Notificar(requisicao)
    except Exception as e:
        print(f"Erro ao tentar notificar o dashboard via gRPC: {e}")

def iniciar_processador():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(('0.0.0.0', SOCKET_PORT))
    servidor.listen(5)
    print(f"Processador escutando conexões Socket na porta {SOCKET_PORT}...")

    while True:
        conexao, endereco = servidor.accept()
        try:
            while True:
                dados = conexao.recv(1024)
                if not dados:
                    break
                
                temperatura_str = dados.decode().strip()
                if temperatura_str:
                    temperatura = float(temperatura_str)
                    
                    is_alerta = temperatura > 80.0
                    
                    if is_alerta:
                        print(f"ALERTA: {temperatura}°C Notificando Dashboard...")
                    else:
                        print(f"Normal: {temperatura}°C. Enviando para gráfico...")
                        
                    notificar_dashboard(temperatura, is_alerta)
        except Exception:
            pass
        finally:
            conexao.close()

if __name__ == "__main__":
    iniciar_processador()