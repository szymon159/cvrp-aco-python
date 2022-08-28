from solver import ACOSolver, ElitistACOSolver, EnhancedACOSolver, HeuristicSolver
from test_parser import CVRPTestParser

MAX_RANGE = 300
NUMBER_OF_ITERATIONS = 200
ALPHA = 1
BETA = 7
EVAPORATE_FACTOR = 0.4
PHEROMONES_FACTOR = 20

def main():
    """Test method comparing all implemented methods"""
    tests = ['A-n32-k5', 'A-n39-k5', 'A-n45-k7', 'A-n53-k7', 'A-n60-k9']
    seeds = [11174, 203019, 473, 22087, 121769]

    for test in tests:
        for seed in seeds:
            test_set = CVRPTestParser.parse(test)
            number_of_ants = len(test_set.cities)
            number_of_elitist = len(test_set.cities) // 6
            solvers = [
                ACOSolver(test_set.cities, test_set.capacity, MAX_RANGE, test_set.truck_count, seed, number_of_ants, ALPHA, BETA, PHEROMONES_FACTOR, EVAPORATE_FACTOR, NUMBER_OF_ITERATIONS),
                ElitistACOSolver(test_set.cities, test_set.capacity, MAX_RANGE, test_set.truck_count, seed, number_of_ants, ALPHA, BETA, PHEROMONES_FACTOR, EVAPORATE_FACTOR, NUMBER_OF_ITERATIONS, number_of_elitist),
                EnhancedACOSolver(test_set.cities, test_set.capacity, MAX_RANGE, test_set.truck_count, seed, number_of_ants, ALPHA, BETA, PHEROMONES_FACTOR, EVAPORATE_FACTOR, NUMBER_OF_ITERATIONS),
                HeuristicSolver(test_set.cities, test_set.capacity, MAX_RANGE, test_set.truck_count, seed)
            ]
            for solver in solvers:
                file_path = F'compare-{test}-{seed}-{solver.get_algorithm_name()}-out.txt'
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(F'Target: {test_set.optimal}\n')
                solver.solve(file_path)
                print(F'Solved for test={test}, seed={seed}, method={solver.get_algorithm_name()}')

if __name__ == '__main__':
    main()
