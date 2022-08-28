from solver import ElitistACOSolver
from test_parser import CVRPTestParser

MAX_RANGE = 300
NUMBER_OF_ITERATIONS = 200
ALPHA = 1
BETA = 7
EVAPORATE_FACTOR = 0.4
PHEROMONES_FACTOR = 20

def main():
    """Test method for finding value of e factor"""
    tests = ['A-n32-k5', 'A-n45-k7', 'A-n60-k9']
    seeds = [11174, 203019, 473, 22087, 121769]
    elitist = [6, 7, 8, 9, 10]

    for test in tests[1:]:
        for seed in seeds:
            test_set = CVRPTestParser.parse(test)
            number_of_ants = len(test_set.cities)
            for e in elitist:
                file_path = F'e-{test}-{seed}-{e}-out.txt'
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(F'Target: {test_set.optimal}\n')
                solver = ElitistACOSolver(test_set.cities, test_set.capacity, MAX_RANGE, test_set.truck_count, seed, number_of_ants, ALPHA, BETA, PHEROMONES_FACTOR, EVAPORATE_FACTOR, NUMBER_OF_ITERATIONS, e)
                solver.solve(file_path)
                print(F'Solved for test={test}, seed={seed}, e={e}')

if __name__ == '__main__':
    main()
