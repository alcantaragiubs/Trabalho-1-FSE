import json
import threading
import time
import socket

import RPi.GPIO as GPIO

import sys

sys.path.append('../shared')

import semaforos, botoes, geral, variaveis_globais

mensagem = ''
infracoes_sinal = 0
infracoes_velocidade = 0
carrosPrincipal = 0
totalCarrosPrincipal = 0
totalCarrosAuxiliar = 0
tempo_inicial = time.time()
tempo_decorrido = 0
totalCarrosPrincipalPorMinuto = 0
totalCarrosAuxiliarPorMinuto = 0


def client(config):
    global infracoes_sinal
    global infracoes_velocidade
    global carrosPrincipal
    global totalCarrosPrincipal
    global totalCarrosAuxiliar
    global tempo_inicial
    global totalCarrosPrincipalPorMinuto
    global totalCarrosAuxiliarPorMinuto
    
    while True:
        try:

            # Criar um socket TCP/IP
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Conectar-se ao servidor
            client_socket.connect((config['host_central'], config['porta_central']))

            while True:

                momento_atual = time.time()
                
                infracoes_sinal = (
                    variaveis_globais.contador_infracoes_principal1
                    + variaveis_globais.contador_infracoes_principal2
                    + variaveis_globais.contador_infracoes_auxiliar1
                    + variaveis_globais.contador_infracoes_auxiliar2
                )
                
                print(f'Infrações sinal: {infracoes_sinal}')
                
                infracoes_velocidade = (
                    variaveis_globais.contador_infracoes_velocidade_auxiliar1
                    + variaveis_globais.contador_infracoes_velocidade_auxiliar2
                    + variaveis_globais.contador_infracoes_velocidade_principal1
                    + variaveis_globais.contador_infracoes_velocidade_principal2
                )

                print(f'Infrações velocidade: {infracoes_velocidade}')

                totalCarrosPrincipal = (
                    variaveis_globais.contador_carros_principal1
                    + variaveis_globais.contador_carros_principal2
                )

                totalCarrosAuxiliar = (
                    variaveis_globais.contador_carros_auxiliar1 
                    + variaveis_globais.contador_carros_auxiliar2
                )


                tempo_decorrido = momento_atual - tempo_inicial

                if tempo_decorrido > 60:
                    totalCarrosPrincipalPorMinuto = 0 
                    totalCarrosAuxiliarPorMinuto = 0
                    variaveis_globais.contador_carros_principal1 = 0
                    variaveis_globais.contador_carros_principal2 = 0
                    variaveis_globais.contador_carros_auxiliar1 = 0 
                    variaveis_globais.contador_carros_auxiliar2 = 0
                    tempo_inicial = momento_atual
                    tempo_decorrido = 0

                else:
                    totalCarrosPrincipalPorMinuto = totalCarrosPrincipal
                    totalCarrosAuxiliarPorMinuto = totalCarrosAuxiliar
                

                print(f'Tempo decorrido (segundos): {tempo_decorrido}')
                print(f'Total Carros Pincipal: {totalCarrosPrincipalPorMinuto}')
                print(f'Total Carros Auxiliar 1: {totalCarrosAuxiliarPorMinuto}')

                print(f'Velocidade Principal {variaveis_globais.registraVelocidadePrincipal}')
                print(f'Velocidade Auxiliar 1 {variaveis_globais.registraVelocidadeAuxiliar}')

                    

                mensagem1 = {
                    "arquivo_id": 1,
                    "dados": {
                        "infracoes_sinal1": infracoes_sinal,
                        "count_prin1": totalCarrosPrincipalPorMinuto,
                        "count_aux1": totalCarrosAuxiliarPorMinuto,
                        "registraVelocidadePrincipal1": variaveis_globais.registraVelocidadePrincipal,
                        "registraVelocidadeAuxiliar1": variaveis_globais.registraVelocidadeAuxiliar,
                        "infracoes_velocidade1": infracoes_velocidade
                    }
                }
                # Enviar mensagem para o servidor central
                client_socket.send(json.dumps(mensagem1).encode())

                # Receber resposta do servidor central
                received_data = client_socket.recv(1024).decode()
                #print("Servidor:", received_data)

                # Se a mensagem recebida do servidor central for vazia, tenta de novo
                if received_data == '':
                    print('Erro ao enviar mensagem para o servidor, tentando novamente...')
                    client_socket.close()
                    return client(config)
                
                time.sleep(2)
                
                # Fechar a conexão com o servidor
                # client_socket.close()
    
        except Exception as e:
            print("Erro:", e)
            print("Tentando estabelecer conexão com o servidor...")
            time.sleep(1)
            return client(config)

