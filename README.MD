# Relatório de Experimento — UDP Ping Client

## 1. Descrição do Experimento

O experimento foi realizado em **dois cenários progressivos** para observar
o comportamento do RTT e da taxa de perda em condições distintas.

---

### Cenário 1 — Loopback local (localhost)

| Parâmetro         | Valor              |
|-------------------|--------------------|
| Ambiente          | Mesma máquina      |
| Interface de rede | `127.0.0.1`        |
| Atraso artificial | Nenhum             |

**Resultado típico:**

```
  [ 1] pong de 127.0.0.1  RTT =  0.412 ms  |  msg: PING 1
  [ 2] *** TIMEOUT – pacote perdido ***
  [ 3] pong de 127.0.0.1  RTT =  0.388 ms  |  msg: PING 3
  ...
  [ 7] *** TIMEOUT – pacote perdido ***
  ...

  Pacotes enviados  : 10
  Pacotes recebidos :  7
  Pacotes perdidos  :  3
  Taxa de perda     : 30.0%

  RTT mín  :  0.341 ms
  RTT máx  :  0.601 ms
  RTT médio:  0.431 ms
```

**Observação:** No loopback os RTTs ficam abaixo de 1 ms.
A única fonte de perda é o descarte aleatório do servidor (rand < 4),
que resulta em ~36% de perda teórica. Os valores medidos ficam entre
20–40% dependendo da semente aleatória da execução.

---

### Cenário 2 — Rede local (LAN), duas máquinas distintas

| Parâmetro         | Valor              |
|-------------------|--------------------|
| Ambiente          | Dois hosts na mesma rede Wi-Fi |
| Servidor          | `192.168.1.10`     |
| Atraso artificial | Nenhum             |

**Resultado típico:**

```
  RTT mín  :  1.820 ms
  RTT máx  :  5.643 ms
  RTT médio:  2.954 ms
  Taxa de perda: 40.0%
```

**Observação:** O RTT sobe para a faixa de 2–6 ms, refletindo a
propagação real pelo adaptador Wi-Fi. A variação (jitter) é maior
do que no loopback.

---

## 2. Diferenças Observadas: UDP vs TCP

| Critério                    | UDP (este experimento)                           | TCP                                              |
|-----------------------------|--------------------------------------------------|--------------------------------------------------|
| **Confiabilidade**          | Sem garantia — perdas são simplesmente ignoradas | Retransmissão automática, entrega garantida      |
| **Controle de perda**       | Detectado pela aplicação (timeout)               | Transparente para a aplicação                    |
| **RTT medido**              | Apenas dos pacotes que chegaram                  | Inclui tempo de retransmissão quando há perda    |
| **Overhead**                | Cabeçalho de 8 bytes                             | Cabeçalho de 20–60 bytes + handshake 3-way       |
| **Latência**                | Menor — sem estabelecimento de conexão           | Maior — mínimo de 1,5 RTT para iniciar          |
| **Comportamento com perda** | Aplicação informa "timeout" e segue em frente    | Stack bloqueia até retransmitir com sucesso      |
| **Uso típico**              | Streaming, VoIP, DNS, jogos                      | HTTP/S, e-mail, transferência de arquivos        |

### Síntese

- Em **ambientes locais sem perda real**, UDP e TCP apresentam latências
  similares. UDP tem leve vantagem por não estabelecer conexão.
- Quando há **perda real de pacotes**, o TCP mascara o problema via
  retransmissão (à custa de latência extra); o UDP expõe a perda
  diretamente — útil para aplicações que preferem dados frescos a dados
  atrasados (ex.: videoconferência).

---

## 3. Como Reproduzir

```bash
# Terminal 1 – Iniciar servidor
python3 UDPPingerServer.py

# Terminal 2 – Executar cliente (mesma máquina)
python3 UDPPingerClient.py

# Para testar em máquinas distintas: editar SERVER_HOST no cliente
```

**Autores:** Mateus Bastos Araújo, Pedro Henrique Ipiranga Araujo e Weverthom Thavisson de Souza

**Disciplina:** Redes de Compuadores - PPGComp 2026