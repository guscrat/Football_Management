from src.ConnectDB import ConnectDB
from src.RequestAPI import ApiJogosConnect
import time

if __name__ == '__main__':
    connectiondb = ConnectDB(db_name='futebol.db')
    connectiondb.criar_tabela_com_campos()

    connection_api = ApiJogosConnect(
        api_key="8da1666cfc9124e7141f45725e946b7c",
        base_url="https://v3.football.api-sports.io/",
        headers="x-apisports-key"
    )

    contador = 0
    while True:
        contador += 1
        retorno_api: dict = connection_api.retorna_response_api_jogos()
        print(f"Response number {contador}, return {retorno_api['results']} results ")
        
        connectiondb.coletar_jogos_ao_vivo(retorno_api)
        print(f"Dados gravados no banco de dados, tamanho atual: {connectiondb.retorna_tamanho_do_banco()}")
        time.sleep(864)  # 864 sao 100 execucoes em 1 dia
        
        # connectiondb.fechar_conexao()
