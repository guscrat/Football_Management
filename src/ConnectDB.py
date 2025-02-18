import sqlite3
import os

class ConnectDB:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.name = db_name
        self.tamanho: int = os.path.getsize(self.name)

    def retorna_tamanho_do_banco(self):
        self.tamanho = os.path.getsize(self.name)
        print(f"Atual tamanho do banco de dados: {self.tamanho / 1024:.2f} KB")

    def criar_tabela_com_campos(self):
        '''
        Cria uma tabela com os campos pre-definidos,
        se não houver uma tabela com esse nome.
        Return:
            arquivo.db
        '''

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
        """Fecha a conexão com o banco de dados."""
        self.conn.close()
