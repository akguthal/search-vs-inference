def generate_problem(problem_name, grid_size):
    f = open("problems/"+problem_name+".csv", "w+")
    f.write("Nodes\n")

    constraints = []
    
    for i in range(grid_size):
        for j in range(grid_size):

            this_spot = str(i)+"-"+str(j)
            line = this_spot+","
            line = line + ','.join(map(str, range(1, grid_size+1)))
            f.write(line+"\n")
                
            for s in range(i+1, grid_size):
                constrained_with = str(s)+"-"+str(j)
                constraints.append(this_spot+",!=,"+constrained_with)
            
            for t in range(j+1, grid_size):
                constrained_with = str(i)+"-"+str(t)
                constraints.append(this_spot+",!=,"+constrained_with)
    
    f.write("Constraints\n")
    for c in constraints:
        f.write(c+"\n")
            
    f.close()

generate_problem("test", 4)
