"""Solver for CVRP problem"""
from abc import abstractmethod
from random import Random
import sys
import numpy
from timeit import default_timer as timer

class BaseSolver:
    """Base class for a CVRP problem solver"""
    def __init__(self, cities, max_capacity, max_range, number_of_trucks, seed):
        self.cities = cities
        self.max_capacity = max_capacity
        self.max_range = max_range
        self.number_of_trucks = number_of_trucks
        self.distances = self._calculate_distances(cities)
        self.was_visited = [-self.number_of_trucks + 1] + [0] * (len(self.cities) - 1)
        self.rem_capacity = self.max_capacity
        self.rem_range = self.max_range
        self.current_id = 0
        self.waiting = self.cities[1:]
        self.route = []
        self.route_length = sys.maxsize
        self.result = None
        self.seed = seed
        self.random = Random(self.seed)

    @abstractmethod
    def solve(self, output = None):
        """Triggers solving the problem and outputs analytics information to output if needed"""
        raise NotImplementedError('Solving not supported in the base class, use subclass instead')

    def print_result(self):
        """Prints solver result"""
        print(self.get_algorithm_name())
        if not self.result:
            print("Nie znaleziono rozwiazania")
        else:
            print("Znalezione sciezki:")
            for i, path in enumerate(self._split_route(self.route)):
                print(F"{i}. {path}")
            print(F'O lacznej dlugosci: {self.route_length}')

    @abstractmethod
    def get_algorithm_name(self):
        """Return name of algorithm used by solver"""
        raise NotImplementedError('Algorithm name not supported in the base class, use subclass instead')

    def _can_visit(self, target_id):
        range_fulfilled = ((target_id == 0 and self._get_distance_to(target_id) <= self.rem_range)
            or self._get_distance_to(target_id) + self.distances[target_id, 0] <= self.rem_range)
        return (self.current_id != target_id
                and self.was_visited[target_id] < 1
                and self.cities[target_id].demand <= self.rem_capacity
                and range_fulfilled)

    def _get_target_id(self, allowed_cities):
        return min(allowed_cities, key=self._get_distance_to)

    def _visit(self, target_id, route):
        self.was_visited[target_id] += 1
        self.rem_capacity -= self.cities[target_id].demand
        self.rem_range -= self._get_distance_to(target_id)
        distance = self._get_distance_to(target_id)
        self.current_id = target_id
        route.append(self.current_id)
        if target_id == 0:
            self.rem_capacity = self.max_capacity
            self.rem_range = self.max_range
        return distance

    def _check_all_visited(self):
        return all(self.was_visited[1:])

    def _get_distance_to(self, target_id):
        return self.distances[self.current_id, target_id]

    def _find_route(self):
        route_length = 0
        route = [0]
        while not self._check_all_visited():
            to_visit = list(filter(self._can_visit, range(0, len(self.cities))))
            if len(to_visit) == 0:
                return ([], -1)
            if 0 in to_visit and len(to_visit) > 1:
                to_visit.remove(0)
            target_id = self._get_target_id(to_visit)
            route_length += self._visit(target_id, route)
        route_length = (route_length + self._visit(0, route) if self._can_visit(0) else -1)
        return (route, route_length)

    def _update_result(self, route, route_length):
        if route_length < self.route_length:
            self.route = route
            self.route_length = route_length
            self.result = True

    def _split_route(self, route):
        result = []
        path = [route[0]]
        for value in route[1:]:
            path.append(value)
            if value == 0:
                result.append(path)
                path = [0]
        return result

    def _get_route_length(self, route):
        length = 0
        for i, city_from in enumerate(route[:-1]):
            city_to = route[i + 1]
            length += self.distances[city_from, city_to]
        return length

    @staticmethod
    def _calculate_distances(cities):
        distances = numpy.zeros((len(cities), len(cities)))
        for i, city1 in enumerate(cities):
            for j, city2 in enumerate(cities):
                if i > j:
                    distances[i,j] = distances[j,i] = city1.distance(city2)
        return distances

class HeuristicSolver(BaseSolver):
    """Class implementing a solver for CVRP problem using heuristic algorithm"""
    def __init__(self, cities, max_capacity, max_range, number_of_trucks, seed):
        super().__init__(cities, max_capacity, max_range, number_of_trucks, seed)
        self._current_route = [0]

    def solve(self, output = None):
        if output is not None:
            file = open(output, 'a', encoding='utf-8')
            file.write(F'{self.get_algorithm_name()}\n')
        try:
            start = timer()
            (route, route_length) = self._find_route()
            if route_length != -1:
                self._update_result(route, route_length)
            else:
                self.result = False
            end = timer()
        finally:
            if output is not None and not file.closed:
                file.write(F'{0} {self.route_length if 0 <= self.route_length < sys.maxsize else 0}\n')
                file.write(F'Time: {(end - start) * 1000} ms\n')
                file.close()

    def get_algorithm_name(self):
        return 'Heuristic'

