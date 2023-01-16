import random

# Apply swarm intelligence algorithm in knapsack problems
# https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/knapsack_01.html for the
# following task: P01, P02, P06, P07, P08.

def fncMax(particle):
    value = fncParticleProfit(particle)
    return value + fncParticleKilogram(particle, value)

def fncParticleProfit(particle):
    total = 0
    for i in range(len(particle)):
        total += particle[i] * profits[i]
    return total

def fncParticleKilogram(particle, resettingElement):
    total = 0
    for i in range(len(particle)):
        total += particle[i] * weightsKg[i]
    if total <= capacityKg:
        if total <= resettingElement:
            return resettingElement - total
        else:
            return 0
    else:
        return -resettingElement

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
        Inertia = 0.99    # The coefficient of the particle's desire to maintain its previous velocity.
        Individuality = 1.99   # The coefficient of willingness to protect one's own best.
        Sociality = 1.99   # The coefficient of willingness to take the best value of the herd.
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
    stepProfit, stepWeightInKg, groupMaxPosition, groupMaxApproach = [], [], [], -1

    def __init__(self, function, initialValues, numberOfParticles, numberOfDimensions, numberOfIterations, printSteps = True):

        global particleNumber

        particleNumber = len(initialValues)
        self.groupMaxApproach = -1  # The best approach for the group
        self.groupMaxPosition = []  # Best position for the group
        dimensions = []
        for i in range(numberOfDimensions):
            dimensions.append(Particle(initialValues))
        counter = 0
        while counter < numberOfIterations:
            counter += 1
            # Calculating the fitness of the swarm particles to the function.
            for j in range(numberOfDimensions):
                dimensions[j].calculate_fitness(function)
                # Checking that the current particle is the global best and making the necessary updates
                if dimensions[j].approach > self.groupMaxApproach or self.groupMaxApproach == -1:
                    self.groupMaxPosition = list(dimensions[j].position)
                    self.groupMaxApproach = float(dimensions[j].approach)
            # Updating speed and positions in the swarm
            for j in range(numberOfDimensions):
                dimensions[j].update_speed(self.groupMaxPosition)
                dimensions[j].update_position()
            totalProfit = 0
            totalWeightInKg = 0
            for i in range(numberOfParticles):
                totalProfit += self.groupMaxPosition[i] * profits[i]
                totalWeightInKg += self.groupMaxPosition[i] * weightsKg[i]
            self.stepProfit.append(totalProfit)
            self.stepWeightInKg.append(totalWeightInKg)
            if printSteps:
                print(self.groupMaxPosition)

    # Printing the results...
    def PrintResults(self):
        print('\nRESULTS:\n')
        totalProfit = 0
        totalWeightInKg = 0        
        print(self.groupMaxPosition)
        for i in range(len(self.groupMaxPosition)):
            totalProfit += self.groupMaxPosition[i] * profits[i]
            totalWeightInKg += self.groupMaxPosition[i] * weightsKg[i]
        print('\nProfit Generated:', totalProfit, '\nWeight in kg:', totalWeightInKg)

capacityKg=0
weightsKg=[]
profits=[]
solution=[]

def resetInitialValues():
    global initialValues
    initialValues=[]
    for i in range(len(weightsKg)):
        initialValues.append(0)

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
    for i in range(len(optimalSolution)):
        if(optimalSolution[i]!=algorithmSolution[i]):
            print("Solution is not optimal")
            return
    print("Solution is optimal")

# initialValues = [0, 0, ..., 0, 0]
for i in range(8):
    print("\n"+"PROBLEM #"+str(i+1))
    capacity_file_name="datasets\\p0"+str(i+1)+"_c.txt"
    weights_file_name="datasets\\p0"+str(i+1)+"_w.txt"
    profits_file_name="datasets\\p0"+str(i+1)+"_p.txt"
    solutions_file_name="datasets\\p0"+str(i+1)+"_s.txt"
    readVariablesFromFiles(capacity_file_name, weights_file_name, profits_file_name, solutions_file_name)
    resetInitialValues()
    pso = PSO(fncMax, initialValues, numberOfParticles=len(weightsKg), numberOfDimensions=1000, numberOfIterations=100, printSteps=False)
    pso.PrintResults()
    checkSolution(solution, pso.groupMaxPosition)