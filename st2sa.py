def st2sa(input_str):
    input_list = [char for char in input_str]
    input_list.append('$')

    sufTree = SuffixTree()
    sufTree.build(input_list)


class SuffixTree:
    class Node:
        def __init__(self, start):
            self.start = start
            self.children = []
            self.end = None
            self.sufLink = self

    def __init__(self):
        self.root = self.Node(None)
        self.active_node = self.root
        self.remainder_index = None
        self.remainder_length = 0
        self.last_j = 0
        self.global_end = 0
        self.active_edge_node = None

    def build(self, input_list):
        n = len(input_list)
        for i in range(n - 1):
            self.global_end += 1
            if i == 0:
                self.add_node(self.active_node, 0)
            else:
                for j in range(self.last_j, i + 2):
                    # skip count down to extension
                    if(self.active_edge_node is not None):
                        while self.remainder_length > self.get_node_length(self.active_node):
                            self.remainder_length -= self.get_node_length(self.active_node)
                            self.remainder_index += self.get_node_length(self.active_node)
                            self.active_node = self.active_edge_node
                            if(self.remainder_length > 0):
                                for node in self.active_node.children:
                                    if input_list[node.start] == input_list[self.remainder_index]:
                                        self.active_edge_node = node
                                        break
                            else:
                                self.active_edge_node = None
                                self.remainder_index = None

                    # rule 3
                    if input_list[self.active_node.start + self.remainder_length] == input_list[i + 1]:
                        self.remainder_length += 1
                        if self.get_node_length(self.active_node) == self.remainder_length:
                            self.active_node = self.active_edge_node
                            self.active_edge_node = None
                            self.remainder_length = 0
                            self.remainder_index = None
                        if self.previous_rule == 2:
                            self.previous_node.sufLink = self.active_node
                        break # showstopper
                    # rule 2
                    else:
                        self.active_node.children.remove(self.active_edge_node)
                        new_node = self.add_node(self.active_node, j)
                        new_node.children.append(self.active_edge_node)

    def add_node(self, parent, start_index):
        child = self.Node(start_index)
        parent.children.append(child)
        return child

    def get_node_end(self, node):
        if node.end is None:
            return self.global_end
        else:
            return node.end

    def get_node_length(self, node):
        return self.get_node_end(node)-node.start


st2sa("mississippi")



