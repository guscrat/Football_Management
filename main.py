from src.create_connect_db import ConnectDB
from src.request_api import ApiJogosConnect

class Main:
    if __name__ == '__main__':
        connectiondb = ConnectDB(db_name='futebol.db')
        connectiondb.cria_tabela_com_campos()

        jogos_api = ApiJogosConnect(
            api_key="8da1666cfc9124e7141f45725e946b7c",
            base_url="https://v3.football.api-sports.io/",
            headers="x-apisports-key"
        )
