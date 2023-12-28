import time
import RPi.GPIO as GPIO

import sys

sys.path.append('..')

import variaveis_globais


# Função para acender a luz verde
def acender_luz_verde(semaforo1_pino1, semaforo1_pino2):
    GPIO.output(semaforo1_pino1, GPIO.LOW)
    GPIO.output(semaforo1_pino2, GPIO.HIGH)

def acender_luz_verde_via_auxiliar(semaforo2_pino1, semaforo2_pino2):
    GPIO.output(semaforo2_pino1, GPIO.LOW)
    GPIO.output(semaforo2_pino2, GPIO.HIGH)

# Função para acender a luz amarela
def acender_luz_amarela(semaforo1_pino1, semaforo1_pino2):
    GPIO.output(semaforo1_pino1, GPIO.HIGH)
    GPIO.output(semaforo1_pino2, GPIO.LOW)

def acender_luz_amarela_via_auxiliar(semaforo2_pino1, semaforo2_pino2):
    GPIO.output(semaforo2_pino1, GPIO.HIGH)
    GPIO.output(semaforo2_pino2, GPIO.LOW)

# Função para acender a luz vermelha
def acender_luz_vermelha(semaforo1_pino1, semaforo1_pino2):
    GPIO.output(semaforo1_pino1, GPIO.HIGH)
    GPIO.output(semaforo1_pino2, GPIO.HIGH)

# Função para acender a luz vermelha
def acender_luz_vermelha_via_auxiliar(semaforo2_pino1, semaforo2_pino2):
    GPIO.output(semaforo2_pino1, GPIO.HIGH)
    GPIO.output(semaforo2_pino2, GPIO.HIGH)

def apaga_luzes(semaforo1_pino1, semaforo1_pino2):
    GPIO.output(semaforo1_pino1, GPIO.LOW)
    GPIO.output(semaforo1_pino2, GPIO.LOW)

def apaga_luzes_via_auxiliar(semaforo2_pino1, semaforo2_pino2):
    GPIO.output(semaforo2_pino1, GPIO.LOW)
    GPIO.output(semaforo2_pino2, GPIO.LOW)
    
# modo emergencia
def modoEmergencia(config):
    semaforo1_pino1 = config['pinos_gpio']['semaforo1_pino1']['numero']
    semaforo1_pino2 = config['pinos_gpio']['semaforo1_pino2']['numero']
    semaforo2_pino1 = config['pinos_gpio']['semaforo2_pino1']['numero']
    semaforo2_pino2 = config['pinos_gpio']['semaforo2_pino2']['numero']
    try:
        while True:
            #Acende a luz da Via Principal
            acender_luz_verde(semaforo1_pino1, semaforo1_pino2)
            acender_luz_vermelha_via_auxiliar(semaforo2_pino1, semaforo2_pino2)

            time.sleep(1)  # Mantém o pino aceso por 1 segundo
    except KeyboardInterrupt:
        GPIO.cleanup()

# modo noturno
def modoNoturno(config):
    semaforo1_pino1 = config['pinos_gpio']['semaforo1_pino1']['numero']
    semaforo1_pino2 = config['pinos_gpio']['semaforo1_pino2']['numero']
    semaforo2_pino1 = config['pinos_gpio']['semaforo2_pino1']['numero']
    semaforo2_pino2 = config['pinos_gpio']['semaforo2_pino2']['numero']

    try:
        while True:
            # Acende o pino amarelo
            acender_luz_amarela(semaforo1_pino1, semaforo1_pino2)
            acender_luz_amarela_via_auxiliar(semaforo2_pino1, semaforo2_pino2)
            time.sleep(1)
            apaga_luzes(semaforo1_pino1, semaforo1_pino2)
            apaga_luzes_via_auxiliar(semaforo2_pino1, semaforo2_pino2)
            time.sleep(1)
        
    except KeyboardInterrupt: #Pega a interrupção do teclado
        GPIO.cleanup()

# Função para controlar os semáforos da via principal com base nas informações do JSON
def controlar_semaforos_principal(config):
    variaveis_globais.contador_tempo_cruzamento
    semaforo1_pino1 = config['pinos_gpio']['semaforo1_pino1']['numero']
    semaforo1_pino2 = config['pinos_gpio']['semaforo1_pino2']['numero']
    semaforo2_pino1 = config['pinos_gpio']['semaforo2_pino1']['numero']
    semaforo2_pino2 = config['pinos_gpio']['semaforo2_pino2']['numero']


    while True:
        print(f'Tempo: {variaveis_globais.contador_tempo_cruzamento}')
        if variaveis_globais.contador_tempo_cruzamento <= 20:
            acender_luz_verde(semaforo1_pino1, semaforo1_pino2)
            acender_luz_vermelha_via_auxiliar(semaforo2_pino1, semaforo2_pino2)
        elif variaveis_globais.contador_tempo_cruzamento > 20 and variaveis_globais.contador_tempo_cruzamento <= 22:
            acender_luz_amarela(semaforo1_pino1, semaforo1_pino2)
            acender_luz_vermelha_via_auxiliar(semaforo2_pino1, semaforo2_pino2)
        elif variaveis_globais.contador_tempo_cruzamento > 22 and variaveis_globais.contador_tempo_cruzamento <= 32:
            acender_luz_vermelha(semaforo1_pino1, semaforo1_pino2)
            acender_luz_verde_via_auxiliar(semaforo2_pino1, semaforo2_pino2)
        elif variaveis_globais.contador_tempo_cruzamento > 32 and variaveis_globais.contador_tempo_cruzamento <= 34:
            acender_luz_vermelha(semaforo1_pino1, semaforo1_pino2)
            acender_luz_amarela_via_auxiliar(semaforo2_pino1, semaforo2_pino2)
        else: 
            variaveis_globais.contador_tempo_cruzamento = 1  # Reinicia o contador
            
        time.sleep(1)
        variaveis_globais.contador_tempo_cruzamento += 1
