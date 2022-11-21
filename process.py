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
        return self.path
    
    def __str__(self):
        return self.label


def read_tree(path: str):
    data = list(csv.reader(open(path), delimiter=','))
    data = list(zip(*data))

    graph = nx.DiGraph()

    for (states, probs) in chunked(data, 2):
        path = '0'
        for (state, prob) in zip(states, probs):
            prob = float(prob)
            new_path = f"{path} -> {state}"
            graph.add_edge(path, new_path, prob=prob, name=state)
            path = new_path

    print(graph.edges)


path, = sys.argv[1:]
read_tree(path)
