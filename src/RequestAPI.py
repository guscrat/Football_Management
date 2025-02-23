"""
Módulo para gerenciamento de conexões com a API de futebol.
Fornece funcionalidades para realizar requisições HTTP e processar respostas da API.
"""

import requests


class ApiJogosConnect:
    """
    Classe para gerenciar conexões e requisições à API de futebol.
    """

    def __init__(self, api_key: str, base_url: str, headers: str):
        """
        Inicializa uma nova instância do conector da API.

        Args:
            api_key (str): Chave de autenticação para a API
            base_url (str): URL base para as requisições
            headers (str): Nome do cabeçalho para a chave de API

        Raises:
            ValueError: Se algum dos parâmetros estiver vazio
        """
        if not all([api_key, base_url, headers]):
            raise ValueError("Todos os parâmetros são obrigatórios")

        self.api_key = api_key
        self.base_url = base_url
        self.headers = {headers: api_key}

    def retorna_response_api_jogos(self) -> dict:
        """
        Realiza uma requisição para obter dados de jogos ao vivo.

        Returns:
            dict: Dados dos jogos em formato JSON

        Raises:
            requests.exceptions.RequestException: Se houver erro na requisição
        """
        try:
            url = f"{self.base_url}fixtures?live=all"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise
