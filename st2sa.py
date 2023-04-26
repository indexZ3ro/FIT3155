def st2sa(input_str):
    input_list = [char for char in input_str]
    input_list.append('$')
    
    sufTree = SuffixTree()
    sufTree.build(input_list)
        
class SuffixTree:
    class Node:
        def __init__(self, index):
            self.index = index
            self.children = []
            self.end = None
        
        
    def __init__(self):
        self.root = self.Node(None)
        self.active_node = self.root
        self.remainder = None
        self.last_j = 0
        self.global_end = 0
        
    def build(self, input_list):
        n = len(input_list)
        for i in range(n):
            self.add(input_list[i])
        
        
    def add(self, char):
        #base case
        if len(self.root.children) == 0:
            self.add_node(self.root, 0)
        
    def add_node(self, parent, start_index):
        child = self.Node(start_index) 
        parent.children.append(child)
        
    def get_node_end(self, node):
            if node.self.end is None:
                return self.global_end
            else:
                return node.self.end
        
        
st2sa("mississippi")



