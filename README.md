# Trabalho 1 (2023-2)
Trabalho 1 da disciplina de Fundamentos de Sistemas Embarcados - Controle de Semáforos

## Visão Geral
Este trabalho tem por objetivo a criação de um sistema distribuído para o controle e monitoramento de um grupo de cruzamentos de sinais de trânsito. O sistema deve ser desenvolvido para funcionar em um conjunto de placas Raspberry Pi com um ***servidor central*** responsável pelo controle e interface com o usuário controlador e ***servidores distribuídos*** para o controle local e monitoramento dos sinais do cruzamento junto aos respectivos sensores que monitoram as vias. Dentre os dispositivos envolvidos estão: o controle de temporizaçãio e acionamento dos sinais de trânsito, o acionmento de botões de passagens de pedestres, o monitoramento de sensores de passagem de carros bem como a velocidade da via e o avanço de sinal vermelho.

![image](https://github.com/FSE-2023-2/trabalho-1-2023-2-alcantaragiubs/assets/54143767/be86581b-94e0-4ff2-9e23-de2237b7b2c3)

![image](https://github.com/FSE-2023-2/trabalho-1-2023-2-alcantaragiubs/assets/54143767/ad8c657b-c64c-4c9f-8ac8-5cb5e9b38ac3)

## Apresentação

  | Conteúdo | Vídeo                                                                                         |
  | -------- | --------------------------------------------------------------------------------------------- |
  | Trabalho 1 | [URL do Vídeo](https://youtu.be/nQP-k-ZkFms)  

## Execução do Projeto

### Pré-Requisitos

- SSH
- Estar num terminal linux (ou WSL dele para Windows)

### Execução do Projeto

#### Clone o repositório

```bash 
$ git clone https://github.com/alcantaragiubs/Trabalho-1-FSE.git
```

#### Abra um terminal e entre no ssh da placa do servidor distribuído do cruzamento 1

```bash 
$ ssh seu-usuario@164.41.98.24 -p 13508
```

#### Abra um terminal e entre no ssh da placa do servidor distribuído do cruzamento 2

```bash 
$ ssh seu-usuario@164.41.98.24 -p 13508
```
- obs: como na configuração dos arquivos json, o host do cruzamento 1 e do cruzamento 2 está configurado para a placa rasp42, é indicado utiliza-la para rodar o projeto, caso se deseje acessar outra placa, mudar a configuração dos arquivos json.

#### Abra um terminal e entre no ssh da placa do servidor central

```bash 
$ ssh seu-usuario@164.41.98.19 -p 3000
```

#### Entre no caminho da pasta para enviar os servidores distribuídos dos cruzamentos 1 e 2

```bash
$ cd .\Trabalho-1-FSE
```

#### Entre no caminho da pasta para enviar o servidor central

```bash
$ cd .\Trabalho-1-FSE\servidor-central
```

#### Envie a pasta de servidor 

```bash 
$ scp -P 13508 -r ./controle-cruzamento seu-usuario@164.41.98.24:~/
```

#### Envie a pasta de servidor-central

```bash 
$ scp -P 3000 -r ./servidor-central seu-usuario@164.41.98.19:~/
```

- obs: caso seja desejado, pode-se enviar os 3 servidores para a mesma placa (não recomendado), então o passo acima seria ignorado

#### Entre nos terminais de cada placa (rasp42 do distribuído 1, rasp42 do distribuído 2, rasp49 do central) e entre na pasta onde está o arquivo de cada servidor

```bash 
$ cd ./controle-cruzamento/servidor-distribuido1
```

```bash
$ cd ./controle-cruzamento/servidor-distribuido2
```

```bash
$ cd ./servidor-central
```

#### Execute os arquivos de cada cruzamento e do servidor central em suas referentes placas

```bash 
$ python cruzamento1.py
```

```bash 
$ python cruzamento2.py
```

```bash
$ python central.py
```
## Utilização do projeto

Para utilização do projeo acesse o [dashboard](http://thingsboard.lappis.rocks:443/dashboard/2997e8d0-6922-11ee-9564-198e90f74020?publicId=ba042a80-0322-11ed-9f25-414fbaf2b065) da placa referida (obs: caso mude a placa da configuração padrão, acesse o dashboard referente a ela)