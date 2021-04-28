from ortools.algorithms import pywrapknapsack_solver

def InputFromFile(file_name):
  file=open(file_name, "r")
  n,capacities=0,0
  values,weights=[],[]
  for line in file:
    line_arr=line.strip().split()
    if len(line_arr)==0:
        continue
    if len(line_arr)==1:
      if n==0:
        n=line_arr[0]
      else:
        capacities=line_arr[0]
    if len(line_arr)==2:
      s1,s2=int(line_arr[0]),int(line_arr[1])
      values.append(s1)
      weights.append(s2)
  return [int(capacities)],values,[weights]

def main():
    # Create the solver.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')
    capacities,values,weights=InputFromFile("kplib/00Uncorrelated/n00050/R01000/s000.kp")
    print(capacities,values,weights)
    solver.Init(values, weights, capacities)
    computed_value = solver.Solve()

    packed_items = []
    packed_weights = []
    total_weight = 0
    print('Total value =', computed_value)
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]
    print('Total weight:', total_weight)
    print('Packed items:', packed_items)
    print('Packed_weights:', packed_weights)


if __name__ == '__main__':
    main()