"""Utilities for handling input test files"""
import re
from city import City

class TestData:
    """Class representing testcase data parsed from input files"""
    def __init__(self, truck_count, capacity, cities, optimal, solution):
        self.truck_count = truck_count
        self.capacity = capacity
        self.cities = cities
        self.optimal = optimal
        self.solution = solution

    def __str__(self):
        cities = '\n\t'.join([F'{i}. {city}' for i, city in enumerate(self.cities)])
        solution = '\n\t'.join([str(path) for path in self.solution])
        return F'''\
Truck count: {self.truck_count}
Capacity: {self.capacity}
Cities: {cities}
Optimal value: {self.optimal}
Optimal:{solution}'''

class CVRPTestParser:
    """Class parsing testcase files to TestData"""
    @classmethod
    def parse(cls, test_name):
        """Static method for parsing test files into instance of TestData class"""
        test_path = 'testsets/' + test_name
        with open(test_path + '.vrp', 'r', encoding='utf-8') as test_file:
            test_content = test_file.read()
            truck_count = re.search(r"No of trucks: (\d+)", test_content, re.MULTILINE).group(1)
            capacity = re.search(r"^\s?CAPACITY\s?: (\d+)\s?$", test_content, re.MULTILINE).group(1)
            positions = re.findall(r"^\s?(\d+) (\d+) (\d+)\s?$", test_content, re.MULTILINE)
            demand = re.findall(r"^\s?(\d+) (\d+)\s?$", test_content, re.MULTILINE)
            cities = []
            for position in positions:
                for dem in demand:
                    if position[0] == dem[0]:
                        cities.append(City(int(position[1]), int(position[2]), int(dem[1])))

        with open(test_path + '.sol', 'r', encoding='utf-8') as solution_file:
            solution_content = solution_file.read()
            optimal = re.search(r"Cost (\d+)", solution_content, re.MULTILINE).group(1)
            raw_sol = re.findall(r"^\s?Route #(\d+)\s?:\s?(.*)\s?$", solution_content, re.MULTILINE)
            paths = [[int(vertex) for vertex in unparsed[1].split()] for unparsed in raw_sol]

        test_data = TestData(int(truck_count), int(capacity), cities, int(optimal), paths)
        return test_data
        