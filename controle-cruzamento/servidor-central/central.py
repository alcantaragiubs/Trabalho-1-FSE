import json
import socket
import time
import threading

mensagem = None
contadorPrincipal1 = 0
contadorPrincipal2 = 0
contadorAuxiliar1 = 0
contadorAuxiliar2 = 0
infracoesSinalVia1 = 0
infracoesVelocidadeVia1 = 0
infracoesSinalVia2 = 0
infracoesVelocidadeVia2 = 0
velocidadePrincipal1 = []
velocidadeAuxiliar1 = []
velocidadeAuxiliar2 = []
velocidadePrincipal2 = []
somaVelocidadePrincipal1 = 0
somaVelocidadePrincipal2 = 0
somaVelocidadePrincipal = 0
tamanhoVelocidadePrincipal = 0
velocidadeMediaPrincipal = 0
somaVelocidadeAuxiliar1 = 0
tamanhoAuxiliar1 = 0
velocidadeMediaAuxiliar1 = 0
somaVelocidadeAuxiliar2 = 0
tamanhoAuxiliar2 = 0
velocidadeMediaAuxiliar2 = 0

def carregar_configuracoes(nomeArquivo):
    with open(nomeArquivo, 'r') as arquivo_config:
        config = json.load(arquivo_config)
    return config

#Client do servidor distribuído
def client(config, mensagem, host, porta):
   
    while True:
        try:
            # Criar um socket TCP/IP
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Conectar-se ao servidor
            client_socket.connect((host, porta))

            while True:
                if mensagem != None:

                    # Enviar mensagem para o servidor central
                    client_socket.send(json.dumps(mensagem).encode())

                    # Receber resposta do servidor central
                    received_data = client_socket.recv(1024).decode()
                    print("Servidor:", received_data)


                    # Se a mensagem recebida do servidor central for vazia, tenta de novo
                    if received_data == '':
                        print('Erro ao enviar mensagem para o servidor, tentando novamente...')
                        client_socket.close()
                        return client(config, mensagem, host, porta)

                    mensagem = None
                time.sleep(1)
    
        except Exception as e:
            print("Erro:", e)
            print("Tentando estabelecer conexão com o servidor...")
            time.sleep(1)
            return client(config, mensagem, host, porta)

# Lida com a conexão de um servi    dor distribuído
def handle_server(client_socket, addr):
    global contadorPrincipal1
    global contadorAuxiliar1
    global contadorAuxiliar2
    global infracoesSinalVia1
    global infracoesVelocidadeVia1
    global infracoesSinalVia2
    global infracoesVelocidadeVia2
    global contadorPrincipal2
    global velocidadePrincipal1
    global velocidadePrincipal2
    global somaVelocidadePrincipal1
    global somaVelocidadePrincipal2
    global tamanhoPrincipal1
    global tamanhoPrincipal2
    global tamanhoVelocidadePrincipal
    global velocidadeAuxiliar1
    global velocidadeAuxiliar2
    global somaVelocidadePrincipal
    global somaVelocidadeAuxiliar1
    global tamanhoAuxiliar1
    global tamanhoAuxiliar2
    global somaVelocidadeAuxiliar2
    global velocidadeMediaPrincipal
    global velocidadeMediaAuxiliar1
    global velocidadeMediaAuxiliar2

    print(f"Conexão com servidor distribuído em {addr}")

    while True:
        try:
            # Receber dados do servidor distribuído
            received_data = client_socket.recv(1024).decode()
            mensagem = json.loads(received_data)

            if not received_data:
                break
            
            arquivo_id = mensagem["arquivo_id"]
            dados = mensagem["dados"]

            if arquivo_id == 1:
                contadorPrincipal1 = dados['count_prin1']
                contadorAuxiliar1 = dados['count_aux1']
                infracoesSinalVia1 = dados['infracoes_sinal1']
                infracoesVelocidadeVia1 = dados['infracoes_velocidade1']
                velocidadePrincipal1 = dados['registraVelocidadePrincipal1']
                velocidadeAuxiliar1 = dados['registraVelocidadeAuxiliar1']

            elif arquivo_id == 2:
                contadorPrincipal2 = dados['count_prin2']
                contadorAuxiliar2 = dados['count_aux2']
                infracoesSinalVia2 = dados['infracoes_sinal2']
                infracoesVelocidadeVia2 = dados['infracoes_velocidade2']
                velocidadePrincipal2 = dados['registraVelocidadePrincipal2']
                velocidadeAuxiliar2 = dados['registraVelocidadeAuxiliar2']

            somaVelocidadePrincipal1 = sum(velocidadePrincipal1)
            somaVelocidadePrincipal2 = sum(velocidadePrincipal2)
            
            tamanhoPrincipal1 = len(velocidadePrincipal1)
            tamanhoPrincipal2 = len(velocidadePrincipal2)

            somaVelocidadePrincipal = somaVelocidadePrincipal1 + somaVelocidadePrincipal2

            tamanhoVelocidadePrincipal = tamanhoPrincipal1 + tamanhoPrincipal2

            if tamanhoVelocidadePrincipal > 0:
                velocidadeMediaPrincipal = somaVelocidadePrincipal/tamanhoVelocidadePrincipal
            else:
                print(f'Nenhum carro passou na Via Principal ainda')
            
            somaVelocidadeAuxiliar1 = sum(velocidadeAuxiliar1)
            somaVelocidadeAuxiliar2 = sum(velocidadeAuxiliar2)

            tamanhoAuxiliar1 = len(velocidadeAuxiliar1)
            tamanhoAuxiliar2 = len(velocidadeAuxiliar2)

            if tamanhoAuxiliar1 > 0:
                velocidadeMediaAuxiliar1 = somaVelocidadeAuxiliar1/tamanhoAuxiliar1
            else:
                print(f'Nenhum carro passou na Via Auxiliar 1 ainda')

            if tamanhoAuxiliar2 > 0:
                velocidadeMediaAuxiliar2 = somaVelocidadeAuxiliar2/tamanhoAuxiliar2
            else:
                print(f'Nenhum carro passou na Via Auxiliar 1 ainda')

            print(f"Via Principal - Carros/min: {contadorPrincipal1 + contadorPrincipal2}")
            print(f"Via Auxiliar 1 - Carros/min: {contadorAuxiliar1}")
            print(f"Via Auxiliar 2 - Carros/min: {contadorAuxiliar2}\n")

            print(f"Via Principal - Velocidade Média: {velocidadeMediaPrincipal}")
            print(f"Via Auxiliar 1 - Velocidade Média : {velocidadeMediaAuxiliar1}")
            print(f"Via Auxiliar 2 - Velocidade Média: {velocidadeMediaAuxiliar2}\n")

            print(f"Total de Infrações - Sinal Vermelho: {infracoesSinalVia1 + infracoesSinalVia2}")
            print(f"Total de Infrações - Velocidade: {infracoesVelocidadeVia1 + infracoesVelocidadeVia2}\n")
            
            # Enviar resposta para o cliente
            response = {"mensagem": "Recebido: " + received_data}
            json_response = json.dumps(response)
            client_socket.send(json_response.encode())

        except Exception as e:
            print(f"Erro na conexão com servidor distribuído em {addr}: {e}")
            break

    # Fecha a conexão com o servidor distribuído
    client_socket.close()
    print(f"Conexão com servidor distribuído em {addr} fechada")

# Inicia a comunicação com os servidores distribuídos
def iniciar_comunicacao_servidores_central():
    # Leitura de configurações
    config = carregar_configuracoes('config.json')
    
    # Configuração do servidor central
    porta_servidor = config['porta_servidor']
    host_servidor  = config['host_servidor']
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host_servidor, porta_servidor)) # Muda a configuração para a placa sendo usada
    servidor.listen(2)  # Suporta até 2 conexões pendentes (uma de cada servidor distribuído)

    print(f"Servidor Central ouvindo na porta {porta_servidor}...")

    while True:
        # Aguarda conexões dos servidores distribuídos
        conexao, endereco = servidor.accept()
        print(f"Conexão estabelecida com {endereco}")
        
        # Inicia uma nova thread para lidar com a conexão do servidor distribuído
        server_handler = threading.Thread(target=handle_server, args=(conexao, endereco))
        server_handler.start()

def main():
    global mensagem
    config = carregar_configuracoes('config.json')
    

    print(f'1. Modo padrão')
    print(f'2. Modo Emergência')
    print(f'3. Modo Noturno')
    entrada = input("Informe a opção de funcionamento desejada:")

    thread2 = threading.Thread(target=iniciar_comunicacao_servidores_central, args=()) 

    if entrada == '1':
        mensagem = {'opcao': '1'}
        thread2.start()

    elif entrada == '2':
        # iniciar comunicacao com modo de emergencia
        mensagem = {'opcao': '2'}
    else:
        # iniciar comunicacao com modo noturno
        mensagem = {'opcao': '3'}
        #Duas threads pra cada client
    thread1 = threading.Thread(target=client, args=(config, mensagem, config['host_distribuido1'], config['porta_servidor_distribuido1']))
    thread3 = threading.Thread(target=client, args=(config, mensagem, config['host_distribuido2'], config['porta_servidor_distribuido2']))  
    thread1.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()

if __name__ == "__main__":
    main()
    
