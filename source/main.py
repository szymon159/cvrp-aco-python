"""Main file for solving CVRP on a selected subset of test cases using given algorithm"""
import sys
from solver import ACOSolver, ElitistACOSolver, EnhancedACOSolver, HeuristicSolver
from testset_parser import CVRPTestParser

MAX_RANGE = 300
NUMBER_OF_ITERATIONS = 200
ALPHA = 1
BETA = 7
EVAPORATE_FACTOR = 0.4
PHEROMONES_FACTOR = 20

def __get_heuristic_solver(number_of_trucks: int, s_max: int, test_set: str):
    return HeuristicSolver(test_set.cities, test_set.capacity, s_max, number_of_trucks, None)

def __get_aco_solver(number_of_trucks: int, s_max: int, test_set: str):
    return ACOSolver(test_set.cities, test_set.capacity, s_max, number_of_trucks, None, len(test_set.cities), ALPHA, BETA, PHEROMONES_FACTOR, EVAPORATE_FACTOR, NUMBER_OF_ITERATIONS)

def __get_elitist_aco_solver(number_of_trucks: int, s_max: int, test_set: str):
    return ElitistACOSolver(test_set.cities, test_set.capacity, s_max, number_of_trucks, None, len(test_set.cities), ALPHA, BETA, PHEROMONES_FACTOR, EVAPORATE_FACTOR, NUMBER_OF_ITERATIONS, len(test_set.cities) // 6)

def __get_enhanced_aco_solver(number_of_trucks: int, s_max: int, test_set: str):
    return EnhancedACOSolver(test_set.cities, test_set.capacity, s_max, number_of_trucks, None, len(test_set.cities), ALPHA, BETA, PHEROMONES_FACTOR, EVAPORATE_FACTOR, NUMBER_OF_ITERATIONS)

def solve_heuristic(number_of_trucks: int, s_max: int, test_set: str):
    """Solver CVRP problem using heuristic algorithm"""
    solver = __get_heuristic_solver(number_of_trucks, s_max, test_set)
    solver.solve()
    solver.print_result()

def solve_aco(number_of_trucks: int, s_max: int, test_set: str):
    """Solver CVRP problem using base ACO algorithm"""
    solver = __get_aco_solver(number_of_trucks, s_max, test_set)
    solver.solve()
    solver.print_result()

def solve_elitist_aco(number_of_trucks: int, s_max: int, test_set: str):
    """Solver CVRP problem using ACO algorithm with elitist ants"""
    solver = __get_elitist_aco_solver(number_of_trucks, s_max, test_set)
    solver.solve()
    solver.print_result()

def solve_enhanced_aco(number_of_trucks: int, s_max: int, test_set: str):
    """Solver CVRP problem using ACO algorithm with reversion of subpaths"""
    solver = __get_enhanced_aco_solver(number_of_trucks, s_max, test_set)
    solver.solve()
    solver.print_result()


def main():
    """Main method solving sample tests with different algorithms"""
    tests = ['A-n32-k5', 'A-n39-k5', 'A-n45-k7', 'A-n53-k7', 'A-n60-k9']
    max_range = int(sys.argv[2]) if len(sys.argv) >= 3 else MAX_RANGE

    for test in tests:
        test_set = CVRPTestParser.parse(test)
        number_of_trucks = int(sys.argv[1]) if len(sys.argv) >= 2 else test_set.truck_count

        print(test)
        solve_heuristic(number_of_trucks, max_range, test_set)
        print(80 * '-')

        print(test)
        solve_aco(number_of_trucks, max_range, test_set)
        print(80 * '-')

        print(test)
        solve_elitist_aco(number_of_trucks, max_range, test_set)
        print(80 * '-')

        print(test)
        solve_enhanced_aco(number_of_trucks, max_range, test_set)
        print(80 * '-')

if __name__ == '__main__':
    main()
