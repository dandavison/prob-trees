import csv
import sys
import networkx as nx
from dataclasses import dataclass
from more_itertools import chunked

@dataclass
class Node:
    path: str
    label: str

    def __hash__(self):
        return hash(self.path)


def make_tree(path: str) -> nx.DiGraph:
    data = list(csv.reader(open(path), delimiter=','))
    data = list(zip(*data))

    root = Node('0', '0')
    graph = nx.DiGraph()

    for (states, probs) in chunked(data, 2):
        parent = root
        nx.set_node_attributes(graph, {parent: parent.label}, 'label')
        for (state, prob) in zip(states, probs):
            prob = float(prob)
            child = Node(f"{parent.path} -> {state}", state)
            graph.add_edge(parent, child, prob=prob, name=state)
            nx.set_edge_attributes(graph, {(parent, child): prob}, 'label')
            nx.set_edge_attributes(graph, {(parent, child): prob * 10}, 'penwidth')
            nx.set_node_attributes(graph, {child: child.label}, 'label')
            parent = child

    return graph

def validate(graph):
    # if the sum of the probabilities is not 1, then the tree is invalid
    for node in nx.dfs_postorder_nodes(graph):
        if graph.out_degree(node) == 0:
            continue
        probs = [graph.edges[node, child]['prob'] for child in graph.successors(node)]
        if sum(probs) != 1:
            print(f"Invalid tree at node {node}: {probs}")
            return False
    return True


def write_dot(graph, path):
    with open(path, 'w') as fp:
        fp.write(str(nx.nx_pydot.to_pydot(graph)))


path, = sys.argv[1:]
tree = make_tree(path)
write_dot(tree, path + '.dot')
validate(tree)
