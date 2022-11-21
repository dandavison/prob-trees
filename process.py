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
    
    def __str__(self):
        return self.path


def read_tree(path: str):
    data = list(csv.reader(open(path), delimiter=','))
    data = list(zip(*data))

    graph = nx.DiGraph()

    for (states, probs) in chunked(data, 2):
        parent =  Node('0', '0')
        for (state, prob) in zip(states, probs):
            child = Node(f"{parent.path} -> {state}", state)
            graph.add_edge(parent, child, prob=float(prob), name=state)
            parent = child

    print(nx.nx_pydot.to_pydot(graph))


path, = sys.argv[1:]
read_tree(path)