# Comunicação com o servidor distribuído
# Lida com a conexão de um servidor central
def handle_server(client_socket, addr):
    global mensagem
    print(f"Conexão com servidor central em {addr}")

    while True:
        try:
            # Receber dados do servidor central
            received_data = client_socket.recv(1024).decode()
            data_received = json.loads(received_data)
            if not received_data:
                break
            
            mensagem = data_received['opcao']
            print(f'Opção selecionada: {mensagem}')


            # Enviar resposta para o cliente
            response = {"message": "Recebido: " + received_data}
            json_response = json.dumps(response)
            client_socket.send(json_response.encode())

        except Exception as e:
            print(f"Erro na conexão com servidor distribuído em {addr}: {e}")
            break

    # Fecha a conexão com o servidor distribuído
    client_socket.close()
    print(f"Conexão com servidor distribuído em {addr} fechada")

# Inicia a comunicação com o servidores central
def iniciar_comunicacao_servidor_central():
    # Leitura de configurações
    config = geral.carregar_configuracoes('config_cruzamento1.json')
    
    # Configuração do distribuído 1
    porta_distribuido1 = config['porta_distribuido1']
    host_distribuido1 = config['host_distribuido1']
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host_distribuido1, porta_distribuido1)) # Muda a configuração para a placa sendo usada
    servidor.listen(2)  # Suporta até 2 conexões pendentes (uma de cada servidor distribuído)

    print(f"Servidor Distribuído 1 ouvindo na porta {porta_distribuido1}...")

    while True:
        # Aguarda conexões dos servidores distribuídos
        conexao, endereco = servidor.accept()
        print(f"Conexão estabelecida com {endereco}")
        
        # Inicia uma nova thread para lidar com a conexão do servidor distribuído
        server_handler = threading.Thread(target=handle_server, args=(conexao, endereco))
        server_handler.start()

def main():
    global mensagem
    config = geral.carregar_configuracoes('config_cruzamento1.json')  # Carrega configurações do JSON
    botoes.configurar_gpio(config)  # Configura GPIO com base nas configurações
    
    # Inicia controle
    thread1 = threading.Thread(target=semaforos.controlar_semaforos_principal, args=(config,))
    thread2 = threading.Thread(target=botoes.captura_eventos, args=(config,))
    thread3 = threading.Thread(target=botoes.trata_eventos, args=())
    thread4 = threading.Thread(target=botoes.monitorar_botao_passa_auxiliar1, args=(config,))
    thread5 = threading.Thread(target=botoes.monitorar_botao_passa_auxiliar2, args=(config,))
    thread6 = threading.Thread(target=botoes.monitorar_botao_passa_principal1, args=(config,))
    thread7 = threading.Thread(target=botoes.monitorar_botao_passa_principal2, args=(config,))
    thread8 = threading.Thread(target=botoes.monitorar_botao_para, args=())
    thread9 = threading.Thread(target=client, args=(config,)) 
    thread10 = threading.Thread(target=semaforos.modoEmergencia, args=(config,))
    thread11 = threading.Thread(target=semaforos.modoNoturno, args=(config,))
    thread12 = threading.Thread(target=iniciar_comunicacao_servidor_central, args=())

    thread12.start()
    #mensagem = '1'

    while True:
        print(f'Mensagem = {mensagem}')
        if mensagem == '1':
            thread1.start()
            thread2.start()
            thread3.start()
            thread4.start()
            thread5.start()
            thread6.start()
            thread7.start()
            thread8.start()
            thread9.start()

            thread1.join()
            thread2.join()
            thread3.join()
            thread4.join()
            thread5.join()
            thread6.join()
            thread7.join()
            thread8.join()
            thread9.join()

        elif mensagem == '2':
            thread10.start()
            thread10.join()

        elif mensagem == '3':
            print(f'Opção Selecionada funcionando')
            thread11.start()
            thread11.join()
        
        time.sleep(0.3)


if __name__ == "__main__":
    main()