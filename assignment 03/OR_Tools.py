from ortools.algorithms import pywrapknapsack_solver
import os, random, time

solver = pywrapknapsack_solver.KnapsackSolver(
    pywrapknapsack_solver.KnapsackSolver.
    KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')

def solve(oSrcFile, oResFile, timeLimit):
    values = []
    weights = [[]]
    capacities = []

    packed_items = []
    packed_weights = []
    total_weight = 0

    hData = oSrcFile.readlines()

    capacities.append(int(hData[2]))

    for i in range(4, 4 + int(hData[1])):
        values.append(int(hData[i].split(" ")[0]))
        weights[0].append(int(hData[i].split(" ")[1]))

    st = time.time()

    solver.Init(values, weights, capacities)
    solver.set_time_limit(timeLimit)

    computed_value = solver.Solve()

    ct = time.time() - st

    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]

    
    oResFile.write("Size: " + str(len(values)) + " items, Time taken: " + str(ct) + " s")
    if (ct > timeLimit):
        oResFile.write(" (time limit exceeded)")
    oResFile.write("\n")
    oResFile.write("Total value = " + str(computed_value) + "\n")
    oResFile.write("Total weight: " + str(total_weight) + "\n")
    oResFile.write("Packed items: " + str(packed_items) + "\n")
    oResFile.write("Packed_weights: " + str(packed_weights) + "\n")
    oResFile.write("\n\n")

    oSrcFile.close()

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

testGroupName = lst[3] # Chọn 1 trong 13 group trong list trên để solve
testGroupPath = "./picked_test_cases/" + testGroupName
testCaseFile = os.listdir(testGroupPath)

resultFile = open("./_OR_Tools_Results/" + testGroupName + ".txt", "w+")

timeLimit = 300

for i in range(0, 8):
    tmpFilePath = testGroupPath + "/" + testCaseFile[i]
    resultFile.write("==> File path: " + tmpFilePath + "\n")
    print("Solving:", tmpFilePath)
    solve(open(tmpFilePath, "r"), resultFile, timeLimit)
            
resultFile.close()

