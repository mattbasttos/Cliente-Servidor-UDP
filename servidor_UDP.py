import random
from socket import *

SERVER_PORT = 12000
LOSS_THRESHOLD = 4   # pacotes com rand < 4 são descartados (≈ 36 % de perda)

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', SERVER_PORT))

print(f"[Servidor] Aguardando conexões na porta {SERVER_PORT} ...")
print(f"[Servidor] Limiar de descarte: rand < {LOSS_THRESHOLD}  "
      f"(perda simulada ≈ {LOSS_THRESHOLD/11*100:.0f}%)\n")

while True:
    rand = random.randint(0, 10)
    message, address = serverSocket.recvfrom(1024)
    message_upper = message.upper()

    if rand < LOSS_THRESHOLD:
        print(f"  [DESCARTADO] rand={rand}  msg={message.decode()!r}  de {address}")
        continue

    serverSocket.sendto(message_upper, address)
    print(f"  [ENVIADO]    rand={rand}  msg={message_upper.decode()!r}  → {address}")