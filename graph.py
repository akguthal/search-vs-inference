import copy 

class Constraint:
    def __init__(self, node1, constraint_type, node2):
        self.node1 = node1
        self.constraint_type = constraint_type
        self.node2 = node2
    
    def print_constraint(self):
        print(self.node1, self.constraint_type, self.node2)
        
class ConstraintNetwork:
    """
        Constructor for the Constraint Network class - stores variables and generates an adjacency list.

        Args:
            nodes (dict(str => list(int))): Mapping of node keys (str) to domains (int list)
            constraints (list(int)): List of type Constraint
    """
    def __init__(self, nodes, constraints):
        self.nodes = nodes
        self.constraints = constraints
        self.adjacency_list = {}
        self.generate_adjacency_list()
        
    def get_nodes(self):
        return self.nodes
    
    def get_constraints(self):
        return self.constraints

    """
        Generates an adjacency list from the list of constraints.
    """
    def generate_adjacency_list(self):
        for constraint in self.constraints:
            if (constraint.node1 in self.adjacency_list):
                self.adjacency_list[constraint.node1].append(constraint)
            else:
                self.adjacency_list[constraint.node1] = [constraint]
            
            if (constraint.node2 in self.adjacency_list):
                self.adjacency_list[constraint.node2].append(constraint)
            else:
                self.adjacency_list[constraint.node2] = [constraint]

    """
        Prints the adjacency list in a readable format.
    """
    def print_adjacency_list(self):
        for node in self.adjacency_list:
            print('Node ' + node)
            for constraint in self.adjacency_list[node]:
                constraint.print_constraint()
            print('')

    """
        Function to initialize and run the search algorithm.
    """
    def search(self):
        unassigned = self.nodes.keys() # Should this be self.nodes.keys()?
        unassigned.sort(key=lambda x : len(self.nodes[x])) #sort nodes from smallest to largest domain
        self.solutions = [] #store solutions in class
        self.nodes_expanded = 0 #store expanded nodes in class
        self.run_search({}, unassigned) #run search with an empty set for known
        return (self.solutions, self.nodes_expanded)
    

    """
        A recursive (helper) function to run naive backtracking search on the given problem domain.

        Args:
            known (dict (str => int)): A mapping of nodes (str) to assigned values (int)
            unassigned (list(str)): A list of nodes that haven't been checked yet
    """
    def run_search(self, known, unassigned):
        if (len(unassigned) == 0): # This is a solution - all nodes have been assigned a value
            self.solutions.append(known) # Add it to our list of solutions
            return

        node = unassigned.pop(0) 
        domain = self.nodes[node]
        for val in domain:
            if (self.check_validity(known, node, val)): # run validity check on this value in the node's domain
                new_known = copy.deepcopy(known)
                new_known[node] = val
                branch = self.run_search(new_known, copy.deepcopy(unassigned)) # add this node => val to the known set, and go deeper
                self.nodes_expanded = self.nodes_expanded + 1 
        

    """
        Function to check if a given variable assignment would work with the remaining assignments.

        Args:
            known (dict (str => int)):  A mapping of nodes (str) to assigned values (int).
            node (str): The node that we want to assign to.
            val (int): The value that we want to assign.
    """
    def check_validity(self, known, node, val):
        constraints = self.adjacency_list[node] # Grab the contraints that pertain to this node
        for cons in constraints: 
            n1 = cons.node1 
            n2 = cons.node2
            rule = cons.constraint_type
            n1val = None
            n2val = None

            # First, check if either variable in this constraint is simply a number
            if isinstance(n1, int):
                n1val = n1
            if isinstance(n2, int):
                n2val = n2

            # Assign values to the nodes so we can check if the constraint is satisfied
            if n1 == node: 
                n1val = val
                if n2 in known:
                    n2val = known[n2]
            elif n2 ==  node:
                n2val = val
                if n1 in known:
                    n1val = known[n1]
            
            # There is a known value for both nodes in the constraint
            if (n1val is not None) and (n2val is not None):
                if rule == '>' and (n1val > n2val):
                    continue
                if rule == '<' and (n1val < n2val):
                    continue
                if rule == '<=' and (n1val <= n2val):
                    continue
                if rule == '>=' and (n1val >= n2val):
                    continue                    
                if rule == '=' and (n1val == n2val):
                    continue
                if rule == '!=' and (n1val != n2val):
                    continue
                
                return False # None of the above statements are true, so the constraint is broken
        
        return True # All constraints in the list are still valid
    
    def isAC(self, n1val, rule, n2val):
        if rule == '>' and (n1val > n2val):
            print("\t\ttrue")
            return True
        if rule == '<' and (n1val < n2val):
            print("\t\ttrue")
            return True
        if rule == '<=' and (n1val <= n2val):
            print("\t\ttrue")
            return True
        if rule == '>=' and (n1val >= n2val):
            print("\t\ttrue")
            return True
        if rule == '=' and (n1val == n2val):
            print("\t\ttrue")
            return True
        if rule == '!=' and (n1val != n2val):
            print("\t\ttrue")
            return True
        print("\t\tfalse")
        return False
    
    def reverse_constraint_type(self, rule):
        if rule == '>':
            return '<'
        if rule == '<':
            return '>'
        if rule == '<=':
            return '>='
        if rule == '>=':
            return '<='
        if rule == '=':
            return '!='
        if rule == '!=':
            return '='
        
    def make_arc_consistent(self, ratio):
        somethingChanged = True
        queue = self.constraints
        while somethingChanged:
            somethingChanged = False
            for con in queue:
                n1 = con.node1
                n2 = con.node2
                n1Domain = self.nodes[n1]
                n2Domain = self.nodes[n2]
                operation = con.constraint_type
                for n1TestVal in n1Domain:
                    n1Val_AC_n2Val = False
                    for n2TestVal in n2Domain:
                        print("Testing " + str(n1TestVal) + operation + str(n2TestVal))
                        if self.isAC(n1TestVal, operation, n2TestVal):
                            n1Val_AC_n2Val = True
                    if not n1Val_AC_n2Val:
                        print("Removing " + str(n1TestVal) + " from " + n1)
                        n1Domain.remove(n1TestVal)
                        somethingChanged = True
                    else:
                        print("Keeping " + str(n1TestVal) + " in " + n1)
                        
                n1 = con.node2
                n2 = con.node1
                n1Domain = self.nodes[n1]
                n2Domain = self.nodes[n2]
                operation = self.reverse_constraint_type(con.constraint_type)
                for n1TestVal in n1Domain:
                    n1Val_AC_n2Val = False
                    for n2TestVal in n2Domain:
                        print("Testing " + str(n1TestVal) + operation + str(n2TestVal))
                        if self.isAC(n1TestVal, operation, n2TestVal):
                            n1Val_AC_n2Val = True
                    if not n1Val_AC_n2Val:
                        print("Removing " + str(n1TestVal) + " from " + n1)
                        n1Domain.remove(n1TestVal)
                        somethingChanged = True
                    else:
                        print("Keeping " + str(n1TestVal) + " in " + n1)

nodess = {}
nodess['A'] = [1,2,3,4]
nodess['B'] = [1,2,3,4]
nodess['C'] = [1,2,3,4]
nodess['D'] = [1,2,3,4]

# Binary constraints
c1 = Constraint('A', '>', 'B')
c2 = Constraint('C', '>', 'B')
c3 = Constraint('A', '=', 'C')
c4 = Constraint('A', '<', 'D')

# Example single constraint
#c5 = Constraint('A', '=', 3)

constraints = [c1, c2, c3, c4]

cn = ConstraintNetwork(nodess, constraints)
#print(cn.search())
#cn.print_adjacency_list()

### AC Test ###
cn.make_arc_consistent(1.0)