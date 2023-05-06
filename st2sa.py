# Author: Kieran Moran
# Student ID: 31482244

import sys


def st2sa(input_str):
    input_list = [char for char in input_str]
    input_list.append('$')
    sufTree = SuffixTree()
    sufTree.build(input_list)
    return sufTree.output_array()


class SuffixTree:
    class Node:
        def __init__(self, start):
            self.start = start
            self.children = []
            self.end = None
            self.suf_link = None
            self.input_index = None

        def debug(self):
            print(
                f"self={self}Node(start={self.start}, end={self.end}, suf_link={self.suf_link}, input_index={self.input_index})")

    def __init__(self):
        self.root = self.Node(None)
        self.active_node = self.root
        self.remainder_index = None
        self.remainder_length = 0
        self.last_j = 0
        self.global_end = 0
        self.active_edge_node = None
        self.previous_node = self.root
        self.input_list = []

    def build(self, input_list):
        self.input_list = input_list
        n = len(input_list)
        for i in range(n):
            self.global_end += 1
            if i == 0:
                first_node = self.add_node(self.active_node, 0)
                self.active_node.suf_link = self.active_node
                first_node.input_index = 0
            else:
                j = self.last_j + 1
                while j <= i:
                    # debug function
                    # self.debug()
                    if self.active_edge_node is None and self.remainder_length > 0:
                        for node in self.active_node.children:
                            if input_list[node.start] == input_list[self.remainder_index]:
                                self.active_edge_node = node

                    # skip count down to extension
                    while self.active_edge_node is not None and self.remainder_length >= self.get_node_length(
                            self.active_edge_node):
                        self.remainder_length -= self.get_node_length(self.active_edge_node)
                        self.remainder_index += self.get_node_length(self.active_edge_node)
                        self.active_node = self.active_edge_node
                        if self.remainder_length > 0:
                            for node in self.active_node.children:
                                if input_list[node.start] == input_list[self.remainder_index]:
                                    self.active_edge_node = node
                        else:
                            self.active_edge_node = None
                            self.remainder_index = None

                    if self.active_edge_node is not None:
                        if input_list[self.active_edge_node.start + self.remainder_length] != input_list[i]:
                            self.rule2(self.active_edge_node, i, j)
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
                            self.rule2(self.active_node, i, j)
                    j += 1

    def rule2(self, node, index, j):

        # leaf only
        if self.active_edge_node is None:
            new_node = self.add_node(node, index)
            new_node.input_index = j
            # resolve previous suffix_link
            if self.previous_node is not None:
                self.previous_node.suf_link = self.active_node
                self.previous_node = None
        else:
            new_node = self.add_node(self.active_node, self.active_edge_node.start)
            new_node.end = self.active_edge_node.start + self.remainder_length
            leaf = self.add_node(new_node, index)
            leaf.input_index = j
            self.active_node.children.remove(self.active_edge_node)
            new_node.children.append(self.active_edge_node)
            self.active_edge_node.start = self.active_edge_node.start + self.remainder_length

            # resolve previous suffix_link
            if self.previous_node is not None:
                self.previous_node.suf_link = new_node
                self.previous_node = None
            self.previous_node = new_node

        # cleanup
        self.last_j = j
        self.active_edge_node = None

        if self.active_node == self.root and self.remainder_length is not None:
            self.remainder_length -= 1
            if self.remainder_length <= 0:
                self.remainder_length = 0
                self.remainder_index = None
            else:
                self.remainder_index += 1
            self.active_edge_node = None

        self.active_node = self.active_node.suf_link

    def rule3(self, node):
        self.active_edge_node = node
        self.remainder_length += 1
        if self.remainder_length == 1:
            self.remainder_index = node.start
        if len(node.children) > 0 and self.get_node_length(node) == self.remainder_length:
            self.active_node = node
            self.active_edge_node = None
            self.remainder_length = 0
            self.remainder_index = None

        # resolve previous
        if self.previous_node is not None:
            self.previous_node.suf_link = self.active_node
            self.previous_node = None

        # self.active_node = self.active_node.suf_link

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

    def output_array(self):
        suffix_array = []
        self.dfs(self.root, suffix_array)
        return suffix_array

    def dfs(self, node, suffix_array):
        sorted_children = sorted(node.children, key=lambda child: self.input_list[child.start])
        for child in sorted_children:
            if len(child.children) == 0:
                suffix_array.append(child.input_index + 1)
            else:
                self.dfs(child, suffix_array)
        return

    def debug(self):
        print("root:", end='')
        self.root.debug()
        for node in self.root.children:
            print("---")
            node.debug()
            for deep_node in node.children:
                print(">>", end='     ')
                deep_node.debug()
                for deep_deep in deep_node.children:
                    print("//", end='                ')
                    deep_deep.debug()


def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()


def clear_file(filename):
    with open(filename, 'w') as file:
        pass


if __name__ == '__main__':
    clear_file('output_sa.txt')
    if len(sys.argv) != 2:
        print("Usage: python st2sa.py <text filename>")
        sys.exit(1)

    text_file = sys.argv[1]

    text = read_file(text_file)

    sa = st2sa(text)

    with open('output_sa.txt', 'w') as file:
        for index in sa:
            file.write(f"{index}\n")
