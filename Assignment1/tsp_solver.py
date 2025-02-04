import sys
import csv
from random import shuffle, choice, randint

#euclidean distance between two coordinates
def calculate_euclidean_distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

#function to calculate the total euclidean distance between the cities in the order provided by nlist
def calculate_path_distance(nlist):
    path_distance = 0
    for i in range(1, len(nlist)):
        path_distance += adjacency_matrix[nlist[i]-1][nlist[i-1]-1]
    return path_distance

#create an adjacency matrix where adjacency_matrix[i][j] is the euclidean distance from city i+1 to city j+1
def calculate_adjacency_matrix(nodes):
    matrix = [[0 for _ in range(len(nodes))] for _ in range(len(nodes))]
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            matrix[i][j] = calculate_euclidean_distance(nodes[i][1], nodes[i][2], nodes[j][1], nodes[j][2])
    return matrix

#This function tries to find a neighbor based on randomly choosing one of the unexplored branches
def find_intelligent_neighbour(current_solution):
    branch = choice(branches) #choose a random unexplored branch
    index1 = randint(branch[0], branch[-1]) #random index between the range of the branch
    index2 = randint(branch[0], branch[-1]) #second random index to swap first one with
    while index2 == index1:
        index2 = randint(branch[0], branch[-1])
    if index1 > index2:
        index1, index2 = index2, index1    #just ensuring index2 is bigger to make it easier
    current_solution[index1], current_solution[index2] = current_solution[index2], current_solution[index1] #swap
    neighbor_distance = calculate_path_distance(current_solution) #calculate neighbor distance
    neighbor_solution = current_solution #neighbor solution is the swapped solution
    return (branch, index1, index2, neighbor_distance, neighbor_solution)  

def solve_tsp(nodes):
    i = 0
    global branches 
    shuffle(nodes)
    best_solution = current_solution = nodes
    current_distance = calculate_path_distance(current_solution)
    best_distance = calculate_path_distance(current_solution)
    while i < 10000:
        j = 0
        while j < 10: #Find first better neighbor solution 
            solution = find_intelligent_neighbour(current_solution)
            solution_distance = solution[3]
            if solution_distance < current_distance:
                #accept the first neighbor solution that is better like first ascent hill climbing
                neighbor_solution =  solution[4]
                #create all the branches that weren't explored
                index1 = solution[1]
                index2 = solution[2]
                branch = solution[0]
                border1 = branch[0]
                border2 = index1 - 2
                border3 = index1 + 2
                border4 = index2 - 2
                border5 = index2 + 2
                border6 = branch[-1]
                branches = [] 
                #when swapping two elements, we can get atmost 3 branches always. We eliminate ones less than 1 element as no swapping possible
                if border2-border1+1 >=2:
                    branches.append([border1, border2])
                if border4-border3+1 >=2:
                    branches.append([border3, border4])
                if border6-border5+1 >= 2:
                    branches.append([border5, border6])
                current_solution = neighbor_solution #adopt neighbor as it had lower distance 
                current_distance = solution_distance
                if best_distance > current_distance: #update best_distance
                    best_distance = current_distance
                    best_solution = current_solution
                if not branches: #if no branches can be made as we reach end of branch then random restart and try to find unexplored regions
                    shuffle(nodes)
                    current_solution = nodes
                    current_distance = calculate_path_distance(current_solution)
                    branches = [[0, len(nodes) - 1]]                                           
                break
            if j == 9: #no better neighbors found 
                #random restart
                shuffle(nodes)
                current_solution = nodes
                current_distance = calculate_path_distance(current_solution)
                branches = [[0, len(nodes) - 1]]
            j = j + 1
        i = i + 1
    return (best_solution, best_distance)
          
#read text file
def textfile_to_nodeslist(content):
    lines = []
    for line in content:
        lines.append(line.strip())
    nodes = []
    flag = False
    for line in lines:
        line = line.split(' ')
        temp = []
        if line[0].isdigit():
            for element in line:
                if element.isdigit():
                    temp.append(int(element))
            nodes.append(temp)
    return nodes

#open text file
with open(sys.argv[1], 'r') as file:
    content = file.readlines()

nodes = textfile_to_nodeslist(content)
adjacency_matrix = calculate_adjacency_matrix(nodes)
nodes = [x[0] for x in nodes] #cities
branches = [[0, len(nodes)-1]] #initially whole input is a branch
best_solution, best_distance = solve_tsp(nodes) #solve for tsp
print(best_distance)

#create csv
csv_file = "solution.csv"
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(best_solution)


