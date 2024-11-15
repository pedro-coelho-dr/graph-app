import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from graph.parser import parse_graph_input
from graph.info import get_graph_info
import io

### CONFIGURAÇÕES ###
st.set_page_config(
    page_title="Simulador de Grafos",
    page_icon="🔗",
    layout="centered",
    initial_sidebar_state="expanded"
)

### ESTADO ###

if "graph" not in st.session_state:
    st.session_state.graph = nx.Graph()
if "graph_text" not in st.session_state:
    st.session_state.graph_text = ""

############## MENU ##############

### CONFIGURAÇÃO ###

# Título do menu lateral
st.sidebar.header("CONFIGURAÇÃO")

# Controle do grafo direcionado
directed = st.sidebar.checkbox("Direcional", value=isinstance(st.session_state.graph, nx.DiGraph))

# Grafo valorado
valued = st.sidebar.checkbox("Valorado", value=False)

# Reinicializa o grafo se o tipo foi alterado
if directed and not isinstance(st.session_state.graph, nx.DiGraph):
    st.session_state.graph = nx.DiGraph()
elif not directed and isinstance(st.session_state.graph, nx.DiGraph):
    st.session_state.graph = nx.Graph()

### VERTICES ###

# Adicionar vértice
st.sidebar.header("VÉRTICES")
st.sidebar.subheader("Adicionar Vértice")
new_node = st.sidebar.text_input("Nome do Vértice")
if st.sidebar.button("Adicionar Vértice"):
    if new_node and new_node not in st.session_state.graph:
        st.session_state.graph.add_node(new_node)

# Remover vértice - exibe apenas se houver vértices
if len(st.session_state.graph.nodes) > 0:
    st.sidebar.subheader("Remover Vértice")
    remove_node = st.sidebar.selectbox("Remover Vértice", options=st.session_state.graph.nodes)
    if st.sidebar.button("Remover Vértice"):
        if remove_node in st.session_state.graph:
            st.session_state.graph.remove_node(remove_node)

### ARESTAS ###

# Adicionar aresta
st.sidebar.header("ARESTAS")

if len(st.session_state.graph.nodes) >= 2:
    st.sidebar.subheader("Adicionar Aresta")
    node1 = st.sidebar.selectbox("Vértice 1", options=st.session_state.graph.nodes)
    node2 = st.sidebar.selectbox("Vértice 2", options=st.session_state.graph.nodes)

    weight = st.sidebar.number_input("Peso da Aresta", value=1.0, step=1.0) if valued else 0.0

    if st.sidebar.button("Adicionar Aresta"):
        if node1 != node2 and not st.session_state.graph.has_edge(node1, node2):
            st.session_state.graph.add_edge(node1, node2, weight=weight)
else:
    st.sidebar.write("Adicione pelo menos dois vértices para criar arestas.")

# Remover aresta - exibe apenas se houver arestas
if len(st.session_state.graph.edges) > 0:
    st.sidebar.subheader("Remover Aresta")
    edge_to_remove = st.sidebar.selectbox("Selecione a Aresta", options=[f"{u}-{v}" for u, v in st.session_state.graph.edges])
    if st.sidebar.button("Remover Aresta"):
        u, v = edge_to_remove.split("-")
        if st.session_state.graph.has_edge(u, v):
            st.session_state.graph.remove_edge(u, v)

### SALVAR ###

# Seção SALVAR
st.sidebar.header("GERAR INSTRUÇÃO DO GRAFO")

# Gera a string a partir do grafo atual
if len(st.session_state.graph.edges) > 0:
    generated_text = []
    for u, v, data in st.session_state.graph.edges(data=True):
        weight = data.get("weight", 1)  # Peso padrão se não especificado
        edge_str = f"{u}-({weight})-{v}"
        generated_text.append(edge_str)
    grafo_string = "\n".join(generated_text)
else:
    grafo_string = ""

# Atualiza o campo de texto ao salvar
if st.sidebar.button("Gerar Instrução"):
    st.session_state.graph_text = grafo_string


# =================LOTE==================
# Exibe e permite a entrada do grafo no campo de texto
st.sidebar.header("INSERÇÃO EM LOTE")
graph_input = st.sidebar.text_area("Formato: A-(1)-B", value=st.session_state.graph_text, height=150)

# Botão para gerar um novo grafo a partir do input de texto
if st.sidebar.button("Gerar Grafo"):
    st.session_state.graph.clear()
    st.session_state.graph = parse_graph_input(graph_input, st.session_state.graph)
    st.rerun()
    


### LIMPAR ###

# Botão para limpar o grafo e resetar o estado
st.sidebar.markdown("---")
if st.sidebar.button("Limpar Grafo"):
    st.session_state.graph = nx.Graph()
    st.session_state.graph_text = ""
    # st.experimental_rerun()  # Refreshes the app to reset the UI

############## MAIN ##############

# Exibe ordem e tamanho do grafo
ordem, tamanho = get_graph_info(st.session_state.graph)
st.write(f"[Ordem: {ordem} ] [Tamanho: {tamanho}]")


