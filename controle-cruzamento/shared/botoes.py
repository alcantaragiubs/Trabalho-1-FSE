
import time
import RPi.GPIO as GPIO

import sys

sys.path.append('..')

import variaveis_globais

botao_para_pressionado = False
botao_para_pressionado_principal = False

botao_passa_pressionado_auxiliar1 = False
botao_passa_pressionado_auxiliar2 = False
botao_passa_pressionado_principal1 = False
botao_passa_pressionado_principal2 = False

tempo_pressionado = 0
tempo_inicial = 0
tempo_final = 0

# Função para configurar as GPIO com base nas configurações
def configurar_gpio(config):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Configura os pinos GPIO com base nas informações do JSON
    configurar_pinos(config['pinos_gpio'])

# Função para configurar os pinos GPIO com base nas informações do JSON
def configurar_pinos(pinos_gpio):
    for _, info in pinos_gpio.items():
        pino = info['numero']
        tipo = info['tipo']

        if tipo == 'saida':
            GPIO.setup(pino, GPIO.OUT)
        elif tipo == 'entrada':
            GPIO.setup(pino, GPIO.IN)

def captura_eventos(config):
    global botao_pedestre_1
    global botao_pedestre_2
    global botao_auxiliar_1
    global botao_auxiliar_2
    global botao_principal_1
    global botao_principal_2

    # GPIO do botao de pedestre 1
    botao_pedestre_1_gpio = config['pinos_gpio']['botao_pedestre1']['numero']
    # GPIO do botao de pedestre 2
    botao_pedestre_2_gpio = config['pinos_gpio']['botao_pedestre2']['numero']
    # GPIO do botao da via auxiliar 1
    botao_auxiliar1_gpio = config['pinos_gpio']['botao_auxiliar1']['numero']
    # GPIO do botao da via auxiliar 2
    botao_auxiliar2_gpio = config['pinos_gpio']['botao_auxiliar2']['numero']
    # GPIO do botao da via principa 1
    botao_principal1_gpio = config['pinos_gpio']['botao_principal1']['numero']
    # GPIO do botao da via principal 2
    botao_principal2_gpio = config['pinos_gpio']['botao_principal2']['numero']

    # Configura o botao como entrada e configura como pull down
    GPIO.setup(botao_pedestre_1_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(botao_pedestre_2_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(botao_auxiliar1_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(botao_auxiliar2_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(botao_principal1_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(botao_principal2_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    while True:
        botao_pedestre_1 = GPIO.input(botao_pedestre_1_gpio)
        botao_pedestre_2 = GPIO.input(botao_pedestre_2_gpio)
        botao_auxiliar_1 = GPIO.input(botao_auxiliar1_gpio)
        botao_auxiliar_2 = GPIO.input(botao_auxiliar2_gpio)
        botao_principal_1 = GPIO.input(botao_principal1_gpio)
        botao_principal_2 = GPIO.input(botao_principal2_gpio)

        time.sleep(0.160) # realiza a leitura a cada 160 ms

def calcular_velocidade(tempo_inicial, tempo_final):

    # Calcular o tempo decorrido entre a ativação e desativação do sensor
    tempo_decorrido = (tempo_final - tempo_inicial) / 3600  # Converter segundos para horas

    # Assumindo que a distância é constante (0.002 km = 2 metro)
    distancia = 0.002  # Altere a distância de acordo com o seu cenário

    # Calcular a velocidade (velocidade = distância / tempo)
    velocidade = distancia / tempo_decorrido if tempo_decorrido > 0 else 0

    return velocidade

def monitorar_botao_passa_principal1(config):
    global botao_passa_pressionado_principal1 
    variaveis_globais.contador_infracoes_principal1
    variaveis_globais.contador_carros_principal1
    variaveis_globais.contador_infracoes_velocidade_principal1
    variaveis_globais.registraVelocidadePrincipal
    global tempo_inicial
    global tempo_final

    while True:
        # Por padrão, o estado do botão é sempre LOW, então 
        # se ele for HIGH, significa que foi ativado
        if botao_principal_1 == GPIO.HIGH:
            tempo_inicial = time.time()
            print(f'Tempo do clique inicial: {tempo_inicial}')
            while botao_principal_1 != GPIO.LOW:
                # Resetamos o valor para realizar novas verificações
                botao_passa_pressionado_principal1 = False
                        
            if botao_principal_1 == GPIO.LOW:                
                # Depois de esperar 300 ms, e o botão voltou para LOW,
                # então podemos concluir que se trata de um botão "passa"
                botao_passa_pressionado_principal1 = True
                # Registra o tempo de desativação
                if tempo_inicial > 0:
                    tempo_final = time.time()
                    print(f'Tempo do clique final: {tempo_final}')
                    # Calcula a velocidade em km/h e imprime
                    velocidade = calcular_velocidade(tempo_inicial, tempo_final)
                    variaveis_globais.registraVelocidadePrincipal.append(velocidade)
                    for val in variaveis_globais.registraVelocidadePrincipal:
                        print(val)
                    print(f'Velocidade do carro: {velocidade}')
                    if velocidade > 80:
                        monitorar_buzzer(config['pinos_gpio']['buzzer']['numero'])
                        variaveis_globais.contador_infracoes_velocidade_principal1 += 1
                        print(f'Infrações de velocidade principal 1: {variaveis_globais.contador_infracoes_velocidade_principal1}\n')
                    variaveis_globais.contador_carros_principal1 += 1

                    print(f'O total de {variaveis_globais.contador_carros_principal1} carros passou na via principal 1\n')
                    print(f"Velocidade do carro na via principal 1: {velocidade} km/h\n")
                    #adiciona o valor da nova velocidade num arrray
                    if variaveis_globais.contador_tempo_cruzamento <= 22:
                        variaveis_globais.contador_infracoes_principal1 += 1
                        print(f'O total de {variaveis_globais.contador_infracoes_principal1} carros ultrapassou o sinal vermelho na via principal 1\n')
                        monitorar_buzzer(config['pinos_gpio']['buzzer']['numero'])
        # Tempo que realiza a verificação
        time.sleep(0.1)

def monitorar_botao_passa_principal2(config):
    global botao_passa_pressionado_principal2 
    variaveis_globais.contador_infracoes_principal2
    variaveis_globais.contador_carros_principal2
    variaveis_globais.contador_infracoes_velocidade_principal2
    variaveis_globais.registraVelocidadePrincipal
    global tempo_inicial
    global tempo_final

    while True:
        # Por padrão, o estado do botão é sempre LOW, então 
        # se ele for HIGH, significa que foi ativado
        if botao_principal_2 == GPIO.HIGH:
            tempo_inicial = time.time()
            print(f'Tempo do clique inicial: {tempo_inicial}')
            while botao_principal_2 != GPIO.LOW:
                # Resetamos o valor para realizar novas verificações
                botao_passa_pressionado_principal2 = False
                        
            if botao_principal_2 == GPIO.LOW:                
                # Depois de esperar 300 ms, e o botão voltou para LOW,
                # então podemos concluir que se trata de um botão "passa"
                botao_passa_pressionado_principal2 = True
                # Registra o tempo de desativação
                if tempo_inicial > 0:
                    tempo_final = time.time()
                    print(f'Tempo do clique final: {tempo_final}')
                    # Calcula a velocidade em km/h e imprime
                    velocidade = calcular_velocidade(tempo_inicial, tempo_final)
                    variaveis_globais.registraVelocidadePrincipal.append(velocidade)
                    for val in variaveis_globais.registraVelocidadePrincipal:
                        print(val)
                    print(f'Velocidade do carro: {velocidade}')
                    if velocidade > 80:
                        monitorar_buzzer(config['pinos_gpio']['buzzer']['numero'])
                        variaveis_globais.contador_infracoes_velocidade_principal2 += 1
                        print(f'Infrações de velocidade principal 2: {variaveis_globais.contador_infracoes_velocidade_principal2}\n')
                    variaveis_globais.contador_carros_principal2 += 1
                    print(f'O total de {variaveis_globais.contador_carros_principal2} carros passou na via principal 2\n')
                    print(f"Velocidade do carro na via principal 2: {velocidade} km/h\n")
                    if variaveis_globais.contador_tempo_cruzamento <= 22:
                        variaveis_globais.contador_infracoes_principal2 += 1
                        print(f'O total de {variaveis_globais.contador_infracoes_principal2} carros ultrapassou o sinal vermelho na via principal 2\n')
                        monitorar_buzzer(config['pinos_gpio']['buzzer']['numero'])
        # Tempo que realiza a verificação
        time.sleep(0.1)


def monitorar_botao_passa_auxiliar1(config):
    global botao_passa_pressionado_auxiliar1 
    variaveis_globais.contador_infracoes_auxiliar1
    variaveis_globais.contador_carros_auxiliar1
    variaveis_globais.contador_infracoes_velocidade_auxiliar1
    variaveis_globais.registraVelocidadeAuxiliar
    global tempo_inicial
    global tempo_final


    while True:
        # Por padrão, o estado do botão é sempre LOW, então 
        # se ele for HIGH, significa que foi ativado
        if botao_auxiliar_1 == GPIO.HIGH:
            tempo_inicial = time.time()
            print(f'Tempo do clique inicial: {tempo_inicial}')
            while botao_auxiliar_1 != GPIO.LOW:
                # Resetamos o valor para realizar novas verificações
                botao_passa_pressionado_auxiliar1 = False
                        
            if botao_auxiliar_1 == GPIO.LOW:                
                # Depois de esperar 300 ms, e o botão voltou para LOW,
                # então podemos concluir que se trata de um botão "passa"
                botao_passa_pressionado_auxiliar1 = True
                # Registra o tempo de desativação
                if tempo_inicial > 0:
                    tempo_final = time.time()
                    print(f'Tempo do clique final: {tempo_final}')
                    # Calcula a velocidade em km/h e imprime
                    velocidade = calcular_velocidade(tempo_inicial, tempo_final)
                    variaveis_globais.registraVelocidadeAuxiliar.append(velocidade)
                    for val in variaveis_globais.registraVelocidadeAuxiliar:
                        print(val)
                    print(f'Velocidade do carro: {velocidade}')
                    if velocidade > 60:
                        monitorar_buzzer(config['pinos_gpio']['buzzer']['numero'])
                        variaveis_globais.contador_infracoes_velocidade_auxiliar1 +=1
                        print(f'Infrações de velocidade auxiliar 1: {variaveis_globais.contador_infracoes_velocidade_auxiliar1}\n')
                    variaveis_globais.contador_carros_auxiliar1 += 1
                    print(f'O total de {variaveis_globais.contador_carros_auxiliar1} carros passou na via auxiliar 1\n')
                    print(f"Velocidade do carro na via auxiliar 1: {velocidade} km/h\n")
                    #adiciona o valor da nova velocidade num arrray
                    if variaveis_globais.contador_tempo_cruzamento <= 22:
                        variaveis_globais.contador_infracoes_auxiliar1 += 1
                        print(f'O total de {variaveis_globais.contador_infracoes_auxiliar1} carros ultrapassou o sinal vermelho na via auxiliar 1\n')
                        monitorar_buzzer(config['pinos_gpio']['buzzer']['numero'])
        # Tempo que realiza a verificação
        time.sleep(0.1)

def monitorar_botao_passa_auxiliar2(config):
    global botao_passa_pressionado_auxiliar2 
    variaveis_globais.contador_infracoes_auxiliar2
    variaveis_globais.contador_carros_auxiliar2
    variaveis_globais.contador_infracoes_velocidade_auxiliar2
    variaveis_globais.registraVelocidadeAuxiliar
    global tempo_inicial
    global tempo_final


    while True:
        # Por padrão, o estado do botão é sempre LOW, então 
        # se ele for HIGH, significa que foi ativado
        if botao_auxiliar_2 == GPIO.HIGH:
            tempo_inicial = time.time()
            print(f'Tempo do clique inicial: {tempo_inicial}')
            while botao_auxiliar_2 != GPIO.LOW:
                # Resetamos o valor para realizar novas verificações
                botao_passa_pressionado_auxiliar2 = False
                        
            if botao_auxiliar_2 == GPIO.LOW:                
                # Depois de esperar 300 ms, e o botão voltou para LOW,
                # então podemos concluir que se trata de um botão "passa"
                botao_passa_pressionado_auxiliar2 = True
                # Registra o tempo de desativação
                if tempo_inicial > 0:
                    tempo_final = time.time()
                    print(f'Tempo do clique final: {tempo_final}')
                    # Calcula a velocidade em km/h e imprime
                    velocidade = calcular_velocidade(tempo_inicial, tempo_final)
                    variaveis_globais.registraVelocidadeAuxiliar.append(velocidade)
                    for val in variaveis_globais.registraVelocidadeAuxiliar:
                        print(val)
                    print(f'Velocidade do carro: {velocidade}')
                    if velocidade > 60:
                        monitorar_buzzer(config['pinos_gpio']['buzzer']['numero'])
                        variaveis_globais.contador_infracoes_velocidade_auxiliar2 += 1
                        print(f'Infrações de velocidade auxiliar 2: {variaveis_globais.contador_infracoes_velocidade_auxiliar2}\n')
                    variaveis_globais.contador_carros_auxiliar2 += 1
                    print(f'O total de {variaveis_globais.contador_carros_auxiliar2} carros passou na via auxiliar 2\n')
                    print(f"Velocidade do carro na via auxiliar 2: {velocidade} km/h\n")
                    #adiciona o valor da nova velocidade num arrray
                    if  variaveis_globais.contador_tempo_cruzamento <= 22:
                        variaveis_globais.contador_infracoes_auxiliar2 += 1
                        print(f'O total de {variaveis_globais.contador_infracoes_auxiliar2} carros ultrapassou o sinal vermelho na via auxiliar 2\n')
                        monitorar_buzzer(config['pinos_gpio']['buzzer']['numero'])
        # Tempo que realiza a verificação
        time.sleep(0.1)

def monitorar_botao_para():
    global botao_para_pressionado
    global botao_para_pressionado_principal
    global tempo_pressionado

    while True:
        if botao_auxiliar_1 == GPIO.HIGH:
            # Botão "para" está pressionado; incrementa o tempo pressionado
            tempo_pressionado += 0.1  # Incrementa em 100ms (tempo de verificação)

            if tempo_pressionado > 0.5:
                # O botão "para" foi mantido pressionado por mais de 300ms
                botao_para_pressionado = True

        elif botao_auxiliar_2 == GPIO.HIGH:
            # Botão "para" está pressionado; incrementa o tempo pressionado
            tempo_pressionado += 0.1  # Incrementa em 100ms (tempo de verificação)

            if tempo_pressionado > 0.5:
                # O botão "para" foi mantido pressionado por mais de 300ms
                botao_para_pressionado = True

        elif botao_principal_1 == GPIO.HIGH:
            # Botão "para" está pressionado; incrementa o tempo pressionado
            tempo_pressionado += 0.1  # Incrementa em 100ms (tempo de verificação)

            if tempo_pressionado > 0.5:
                # O botão "para" foi mantido pressionado por mais de 300ms
                botao_para_pressionado_principal = True

        elif botao_principal_2 == GPIO.HIGH:
            # Botão "para" está pressionado; incrementa o tempo pressionado
            tempo_pressionado += 0.1  # Incrementa em 100ms (tempo de verificação)

            if tempo_pressionado > 0.5:
                # O botão "para" foi mantido pressionado por mais de 300ms
                botao_para_pressionado_principal = True

        else:
            # Botão "para" foi solto; resetar o tempo pressionado
            tempo_pressionado = 0
            if botao_para_pressionado:
                botao_para_pressionado = False
            elif botao_para_pressionado_principal:
                botao_para_pressionado_principal = False
           

        # Tempo que realiza a verificação
        time.sleep(0.1)

def monitorar_buzzer(buzzer):
    GPIO.output(buzzer, GPIO.LOW)
    GPIO.output(buzzer, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(buzzer, GPIO.LOW)


def trata_eventos():
    variaveis_globais.contador_tempo_cruzamento
    is_botao_pedestre_1_antes_10_seg = False
    is_botao_pedestre_2_antes_10_seg = False

    while True:
        # Verifica se o botão de pedestre 1 foi acionado ou se o botão passa está acionado
        if botao_pedestre_1 | botao_para_pressionado:
            if variaveis_globais.contador_tempo_cruzamento >= 10 and variaveis_globais.contador_tempo_cruzamento < 21:
                print(f'[c1]: Botão 1 pressionado aos: {variaveis_globais.contador_tempo_cruzamento}')
                variaveis_globais.contador_tempo_cruzamento = 21
                
            elif variaveis_globais.contador_tempo_cruzamento < 10:
                is_botao_pedestre_1_antes_10_seg = True

        # Verifica se o botão de pedestre 2 foi acionado
        if botao_pedestre_2 | botao_para_pressionado_principal:
            if variaveis_globais.contador_tempo_cruzamento >= 27 and variaveis_globais.contador_tempo_cruzamento < 32:
                print(f'[c1]: Botão 2 pressionado aos: {variaveis_globais.contador_tempo_cruzamento}\n')
                variaveis_globais.contador_tempo_cruzamento = 32

            elif variaveis_globais.contador_tempo_cruzamento >= 22 and variaveis_globais.contador_tempo_cruzamento < 27:
                is_botao_pedestre_2_antes_10_seg = True

        # Se o botão de pedestre foi clicado antes de 10s e o contador agora eh maior ou igual ao tempo minimo
        if is_botao_pedestre_1_antes_10_seg and variaveis_globais.contador_tempo_cruzamento >= 10:
            print(f'[c1]: Botão 1 pressionado aos: {variaveis_globais.contador_tempo_cruzamento}\n')
            variaveis_globais.contador_tempo_cruzamento = 21
            is_botao_pedestre_1_antes_10_seg = False

        if is_botao_pedestre_2_antes_10_seg and variaveis_globais.contador_tempo_cruzamento >= 27:
            variaveis_globais.contador_tempo_cruzamento = 32
            is_botao_pedestre_2_antes_10_seg = False

        if is_botao_pedestre_1_antes_10_seg and (variaveis_globais.contador_tempo_cruzamento > 20):
            is_botao_pedestre_1_antes_10_seg = False
        
        if is_botao_pedestre_2_antes_10_seg and (variaveis_globais.contador_tempo_cruzamento < 22 | variaveis_globais.contador_tempo_cruzamento > 32):
            is_botao_pedestre_2_antes_10_seg = False


        time.sleep(0.160)
