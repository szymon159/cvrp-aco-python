"""Test file for comparing different values of alpha and beta coefficients"""
from solver import ACOSolver
from testset_parser import CVRPTestParser

MAX_RANGE = 300
NUMBER_OF_ITERATIONS = 200
PHEROMONES_FACTOR = 1
EVAPORATE_FACTOR = 0.5

def main() -> None:
    """Test method for finding value of \u03b1 and \u03b2 factors"""
    tests = ['A-n32-k5', 'A-n45-k7', 'A-n60-k9']
    seeds = [11174, 203019, 473, 22087, 121769]
    alphas = [0.5, 1, 1.5, 2, 2.5, 3, 3.5]
    betas = [3, 4, 4.5, 5, 5.5, 6, 7]

    for test in tests:
        for seed in seeds:
            test_set = CVRPTestParser.parse(test)
            number_of_ants = len(test_set.cities)
            for alpha in alphas:
                for beta in betas:
                    file_path = F'ab-{test}-{seed}-{alpha}-{beta}-out.txt'
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(F'Target: {test_set.optimal}\n')
                    solver = ACOSolver(test_set.cities, test_set.capacity, MAX_RANGE, test_set.truck_count, seed, number_of_ants, alpha, beta, PHEROMONES_FACTOR, EVAPORATE_FACTOR, NUMBER_OF_ITERATIONS)
                    solver.solve(file_path)
                    print(F'Solved for test={test}, seed={seed}, alpha={alpha}, beta={beta}')

if __name__ == '__main__':
    main()
