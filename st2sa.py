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
        
    def build(self, input_list):
        n = len(input_list)
        for i in range(n-1):
            self.global_end += 1
            if i == 0:
                self.add_node(self.active_node, 0)
            else:
                for j in range(self.last_j, i+2):
                    match = False
                    
                    if self.remainder_index is None:
                        compare_str = [input_list[j]]
                    else:
                        compare_str = input_list[self.remainder_index: self.remainder_length] + [input_list[j]]
                    
                    
                    for node in self.active_node.children:
                        node_str = input_list[node.start:self.remainder_length+1]
                    
                        if node_str == compare_str:
                            match = True
                    
                    #rule(3)  
                    if match:
                        rule3()
                    #rule 2
                    else:
                        rule2()
            
        
    def add_node(self, parent, start_index):
        child = self.Node(start_index) 
        parent.children.append(child)
        
    def get_node_end(self, node):
            if node.end is None:
                return self.global_end
            else:
                return node.self.end
        
        
st2sa("mississippi")



