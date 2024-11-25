import networkx as nx

def get_graph_info(graph):
    ordem = graph.number_of_nodes()
    tamanho = graph.number_of_edges()
    return ordem, tamanho

def calculate_layout(graph):
    k = 3.0
    scale = 2.0
    pos = nx.spring_layout(graph, k=k, scale=scale)
    return pos