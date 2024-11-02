import streamlit as st
import networkx as nx
import plotly.graph_objects as go
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
    

    #ORDEM E TAMANHO
    ordem, tamanho = get_graph_info(st.session_state.graph)
    st.write(f"**Ordem: {ordem} // Tamanho:** {tamanho}")

    # Define a posição inicial dos vértices
    pos = nx.spring_layout(st.session_state.graph)

    # Coleta coordenadas para arestas
    edge_x = []
    edge_y = []
    edge_weight_text = []  # Para armazenar o texto do peso

    for edge in st.session_state.graph.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

        # Posição média para exibir o peso no meio da aresta
        mid_x = (x0 + x1) / 2
        mid_y = (y0 + y1) / 2
        edge_weight_text.append((mid_x, mid_y, edge[2].get("weight", 1)))  # Padrão: peso 1

    # Configura o traçado das arestas no Plotly
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    # Coleta coordenadas para nós
    node_x = []
    node_y = []
    for node in st.session_state.graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    # Configura o traçado dos nós no Plotly
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=list(st.session_state.graph.nodes),
        textposition="bottom center",
        marker=dict(
            color='skyblue',
            size=20,
        ),
        textfont=dict(
            color='darkblue',
            size=14,
        ),
        hoverinfo="text"
    )

    # Configura o traçado dos pesos das arestas no Plotly
    weight_trace = go.Scatter(
        x=[pos[0] for pos in edge_weight_text],
        y=[pos[1] for pos in edge_weight_text],
        text=[f"{pos[2]}" for pos in edge_weight_text],
        mode="text",
        textposition="middle center",
        textfont=dict(
            color="red",
            size=12
        ),
        hoverinfo="none"
    )

    # Exibe o grafo interativo no Streamlit usando Plotly
    fig = go.Figure(data=[edge_trace, node_trace, weight_trace],
                    layout=go.Layout(
                        title="Grafo Interativo",
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=40),
                        paper_bgcolor='white',
                        plot_bgcolor='white',
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
    )

    st.plotly_chart(fig, use_container_width=True)

# Executa o app
if __name__ == "__main__":
    app()
