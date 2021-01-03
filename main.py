from person import Person
from problem import Problem
from solution import Solution
from solver import Solver
from termcolor import colored


# 1. Execute: pip install matplotlib
# 2. Download basemap-1.2.2 (https://download.lfd.uci.edu/pythonlibs/z4tqcw5k/basemap-1.2.2-cp39-cp39-win_amd64.whl)
# 3. Execute: pip install basemap-1.2.2-cp39-cp39-win_amd64.whl
#
# If run fails:
# 4. Execute: pip uninstall numpy
# 5. pip install numpy==1.19.3

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

## User Params

number_of_cars = input("Enter number of cars [int]: ")  # 5
try:
    number_of_cars = int(number_of_cars)
except ValueError:
    print(colored("[Parse error] Number of cars default value (5) loaded", 'red'))
    number_of_cars = 5

car_capacity = input("Enter car capacity [int]: ")  # 1_000
try:
    car_capacity = int(car_capacity)
except ValueError:
    print(colored("[Parse error] Car capacity default value (1_000) loaded", 'red'))
    car_capacity = 1_000

maxTabuSize = input("Enter tabu list size [int]: ")  # 8
try:
    maxTabuSize = int(maxTabuSize)
except ValueError:
    print(colored("[Parse error] Max Tabu Size default value (8) loaded", 'red'))
    maxTabuSize = 8

mutation_rate = input("Enter mutation rate [float]: ")  # 0.05
try:
    mutation_rate = float(mutation_rate)
except ValueError:
    print(colored("[Parse error] Mutation rate default value (0.05) loaded", 'red'))
    mutation_rate = 0.05

max_iterations = input("Enter max iterations [int]: ")  # 10_000
try:
    max_iterations = int(max_iterations)
except ValueError:
    print(colored("[Parse error] Max iteration default value (10_000) loaded", 'red'))
    max_iterations = 10_000

## Problem
cities = [
    Problem.City('Białystok', 53.132488, 23.16884, 500),
    Problem.City('Bielsko-Biała', 49.807621, 19.05584, 50),
    Problem.City('Chrzanów', 50.144138, 19.40601, 400),
    Problem.City('Gdańsk', 54.352024, 18.646639, 200),
    Problem.City('Gdynia', 54.51889, 18.53054, 100),
    Problem.City('Gliwice', 50.292961, 18.66893, 40),
    Problem.City('Gromnik', 49.832588, 20.95686, 200),
    Problem.City('Katowice', 50.264893, 19.023781, 300),
    Problem.City('Kielce', 50.866077, 20.628569, 30),
    Problem.City('Krosno', 49.693722, 21.765921, 60),
    Problem.City('Krynica', 54.383389, 19.441031, 50),
    Problem.City('Lublin', 51.24691, 22.57362, 60),
    Problem.City('Łódź', 51.759048, 19.458599, 160),
    Problem.City('Malbork', 54.035091, 19.048571, 100),
    Problem.City('Nowy Targ', 49.482479, 20.031771, 120),
    Problem.City('Olsztyn', 53.775711, 20.47798, 300),
    Problem.City('Poznań', 52.406376, 16.925167, 100),
    Problem.City('Puławy', 51.416481, 21.96904, 200),
    Problem.City('Radom', 51.40667, 21.125441, 100),
    Problem.City('Rzeszów', 50.04015, 21.97979, 60),
    Problem.City('Sandomierz', 50.68224, 21.750177, 200),
    Problem.City('Szczecin', 53.428543, 14.552812, 150),
    Problem.City('Szczucin', 50.308441, 21.07795, 60),
    Problem.City('Szklarska Poręba', 50.830189, 15.51875, 50),
    Problem.City('Tarnów', 50.015732, 20.986601, 70),
    Problem.City('Warszawa', 52.229675, 21.01223, 200),
    Problem.City('Wieliczka', 49.983528, 20.06049, 90),
    Problem.City('Wrocław', 51.107883, 17.038538, 40),
    Problem.City('Zakopane', 49.299171, 19.94902, 200),
    Problem.City('Zamość', 50.717369, 23.25276, 300),
]

fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='gnom', lat_0=52, lon_0=19.25,
            width=7E5, height=7E5, resolution='h')

m.fillcontinents(color="#FFDDCC", lake_color='#DDEEFF')
m.drawmapboundary(fill_color="#DDEEFF")
m.drawcountries()

for city in cities:
    x, y = m(city.longitude, city.latitude)
    plt.plot(x, y, 'ok', markersize=5)

    if city.name == 'Gliwice':
        plt.text(x, y, city.name + '  ', fontsize=7, horizontalalignment='right')
    else:
        plt.text(x, y, '  ' + city.name, fontsize=7)

fig.tight_layout()

p = Problem(number_of_cars, car_capacity, cities)
solver = Solver(p, mutation_rate)

s0 = solver.generateDummySolution(1024)

sBest = s0
bestCandidate = s0
tabuList = []
tabuList.append(s0)
iterations = 0

while (iterations < max_iterations):  # Dodać warunek wyjścia z pętli
    # sNeighborHood = solver.get_neighbors(bestCandidate)
    sNeighborHood = solver.get_neighbors_v2(bestCandidate)
    # sNeighborHood = solver.get_fake_neighbors(bestCandidate)
    bestCandidate = sNeighborHood[0]  # sNeighborHood.firstElement

    for sCandidate in sNeighborHood:
        if ((not sCandidate in tabuList) and (solver.fitness(sCandidate) < solver.fitness(bestCandidate))):
            bestCandidate = sCandidate

    if (solver.fitness(bestCandidate) < solver.fitness(sBest)):
        sBest = bestCandidate
        print('Current best: ' + str(solver.fitness(sBest)) + ' (iteration: ' + str(iterations) + ')')

    tabuList.append(bestCandidate)

    if (len(tabuList) > maxTabuSize):
        del tabuList[0]  # removeFirst

    iterations = iterations + 1

print(sBest)

for index, singleCarSolution in enumerate(sBest.single_car_solutions):
    roadLatitude = [singleCarSolution.base.latitude]
    roadLongitude = [singleCarSolution.base.longitude]

    for cityToVisit in singleCarSolution.cities:
        roadLatitude.append(cityToVisit.latitude)
        roadLongitude.append(cityToVisit.longitude)

    roadLatitude.append(singleCarSolution.base.latitude)
    roadLongitude.append(singleCarSolution.base.longitude)

    x, y = m(roadLongitude, roadLatitude)
    m.plot(x, y, 'o-', markersize=5, linewidth=1)

plt.show()
