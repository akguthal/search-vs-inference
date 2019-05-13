import random

def generate_problem(problem_name, grid_size):
    f = open("problems/"+problem_name+".csv", "w+")
    f.write("Nodes\n")

    constraints = []
    
    for i in range(grid_size):
        for j in range(grid_size):

            choose_random = (random.randint(0,int(grid_size*2)) == 0)
            if choose_random:
                domain = str(random.randint(1, grid_size+1))
            else:
                domain = ','.join(map(str, range(1, grid_size+1)))

            this_spot = str(i)+"-"+str(j)
            line = this_spot+","
            line = line + domain
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
