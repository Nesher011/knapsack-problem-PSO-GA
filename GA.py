import numpy as np
import matplotlib.pyplot as plt
import random

def readVariablesFromFiles(capacityFileName, weightsFileName, profitsFileName, solutionFileName):
    global capacityKg, weightsKg, profits, solution
    with open(capacityFileName, "r") as file:
        capacityKg=int(file.read())
    with open(weightsFileName, "r") as file:
        weightsKg=[]
        readContent=file.read()
        for line in readContent.split() :
            weightsKg.append(int(line))
    with open(profitsFileName, "r") as file:
        profits=[]
        readContent=file.read()
        for line in readContent.split() :
            profits.append(int(line))
    with open(solutionFileName, "r") as file:
        solution=[]
        readContent=file.read()
        for line in readContent.split() :
            solution.append(int(line))

def tournament_selection(population, scores, k=3):
    selected=np.random.randint(0,len(population))
    for randomly_chosen in np.random.randint(0,len(population), k-1):
        if scores[randomly_chosen]>scores[selected]:
            selected=randomly_chosen
    return population[selected]

def crossover(parent_1, parent_2, rate_of_crossover):
    child_1=parent_1.copy()
    child_2=parent_2.copy()
    if np.random.rand()<rate_of_crossover:
        crossover_point=np.random.randint(1,len(child_1)-1)
        child_1=parent_1[:crossover_point]+parent_2[crossover_point:]
        child_2=parent_2[:crossover_point]+parent_1[crossover_point:]
    return [child_1, child_2]

def mutation(candidate):
    for i in range(len(candidate)):
        if np.random.rand()<rate_of_mutation:
            candidate[i]=1-candidate[i]
    return candidate

def create_new_gen(number_of_population, parents):
    children=[]
    for i in range(0, number_of_population, 2):
        parent_1=parents[i]
        parent_2=parents[i+1]
        for candidate in crossover(parent_1, parent_2, rate_of_crossover):
            candidate=mutation(candidate)
            children.append(candidate)
    return children

def fitness_function(weights, costs, weight_limit, chromosomes):
    actual_weight=0
    actual_costs=0
    for i in range(len(weights)):
        actual_weight=actual_weight+np.sum(weights[i]*chromosomes[i])
    if actual_weight>weight_limit:
        fitness=0
    else:
        for i in range(len(weights)):
            actual_costs=actual_costs+np.sum(costs[i]*chromosomes[i])
        fitness=actual_costs
    return fitness

def genetic_algorithm(number_of_bits, number_of_population, number_of_generations):
    population=list()
    for _ in range(number_of_population):
        candidate=np.random.randint(0,1, number_of_bits).tolist()
        population.append(candidate) 
    
    best_candidate=population[0]
    best_solution=fitness_function(weightsKg,profits,capacityKg,candidate)
    for generation in range(number_of_generations):
        scores=[fitness_function(weightsKg,profits,capacityKg,candidate) for candidate in population]
        for i in range(number_of_population):
            if scores[i]>best_solution:
                best_candidate=population[i]
                best_solution=scores[i]
        parents=[tournament_selection(population, scores) for _ in range(number_of_population)]
        population=create_new_gen(number_of_population, parents)
    return best_candidate, best_solution


def checkSolution(optimalSolution, algorithmSolution):
    print(optimalSolution)
    print(algorithmSolution)
    for i in range(len(optimalSolution)):
        if(optimalSolution[i]!=algorithmSolution[i]):
            print('Solution is not optimal\n')
            print(optimalSolution)
            totalProfit = 0
            totalWeightInKg = 0        
        
            for i in range(len(optimalSolution)):
                totalProfit += optimalSolution[i] * profits[i]
                totalWeightInKg += optimalSolution[i] * weightsKg[i]
            print('Profit Generated in optimal:', totalProfit, '\nWeight in kg in optimal:', totalWeightInKg)
            return
    print("Solution is optimal")

def resetInitialValues():
    global initialValues
    initialValues=[]
    for i in range(len(weightsKg)):
        initialValues.append(random.randint(0,1))

capacityKg=0
weightsKg=[]
profits=[]
solution=[]

number_of_population=100
number_of_generations=1000
rate_of_crossover=0.9

for i in range(8):
    print("\n"+"PROBLEM #"+str(i+1))
    capacity_file_name="datasets\\p0"+str(i+1)+"_c.txt"
    weights_file_name="datasets\\p0"+str(i+1)+"_w.txt"
    profits_file_name="datasets\\p0"+str(i+1)+"_p.txt"
    solutions_file_name="datasets\\p0"+str(i+1)+"_s.txt"
    
    readVariablesFromFiles(capacity_file_name, weights_file_name, profits_file_name, solutions_file_name)
    number_of_bits=len(profits)
    rate_of_mutation=1/(number_of_bits)
    resetInitialValues()
    best_candidate,best_solution=genetic_algorithm(number_of_bits,number_of_population,number_of_generations)
    checkSolution(solution, best_candidate)
    print("Overall best candidate: {},with score of: {}".format(best_candidate,best_solution))
