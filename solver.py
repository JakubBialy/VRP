from solution import Solution
from random import randrange


class Solver:
    def __init__(self, problem):
        self.problem = problem

    def generateDummySolution(self):
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

                    if self.single_car_solution_fitness(
                            Solution.SingleCarSolution(base_city, car_cities_candidate)) < self.problem.capacity:
                        car_cities = car_cities_candidate
                        del cities_copy[random_city_index]
                    else:
                        keep_searching = False

                if len(car_cities) > 0:
                    problem_solution.add_single_car_solution(Solution.SingleCarSolution(base_city, car_cities))

        print(self.fitness(problem_solution))
        return problem_solution

    def getNeighbors(self, bestCandidate):
        return [Solution(), Solution()]  # todo

    def fitness(self, solution: Solution):
        return 0  # todo

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
