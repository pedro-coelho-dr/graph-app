import re


def parse_graph_input(graph_input, graph):
    pattern = r'(\w+)\s*(<|>|-)\s*(?:\((\d*\.?\d+)\))?\s*(>|-)?\s*(\w+)'
    
    for match in re.finditer(pattern, graph_input):
        node1, connector1, weight, connector2, node2 = match.groups()

        # Converte o peso para float, se existir
        weight = float(weight) if weight else 1.0

        # Adiciona nós ao grafo, se não existirem
        graph.add_node(node1)
        graph.add_node(node2)

        # Decide o tipo de aresta baseado nos conectores
        if connector1 == '-' and connector2 == '-':
            graph.add_edge(node1, node2, weight=weight)
        elif connector1 == '>' or connector2 == '>':
            graph.add_edge(node1, node2, weight=weight, directed=True)
        elif connector1 == '<' or connector2 == '<':
            graph.add_edge(node2, node1, weight=weight, directed=True)