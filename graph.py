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
    def __init__(self, filename):

        self.nodes = {}
        self.constraints = []
        self.adjacency_list = {}

        f = open("problems/"+filename, "r")
        reading = "nodes"
        for line in f:
            tokens = filter(lambda x : (x != '' and x != '\n'), line.split(','))
            tokens = [x.replace("\n", "") for x in tokens]            

            if (tokens[0] == "Nodes"):
                reading = "nodes"
                
            elif (tokens[0] == "Constraints"):
                reading = "constraints"

            elif (reading == "nodes"):
                node = tokens[0]
                domain = [float(i) for i in tokens[1:]]
                self.nodes[node] = domain

            elif (reading == "constraints"):
                n1 = tokens[0]
                constraint_type = tokens[1]
                n2 = tokens[2]
                if (self.is_number(n1)):
                    n1 = float(n1)
                if (self.is_number(n2)):
                    n2 = float(n2)
                constraint = Constraint(n1, constraint_type, n2)
                self.constraints.append(constraint)            

        self.generate_adjacency_list()
        
    def get_nodes(self):
        return self.nodes
    
    def get_constraints(self):
        return self.constraints

    def get_num_values(self):
        total_values = 0
        for n in self.nodes.keys():
            total_values = total_values + len(self.nodes[n])
        return total_values

    """
        Generates an adjacency list from the list of constraints.
    """
    def generate_adjacency_list(self):
        for constraint in self.constraints:
            if (constraint.node1 in self.adjacency_list):
                self.adjacency_list[constraint.node1].append(constraint)
            elif (not isinstance(constraint.node1, float)):
                self.adjacency_list[constraint.node1] = [constraint]
            
            if (constraint.node2 in self.adjacency_list):
                self.adjacency_list[constraint.node2].append(constraint)
            elif (not isinstance(constraint.node2, float)):
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

        Args:
            all_solutions (bool): Determines whether to return all solutions, or first one. By default, it returns all solutions.
    """
    def search(self, all_solutions = True):
        unassigned = self.nodes.keys() # Should this be self.nodes.keys()?
        unassigned.sort(key=lambda x : len(self.nodes[x])) #sort nodes from smallest to largest domain
        self.solutions = [] #store solutions in class
        self.nodes_expanded = 0 #store expanded nodes in class
        self.run_search({}, unassigned, all_solutions) #run search with an empty set for known
        return (self.solutions, self.nodes_expanded)
    

    """
        A recursive (helper) function to run naive backtracking search on the given problem domain.

        Args:
            known (dict (str => int)): A mapping of nodes (str) to assigned values (int)
            unassigned (list(str)): A list of nodes that haven't been checked yet
    """
    def run_search(self, known, unassigned, all_solutions):
        if (len(unassigned) == 0): # This is a solution - all nodes have been assigned a value
            self.solutions.append(known) # Add it to our list of solutions
            return 1

        node = unassigned.pop(0) 
        domain = self.nodes[node]
        for val in domain:
            if (self.check_validity(known, node, val)): # run validity check on this value in the node's domain
                new_known = copy.deepcopy(known)
                new_known[node] = val
                branch = self.run_search(new_known, copy.deepcopy(unassigned), all_solutions) # add this node => val to the known set, and go deeper
                self.nodes_expanded = self.nodes_expanded + 1 
                if (not(all_solutions)) and (branch == 1):
                    return 1
        

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
            if isinstance(n1, float):
                n1val = n1
            if isinstance(n2, float):
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
                if (not self.consistent(n1val, n2val, rule)):
                    return False                
                        
        return True # All constraints in the list are still valid
    
    def consistent(self, n1val, n2val, rule):
        valid = False

        if rule == '>' and (n1val > n2val):
            valid = True
        if rule == '<' and (n1val < n2val):
            valid = True
        if rule == '<=' and (n1val <= n2val):
            valid = True
        if rule == '>=' and (n1val >= n2val):
            valid = True                    
        if rule == '=' and (n1val == n2val):
            valid = True
        if rule == '!=' and (n1val != n2val):
            valid = True   

        return valid     

    def arc_consistency(self, ratio):
        changed = 1
        
        self.arc_total_values = (self.get_num_values() - len(self.nodes.keys())) * ratio
        self.arc_checked_values = 0

        if (self.arc_total_values < 1):
            return 

        while (changed == 1):
            changed = 0
            for node in self.adjacency_list.keys():
                constraints = self.adjacency_list[node]
                check_node = self.trim_domain(node, constraints)
                if (check_node == -1):
                    return
                changed = check_node or (changed == 1)
            


    def trim_domain(self, node, constraints):
        domain = self.nodes[node]
        new_domain = copy.deepcopy(domain)
        trimmed = 0
        for cons in constraints:
            for val_to_check in new_domain:
                if (val_to_check not in domain):
                    continue
                
                if node == cons.node1:
                    n1val = val_to_check
                    other = "node2"
                else:
                    n2val = val_to_check
                    other = "node1"
                
                if isinstance(getattr(cons, other), float):
                    other_domain = [getattr(cons, other)]
                else:
                    other_domain = self.nodes[getattr(cons, other)]

                valid_other_value = False

                for other_val in other_domain:
                    if (other == "node1"):
                        n1val = other_val
                    else:
                        n2val = other_val
                        
                    valid_other_value = valid_other_value or self.consistent(n1val, n2val, cons.constraint_type)

                if (not valid_other_value):
                    self.nodes[node].remove(val_to_check)
                    self.arc_checked_values = self.arc_checked_values + 1
                    if (self.arc_checked_values >= self.arc_total_values):
                        return -1
                    trimmed = 1        
        return trimmed

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

cn = ConstraintNetwork("test.csv")
print("Number of values before AC: ", cn.get_num_values())
print("Running AC")
cn.arc_consistency(1)
print("Nodes in CSP: ", cn.nodes)
print("Number of values after AC: ", cn.get_num_values())
results = cn.search(False)
print("First solution:", results[0][0])
print("Number of results: ", len(results[0]))
print("Nodes expanded: ", results[1])

# import time
# import numpy as np

# allMinTimes = []
# allMinRatios = []
# for linspaceSpacing in np.linspace(1, 50, 50):
#     print("Linspace Spacing: " + str(int(linspaceSpacing)))
#     allRatios = np.linspace(0.0, 1.0, int(linspaceSpacing))
#     allTimes = []
    
#     print("All ratios: " + str(allRatios))
    
#     for ratio in allRatios:
#         totalTime = 0.0
#         nTrials = 1000
#         for i in range(nTrials):
#             cn = ConstraintNetwork("sudoku.csv")
            
#             start = time.time()
#             cn.arc_consistency(ratio)
#             results = cn.search()
#             end = time.time()
            
#             totalTime += (end - start)
#         print("Ratio: " + str(ratio) + "\tTime taken: " + str(totalTime/float(nTrials)))
#         allTimes.append(totalTime/float(nTrials))
    
#     import matplotlib.pyplot as plt
#     minIdx = np.argmin(allTimes)
#     print("Min ratio: " + str(allRatios[minIdx]))
#     print("Min time: " + str(allTimes[minIdx]))
    
#     allMinRatios.append(allRatios[minIdx])
#     allMinTimes.append(allTimes[minIdx])
    
#     plt.figure(1)
#     plt.plot(allRatios, allTimes)
#     plt.axis([0.0, 1.0, 0.0, 0.006])
#     plt.title(str(int(linspaceSpacing)) + " Spacings between Ratio Values of 0.0 and 1.0")
#     plt.xlabel("Ratio")
#     plt.ylabel("Average time (sec)")
#     plt.savefig("graph" + str(int(linspaceSpacing)) + ".png", dpi=800, bbox_inches="tight", pad_inches=0)
#     plt.close()
    
#     plt.figure(2)
#     plt.plot(allRatios, allTimes)
#     plt.axis([0.0, 1.0, 0.0, 0.006])
#     plt.title("All Spacings")
#     plt.xlabel("Ratio")
#     plt.ylabel("Average time (sec)")
#     plt.savefig("graphAll.png", dpi=800, bbox_inches="tight", pad_inches=0)
#     plt.close()
    
#     np.savetxt("allMinRatios.txt")
#     np.savetxt("allMinTimes.txt")