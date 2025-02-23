"""
Script principal para coleta de dados de jogos de futebol em tempo real.
Este módulo gerencia a conexão com a API de futebol e o banco de dados SQLite,
realizando coletas periódicas de informações sobre partidas ao vivo.

Características principais:
- Logging rotativo com backup
- Conexão com API de futebol
- Armazenamento em SQLite
- Execução contínua com tratamento de erros
"""

from src.ConnectDB import ConnectDB
from src.RequestAPI import ApiJogosConnect
import time
import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

# Configuração dos logs
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_file = os.path.join(LOG_DIR, 'futebol_api.log')
handler = RotatingFileHandler(
    log_file,
    maxBytes=1024*1024,
    backupCount=5,
    encoding='utf-8'
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
handler.setFormatter(formatter)

# Configurar o logger root
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(handler)

# Modificar o StreamHandler para incluir data e hora
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)  # Usar o mesmo formatter do arquivo
root_logger.addHandler(console_handler)

# Configurar loggers específicos
logger = logging.getLogger(__name__)
db_logger = logging.getLogger('database')
api_logger = logging.getLogger('api')

# Constantes
SLEEP_TIME = 864  # 100 execuções em 1 dia
DB_NAME = 'futebol.db'

if __name__ == '__main__':
    # Carrega variáveis de ambiente
    load_dotenv()
    API_KEY = os.getenv('API_KEY')

    try:
        connectiondb = ConnectDB(db_name=DB_NAME)
        connectiondb.criar_tabela_com_campos()
        db_logger.info("Conexão com banco de dados estabelecida com sucesso")

        connection_api = ApiJogosConnect(
            api_key=API_KEY,
            base_url="https://v3.football.api-sports.io/",
            headers="x-apisports-key"
        )
        api_logger.info("Conexão com API configurada com sucesso")

        contador = 0
        while True:
            try:
                contador += 1
                retorno_api: dict = connection_api.retorna_response_api_jogos()
                api_logger.info(f"Response number {contador}, return {retorno_api['results']} results")
                
                connectiondb.coletar_jogos_ao_vivo(retorno_api)
                db_logger.info(f"Dados gravados no banco de dados, tamanho atual: {connectiondb.retorna_tamanho_do_banco()}")
                time.sleep(SLEEP_TIME)
                
            except Exception as e:
                api_logger.error(f"Erro durante a execução: {str(e)}", exc_info=True)
                time.sleep(60)  # Espera 1 minuto antes de tentar novamente
                
    except Exception as e:
        api_logger.critical(f"Erro fatal: {str(e)}", exc_info=True)
    finally:
        connectiondb.fechar_conexao()
        db_logger.info("Conexão com banco de dados fechada")
