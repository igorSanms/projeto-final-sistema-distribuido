import socket
import time
import random
import os

PROCESSADOR_HOST = os.getenv("PROCESSADOR_HOST", "localhost")
PROCESSADOR_PORT = 5000

def iniciar_sensor():
    print(f"Iniciando sensor IoT. Conectando a {PROCESSADOR_HOST}:{PROCESSADOR_PORT}...")
    
    while True:
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect((PROCESSADOR_HOST, PROCESSADOR_PORT))
            print("Conectado ao Processador")
            
            while True:
                temperatura = round(random.uniform(40.0, 100.0), 2)
                mensagem = f"{temperatura}\n"
                
                cliente.sendall(mensagem.encode())
                print(f"Temperatura enviada: {temperatura}°C")
                
                time.sleep(2) 
                
        except ConnectionRefusedError:
            print("Processador indisponível. Tentando reconectar em 3 segundos...")
            time.sleep(3)
        except Exception as e:
            print(f"Conexão perdida ({e}). Reconectando...")
            time.sleep(3)

if __name__ == "__main__":
    iniciar_sensor()