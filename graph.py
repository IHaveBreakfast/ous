import numpy as np

class Node:
    def __init__(self, bind, index = None, intensity = 0):
        self.bind = bind
        self.index = index
        self.intensity = intensity

class Edge:
    def __init__(self, bind, binding_indexes, length = 0, intensity = 0):
        self.bind = bind
        self.binding_indexes = binding_indexes
        self.length = length
        self.intensity = intensity

class Graph:
    def __init__(self, num, nodes = None, edges = None):
        self.matrix = np.zeros((num, num))
        self.nodes = nodes
        self.edges = edges
        self.list_binds = []
        if self.nodes is not None:
            for i in range(len(self.nodes)):
                self.nodes[i].index = i

    def generate_nodes(self, bind_nodes: list):
        self.nodes = []
        for bind in bind_nodes:
            self.nodes.append(Node(bind, bind_nodes.index(bind)))

    def connect_dual(self):
        for item in self.edges:
            self.matrix[item.binding_indexes[0]][item.binding_indexes[1]] = 1
            self.matrix[item.binding_indexes[1]][item.binding_indexes[0]] = 1

    def get_matrix(self):
        return self.matrix

    def get_nodes(self):
        return self.nodes

    def get_binds(self):
        return self.edges

    def build_graph(self, data):
        self.nodes = []
        self.edges = []
        for node in data['Nodes']:
            self.nodes.append(Node(data['Nodes'][node]['bind'], data['Nodes'][node]['index'], intensity=data['Nodes'][node]['intensity']))
        for edge in data['Binds']:
            self.edges.append(Edge(data['Binds'][edge]['bind'], (data['Binds'][edge]['binding_indexes'][0], data['Binds'][edge]['binding_indexes'][1]), length=data['Binds'][edge]['length']))
        self.connect_dual()

    def get_labels(self):
        data = {}
        for item in self.nodes:
            data[item.index] = item.bind
        return data

    def get_path_elements(self, paths):
        common_list = []
        for path in paths:
            path_list = []
            for item in path:
                element_list = [0, 0.0]
                index_path = path.index(item)
                element_list[0] = str(item)
                for node in self.nodes:
                    if node.index == item:
                        element_list[1] = node.intensity
                path_list.append(element_list.copy())
                if index_path == 0:
                    continue
                else:
                    node_1 = path[index_path - 1]
                    node_2 = path[index_path]
                    for edge in self.edges:
                        if (edge.binding_indexes[0] == node_1 and edge.binding_indexes[1] == node_2) or \
                           (edge.binding_indexes[1] == node_1 and edge.binding_indexes[0] == node_2):
                            path_list.insert(path_list.index(path_list[-1]), [f'{edge.binding_indexes[0]}{edge.binding_indexes[1]}', edge.intensity])
                            break
            common_list.append(path_list)
        return common_list
