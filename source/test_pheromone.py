"""Test file for comparing different values of pheromones factor"""
from solver import ACOSolver
from testset_parser import CVRPTestParser

MAX_RANGE = 300
NUMBER_OF_ITERATIONS = 200
ALPHA = 1
BETA = 7
EVAPORATE_FACTOR = 0.4

def main() -> None:
    """Test method for finding value of Q factor"""
    tests = ['A-n32-k5', 'A-n45-k7', 'A-n60-k9']
    seeds = [11174, 203019, 473, 22087, 121769]
    q_factors = [0.5, 1, 5, 10, 15, 20]

    for test in tests[1:]:
        for seed in seeds:
            test_set = CVRPTestParser.parse(test)
            number_of_ants = len(test_set.cities)
            for q_factor in q_factors:
                file_path = F'q-{test}-{seed}-{q_factor}-out.txt'
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(F'Target: {test_set.optimal}\n')
                solver = ACOSolver(test_set.cities, test_set.capacity, MAX_RANGE, test_set.truck_count, seed, number_of_ants, ALPHA, BETA, q_factor, EVAPORATE_FACTOR, NUMBER_OF_ITERATIONS)
                solver.solve(file_path)
                print(F'Solved for test={test}, seed={seed}, q={q_factor}')

if __name__ == '__main__':
    main()
