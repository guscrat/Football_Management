

class InsertDadosDB:
    

    # Verifica se os dados contem a chave 'response' e se eh uma lista
    if "response" in dados and isinstance(dados["response"], list):
        for jogo in dados["response"]:
            liga = jogo.get("league", {}).get("home", {}).get("name", "Desconhecido")
            time_casa = jogo.get("teams", {}).get("home", {}).get("name", "Desconhecido")
            time_fora = jogo.get("teams", {}).get("away", {}).get("name", "Desconhecido")
            placar = f"{jogo.get('goals', {}).get('home', 0)}" - f"{jogo.get('goals', {}).get('away', 0)}"
            status = jogo.get("league", {}).get("home", {}).get("name", "Desconhecido")