# Exibe o grafo usando a visualização original do NetworkX e matplotlib
fig, ax = plt.subplots(figsize=(8, 6))

pos = nx.spring_layout(st.session_state.graph)

nx.draw_networkx_nodes(st.session_state.graph, pos, ax=ax, node_color='skyblue', node_size=500)

# Desenha arestas
if directed:
    nx.draw_networkx_edges(st.session_state.graph, pos, ax=ax, arrows=True, arrowstyle='->', edge_color='#888', arrowsize=15)
else:
    nx.draw_networkx_edges(st.session_state.graph, pos, ax=ax, edge_color='#888')

# Desenha legendas
nx.draw_networkx_labels(st.session_state.graph, pos, ax=ax, font_size=12, font_color='darkblue')

# Exibe pesos das arestas no meio delas
if valued:
    edge_labels = nx.get_edge_attributes(st.session_state.graph, 'weight')
    nx.draw_networkx_edge_labels(st.session_state.graph, pos, edge_labels=edge_labels, ax=ax, font_color='red')


st.pyplot(fig)

# Salva o gráfico em um buffer de memória
buffer = io.BytesIO()
plt.savefig(buffer, format="png")
buffer.seek(0)

# Botão de download para o gráfico gerado
st.download_button(
    label="Baixar Grafo",
    data=buffer,
    file_name="grafo.png",
    mime="image/png"
)

col1, col2 = st.columns(2)

# Coluna 1: Selecionar um vértice
with col1:
    st.subheader("Selecionar Um Vértice")
    if len(st.session_state.graph.nodes) > 0:
        selected_node = st.selectbox("Escolha um Vértice", options=st.session_state.graph.nodes)
        if selected_node:
            # Exibe informações sobre o vértice selecionado
            degree = st.session_state.graph.degree[selected_node]
            adjacents = list(st.session_state.graph.neighbors(selected_node))
            st.write(f"**Grau:** {degree}")
            st.write(f"**Vértices Adjacentes:** {', '.join(map(str, adjacents))}")

            if isinstance(st.session_state.graph, nx.DiGraph):
                in_degree = st.session_state.graph.in_degree[selected_node]
                out_degree = st.session_state.graph.out_degree[selected_node]
                st.write(f"**Grau de Entrada:** {in_degree}")
                st.write(f"**Grau de Saída:** {out_degree}")
            
            # Centralidade de Grau
            degree_centrality = nx.degree_centrality(st.session_state.graph)[selected_node]
            st.write(f"**Centralidade de Grau:** {degree_centrality:.2f}")

            # Centralidade de Proximidade
            closeness_centrality = nx.closeness_centrality(st.session_state.graph, selected_node)
            st.write(f"**Centralidade de Proximidade:** {closeness_centrality:.2f}")

            # Centralidade de Intermediação (Betweenness)
            betweenness_centrality = nx.betweenness_centrality(st.session_state.graph)[selected_node]
            st.write(f"**Centralidade de Intermediação:** {betweenness_centrality:.2f}")

            # Coeficiente de Agrupamento (Clustering Coefficient)
            clustering_coefficient = nx.clustering(st.session_state.graph, selected_node)
            st.write(f"**Coeficiente de Agrupamento:** {clustering_coefficient:.2f}")

            # Excentricidade (caso o grafo seja conexo)
            try:
                eccentricity = nx.eccentricity(st.session_state.graph, selected_node)
                st.write(f"**Excentricidade:** {eccentricity}")
            except nx.NetworkXError:
                st.write("**Excentricidade:** Não aplicável (grafo desconexo)")

    else:
        st.write("Adicione vértices ao grafo.")

# Coluna 2: Selecionar um segundo vértice para comparação com o vértice selecionado na Coluna 1
with col2:
    st.subheader("Comparar Outro Vértice")
    if len(st.session_state.graph.nodes) > 1:
        node2 = st.selectbox("Escolha Outro Vértice", options=[node for node in st.session_state.graph.nodes], key="node2")
        
        if selected_node and node2:
            # Verifica adjacência  entre os vértices selecionados
            adjacent = st.session_state.graph.has_edge(selected_node, node2)
            st.write(f"**Adjacentes:** {'Sim' if adjacent else 'Não'}")
            
            # Calcula o caminho mais curto se os vértices não forem iguais
            if selected_node != node2:
                try:
                    shortest_path = nx.shortest_path(st.session_state.graph, source=selected_node, target=node2, weight='weight' if valued else None)
                    path_length = nx.shortest_path_length(st.session_state.graph, source=selected_node, target=node2, weight='weight' if valued else None)
                    st.write(f"**Caminho Mais Curto:** {' → '.join(shortest_path)}")
                    st.write(f"**Custo do Caminho:** {path_length}")
                except nx.NetworkXNoPath:
                    st.write("**Caminho Mais Curto:** Nenhum caminho disponível.")
    else:
        st.write("Adicione pelo menos dois vértices ao grafo.")
