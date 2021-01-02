import geopy.distance


class Problem:

    def __init__(self, cars, capacity, cities):
        self.cars = cars
        self.capacity = capacity
        self.cities = cities
        self.distance_matrix = self.__compute_distance_matrix(self.cities)

    def __compute_distance_matrix(self, cities):
        rows, cols = (len(cities), len(cities))
        result = []  # array initialization
        for i in range(cols):
            col = []
            for j in range(rows):
                col.append(0)
            result.append(col)

        for first_index, first_city in enumerate(cities):
            for second_index, second_city in enumerate(cities):
                coords_1 = (first_city.latitude, first_city.longitude)
                coords_2 = (second_city.latitude, second_city.longitude)

                dist = geopy.distance.geodesic(coords_1, coords_2).km
                result[first_index][second_index] = dist

    class City:

        def __init__(self, name, latitude, longitude, demand):
            self.name = name
            self.demand = demand
            self.latitude = latitude
            self.longitude = longitude
