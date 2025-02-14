import requests

class ApiJogosConnect:

    def __init__(self, api_key, base_url, headers):
        self.api_key = api_key  # Chave da API
        self.base_url = base_url  # URL base da API
        self.headers = {headers: api_key}  # Cabecalhos HTTP para autenticacao na API

    def retorna_response_api_jogos(self):
        url = f"{self.BASE_URL}fixtures?live=all"  # Endpoint da API para jogos ao vivo
        response = requests.get(url, headers=self.HEADERS)  # Requisicao para AP
        response.raise_for_status()  # Lanca um erro se a resposta tiver um HTTP ruim
        dados = response.json()  # Resposta para JSON
        
        return dados
