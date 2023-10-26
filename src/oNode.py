import socket
import time
import json

def medir_latencia(vizinho):
    try:
        start_time = time.time()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(1)  # Defina um tempo limite para a resposta
            s.connect((vizinho["ip"], vizinho["porta"]))
            s.send(b"PING")  # Envie um pacote de ping
            s.recv(1024)  # Aguarde a resposta
        end_time = time.time()
        latencia = (end_time - start_time) * 1000  # Converta para milissegundos
        return latencia
    except Exception as e:
        return None



# Função para atualizar o JSON com as medições de latência
def atualizar_medicoes_latencia(cliente_json):
    for vizinho in cliente_json["vizinhos"]:
        latencia = medir_latencia(vizinho)
        if latencia is not None:
            vizinho["latencia"] = latencia

# Aqui você carrega o JSON do cliente, faz a medição de latência e atualiza o JSON
with open("cliente1.json", "r") as json_file:
    cliente_json = json.load(json_file)
    atualizar_medicoes_latencia(cliente_json)
    # Salve o JSON atualizado de volta no arquivo, se necessário
    with open("cliente1.json", "w") as json_file:
        json.dump(cliente_json, json_file)

# Resto do seu código
