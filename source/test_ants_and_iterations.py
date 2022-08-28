from solver import ACOSolver
from test_parser import CVRPTestParser

MAX_RANGE = 300
ALPHA = 1
BETA = 5
NUMBER_OF_ITERATIONS = 1000
PHEROMONES_FACTOR = 1
EVAPORATE_FACTOR = 0.5

def main():
    """Test method for finding number of ants and iterations"""
    tests = ['A-n32-k5', 'A-n45-k7', 'A-n60-k9']
    seeds = [11174, 203019, 473, 22087, 121769]

    for test in tests:
        for seed in seeds:
            test_set = CVRPTestParser.parse(test)
            number_of_cities = len(test_set.cities)
            for number_of_ants in [number_of_cities // 8, number_of_cities // 4, number_of_cities // 3, number_of_cities // 2, number_of_cities]:
                file_path = F'nm-{test}-{seed}-{number_of_ants}-out.txt'
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(F'Target: {test_set.optimal}\n')
                solver = ACOSolver(test_set.cities, test_set.capacity, MAX_RANGE, test_set.truck_count, seed, number_of_ants, ALPHA, BETA, PHEROMONES_FACTOR, EVAPORATE_FACTOR, NUMBER_OF_ITERATIONS)
                solver.solve(file_path)
                print(F'Solved for test={test}, seed={seed}, number_of_ants={number_of_ants}')

if __name__ == '__main__':
    main()
