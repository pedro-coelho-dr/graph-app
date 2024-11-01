import streamlit as st
import networkx as nx
import plotly.graph_objects as go

def app():
    # Título da aplicação
    st.title("Simulador de Grafos Interativo")


    # Inicializa o grafo
    if "graph" not in st.session_state:
        st.session_state.graph = nx.Graph()



    # ============MENU-START=================

    # Opções para adicionar vértices
    st.sidebar.header("Adicionar Vértices")
    new_node = st.sidebar.text_input("Nome do Vértice")
    if st.sidebar.button("Adicionar Vértice"):
        if new_node and new_node not in st.session_state.graph:
            st.session_state.graph.add_node(new_node)
            st.success(f"Vértice '{new_node}' adicionado!")

    # Opções para adicionar arestas com peso
    st.sidebar.header("Adicionar Arestas")
    node1 = st.sidebar.selectbox("Vértice 1", options=st.session_state.graph.nodes)
    node2 = st.sidebar.selectbox("Vértice 2", options=st.session_state.graph.nodes)
    weight = st.sidebar.number_input("Peso da Aresta", value=1.00, step=1.00)

    if st.sidebar.button("Adicionar Aresta"):
        if node1 != node2 and not st.session_state.graph.has_edge(node1, node2):
            st.session_state.graph.add_edge(node1, node2, weight=weight)
            st.success(f"Aresta entre '{node1}' e '{node2}' com peso {weight} adicionada!")


    # ===========MENU-END============

    # Define a posição inicial dos vértices
    pos = nx.spring_layout(st.session_state.graph)

    # Coleta coordenadas para arestas
    edge_x = []
    edge_y = []
    for edge in st.session_state.graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    # Configura o traçado das arestas no Plotly
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=3, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Coleta coordenadas para nós
    node_x = []
    node_y = []
    for node in st.session_state.graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    # Configura o traçado dos nós no Plotly com cor fixa e sem barra de cores
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=list(st.session_state.graph.nodes),
        textposition="bottom center",
        marker=dict(
            color='skyblue',  # Define uma cor fixa para os nós
            size=20,
        ),
        hoverinfo="text"
    )

    # Exibe o grafo interativo no Streamlit usando Plotly
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title="Grafo Interativo",
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=40),
                        paper_bgcolor='white',  # Fundo claro
                        plot_bgcolor='white',  # Fundo claro
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
    )

    st.plotly_chart(fig, use_container_width=True)

# Executa o app
if __name__ == "__main__":
    app()
