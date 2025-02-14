import sqlite3

class ConnectDB:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def cria_tabela_com_campos(self):
        '''
        Cria uma tabela com os campos pre-definidos,
        se não houver uma tabela com esse nome.
        Return:
            arquivo.db
        '''
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS jogos(
            id INTEGER PRIMARY KEY,
            liga TEXT,
            time_casa TEXT,
            time_fora TEXT,
            placar TEXT,
            status TEXT,
            ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
