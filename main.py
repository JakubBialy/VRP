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


## Main Functions

def parse_file(filepath):
    data = []
    with open(filepath, 'r', encoding="utf8") as file_to_read:
        for line in file_to_read.readlines():
            city_name, latitude, longitude, demand = line.split(",")

            city_data = Problem.City(
                city_name.strip(),
                float(latitude.strip()),
                float(longitude.strip()),
                int(demand.strip())
            )

            data.append(city_data)

    return data


## Problem
cities = []

try:
    cities = parse_file('cities_user')

except:
    print(colored("[Parse file error] Default cities loaded", 'red'))
    cities = parse_file('cities_default')

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

## Algorithm

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
