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
            self.sufLink = self
        
        
    def __init__(self):
        self.root = self.Node(None)
        self.active_node = self.root
        self.remainder = None
        self.last_j = 0
        self.global_end = 0
        
    def build(self, input_list):
        n = len(input_list)
        for i in range(n-1):
            self.global_end += 1
            if i == 0:
                self.add_node(self.active_node, 0)
            else:
                for j in range(self.last_j, i+2):
                    self.active_node.children
                    
                    self.active_node.children.append(self.Node(j))
                    self.last_j += 1
                    self.active_node = self.active_node.sufLink
                    self.remainder -= 1
            
        
    def add_node(self, parent, start_index):
        child = self.Node(start_index) 
        parent.children.append(child)
        
    def get_node_end(self, node):
            if node.end is None:
                return self.global_end
            else:
                return node.self.end
        
        
st2sa("mississippi")



