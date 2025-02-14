import requests

# Configuracao da API
API_KEY = "8da1666cfc9124e7141f45725e946b7c"  # Chave da API
BASE_URL = "https://v3.football.api-sports.io/"  # URL base da API
HEADERS = {"x-apisports-key": API_KEY}  # Cabecalhos HTTP para autenticacao na API

def coletar_jogos():
    url = f"{BASE_URL}fixtures?live=all"  # Endpoint da API para jogos ao vivo
    response = requests.get(url, headers=HEADERS)  # Requisicao para AP
    response.raise_for_status()  # Lanca um erro se a resposta tiver um HTTP ruim
    dados = response.json()  # Resposta para JSON

    print("->> ", dados)

    # Verifica se os dados contem a chave 'response' e se eh uma lista
    # if "response" in dados and isinstance(dados["response"], list):
    #     for jogo in dados["response"]:
    #         liga = jogo.get("league", {}).get("home", {}).get("name", "Desconhecido")
    #         time_casa = jogo.get("teams", {}).get("home", {}).get("name", "Desconhecido")
    #         time_fora = jogo.get("teams", {}).get("away", {}).get("name", "Desconhecido")
    #         placar = f"{jogo.get("goals", {}).get("home", 0)} - {jogo.get("goals", {}).get("away", 0)}"
    #         status = jogo.get("league", {}).get("home", {}).get("name", "Desconhecido")

    # Insere os dados coletados no banco de dados
    # cursor.execute('''
        
    # ''')
coletar_jogos()