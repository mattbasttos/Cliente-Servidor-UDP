import time
from socket import *

# Configurações
SERVER_HOST = 'localhost'   # Altere para o IP do servidor em testes remotos
SERVER_PORT = 12000
NUM_PINGS   = 10
TIMEOUT     = 1.0           # segundos – tempo máximo de espera por resposta

def run_ping():
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)

    rtts        = []   # lista com os RTTs bem-sucedidos (ms)
    lost        = 0    # contador de pacotes perdidos

    print("=" * 55)
    print(f"  UDP Ping  →  {SERVER_HOST}:{SERVER_PORT}  ({NUM_PINGS} mensagens)")
    print("=" * 55)

    for seq in range(1, NUM_PINGS + 1):
        message = f"ping {seq}"

        send_time = time.time()                        # marca t0

        try:
            # Envio 
            client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))

            # Recepção 
            response, server_addr = client_socket.recvfrom(1024)
            recv_time = time.time()                    # marca t1

            rtt_ms = (recv_time - send_time) * 1000   # converte para ms
            rtts.append(rtt_ms)

            print(f"  [{seq:>2}] pong de {server_addr[0]}  "
                  f"RTT = {rtt_ms:.3f} ms  |  msg: {response.decode()}")

        except timeout:
            lost += 1
            print(f"  [{seq:>2}] *** TIMEOUT – pacote perdido ***")

    client_socket.close()

    # Estatísticas 
    received   = NUM_PINGS - lost
    loss_rate  = (lost / NUM_PINGS) * 100

    print("\n" + "=" * 55)
    print("  Estatísticas")
    print("=" * 55)
    print(f"  Pacotes enviados  : {NUM_PINGS}")
    print(f"  Pacotes recebidos : {received}")
    print(f"  Pacotes perdidos  : {lost}")
    print(f"  Taxa de perda     : {loss_rate:.1f}%")

    if rtts:
        rtt_min  = min(rtts)
        rtt_max  = max(rtts)
        rtt_avg  = sum(rtts) / len(rtts)
        print(f"\n  RTT mín  : {rtt_min:.3f} ms")
        print(f"  RTT máx  : {rtt_max:.3f} ms")
        print(f"  RTT médio: {rtt_avg:.3f} ms")
    else:
        print("\n  Nenhuma resposta recebida – RTT não calculado.")

    print("=" * 55)

if __name__ == "__main__":
    run_ping()