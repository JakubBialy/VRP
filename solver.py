from typing import List

from problem import Problem
from solution import Solution
from random import randrange


class Solver:
    def __init__(self, problem, mutation_rate: int):
        self.problem = problem
        self.mutation_rate = mutation_rate

    def generateDummySolution(self, max_tries):
        tries_counter = 0

        while tries_counter < max_tries:
            cities_copy = self.problem.cities[:]
            base_city = self.problem.cities[0]
            problem_solution = Solution()

            for current_car_index in range(self.problem.cars):
                if len(cities_copy) > 0:

                    car_cities = []
                    keep_searching = True
                    while len(cities_copy) > 0 and keep_searching:
                        random_city_index = randrange(len(cities_copy))

                        if car_cities is None:
                            car_cities_candidate = []
                        else:
                            car_cities_candidate = car_cities[:]
                            car_cities_candidate.append(cities_copy[random_city_index])

                        # if self.single_car_solution_fitness(
                        #         Solution.SingleCarSolution(base_city, car_cities_candidate)) < self.problem.capacity:
                        if self.compute_cities_demand(car_cities_candidate) < self.problem.capacity:
                            car_cities = car_cities_candidate
                            del cities_copy[random_city_index]
                        else:
                            keep_searching = False

                    if len(car_cities) > 0:
                        problem_solution.add_single_car_solution(Solution.SingleCarSolution(base_city, car_cities))
                    else:
                        return problem_solution

            if len(cities_copy) == 0:
                # print("Initial solution found in " + str(tries_counter + 1) + " try!")
                return problem_solution

            tries_counter = tries_counter + 1

        raise Exception('Valid solution can\'t be found')

    def generate_single_neighbour(self, bestCandidate: Solution):
        city_swap_num = randrange(max(int(bestCandidate.get_cities_count() * self.mutation_rate), 1)) + 1

        # single_solutions_copy = bestCandidate.single_car_solutions[:]
        single_solutions_copy = bestCandidate.copy().single_car_solutions

        for i in range(city_swap_num):
            src_single_solution = single_solutions_copy[randrange(len(single_solutions_copy))]
            src_city_index = randrange(len(src_single_solution.cities))

            dst_single_solution = single_solutions_copy[randrange(len(single_solutions_copy))]
            dst_city_index = randrange(len(dst_single_solution.cities))

            tmp_city = dst_single_solution.cities[dst_city_index]

            dst_single_solution.cities[dst_city_index] = src_single_solution.cities[src_city_index]
            src_single_solution.cities[src_city_index] = tmp_city

        return Solution(single_solutions_copy)

    def getNeighbors(self, bestCandidate: Solution):
        result = []

        for i in range(randrange(8) + 1):
            candidate = self.generate_single_neighbour(bestCandidate)
            while not candidate.is_valid_solution(self.problem):
                candidate = self.generate_single_neighbour(bestCandidate)

            result.append(candidate)

        return result

    def get_fake_neighbors(self, ignored):
        tmp = []

        for i in range(randrange(10) + 1):
            tmp.append(self.generateDummySolution(1024))

        return tmp
    def fitness(self, solution: Solution):
        distances_sum = 0

        for single_car_solution in solution.single_car_solutions:
            distances_sum = distances_sum + self.single_car_solution_fitness(single_car_solution)

        return distances_sum

    def single_car_solution_fitness(self, solution: Solution.SingleCarSolution):
        if len(solution.cities) == 0:  # if solution is empty
            return 0
        elif len(solution.cities) == 1 and solution.cities[0] is solution.base:  # if solution contains only base
            return 0

        distances_sum = 0

        for current_city_index in range(len(solution.cities) - 1):
            first_city = solution.cities[current_city_index]
            second_city = solution.cities[current_city_index + 1]
            distances_sum = distances_sum + self.problem.get_distance_between(first_city, second_city)

        distances_sum = distances_sum + self.problem.get_distance_between(solution.base, solution.cities[0])
        distances_sum = distances_sum + self.problem.get_distance_between(solution.base, solution.cities[-1])

        return distances_sum

    @staticmethod
    def compute_cities_demand(cities: List[Problem.City]):
        demand_sum = 0
        for city in cities:
            demand_sum = demand_sum + city.demand

        return demand_sum
