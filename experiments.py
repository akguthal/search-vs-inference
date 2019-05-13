import time
import numpy as np
import random_generator as rg
import sudoku_generator as sg
import graph
import matplotlib.pyplot as plt

def plot(title, xlabel, xdata, ylabel, ydata, filename, plot_type="line"):
    """
    Plot a graph given data, labels and a filename.
    """
    colors = (0,0,0)
    plt.figure(1)
    if (plot_type == "scatter"):
        plt.scatter(xdata, ydata)
    else:
        plt.plot(xdata, ydata)
    plt.axis([0.0, max(xdata)+(max(xdata)*0.1), 0.0, max(ydata)+(max(ydata)*0.1)])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig("graphs/" + str(filename) + ".png", dpi=800, bbox_inches="tight", pad_inches=0.2)
    plt.close() 

def run_problem(problem_name, ratio, all_solutions):
    """
    Run a problem and get the (time, nodes_expanded) from it
    """
    cn = graph.ConstraintNetwork(problem_name+".csv")
    start = time.time()
    cn.arc_consistency(ratio)
    results = cn.search(all_solutions)
    end = time.time()
    run_time = (end - start)
    return (run_time, results[1], cn.arc_checked_values)

def ratio_nodes_expanded(problem_size, num_ratios=50, draw_plot=True, all_solutions=False):
    sg.generate_problem("ratio_nodes_expanded", problem_size)
    ratios = np.linspace(0,1,num_ratios, endpoint=False)
    nodes_expanded_list = []
    for r in ratios:
        print("Running for ratio {}".format(r))
        (_, expanded, _) = run_problem("ratio_nodes_expanded", r, all_solutions)
        nodes_expanded_list.append(expanded)

    if (draw_plot):
        plot("Search/Inference Ratio vs. Nodes Expanded for Problem Size="+str(problem_size), "Ratio", ratios, "Nodes Expanded", nodes_expanded_list, "ratio_nodes_expanded_" + str(problem_size))

def ratio_time(problem_size, trials_per_point, num_ratios=50, draw_plot=True, all_solutions=False):
    sg.generate_problem("ratio_one_problem", problem_size)
    ratios = np.linspace(0,1,num_ratios, endpoint=False)
    times = []
    for r in ratios:
        print("Running for ratio {}".format(r))
        comp_time = 0
        for i in range(trials_per_point):
            (time, _, _) = run_problem("ratio_one_problem", r, all_solutions)
            comp_time = comp_time + time
        times.append(comp_time/trials_per_point)

    if (draw_plot):
        plot("Search/Inference Ratio vs. Search Time for Problem Size="+str(int(problem_size)), "Ratio", ratios, \
        "Search Time", times, "ratio_time_" + str(int(problem_size)))
    


def optimal_ratio_problem_size(size_range, trials_per_point=20, num_ratios=50):
    optimal_ratios = []
    ratios = np.linspace(0,1,num_ratios,endpoint=False)

    for size in size_range:
        print("Running for problem size {}".format(size))
        problem = sg.generate_problem("optimal_ratio_prob_size", size)
        times = []
        expanded = []
        ac_removed = []
        for r in ratios:
            print(r)
            tot_time = 0
            tot_nodes_expanded = 0
            tot_checked_values = 0
            for i in range(trials_per_point):
                (time, nodes_expanded, arc_checked_values) = run_problem("optimal_ratio_prob_size", r, True)
                tot_time = tot_time + time
                tot_nodes_expanded = tot_nodes_expanded + nodes_expanded
                tot_checked_values = tot_checked_values + arc_checked_values
                
            times.append(float(tot_time)/float(trials_per_point))
            expanded.append(float(tot_nodes_expanded)/float(trials_per_point))
            ac_removed.append(float(tot_checked_values)/float(trials_per_point))
        
        print("OPTIMAL RATIO BY TIME: {}".format(ratios[np.argmin(times)]))
        print("OPTIMAL RATIO BY NODES EXPANDED: {}".format(ratios[np.argmin(expanded)]))
            
# optimal_ratio_problem_size(size_range=range(2, 9), trials_per_point=1)
ratio_nodes_expanded(5, all_solutions=True)
ratio_time(3, 20, all_solutions=True)
# print(run_problem("australia_gcp", 1))