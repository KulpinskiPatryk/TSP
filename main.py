import re
import numpy as np


def read_tsp_data(tsp_name):
    tsp_name = tsp_name
    with open(tsp_name) as f:
        content = f.read().splitlines()
        cleaned = [x.lstrip() for x in content if x != ""]
        return cleaned


def detect_dimension(in_list):
    non_numeric = re.compile(r'[^\d]+')
    for element in in_list:
        if element.startswith("DIMENSION"):
            return non_numeric.sub("", element)


def get_cities(list, dimension):
    dimension = int(dimension)
    for item in list:
        for num in range(1, dimension + 1):
            if item.startswith(str(num)):
                index, space, rest = item.partition(' ')
                if rest not in cities_set:
                    cities_set.append(rest)
    return cities_set


def city_tup(list):
    number = 1
    for item in list:
        first_coord, space, second_coord = item.partition(' ')
        cities_tups.append((number, float(first_coord.strip()), float(second_coord.strip())))
        number += 1
    return cities_tups


def produce_final(file_data):
    data = read_tsp_data(file_data)
    dimension = detect_dimension(data)
    cities_set = get_cities(data, dimension)
    cities_tups = city_tup(cities_set)
    return dimension


def create_matrix_of_distance(dimension):
    distance_matrix = []
    for i in range(dimension):
        distance_matrix.append([])
    k = 0
    for i in distance_matrix:
        for j in range(dimension):
            i.append(manhattan_calc(k, j))
        k += 1
    return distance_matrix


def manhattan_calc(a, b):
    x1 = cities_tups[a][1]
    x2 = cities_tups[a][2]
    y1 = cities_tups[b][1]
    y2 = cities_tups[b][2]
    distance = abs(x1 - y1) + abs(x2 - y2)
    return distance


def create_entity(dimension):
    support_table = []
    for i in range(dimension):
        support_table.append(i)
    live = []
    entity = np.random.permutation(support_table)
    full_distance = 0
    for i in range(dimension - 1):
        x = entity[i]
        y = entity[i + 1]
        full_distance += distance_matrix[x][y]
    full_distance += distance_matrix[entity[0]][entity[dimension-1]]
    print(full_distance)
    for i in entity:
        live.append(i)
    live.append(int(full_distance))
    return live


def rewrite_score(a, dimension):
    full_distance = 0
    for i in range(dimension - 1):
        x = a[i]
        y = a[i + 1]
        full_distance += distance_matrix[x][y]
    full_distance += distance_matrix[a[0]][a[dimension - 1]]
    print(full_distance)
    a[dimension] = full_distance
    return a



if __name__ == '__main__':
    cities_set = []
    cities_tups = []
    file_data = "pr144.tsp"
    #Stworzenie nie edytowalnej listy z miastami
    dimension = produce_final(file_data)
    dimension = int(dimension)
    #stworzenie listy dystansów
    distance_matrix = create_matrix_of_distance(dimension)
    #print(cities_tups)
    #print(distance_matrix)
    #stworzorzenie osobników
    a = create_entity(dimension)
    b = create_entity(dimension)
    if a[dimension] < b[dimension]:
        b = rewrite_score(a, dimension)
    else:
        print(b)
#Dodać w najlepszym wyniku dodatkowe 1 do każdego miejsca aby działało pikobelo

