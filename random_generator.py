from random import randint

def generate_problem(problem_name, problem_size):
    f = open("problems/"+problem_name+".csv", "w+")
    f.write("Nodes\n")

    nodes = {}
    constraints = []

    for i in range(problem_size):
        node_name = "node"+str(i)
        node_val = randint(0, problem_size)
        nodes[node_name] = node_val #assigned actual value for the node

        line = node_name+","+','.join(map(str, range(0, problem_size+1))) #write node and domain to the file
        f.write(line+"\n")

        for existing_node in nodes.keys(): #constrain the node we're adding with all the other exsting nodes
            constraint_type = '!='
            existing_node_val = nodes[existing_node]
            if (node_val == existing_node_val):
                constraint_type = '='
            elif (node_val < existing_node_val):
                constraint_type = '<'
            else:
                constraint_type = '>'
            constraints.append(node_name + ',' + constraint_type + ',' + existing_node) #add constraint into our master list
    
    f.write("Constraints\n")
    for c in constraints: #finally, write all of our constraints
        f.write(c+"\n")
            
    f.close()

generate_problem("random_prob", 50)
