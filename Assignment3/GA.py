from deap import base
from deap import creator
from deap import tools

import random
import os
import numpy
import matplotlib.pyplot as plt
import seaborn as sns
import GA_Problem_Init

import GA_Algo_Modified # modified "algorithms" module from deap

def knapsackValue(individual):
    return knapsack.getValue(individual),

def solve(oSrcFile, oResFile, timeLimit):
    global knapsack
    knapsack = GA_Problem_Init.KnapsackProblem(oSrcFile)

    POPULATION_SIZE = 300
    P_CROSSOVER = 0.9
    P_MUTATION = 0.1
    MAX_GENERATIONS = 50
    HALL_OF_FAME_SIZE = 1

    RANDOM_SEED = 42
    random.seed(RANDOM_SEED)

    toolbox = base.Toolbox()
    toolbox.register("zeroOrOne", random.randint, 0, 1)
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.zeroOrOne, len(knapsack))
    toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)


    toolbox.register("evaluate", knapsackValue)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=1.0/len(knapsack))

    population = toolbox.populationCreator(n=POPULATION_SIZE)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    population, logbook, elapsedTime = GA_Algo_Modified.eaSimple(population, toolbox, timeLimit, cxpb=P_CROSSOVER, mutpb=P_MUTATION, ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)

    # print("Size:", knapsack.__len__(), "items, Time taken:", elapsedTime, "s (time limit exceeded)" if elapsedTime > timeLimit else "s")                                          
    oResFile.write("Size: " + str(knapsack.__len__()) + " items, Time taken: " + str(elapsedTime) + ("s (time limit exceeded)" if elapsedTime > timeLimit else "s"))
    
    best = hof.items[0]
    computed_value, total_weight, packed_items = knapsack.getSumResults(best, oResFile)

    oResFile.write("\n")
    oResFile.write("Total value = " + str(computed_value) + "\n")
    oResFile.write("Total weight = " + str(total_weight) + "\n")
    oResFile.write("Total packed items = " + str(packed_items) + "\n")
    oResFile.write("\n\n")

def main():
    # lst = os.listdir("./test_cases")
    lst = [
        "00Uncorrelated", 
        "01WeaklyCorrelated",
        "02StronglyCorrelated",
        "03InverseStronglyCorrelated",
        "04AlmostStronglyCorrelated",
        "05SubsetSum",
        "06UncorrelatedWithSimilarWeights",
        "07SpannerUncorrelated",
        "08SpannerWeaklyCorrelated",
        "09SpannerStronglyCorrelated",
        "10MultipleStronglyCorrelated",
        "11ProfitCeiling",
        "12Circle"
    ]
    for test in range(0,8):
        testGroupName = lst[test] # Chọn 1 trong 13 group trong list trên để solve
        testGroupPath = "./picked_test_cases/" + testGroupName
        testCaseFile = os.listdir(testGroupPath)

        resultFile = open("./_GA_Results/" + testGroupName + ".txt", "a")

        timeLimit = 120

        for i in range(0, 6):
            tmpFilePath = testGroupPath + "/" + testCaseFile[i]
            resultFile.write("==> File path: " + tmpFilePath + "\n")
            print("Solving:", tmpFilePath)
            solve(open(tmpFilePath, "r"), resultFile, timeLimit)

        resultFile.close()

if (__name__ == "__main__"):
    main()