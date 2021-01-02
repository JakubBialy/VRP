from person import Person


def generateDummySolution():
    pass  # todo


maxTabuSize = 1  # todo pobrac wartosc od usera

s0 = generateDummySolution()

sBest = s0
bestCandidate = s0
tabuList = []
tabuList.push(s0)


def getNeighbors(bestCandidate):
    pass  # todo


def fitness(sCandidate):
    pass  # todo


while (True):  # Dodać warunek wyjścia z pętli
    sNeighborHood = getNeighbors(bestCandidate)
    bestCandidate = sNeighborHood[0]  # sNeighborHood.firstElement

    for sCandidate in sNeighborHood:
        if ((not tabuList.contains(sCandidate)) and (fitness(sCandidate) > fitness(bestCandidate))):
            bestCandidate = sCandidate

    if (fitness(bestCandidate) > fitness(sBest)):
        sBest = bestCandidate

    tabuList.push(bestCandidate)  # todo czy nie trzeba zamienć na append?

    if (tabuList.size > maxTabuSize):
        tabuList.removeFirst()

print(sBest)
