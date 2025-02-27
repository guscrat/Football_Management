import logging
import os
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self, logger_name: str):
        # Definir o diretório de logs como constante da classe
        self.LOG_DIR = 'logs'
        
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
        
        # Criar diretório e configurar arquivo de log
        self.cria_diretorio_logs()
        log_file = os.path.join(self.LOG_DIR, 'futebol_api.log')
        
        self.handler = RotatingFileHandler(
            log_file,
            maxBytes=1024*1024,
            backupCount=5,
        )
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def cria_diretorio_logs(self):
        """
        Cria o diretório de logs se não existir
        """
        if not os.path.exists(self.LOG_DIR):
            os.makedirs(self.LOG_DIR)
