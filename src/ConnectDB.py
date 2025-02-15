import sqlite3


class ConnectDB:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def criar_tabela_com_campos(self):
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

    def coletar_jogos_ao_vivo(self, json_jogos):
        if "response" in json_jogos and isinstance(json_jogos["response"], list):
            for jogo in json_jogos["response"]:
                liga = (
                    jogo.get("league", {}).get("name", "Desconhecido")
                    )
                time_casa = (
                    jogo.get("teams", {}).get("home", {}).get("name", "Desconhecido")
                )
                time_fora = (
                    jogo.get("teams", {}).get("away", {}).get("name", "Desconhecido")
                    )
                placar = (
                    f"{jogo.get('goals', {}).get('home', 0)} - {jogo.get('goals', {}).get('away', 0)}"
                    )
                status = (
                    jogo.get("fixture", {}).get("status", {}).get("long", "Desconhecido")
                    )

                self.insere_dados_coletados_no_bd(
                    liga, time_casa, time_fora, placar, status
                    )

    def insere_dados_coletados_no_bd(
            self, liga, time_casa, time_fora, placar, status
            ):
        try:
            self.cursor.execute("""
                INSERT INTO jogos (liga, time_casa, time_fora, placar, status)
                VALUES (?, ?, ?, ?, ?)
            """, (liga, time_casa, time_fora, placar, status))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao salvar no banco de dados: {e}")
