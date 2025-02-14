import requests  # Biblioteca para fazer requisições HTTP
import sqlite3  # Biblioteca para interagir com um banco de dados SQLite
import time  # Biblioteca para lidar com tempo e atrasos na execução

# Configuração da API
API_KEY = "SUA_CHAVE_DA_API"  # Chave da API para autenticação
BASE_URL = "https://v3.football.api-sports.io/"  # URL base da API
HEADERS = {"x-apisports-key": API_KEY}  # Cabeçalhos HTTP para autenticação na API

# Conectar ao banco de dados SQLite
conn = sqlite3.connect("futebol.db", check_same_thread=False)  # Abre conexão com o banco
cursor = conn.cursor()  # Cria um cursor para executar comandos SQL

# Criar tabela para armazenar informações sobre jogos ao vivo
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jogos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  # Chave primária autoincrementada
        liga TEXT,  # Nome da liga
        time_casa TEXT,  # Nome do time da casa
        time_fora TEXT,  # Nome do time visitante
        placar TEXT,  # Placar do jogo
        status TEXT,  # Status da partida (ex: Em andamento, Finalizado)
        ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP  # Data e hora da última atualização
    )
''')
conn.commit()  # Confirma a criação da tabela no banco de dados

def coletar_jogos_ao_vivo():
    """Coleta dados de jogos ao vivo da API e insere no banco de dados."""
    try:
        url = f"{BASE_URL}fixtures?live=all"  # Endpoint da API para jogos ao vivo
        response = requests.get(url, headers=HEADERS)  # Faz a requisição para a API
        response.raise_for_status()  # Lança um erro se a resposta tiver um código HTTP ruim
        dados = response.json()  # Converte a resposta para JSON
        
        # Verifica se os dados contêm a chave 'response' e se é uma lista
        if "response" in dados and isinstance(dados["response"], list):
            for jogo in dados["response"]:
                liga = jogo.get("league", {}).get("name", "Desconhecido")  # Obtém o nome da liga
                time_casa = jogo.get("teams", {}).get("home", {}).get("name", "Desconhecido")  # Nome do time da casa
                time_fora = jogo.get("teams", {}).get("away", {}).get("name", "Desconhecido")  # Nome do time visitante
                placar = f"{jogo.get("goals", {}).get('home', 0)} - {jogo.get('goals', {}).get('away', 0)}"  # Placar do jogo
                status = jogo.get("fixture", {}).get("status", {}).get("long", "Desconhecido")  # Status do jogo
                
                # Insere os dados coletados no banco de dados
                cursor.execute('''
                    INSERT INTO jogos (liga, time_casa, time_fora, placar, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (liga, time_casa, time_fora, placar, status))
                conn.commit()  # Salva as mudanças no banco de dados
    except requests.exceptions.RequestException as e:
        print(f"Erro ao coletar dados da API: {e}")  # Exibe erro caso a requisição falhe
    except sqlite3.Error as e:
        print(f"Erro ao salvar no banco de dados: {e}")  # Exibe erro caso haja falha no banco de dados
    except Exception as e:
        print(f"Erro inesperado: {e}")  # Captura e exibe qualquer outro erro inesperado

# Executar coleta de tempos em tempos
if __name__ == "__main__":  # Garante que o código só rode se for executado diretamente
    while True:
        coletar_jogos_ao_vivo()  # Chama a função para coletar os jogos ao vivo
        print("Dados coletados!")  # Exibe mensagem de confirmação
        time.sleep(60)  # Aguarda 60 segundos antes de coletar novamente
