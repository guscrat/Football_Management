import sqlite3
import json

# Carregar os dados do callback da API
with open('callbackapi.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Conectar ao banco SQLite
conn = sqlite3.connect('futebol.db')
c = conn.cursor()

# Criar tabelas
c.execute('''
CREATE TABLE IF NOT EXISTS leagues (
    id INTEGER PRIMARY KEY,
    name TEXT,
    country TEXT,
    season INTEGER
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY,
    name TEXT,
    logo TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS fixtures (
    id INTEGER PRIMARY KEY,
    league_id INTEGER,
    home_team_id INTEGER,
    away_team_id INTEGER,
    venue TEXT,
    status TEXT,
    elapsed INTEGER,
    FOREIGN KEY (league_id) REFERENCES leagues(id),
    FOREIGN KEY (home_team_id) REFERENCES teams(id),
    FOREIGN KEY (away_team_id) REFERENCES teams(id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS goals (
    fixture_id INTEGER,
    home INTEGER,
    away INTEGER,
    PRIMARY KEY (fixture_id),
    FOREIGN KEY (fixture_id) REFERENCES fixtures(id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS events (
    fixture_id INTEGER,
    time INTEGER,
    team_id INTEGER,
    player TEXT,
    type TEXT,
    detail TEXT,
    FOREIGN KEY (fixture_id) REFERENCES fixtures(id),
    FOREIGN KEY (team_id) REFERENCES teams(id)
)
''')

# Inserir dados
for match in data['response']:
    league = match['league']
    fixture = match['fixture']
    teams = match['teams']
    goals = match['goals']
    events = match.get('events', [])
    
    # Inserir liga
    c.execute('INSERT OR IGNORE INTO leagues VALUES (?, ?, ?, ?)',
              (league['id'], league['name'], league['country'], league['season']))
    
    # Inserir times
    for team_key in ['home', 'away']:
        team = teams[team_key]
        c.execute('INSERT OR IGNORE INTO teams VALUES (?, ?, ?)',
                  (team['id'], team['name'], team['logo']))
    
    # Inserir partida
    c.execute('INSERT OR IGNORE INTO fixtures VALUES (?, ?, ?, ?, ?, ?, ?)',
              (fixture['id'], league['id'], teams['home']['id'], teams['away']['id'],
               fixture['venue']['name'], fixture['status']['long'], fixture['status']['elapsed']))
    
    # Inserir gols
    c.execute('INSERT OR IGNORE INTO goals VALUES (?, ?, ?)',
              (fixture['id'], goals['home'], goals['away']))
    
    # Inserir eventos
    for event in events:
        c.execute('INSERT INTO events VALUES (?, ?, ?, ?, ?, ?)',
                  (fixture['id'], event['time']['elapsed'], event['team']['id'],
                   event['player']['name'] if event['player'] else None,
                   event['type'], event['detail']))

# Salvar alterações e fechar conexão
conn.commit()
conn.close()

print("Dados inseridos com sucesso!")
nl-=
