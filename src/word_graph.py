class Node(object):
    def __init__(self, key, weight, source=None, freq=None):
        self.key = key
        self.weight = weight
        self.source = source
        self.freq = freq

    def __str__(self):
        return ''.join(
            ['Node(key=', self.key, ',weight=', str(self.weight), ',source=',
             str(self.source),
             ',freq=', str(self.freq), ')'])


class WordGraph(object):
    NODE_S = Node('#S#', 0)
    NODE_E = Node('#E#', 0)

    def __init__(self):
        self._start_node_list = []
        self._end_nodes_index_list = []
        self._size = 0

    def __len__(self):
        return self._size

    def insert_start_word(self, node):
        self._start_node_list.append(node)
        self._size += 1


    def insert_end_words(self, row):
        self._end_nodes_index_list.append(row)


    def __str__(self):
        graph_list = []
        for i in range(self._size):
            graph_list.extend([str(self._start_node_list[i]), ' => '])
            graph_list.extend([str(node) for node in list(map(self.get_node, self._end_nodes_index_list[i]))])
            graph_list.append('\n')


    def get_node(self, index):
        return self._start_node_list[index]

    def calculate(self):
        self._start_node_list.append(WordGraph.NODE_E)
        route = {self._size: (0, self._size)}

        for i in range(self._size - 1, -1, -1):
            route[i] = max(
                (self._start_node_list[i].weight + route[index][0], index) for index in self._end_nodes_index_list[i]
            )

        return route


if __name__ == '__main__':
    graph = WordGraph()

    graph.insert_start_word(WordGraph.NODE_S)  # 0
    graph.insert_start_word(Node('我', 1, 'core_dict'))  # 1
    graph.insert_start_word(Node('喜', 2, 'core_dict'))  # 2
    graph.insert_start_word(Node('喜欢', 4, 'user_dict'))  # 3
    graph.insert_start_word(Node('欢', 1, 'core_dict'))  # 4

    graph.insert_end_words([1])
    graph.insert_end_words([2, 3])
    graph.insert_end_words([4])
    graph.insert_end_words([5])
    graph.insert_end_words([5])

    route = graph.calculate()

    print('词图：\n', graph)
    print('最优路径：\n', route)


