import random
import matplotlib.pyplot as plt
import numpy as np

# Apply swarm intelligence algorithm in knapsack problems
# https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/knapsack_01.html for the
# following task: P01, P02, P06, P07, P08.

def fncMax(particle):
    actual_weight=0
    actual_costs=0
    for i in range(len(particle)):
        actual_weight=actual_weight+np.sum(weightsKg[i]*particle[i])
    if actual_weight>capacityKg:
        fitness=0
    else:
        for i in range(len(particle)):
            actual_costs=actual_costs+np.sum(profits[i]*particle[i])
        fitness=actual_costs
    return fitness

class Particle:
    def __init__(self, initialValues):
        self.position = []      
        self.speed = []           
        self.positionBest = []        
        self.approachBest = -1 
        self.approach = -1     

        for i in range(particleNumber):
            self.speed.append(random.uniform(-1, 1))
            self.position.append(initialValues[i])

    def calculate_fitness(self, function):
        self.approach = function(self.position)
        # Check if your current position is your individual best
        if self.approach > self.approachBest or self.approachBest == -1:
            self.positionBest = self.position
            self.approachBest = self.approach

    # Update particle velocity
    def update_speed(self, group_max_position):
        Inertia = 0.9    # The coefficient of the particle's desire to maintain its previous velocity.
        Individuality = 2   # The coefficient of willingness to protect one's own best.
        Sociality = 2  # The coefficient of willingness to take the best value of the herd.
        for i in range(particleNumber):
            r1 = random.random()
            r2 = random.random()
            cognitive_speed = Individuality * r1 * (self.positionBest[i] - self.position[i])
            social_speed = Sociality * r2 * (group_max_position[i] - self.position[i])
            self.speed[i] = Inertia * self.speed[i] + cognitive_speed + social_speed

    # Calculating new positions according to the newly updated particle velocity
    def update_position(self):
        for i in range(particleNumber):              
            if self.speed[i] < -1:
                self.speed[i] = -1
            elif self.speed[i] > 1:
                self.speed[i] = 1
            self.position[i] = self.position[i] + self.speed[i]
            if self.position[i] > 1:      # If the position is above the upper limit value, pull to the upper limit value
                self.position[i] = 1
            elif self.position[i] < 0:    # If the position is below the lower limit value, check to the lower limit value
                self.position[i] = 0
            else:
                self.position[i] = round(self.position[i])

class PSO:
    stepProfit = []
    stepWeightInKg = []
    groupMaxPosition = []
    groupMaxApproach = -1
  
    def __init__(self, function, initialValues, numberOfObjects, numberOfParticles, numberOfIterations):

        global particleNumber, optimal_profit

        particleNumber = len(initialValues)
        self.groupMaxApproach = -1  # The best approach for the group
        self.groupMaxPosition = []  # Best position for the group
        dimensions = []
        self.stepProfit=[]
        self.stepWeightInKg=[]
        for i in range(numberOfParticles):
            dimensions.append(Particle(initialValues))
        counter = 0
        while counter < numberOfIterations:
            counter += 1
            # Calculating the fitness of the swarm particles to the function.
            for j in range(numberOfParticles):
                dimensions[j].calculate_fitness(function)
                # Checking that the current particle is the global best and making the necessary updates
                if dimensions[j].approach > self.groupMaxApproach or self.groupMaxApproach == -1:
                    self.groupMaxPosition = list(dimensions[j].position)
                    self.groupMaxApproach = float(dimensions[j].approach)
            # Updating speed and positions in the swarm
            for j in range(numberOfParticles):
                dimensions[j].update_speed(self.groupMaxPosition)
                dimensions[j].update_position()
            totalProfit = 0
            totalWeightInKg = 0
            for i in range(numberOfObjects):
                totalProfit += self.groupMaxPosition[i] * profits[i]
                totalWeightInKg += self.groupMaxPosition[i] * weightsKg[i]
            print(totalWeightInKg, capacityKg) 
            print(totalProfit, optimal_profit)
            if totalWeightInKg<=capacityKg:               
                self.stepProfit.append(totalProfit)
                self.stepWeightInKg.append(totalWeightInKg)
            elif counter != 1:
                self.stepProfit.append(self.stepProfit[counter-1])
                self.stepWeightInKg.append(self.stepWeightInKg[counter-1])
            else:
                self.stepProfit.append(0)
                self.stepWeightInKg.append(0)
            if totalProfit==optimal_profit and totalWeightInKg<=capacityKg:
                break

    # Printing the results...
    def CalculateResults(self):
        totalProfit = 0
        totalWeightInKg = 0 
        for i in range(len(self.groupMaxPosition)):
            totalProfit += self.groupMaxPosition[i] * profits[i]
            totalWeightInKg += self.groupMaxPosition[i] * weightsKg[i]
        return totalProfit, totalWeightInKg

capacityKg=0
weightsKg=[]
profits=[]
solution=[]
optimal_profit=0

def resetInitialValues():
    global initialValues
    initialValues=[]
    for i in range(len(weightsKg)):
        initialValues.append(random.randint(0,1))

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

def checkSolution(optimalSolution, algorithmSolution):
    print(optimalSolution)
    print(algorithmSolution)
    totalProfit=0
    totalProfitOptimal=0
    for i in range(len(optimalSolution)):
        totalProfit+=algorithmSolution[i]*profits[i]
        totalProfitOptimal+=optimalSolution[i]*profits[i]
    
    if(totalProfit!=totalProfitOptimal):
        print('Solution is not optimal\n')
        print('Profit Generated in optimal:', totalProfitOptimal)
        return totalProfit
    print("Solution is optimal")
    return totalProfit

def calculateProfit(solution):
    totalProfit=0    
    for i in range(len(solution)):
        totalProfit+=solution[i]*profits[i]
    return totalProfit

for i in range(8):
    if i<0 or i>5:
        continue
    print("\n"+"PROBLEM #"+str(i+1))
    capacity_file_name="datasets\\p0"+str(i+1)+"_c.txt"
    weights_file_name="datasets\\p0"+str(i+1)+"_w.txt"
    profits_file_name="datasets\\p0"+str(i+1)+"_p.txt"
    solutions_file_name="datasets\\p0"+str(i+1)+"_s.txt"    
    readVariablesFromFiles(capacity_file_name, weights_file_name, profits_file_name, solutions_file_name)
    optimal_profit=calculateProfit(solution)
    resetInitialValues()
    pso = PSO(fncMax, initialValues, numberOfObjects=len(weightsKg), numberOfParticles=500, numberOfIterations=10)
    bestProfit, bestWeight= pso.CalculateResults()
    best_solution=pso.groupMaxPosition
    checkSolution(solution, best_solution)

    print(pso.stepProfit)
    print(pso.stepWeightInKg)

    plt.figure()
    plt.plot(pso.stepProfit)
    plt.axhline(y=optimal_profit, color='r')
    plt.title('Problem '+str(i+1)+' Solution - Profit')
    plt.xlabel("Generation")
    plt.ylabel("Profit")
    plt.ticklabel_format(style='plain')
    plt.savefig('Problem_'+str(i+1)+'_Profit.png')

    plt.figure()
    plt.plot(pso.stepWeightInKg)
    plt.axhline(y=capacityKg, color='r')
    plt.title('Problem '+str(i+1)+' Solution - Weight')
    plt.xlabel("Iteration")
    plt.ylabel("Weight")
    plt.ticklabel_format(style='plain')
    plt.savefig('Problem_'+str(i+1)+'_Weight.png')
    
    print("Overall best candidate: {},with score of: {}".format(bestProfit,best_solution))    

