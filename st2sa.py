def st2sa(input_str):
    input_list = [char for char in input_str]
    input_list.append('$')

    sufTree = SuffixTree()
    sufTree.build(input_list)

    for node in sufTree.root.children:
        print("---")
        node.debug()
        for deep_node in node.children:
            print(">>", end='     ')
            deep_node.debug()
            for deep_deep in deep_node.children:
                print("//", end='                ')
                deep_deep.debug()

    print(sufTree.output_array(input_list))


class SuffixTree:
    class Node:
        def __init__(self, start):
            self.start = start
            self.children = []
            self.end = None
            self.suf_link = None

        def debug(self):
            print(f"self={self}Node(start={self.start}, end={self.end}, suf_link={self.suf_link})")

    def __init__(self):
        self.root = self.Node(None)
        self.active_node = self.root
        self.remainder_index = None
        self.remainder_length = 0
        self.last_j = 0
        self.global_end = 0
        self.active_edge_node = None
        self.previous_node = self.root

    def build(self, input_list):
        n = len(input_list)
        n=8
        for i in range(n):
            self.global_end += 1
            if i == 0:
                self.add_node(self.active_node, 0)
                self.active_node.suf_link = self.active_node
            else:
                j = self.last_j
                while j < i:
                    if(i==6):
                        print(f"self.root: {self.root}")
                        print(f"activeNodeL:{self.active_node}")
                        print(f"activeEDGE:{self.active_edge_node}")
                        print(f"remainder_len:{self.remainder_length}")
                    # skip count down to extension
                    if self.active_edge_node is not None:
                        while self.remainder_length > self.get_node_length(self.active_edge_node):
                            self.remainder_length -= self.get_node_length(self.active_node)
                            self.remainder_index += self.get_node_length(self.active_node)
                            self.active_node = self.active_edge_node
                            if self.remainder_length > 0:
                                for node in self.active_node.children:
                                    if input_list[node.start] == input_list[self.remainder_index]:
                                        self.active_edge_node = node
                                        break
                            else:
                                self.active_edge_node = None
                                self.remainder_index = None
                    if self.active_edge_node is not None:
                        if input_list[self.active_edge_node.start + self.remainder_length] != input_list[i]:
                            self.rule2(self.active_edge_node, i)
                        else:
                            self.rule3(self.active_edge_node)
                            j = i + 1  # set j to outside loop
                    else:
                        do_rule2 = True
                        for node in self.active_node.children:
                            if input_list[node.start] == input_list[i]:
                                do_rule2 = False
                                self.rule3(node)
                                j = i + 1  # set j to outside loop
                        if do_rule2:
                            self.rule2(self.active_node, i)
                    j += 1

    def rule2(self, node, index):
        # resolve previous suffix_link
        if self.previous_node is not None:
            self.previous_node.suf_link = self.active_node
            self.previous_node = None
        # leaf only
        if self.active_edge_node is None:
            new_node = self.add_node(node, index)
        else:
            node.end = node.start + self.remainder_length

            self.add_node(node, index)
            self.add_node(node, node.start + self.remainder_length)
            self.previous_node = node

        # cleanup
        self.last_j = index
        self.active_edge_node = None
        self.remainder_index = None
        self.remainder_length = 0
        self.active_node = self.active_node.suf_link

    def rule3(self, node):
        self.active_edge_node = node
        self.remainder_length += 1
        if len(node.children) > 0 and self.get_node_length(node) == self.remainder_length:
            self.active_node = node
            self.active_edge_node = None
            self.remainder_length = 0
            self.remainder_index = None

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
        return self.get_node_end(node) - node.start

    def output_array(self, input_list):
        suffix_array = []
        self.dfs(self.root, input_list, suffix_array)
        return suffix_array

    def dfs(self, node, input_list, suffix_array):
        sorted_children = sorted(node.children, key=lambda child: input_list[child.start])
        for child in sorted_children:
            if len(child.children) == 0:
                suffix_array.append(child.start + 1)
            else:
                self.dfs(child, input_list, suffix_array)
        return


# st2sa("mississippi")
st2sa("abacabad")
