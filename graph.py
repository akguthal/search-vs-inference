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
            # Can this be replaced with self.isAC(n1val, rule, n2val) somehow?
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
            return True
        if rule == '<' and (n1val < n2val):
            return True
        if rule == '<=' and (n1val <= n2val):
            return True
        if rule == '>=' and (n1val >= n2val):
            return True
        if rule == '=' and (n1val == n2val):
            return True
        if rule == '!=' and (n1val != n2val):
            return True
        return False
    
    # Used to flip constraints around, e.g. A > B becomes B < A
    # Allows iteration through constraints to check both related nodes
    def flip_constraint_type(self, rule):
        if rule == '>':
            return '<'
        if rule == '<':
            return '>'
        if rule == '<=':
            return '>='
        if rule == '>=':
            return '<='
        if rule == '=':
            return '='
        if rule == '!=':
            return '!='
        
    # Tests each value in n1's domain for arc consistency with n2's domain
    # n1's domain is changed, while n2's domain remains the same.
    # 'operation' refers to the constraint type/rule/whatever you want to call it.
    def test_for_arc_consistency(self, n1, n2, n1Domain, n2Domain, operation):
        # Keep a flag to see if anything has changed
        somethingChanged = False
        
        # Looping through each value in domain 1
        for n1TestVal in n1Domain:
            # Initializing a temporary variable to remember if this test value is arc-consistent with n2
            n1Val_AC_n2Val = False
            
            # Looping through values in domain 2
            for n2TestVal in n2Domain:
                # If the value is arc-consistent
                if self.isAC(n1TestVal, operation, n2TestVal):
                    n1Val_AC_n2Val = True # Set the flag to true
            
            # If the flag has not been set to true, it must not be arc-consistent with domain 2
            if not n1Val_AC_n2Val:
                # Remove the value
                n1Domain.remove(n1TestVal)
                somethingChanged = True # And since you removed something, something has changed
        
        # Domain 1 has been changed so it is arc-consistent with domain 2.                
        # Return the flag that something has changed
        return somethingChanged 
        
    # Will probably be renamed to "AC1" or have a switch for which AC algorithm to use
    # Makes itself (the constraint network) arc-consistent
    # 'ratio' will be used later to interpolate between search and inference
    def make_arc_consistent(self, ratio):
        # Flag to see if something has changed (for AC-1)
        somethingChanged = True
        
        # Keep looping as long as something is changing
        while somethingChanged:
            somethingChanged = False # Assume nothing has changed
            
            # Loop over all of the constraints in the network
            for con in self.constraints:
                # Setting node 1 and 2 for each constraint
                n1 = con.node1
                n2 = con.node2
                n1Domain = self.nodes[n1]
                n2Domain = self.nodes[n2]
                operation = con.constraint_type
                
                # Make domain 1 arc-consistent and remember if something has changed
                somethingChanged1 = self.test_for_arc_consistency(n1, n2, n1Domain, n2Domain, operation)
                
                # Make domain 2 arc-consistentand remember if something has changed
                operation = self.flip_constraint_type(con.constraint_type) # Flipping the operation around
                somethingChanged2 = self.test_for_arc_consistency(n2, n1, n2Domain, n1Domain, operation)
            
            # Check if something has changed in either domain
            somethingChanged = somethingChanged1 or somethingChanged2
        
# nodess['VariableName'] = [List, of, domain, values]
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
constraints = [c1, c2, c3, c4]

# Example single constraint
#c5 = Constraint('A', '=', 3)
#constraints = [c1, c2, c3, c4, c5]

cn = ConstraintNetwork(nodess, constraints)
#print(cn.search())
#cn.print_adjacency_list()

### AC Test ###
cn.make_arc_consistent(1.0)