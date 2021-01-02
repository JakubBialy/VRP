from solution import Solution


class Solver:
    def __init__(self, problem):
        self.problem = problem

    def generateDummySolution(self):
        return Solution()  # todo

    def getNeighbors(self, bestCandidate):
        return [Solution(), Solution()]  # todo

    def fitness(self, sCandidate):
        return 0  # todo
