import json

# Função para carregar configurações do arquivo JSON
def carregar_configuracoes(nomeArquivo):
    with open(nomeArquivo, 'r') as arquivo_config:
        config = json.load(arquivo_config)
    return config
