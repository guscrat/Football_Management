import sqlite3
import os

"""
Módulo para gerenciamento de conexões com banco de dados SQLite3.
Responsável por criar e gerenciar tabelas de jogos de futebol, incluindo ligas,
times, partidas, gols e eventos.
"""

class ConnectDB:
    """
    Classe para gerenciar conexões e operações com banco de dados SQLite3.
    
    Attributes:
        conn (sqlite3.Connection): Conexão com o banco de dados
        cursor (sqlite3.Cursor): Cursor para executar operações no banco
        name (str): Nome do arquivo do banco de dados
        tamanho (int): Tamanho do arquivo do banco de dados em bytes
    """

    def __init__(self, db_name):
        """
        Inicializa uma nova conexão com o banco de dados.

        Args:
            db_name (str): Nome do arquivo do banco de dados SQLite
        """
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.name = db_name
        self.tamanho: int = os.path.getsize(self.name)

    def retorna_tamanho_do_banco(self):
        """
        Calcula e retorna o tamanho atual do banco de dados em KB.

        Returns:
            str: Tamanho do banco formatado em KB com 2 casas decimais
        """
        self.tamanho = os.path.getsize(self.name)
        return f"{self.tamanho / 1024:.2f} KB"

    def criar_tabela_com_campos(self):
        """
        Cria as tabelas necessárias no banco de dados se não existirem.
        
        Tabelas criadas:
            - leagues: Informações sobre ligas de futebol
            - teams: Dados dos times
            - fixtures: Informações sobre partidas
            - goals: Registro de gols das partidas
            - events: Eventos ocorridos durante as partidas
        
        Returns:
            None
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS leagues (
                id INTEGER PRIMARY KEY,
                name TEXT,
                country TEXT,
                season INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY,
                name TEXT,
                logo TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS fixtures (
                id INTEGER,
                league_id INTEGER,
                home_team_id INTEGER,
                away_team_id INTEGER,
                venue TEXT,
                status TEXT,
                elapsed INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id, timestamp),
                FOREIGN KEY (league_id) REFERENCES leagues(id),
                FOREIGN KEY (home_team_id) REFERENCES teams(id),
                FOREIGN KEY (away_team_id) REFERENCES teams(id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                fixture_id INTEGER,
                home INTEGER,
                away INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (fixture_id, timestamp),
                FOREIGN KEY (fixture_id) REFERENCES fixtures(id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                fixture_id INTEGER,
                time INTEGER,
                team_id INTEGER,
                player TEXT,
                type TEXT,
                detail TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (fixture_id) REFERENCES fixtures(id),
                FOREIGN KEY (team_id) REFERENCES teams(id)
            )
        ''')
        self.conn.commit()

    def coletar_jogos_ao_vivo(self, json_jogos):
        """
        Insere ou atualiza dados de jogos ao vivo no banco de dados.

        Args:
            json_jogos (dict): Dicionário contendo dados dos jogos no formato JSON
                             com informações de liga, times, partida, gols e eventos

        Raises:
            sqlite3.Error: Em caso de erro na operação com o banco de dados
        
        Note:
            O método realiza rollback automático em caso de erro durante as inserções
        """
        try:
            if "response" in json_jogos and isinstance(json_jogos["response"], list):
                for match in json_jogos['response']:
                    
                    league = match['league']
                    teams = match['teams']
                    fixture = match['fixture']
                    goals = match['goals']
                    events = match.get('events', [])

                    #  Leagues
                    self.cursor.execute("""
                        INSERT OR IGNORE INTO leagues VALUES (?, ?, ?, ?)""",
                        (
                            league['id'],
                            league['name'],
                            league['country'],
                            league['season']
                        )
                    )

                    #  Teams
                    for team_key in ('home', 'away'):
                        team = teams[team_key]
                        self.cursor.execute("""
                            INSERT OR IGNORE INTO teams VALUES (?, ?, ?)""",
                            (
                                team['id'],
                                team['name'],
                                team['logo']
                            )
                        )

                    #  Fixture
                    self.cursor.execute("""
                        INSERT INTO fixtures (
                                        id,
                                        league_id,
                                        home_team_id,
                                        away_team_id,
                                        venue,
                                        status,
                                        elapsed
                                        ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (
                            fixture['id'],
                            league['id'],
                            teams['home']['id'],
                            teams['away']['id'],
                            fixture['venue']['name'],
                            fixture['status']['long'],
                            fixture['status']['elapsed']
                        )
                    )

                    #  Goals
                    self.cursor.execute("""
                        INSERT INTO goals (fixture_id, home, away) VALUES (?, ?, ?)
                    """,
                        (
                            fixture['id'],
                            goals['home'],
                            goals['away']
                        )
                    )

                    #  Events
                    for event in events:
                        self.cursor.execute("""
                            INSERT INTO events (
                                            fixture_id,
                                            time,
                                            team_id,
                                            player,
                                            type,
                                            detail) VALUES (?, ?, ?, ?, ?, ?)""",
                            (
                                fixture['id'],
                                event['time']['elapsed'],
                                event['team']['id'] if event['team'] else None,
                                event['player']['name'] if event['player'] else None,
                                event['type'],
                                event['detail']
                            )
                        )

            self.conn.commit()

        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Erro ao salvar no banco de dados: {e}")

    def fechar_conexao(self):
        """
        Fecha a conexão atual com o banco de dados.
        Deve ser chamado ao finalizar as operações com o banco.
        """
        self.conn.close()
