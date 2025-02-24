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

import os
import sys
import time
import logging
import boto3
from src.ConnectDB import ConnectDB
from src.RequestAPI import ApiJogosConnect
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from datetime import datetime
from src.Logger import Logger
from src.ConnectS3 import ConnectS3


# Configurar loggers específicos


# Constantes
SLEEP_TIME = 864  # 100 execuções em 1 dia
DB_NAME = 'futebol.db'
BUCKET_NAME = 'seu-bucket-name'
S3_FOLDER = 'database-backups'

if __name__ == '__main__':
    # Carrega variáveis de ambiente
    load_dotenv()
    API_KEY = os.getenv('API_KEY')

    try:
        logger = Logger('app_logger').get_logger()
        db_logger = Logger('db_logger').get_logger()
        api_logger = Logger('api_logger').get_logger()
        s3_logger = Logger('s3_logger').get_logger()
        connectiondb = ConnectDB(db_name=DB_NAME)
        connects3 = ConnectS3()  # Instanciar a classe ConnectS3
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
                retorno_api = connection_api.retorna_response_api_jogos()
                if retorno_api:
                    api_logger.info(f"API retornou {retorno_api['results']} jogos ao vivo")
                    connectiondb.coletar_jogos_ao_vivo(retorno_api)
                    db_logger.info(f"Dados gravados no banco de dados, tamanho atual: {connectiondb.retorna_tamanho_do_banco()}")
                    
                    # if contador % 10 == 0:
                    #     if connects3.upload_to_s3(DB_NAME, BUCKET_NAME, S3_FOLDER):
                    #         logger.info("Backup para S3 realizado com sucesso")
                    #     else:
                    #         logger.warning("Falha ao realizar backup para S3")
                else:
                    api_logger.warning("API não retornou dados de jogos ao vivo")
                
                time.sleep(SLEEP_TIME)
                contador += 1
                
            except Exception as e:
                api_logger.error(f"Erro ao processar dados da API: {str(e)}", exc_info=True)
                time.sleep(SLEEP_TIME)
                
    except KeyboardInterrupt:
        logger.info("Aplicação encerrada pelo usuário")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Erro crítico na aplicação: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        connectiondb.fechar_conexao()
        db_logger.info("Conexão com banco de dados fechada")
