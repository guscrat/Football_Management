from src.ConnectDB import ConnectDB
from src.request_api import ApiJogosConnect

if __name__ == '__main__':
    connectiondb = ConnectDB(db_name='futebol.db')
    connectiondb.criar_tabela_com_campos()

    connection_api = ApiJogosConnect(
        api_key="8da1666cfc9124e7141f45725e946b7c",
        base_url="https://v3.football.api-sports.io/",
        headers="x-apisports-key"
    )

    retorno_api: dict = connection_api.retorna_response_api_jogos()

    connectiondb.coletar_jogos_ao_vivo(retorno_api)
