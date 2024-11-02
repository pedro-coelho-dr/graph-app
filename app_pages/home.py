import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from utils.graph_parser import parse_graph_input
from utils.graph_info import get_graph_info

def app():
    st.title("Simulador de Grafos Interativo")

    if "graph" not in st.session_state:
        st.session_state.graph = nx.DiGraph()  # DiGraph para suportar arestas direcionadas

    # ============MENU-START=================

    # Opção para inserir grafo por texto
    st.sidebar.header("Inserir Grafo por Texto")
    graph_input = st.sidebar.text_area("Insira as arestas no formato especificado:")
    if st.sidebar.button("Criar Grafo por Texto"):
        st.session_state.graph.clear()  # Limpa o grafo existente antes de adicionar novos nós/arestas
        parse_graph_input(graph_input, st.session_state.graph)
        st.success("Grafo criado com sucesso a partir do texto!")

    # Opções para adicionar vértices manualmente
    st.sidebar.header("Adicionar Vértices Manualmente")
    new_node = st.sidebar.text_input("Nome do Vértice")
    if st.sidebar.button("Adicionar Vértice"):
        if new_node and new_node not in st.session_state.graph:
            st.session_state.graph.add_node(new_node)
            st.success(f"Vértice '{new_node}' adicionado!")

    # Opções para adicionar arestas manualmente
    st.sidebar.header("Adicionar Arestas Manualmente")
    node1 = st.sidebar.selectbox("Vértice 1", options=st.session_state.graph.nodes)
    node2 = st.sidebar.selectbox("Vértice 2", options=st.session_state.graph.nodes)
    weight = st.sidebar.number_input("Peso da Aresta", value=1.0, step=1.0)
    directed = st.sidebar.checkbox("Aresta Direcionada")

    if st.sidebar.button("Adicionar Aresta"):
        if node1 != node2 and not st.session_state.graph.has_edge(node1, node2):
            if directed:
                st.session_state.graph.add_edge(node1, node2, weight=weight)
            else:
                st.session_state.graph.add_edge(node1, node2, weight=weight)
            st.success(f"Aresta entre '{node1}' e '{node2}' com peso {weight} adicionada!")

    # ===========MENU-END============

    # Exibe ordem e tamanho do grafo
    ordem, tamanho = get_graph_info(st.session_state.graph)
    st.write(f"**Ordem: {ordem} // Tamanho:** {tamanho}")

    # Exibe o grafo usando a visualização original do NetworkX e matplotlib
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.spring_layout(st.session_state.graph)
    
    # Desenha nós e arestas com pesos e setas direcionadas
    nx.draw_networkx_nodes(st.session_state.graph, pos, ax=ax, node_color='skyblue', node_size=500)
    nx.draw_networkx_edges(st.session_state.graph, pos, ax=ax, arrows=True, arrowstyle='->', edge_color='#888')
    nx.draw_networkx_labels(st.session_state.graph, pos, ax=ax, font_size=12, font_color='darkblue')
    
    # Exibe pesos das arestas no meio delas
    edge_labels = nx.get_edge_attributes(st.session_state.graph, 'weight')
    nx.draw_networkx_edge_labels(st.session_state.graph, pos, edge_labels=edge_labels, ax=ax, font_color='red')

    st.pyplot(fig)

# Executa o app
if __name__ == "__main__":
    app()
