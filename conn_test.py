import sqlite3

conn = sqlite3.connect('futebol.db')
cursor = conn.cursor()

# Obter todas as tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

schema_completo = {}

# Para cada tabela, obter sua estrutura
for tabela in tabelas:
    nome_tabela = tabela[0]
    cursor.execute(f"PRAGMA table_info({nome_tabela})")
    colunas = cursor.fetchall()
    schema_completo[nome_tabela] = colunas

conn.close()

# Imprimir o schema de forma organizada
for tabela, colunas in schema_completo.items():
    print(f"\nTabela: {tabela}")
    print("-" * 50)
    for coluna in colunas:
        print(f"Nome: {coluna[1]}, Tipo: {coluna[2]}, NotNull: {coluna[3]}, Default: {coluna[4]}, PK: {coluna[5]}")