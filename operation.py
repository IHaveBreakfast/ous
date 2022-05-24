import networkx as nx
import yaml
from pyqt import pyqt
from graph import Graph
from failure import Failure
from os import path
import gc

class Operation:
    def __init__(self, data, report):
        self.data = data
        self.view = pyqt(self)
        self.view.set_settings(self.data.get_settings())

        self.graph = None
        self.network = None
        self.graphs_data = None
        self.modeling = None
        self.report = report
        self.read_structure_graphs_yaml()

    def window_show(self):
        self.view.show()

    def read_structure_graphs_yaml(self):
        read_graphs = path.exists('structure_graphs.yaml')
        if read_graphs is True:
            with open('structure_graphs.yaml', 'r', encoding='utf-8') as file:
                self.graphs_data = yaml.load(file, Loader=yaml.FullLoader)
            self.view.GraphsList(list(self.graphs_data.keys()))
        else:
            pass

    def building_graph_topology(self, topology):
        self.graph = Graph(self.graphs_data[topology]['CountNodes'])
        self.graph.build_graph(self.graphs_data[topology])
        if self.network is not None:
           self.network = None
        self.network = nx.from_numpy_matrix(self.graph.get_matrix(), create_using=nx.MultiGraph)
        self.view.DrawGraph(self.network, self.graph.get_labels())
        self.view.NodesTable(self.graph.get_nodes())
        self.view.BindsTable(self.graph.get_binds())

    def save_settings(self, count_failure, count_restore, intensity, policy_restore):
        self.data.set_settings('settings.yaml', [count_failure, count_restore, intensity, policy_restore])

    def start_modeling(self, start_node, stop_node, node_list, bind_list, intensity_connection, check):
        settings = self.data.get_settings()
        self.modeling = Failure(self.network, settings[0], settings[1], settings[2], settings[3], check, self.report)
        del settings
        nodes = self.graph.get_nodes()
        for node in nodes:
            node.intensity = float(node_list[node.bind]) * 1e-6
        node1 = None
        node2 = None
        binds = self.graph.get_binds()
        for bind in binds:
            bind.intensity = float(bind_list[bind.bind]) * float(intensity_connection) * 1e-6
        for node in nodes:
            if node.bind == start_node:
                node1 = node.index
            elif node.bind == stop_node:
                node2 = node.index
        paths = list(nx.all_simple_paths(self.network, node1, node2))
        data = self.graph.get_path_elements(paths)


        self.modeling.start(node1, node2, binds, nodes)
        self.view.Paths(paths, self.graph.get_labels())
        self.view.Result(self.report.get_data_result())
        self.view.Histogram(self.report.get_histogram_failure(), False)
        if check:
            self.view.Histogram(self.report.get_histogram_restore(), True)
        self.view.ProbChart(self.report.Prob(data))
        self.view.ProbFormula(data)
        del paths, binds, nodes, data
        del self.modeling
        gc.collect()