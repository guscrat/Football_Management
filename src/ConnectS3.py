import boto3
import os
from datetime import datetime
from src.Logger import Logger


class ConnectS3:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.s3_key = 'database-backups'
        self.logger = Logger('s3_logger').get_logger()

    def upload_to_s3(self, file_path: str, bucket: str, s3_folder: str) -> bool:
        """
        Faz upload do arquivo SQLite para o S3
        
        Args:
            file_path (str): Caminho do arquivo a ser enviado
            bucket (str): Nome do bucket S3
            s3_folder (str): Pasta de destino no S3
            
        Returns:
            bool: True se o upload foi bem sucedido, False caso contrário
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_name = os.path.basename(file_path)
            s3_key = f"{s3_folder}/{timestamp}_{file_name}"
            
            self.s3_client.upload_file(file_path, bucket, s3_key)
            self.logger.info(f"Arquivo {file_name} enviado com sucesso para S3://{bucket}/{s3_key}")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao fazer upload para S3: {str(e)}", exc_info=True)
            return False