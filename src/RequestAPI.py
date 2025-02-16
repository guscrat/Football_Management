import requests


class ApiJogosConnect:

    def __init__(self, api_key, base_url, headers):
        self.api_key = api_key  # Chave da API
        self.base_url = base_url  # URL base da API
        self.headers = {headers: api_key}  # Cabecalhos HTTP

    def retorna_response_api_jogos(self):
        try:
            url = f"{self.base_url}fixtures?live=all"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            dados = response.json()

        except requests.exceptions.RequestException as e:
            print(f"Erro ao coletar dados da API: {e}")

        return dados