class _AntSolution:
    def __init__(self):
        self.current_route = [0]
        self.current_route_length = -1
        self.best_route = []
        self.best_route_length = sys.maxsize

    def check_current_route(self):
        """Checks if current solution is better than the best one and updates it if it is needed"""
        if (self.current_route_length == -1 or self.current_route_length >= self.best_route_length):
            return False
        self.best_route = self.current_route
        self.best_route_length = self.current_route_length
        return True

    def reset(self):
        """Resets current route and solution"""
        self.current_route = [0]
        self.current_route_length = -1

class ACOSolver(BaseSolver):
    """Class implementing a solver for CVRP problem using ACO"""
    def __init__(self, cities, max_capacity, max_range, number_of_trucks, seed,
                number_of_ants, alpha, beta, pheromones_factor, evaporate_factor, number_of_iterations):
        super().__init__(cities, max_capacity, max_range, number_of_trucks, seed)
        self.number_of_ants = number_of_ants
        self.alpha = alpha
        self.beta = beta
        self.pheromones_factor = pheromones_factor
        self.evaporate_factor = evaporate_factor
        self.number_of_iterations = number_of_iterations
        self.pheromones = numpy.ones((len(cities), len(cities)))
        self.current_ant_id = 0
        self.ants = [_AntSolution() for _ in range(number_of_ants)]

    def solve(self, output = None):
        if output is not None:
            file = open(output, 'a', encoding='utf-8')
            file.write(F'{self.get_algorithm_name()}\n')
        try:
            start = timer()
            for i in range(self.number_of_iterations):
                for ant in self.ants:
                    ant.reset()
                    self.was_visited = [-self.number_of_trucks + 1] + [0] * (len(self.cities) - 1)
                    (ant.current_route, ant.current_route_length) = self._find_route()
                    self._lay_pheromones(ant.current_route)
                    if ant.check_current_route():
                        self._update_result(ant.best_route, ant.best_route_length)
                if output is not None and not file.closed:
                    file.write(F'{i+1} {self.route_length if 0 <= self.route_length < sys.maxsize else 0}\n')
                self._update_pheromones()
            end = timer()
        finally:
            if output is not None and not file.closed:
                file.write(F'Time: {(end - start) * 1000} ms\n')
                file.close()

    def get_algorithm_name(self):
        return 'ACO'

    def _get_target_id(self, allowed_cities):
        weights = []
        for city in allowed_cities:
            if self._get_distance_to(city) == 0:
                return city
            pheromon_factor = self.pheromones[self.current_id, city]
            heuristic_factor = 1 / self._get_distance_to(city)
            weights.append((pheromon_factor ** self.alpha) * (heuristic_factor ** self.beta))
        if sum(weights) <= 0.0:
            weights = None
        return self.random.choices(allowed_cities, weights, k = 1)[0]

    def _lay_pheromones(self, route, factor = None):
        if factor is None:
            factor = self.pheromones_factor
        if len(route) <= 0:
            return
        for i in range(len(route) - 1):
            city_from = route[i]
            city_to = route[i+1]
            if city_from != city_to:
                self.pheromones[city_from, city_to] += factor / self._get_route_length(route)

    def _update_pheromones(self):
        for i in range(len(self.cities)):
            for j in range(len(self.cities)):
                if i != j:
                    self.pheromones[i, j] *= (1 - self.evaporate_factor)

class ElitistACOSolver(ACOSolver):
    """Class implementing a solver for CVRP problem using ACO with elitist ants"""
    def __init__(self, cities, max_capacity, max_range, number_of_trucks, seed,
                number_of_ants, alpha, beta, pheromones_factor, evaporate_factor, number_of_iterations,
                number_of_elitist_ants):
        super().__init__(cities, max_capacity, max_range, number_of_trucks, seed,
                        number_of_ants, alpha, beta, pheromones_factor, evaporate_factor, number_of_iterations)
        self.number_of_elitist_ants = number_of_elitist_ants

    def get_algorithm_name(self):
        return 'Elitist'

    def _update_pheromones(self):
        super()._update_pheromones()
        if len(self.route) > 0:
            self._lay_pheromones(self.route, self.number_of_elitist_ants * self.pheromones_factor)
        else:
            print('No solution so far')

class EnhancedACOSolver(ACOSolver):
    """Class implementing a solver for CVRP problem using ACO with inversion of subpaths"""
    def _find_route(self):
        (base_route, base_route_length) = super()._find_route()
        if base_route_length <= 0:
            return (base_route, base_route_length)
        return self.__reverse_subpaths(base_route)

    def get_algorithm_name(self):
        return 'Enhanced'

    def __reverse_subpaths(self, base_route):
        best_route, best_length = [0], 0
        paths = [path for path in self._split_route(base_route)]
        lengths = [self._get_route_length(path) for path in paths]
        for i, path in enumerate(paths):
            if len(path) <= 3:
                best_route.extend(paths[i][1:])
                best_length += lengths[i]
                continue
            modified_subpath = path
            for j in range(1, len(path) - 2):
                for k in range(j + 1, len(path) - 1):
                    modified_subpath[j], modified_subpath[k] = modified_subpath[k], modified_subpath[j]
                    modified_subpath_length = self._get_route_length(modified_subpath)
                    if modified_subpath_length < lengths[i]:
                        paths[i], lengths[i] = modified_subpath, modified_subpath_length
            best_route.extend(paths[i][1:])
            best_length += lengths[i]
        return (best_route, best_length)
