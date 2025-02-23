import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def carregar_dados():
    conn = sqlite3.connect('futebol.db')
    
    # Query principal com joins para todas as informações relevantes
    df = pd.read_sql_query("""
        SELECT 
            f.*,
            l.name as league_name,
            l.country as league_country,
            l.season,
            ht.name as home_team_name,
            ht.logo as home_team_logo,
            at.name as away_team_name,
            at.logo as away_team_logo,
            g.home as home_goals,
            g.away as away_goals
        FROM fixtures f
        LEFT JOIN leagues l ON f.league_id = l.id
        LEFT JOIN teams ht ON f.home_team_id = ht.id
        LEFT JOIN teams at ON f.away_team_id = at.id
        LEFT JOIN goals g ON f.id = g.fixture_id
    """, conn)
    
    # Carregar eventos
    eventos = pd.read_sql_query("""
        SELECT 
            e.*,
            t.name as team_name
        FROM events e
        LEFT JOIN teams t ON e.team_id = t.id
    """, conn)
    
    conn.close()
    return df, eventos

def main():
    st.title('Dashboard de Análise de Jogos')
    
    # Carregar dados
    df, eventos = carregar_dados()
    
    # Sidebar para filtros
    st.sidebar.header('Filtros')
    
    # Filtro por país
    paises = sorted(df['league_country'].unique())
    pais_selecionado = st.sidebar.multiselect(
        'Selecione os Países',
        options=paises
    )
    
    # Filtro por liga
    ligas = sorted(df['league_name'].unique())
    liga_selecionada = st.sidebar.multiselect(
        'Selecione as Ligas',
        options=ligas
    )
    
    # Filtro por status
    status_options = sorted(df['status'].unique())
    status_selecionado = st.sidebar.multiselect(
        'Status do Jogo',
        options=status_options
    )
    
    # Aplicar filtros
    df_filtrado = df.copy()
    if pais_selecionado:
        df_filtrado = df_filtrado[df_filtrado['league_country'].isin(pais_selecionado)]
    if liga_selecionada:
        df_filtrado = df_filtrado[df_filtrado['league_name'].isin(liga_selecionada)]
    if status_selecionado:
        df_filtrado = df_filtrado[df_filtrado['status'].isin(status_selecionado)]
    
    # Tabs para diferentes visualizações
    tab1, tab2, tab3 = st.tabs(["Visão Geral", "Detalhes dos Jogos", "Eventos"])
    
    with tab1:
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Jogos", len(df_filtrado))
        with col2:
            jogos_ao_vivo = len(df_filtrado[df_filtrado['status'] == 'LIVE'])
            st.metric("Jogos ao Vivo", jogos_ao_vivo)
        with col3:
            total_gols = df_filtrado['home_goals'].sum() + df_filtrado['away_goals'].sum()
            st.metric("Total de Gols", total_gols)
        with col4:
            media_gols = total_gols / len(df_filtrado) if len(df_filtrado) > 0 else 0
            st.metric("Média de Gols", f"{media_gols:.2f}")
        
        # Gráfico de gols por liga
        fig_gols = px.bar(
            df_filtrado.groupby('league_name').agg({
                'home_goals': 'sum',
                'away_goals': 'sum'
            }).reset_index(),
            x='league_name',
            y=['home_goals', 'away_goals'],
            title='Gols por Liga',
            labels={'value': 'Número de Gols', 'league_name': 'Liga'}
        )
        st.plotly_chart(fig_gols)
    
    with tab2:
        # Tabela de jogos em andamento
        st.subheader('Jogos')
        jogos_detalhes = df_filtrado[[
            'league_name', 'home_team_name', 'away_team_name',
            'home_goals', 'away_goals', 'status', 'elapsed', 'venue'
        ]].copy()
        
        # Formatando o placar
        jogos_detalhes['Placar'] = jogos_detalhes.apply(
            lambda x: f"{x['home_goals']} - {x['away_goals']}"
            if pd.notna(x['home_goals']) and pd.notna(x['away_goals'])
            else "0 - 0", axis=1
        )
        
        st.dataframe(jogos_detalhes)
    
    with tab3:
        # Análise de eventos
        st.subheader('Eventos dos Jogos')
        
        # Filtrar eventos para jogos selecionados
        eventos_filtrados = eventos[eventos['fixture_id'].isin(df_filtrado['id'])]
        
        # Gráfico de tipos de eventos
        fig_eventos = px.pie(
            eventos_filtrados,
            names='type',
            title='Distribuição de Tipos de Eventos'
        )
        st.plotly_chart(fig_eventos)
        
        # Lista de eventos recentes
        st.subheader('Eventos Recentes')
        eventos_recentes = eventos_filtrados.sort_values('timestamp', ascending=False).head(10)
        for _, evento in eventos_recentes.iterrows():
            st.text(f"{evento['time']}' - {evento['team_name']}: {evento['type']} - {evento['player']}")

if __name__ == "__main__":
    main() 