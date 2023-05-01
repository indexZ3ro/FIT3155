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
                    # NOTE: J = the tree up until the active node!
                    # TODO: Change this so that we compare the next character (i+1) to the [active_node index + the remainder length] 
                    # TODO: if we dont have an active edge iterate children and find if we have an active edge otherwise we can simply use the active edge
                    #       if we have no match we need to add 
                    # psudo code = 
                       # if remainder exists: compare [remainder_index + remainder_len], [i+1]
                       # else:
                    for node in self.active_node.children:
                        # compare [child.start], [i+1]
                    
                        if node_str == compare_str:
                            match = True
                    
                    #rule(3)  
                    if match:
                        rule3()
                    #rule 2: uses j to create the start index of new node && update last j
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



