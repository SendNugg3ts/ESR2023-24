import socket
import time
import json
import sys
import os
import re


from Servidor.Servidor import *
from Cliente.Cliente import *

nodeID = sys.argv[1]

current_pwd_path = os.path.dirname(os.path.abspath(__file__))
video_pwd_path = (re.findall("(?:(.*?)src)", current_pwd_path))[0]
path_to_nodeID = os.path.join(video_pwd_path, "util/" + str(nodeID) + ".json")


i = open(path_to_nodeID)

info = json.load(i)

nodeIP = info["ip"]
if info["server"] == "False":
    isServer = False
else:
    isServer = True
hostIP = info["vizinhos"][0]["ip"]


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

def atualizar_medicoes_latencia(cliente_json, nodeID):
    if not isServer:  # Somente para clientes
        for vizinho in cliente_json["vizinhos"]:
            latencia = medir_latencia(vizinho)
            if latencia is not None:
                vizinho["latencia"] = latencia

filename = "movie.Mjpeg"
SERVERPORT = 2500
if isServer:
    StartStreaming(nodeIP, SERVERPORT)
else:
    clientGuiStart(hostIP, SERVERPORT, nodeIP, 3500, nodeID, filename)

if not isServer:
    with open(f"{nodeID}.json", "r") as json_file:
        cliente_json = json.load(json_file)
        atualizar_medicoes_latencia(cliente_json, nodeID)
        with open(f"{nodeID}.json", "w") as json_file:
            json.dump(cliente_json, json_file)

