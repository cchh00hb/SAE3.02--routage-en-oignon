#ce code est a mettre sur la machine debian 2 clientB.py 

from common.network import start_server, send_message
def handle_bob(msg):
    print(f"MESSAGE RECU : {msg}")
    return "Recu par Bob"
print("Client B (Bob) en attente sur port 8888...")
start_server(8888, handle_bob)
 