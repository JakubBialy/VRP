class Solution:

    def __init__(self, single_car_solutions=None):
        if single_car_solutions is None:
            single_car_solutions = []
        self.single_car_solutions = single_car_solutions

    class SingleCarSolution:
        def __init__(self, base, cities: []):
            self.base = base
            self.cities = cities

    def add_single_car_solution(self, single_car_solution: SingleCarSolution):
        self.single_car_solutions.append(single_car_solution)
