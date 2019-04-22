class Node:
    def __init__(self, key, values):
        self.key = key
        self.values = values

class Constraint:
    def __init__(self, node1, node2, constraint_type):
        self.node1 = node1
        self.node2 = node2
        self.constraint_type = constraint_type
    
    def print_constraint(self):
        print(self.node1.key, self.constraint_type, self.node2.key)
        
    def check_for_solution(self):
        # Check that both nodes are initialized
        if self.node1 is None or self.node2 is None:
            return False
        
        # Check that both domains aren't empty
        if len(self.node1.values) <= 0 or len(self.node2.values) <= 0:
            return False
        
        # TODO: Check that the a value in one domain matches the constraint relative to the other domain
        
        return True
    

class ConstraintNetwork:
    def __init__(self, nodes, constraints):
        self.nodes = nodes
        self.constraints = constraints
        self.adjacency_list = {}
        self.generate_adjacency_list()
        
    def get_nodes(self):
        return self.nodes
    
    def get_constraints(self):
        return self.constraints

    def generate_adjacency_list(self):
        for constraint in self.constraints:
            if (constraint.node1.key in self.adjacency_list):
                self.adjacency_list[constraint.node1.key].append(constraint)
            else:
                self.adjacency_list[constraint.node1.key] = [constraint]
            
            if (constraint.node2.key in self.adjacency_list):
                self.adjacency_list[constraint.node2.key].append(constraint)
            else:
                self.adjacency_list[constraint.node2.key] = [constraint]

    def print_adjacency_list(self):
        for node in self.adjacency_list:
            print('Node ' + node)
            for constraint in self.adjacency_list[node]:
                constraint.print_constraint()
            print('')


a = Node('A', [1,2,3,4])
b = Node('B', [1,2,3,4])
c = Node('C', [1,2,3,4])
d = Node('D', [1,2,3,4])
nodes = [a, b, c, d]

c1 = Constraint(a, b, '>')
c2 = Constraint(a, d, '<')
c3 = Constraint(a, c, '=')
c4 = Constraint(b, c, '<')
constraints = [c1, c2, c3, c4]

cn = ConstraintNetwork(nodes, constraints)
cn.print_adjacency_list()

for c in cn.get_constraints():
#    print(c.values)
    print(c.check_for_solution())