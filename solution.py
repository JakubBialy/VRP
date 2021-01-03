from typing import List

from problem import Problem


class Solution:

    def __init__(self, single_car_solutions=None):
        if single_car_solutions is None:
            single_car_solutions = []
        self.single_car_solutions = single_car_solutions

    # def __eq__(self, other): #v1
    #     if not isinstance(other, Solution):
    #         return False
    #
    #     return set(self.single_car_solutions) == set(other.single_car_solutions)

    def __eq__(self, other):  # v2
        if not isinstance(other, Solution):
            return False

        if len(self.single_car_solutions) == len(other.single_car_solutions):
            self_demands = []
            other_demands = []

            for sol in self.single_car_solutions:
                self_demands.append(sol.compute_demand())

            for sol in other.single_car_solutions:
                other_demands.append(sol.compute_demand())

            if sorted(self_demands) == sorted(other_demands):
                return set(self.single_car_solutions) == set(other.single_car_solutions)
        else:
            return False


    # def __eq__(self, other):  # v3
    #     if not isinstance(other, Solution):
    #         return False
    #
    #     if len(self.single_car_solutions) == len(other.single_car_solutions):
    #         self_routes = []
    #         other_routes = []
    #
    #         for sol in self.single_car_solutions:
    #             self_routes.append(sol.get_cities_name_list())
    #
    #         for sol in other.single_car_solutions:
    #             other_routes.append(sol.get_cities_name_list())
    #
    #         if sorted(self_routes) == sorted(other_routes):
    #             return True
    #     else:
    #         return False

    def get_cities_count(self):
        cities_sum = 0
        for single_car_solution in self.single_car_solutions:
            cities_sum = cities_sum + len(single_car_solution.cities)

        return cities_sum

    class SingleCarSolution:
        def __init__(self, base, cities: []):
            self.base = base
            self.cities = cities

        def compute_demand(self):
            demand_sum = 0
            for city in self.cities:
                demand_sum = demand_sum + city.demand

            return demand_sum

        def get_cities_name_list(self):
            result = []
            for city in self.cities:
                result.append(city.name)

            return result

        def __eq__(self, other):
            if not isinstance(other, Solution.SingleCarSolution):
                return False

            # return self.base == other.base and set(self.cities) == set(other.cities)
            # return self.base == other.base and self.cities == other.cities
            return self.cities == other.cities

        def __hash__(self):
            return int(hash(hash(self.base) * (len(self.cities) + 1)))

    def copy(self):
        single_car_solutions_deep_copy = []

        for sol in self.single_car_solutions:
            single_car_solutions_deep_copy.append(Solution.SingleCarSolution(sol.base, sol.cities[:]))

        return Solution(single_car_solutions_deep_copy)

    def add_single_car_solution(self, single_car_solution: SingleCarSolution):
        self.single_car_solutions.append(single_car_solution)

    def is_valid_solution(self, problem: Problem):
        for sol in self.single_car_solutions:
            if sol.compute_demand() > problem.capacity:
                return False

        return True
