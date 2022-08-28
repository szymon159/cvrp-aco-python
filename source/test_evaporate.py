from solver import ACOSolver
from test_parser import CVRPTestParser

MAX_RANGE = 300
NUMBER_OF_ITERATIONS = 200
PHEROMONES_FACTOR = 1
ALPHA = 1
BETA = 7

def main():
    """Test method for finding value of \u03C1 factor"""
    tests = ['A-n32-k5', 'A-n45-k7', 'A-n60-k9']
    seeds = [11174, 203019, 473, 22087, 121769]
    rhos = [0.3, 0.4, 0.5, 0.6, 0.7]

    for test in tests:
        for seed in seeds:
            test_set = CVRPTestParser.parse(test)
            number_of_ants = len(test_set.cities)
            for rho in rhos:
                file_path = F'ro-{test}-{seed}-{rho}-out.txt'
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(F'Target: {test_set.optimal}\n')
                solver = ACOSolver(test_set.cities, test_set.capacity, MAX_RANGE, test_set.truck_count, seed, number_of_ants, ALPHA, BETA, PHEROMONES_FACTOR, rho, NUMBER_OF_ITERATIONS)
                solver.solve(file_path)
                print(F'Solved for test={test}, seed={seed}, rho={rho}')

if __name__ == '__main__':
    main()
