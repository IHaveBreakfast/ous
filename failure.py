import networkx, random, math
from graph import Node, Edge
from networkx import exception

from restore import Restore


class Failure:
    def __init__(self, graph: networkx, count_failures, count_teams, intensity_recovery, policy, restore, result):
        self.graph = graph
        self.count_failures = count_failures
        self.count_teams = count_teams
        self.intensity_recovery = intensity_recovery
        self.policy = policy
        self.restore = restore
        self.result = result
        self.calc_graph = None
        self.list_elements = None
        self.list_failures_times = []
        self.list_restore_times = []

    def get_graph_list(self, bind_list, node_list):
        common_list = []
        list_node = list(self.graph.nodes)
        for item in list_node:
            for node in node_list:
                if item == node.index:
                    common_list.append(node)
                    break
            for edge in bind_list:
                if item == edge.binding_indexes[0]:
                    common_list.append(edge)
        return common_list

    def check_restore(self):
        for item in self.list_elements:
            item.destroyed = False

    def start(self, first_node, last_node, list_edges, list_nodes):
        is_path = networkx.shortest_paths.has_path(self.graph, first_node, last_node)
        self.list_elements = self.get_graph_list(list_edges, list_nodes)
        self.check_restore()
        if is_path:
            for i in range(self.count_failures):
                self.calc_graph = self.graph.copy()
                self.check_restore()
                state = self.system_iteration(first_node, last_node)
                self.list_failures_times.append(state[0])
                if self.restore:
                    self.list_restore_times.extend(state[1])
            self.result.CalcMinTime(self.list_failures_times)
            self.result.CalcMaxTime(self.list_failures_times)
            self.result.CalcSredTime(self.list_failures_times)
            if self.restore:
                self.result.CalcSredTimeRestore(self.list_restore_times)
                self.result.CalcCoefReady()
                self.result.CalcHistogram(self.list_restore_times, restore=True)
            self.result.CalcHistogram(self.list_failures_times)
            self.list_failures_times = None
            self.list_restore_times = None

    def system_iteration(self, first_node, last_node):
        timestamp = 0.0
        list_task = []
        list_restore_time = []
        restore_tasks = Restore(self.policy)
        restore_team = self.count_teams

        first_failure = self.create_failure(timestamp)

        list_task.append(first_failure)

        path = True
        while path:
            try:
                path = networkx.shortest_paths.has_path(self.calc_graph, first_node, last_node)
                if not path:
                    break
            except (exception.NodeNotFound, exception.NetworkXNoPath):
                break
            min_element = list_task[0]

            for item in list_task:
                if item[0] < min_element[0]:
                    min_element = item
            list_task.remove(min_element)
            timestamp = min_element[0]
            if min_element[2] == 'refusal':
                min_element[1].destroyed = True
                failure = self.create_failure(timestamp)
                if isinstance(min_element[1], Node):
                    self.calc_graph.remove_node(min_element[1].index)
                elif isinstance(min_element[1], Edge):
                    try:
                        self.calc_graph.remove_edge(min_element[1].binding_indexes[0], min_element[1].binding_indexes[1])
                    except exception.NetworkXError:
                        pass
                list_task.append(failure)

                if self.restore:
                    restore_tasks.add_task([min_element[1],
                                           min_element[0],
                                           -1 * math.log(random.random()) / self.intensity_recovery])
            elif min_element[2] == 'restore':
                min_element[1].destroyed = False
                restore_team += 1
                self.restore_graph(min_element[1])

            while restore_team > 0 and not restore_tasks.check_empty_queue() and self.restore:
                task = restore_tasks.get_task()
                list_task.append([task[2] + timestamp, task[0], 'restore'])
                restore_team -= 1
                list_restore_time.append(task[2])
        return [timestamp, list_restore_time]

    def restore_graph(self, element):
        if isinstance(element, Node):
            self.calc_graph.add_node(element.index)
            for item in self.list_elements:
                if isinstance(item, Edge):
                    if item.binding_indexes[0] == element.index or item.binding_indexes[1] == element.index:
                        self.calc_graph.add_edge(item.binding_indexes[0], item.binding_indexes[1])
        elif isinstance(element, Edge):
            try:
                self.calc_graph.add_edge(element.binding_indexes[0], element.binding_indexes[1])
            except exception.NetworkXError:
                pass

    def create_failure(self, time):
        sum = 0
        value = 0.0
        fail = None
        for element in self.list_elements:
            if not element.destroyed:
                value = value + element.intensity
        random_value = random.random()
        rand = random_value * value
        for element in self.list_elements:
            if not element.destroyed:
                sum = sum + element.intensity
                if sum > rand:
                    fail = element
                    break
        if fail is None:
            return None
        time_fail = -1 * math.log(random_value) / fail.intensity
        time = time + time_fail
        return [time, fail, 'refusal']
