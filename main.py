from person import Person
from problem import Problem
from solution import Solution
from solver import Solver

# 1. Execute: pip install matplotlib
# 2. Download basemap-1.2.2 (https://download.lfd.uci.edu/pythonlibs/z4tqcw5k/basemap-1.2.2-cp39-cp39-win_amd64.whl)
# 3. Execute: pip install basemap-1.2.2-cp39-cp39-win_amd64.whl
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

##Params
maxTabuSize = 8  # todo pobrac wartosc od usera
mutation_rate = 0.05

##Problem
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
m = m = Basemap(projection='gnom', lat_0=52, lon_0=19.25,
                width=7E5, height=7E5, resolution='h')

m.fillcontinents(color="#FFDDCC", lake_color='#DDEEFF')
m.drawmapboundary(fill_color="#DDEEFF")
m.drawcountries()


for city in cities:
    x, y = m(city.longitude, city.latitude)
    plt.plot(x, y, 'ok', markersize=5)

    if city.name == 'Gliwice' :
        plt.text(x, y, city.name + '  ', fontsize=7, horizontalalignment='right')
    else:
        plt.text(x, y, '  ' + city.name, fontsize=7)

fig.tight_layout()
plt.show()


p = Problem(5, 1000, cities)
solver = Solver(p, mutation_rate)

s0 = solver.generateDummySolution(1024)

sBest = s0
bestCandidate = s0
tabuList = []
tabuList.append(s0)
iterations = 0
max_iterations = 16_000

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
        print('Current best: ' + str(solver.fitness(sBest)))

    tabuList.append(bestCandidate)

    if (len(tabuList) > maxTabuSize):
        del tabuList[0]  # removeFirst

    iterations = iterations + 1

print(sBest)
