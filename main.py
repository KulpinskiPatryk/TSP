import random
import re
import numpy as np
import sys


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
    #print(full_distance)
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
    a[dimension] = int(full_distance)
    return a


def tournament_selection(pop, k, dimension):
    selected = []
    for i in range(int(k/2)):
        sel = random.randint(0, k-1)
        selected.append(pop[sel])
    best = selected[0].copy()
    for i in range(int(k/2)):
        if selected[i][dimension] <= best[dimension]:
            best = selected[i].copy()
    return best


def cross(parent1, parent2, dimension):
    child = []
    child_p1 = []
    child_p2 = []

    gene_a = random.randint(0, dimension-2)
    gene_b = random.randint(0, dimension-2)

    start_gene = min(gene_a, gene_b)
    endGene = max(gene_a, gene_b)

    for i in range(start_gene, endGene):
        child_p1.append(parent1[i])

    child_p2 = [item for item in parent2 if item not in child_p1]

    child = child_p1 + child_p2
    return child


def mutate(individual, mutationRate):
    for swapped in range(len(individual)-1):
        if (random.random() < mutationRate):
            swapWith = int(random.random() * (len(individual)-1))

            city1 = individual[swapped]
            city2 = individual[swapWith]

            individual[swapped] = city2
            individual[swapWith] = city1
    return individual


def find_best(pop, k, dimension):
    best = pop[0]
    for xy in range(k):
        if pop[xy][dimension] <= best[dimension]:
            best = pop[xy].copy()
    return best


def true_form(x, dim):
    for h in range(dim-1):
        x[h] = x[h] + 1
    return x


def route_finder(k, dimension):
    pop = []
    mutation_rate = 0.01
    #stworzorzenie osobników
    for z in range(k):
        pop.append(create_entity(dimension))
    for an in range(z):
        children = []
        for population in range(k):
            children.append(tournament_selection(pop, k, dimension))
        pop = children.copy()
        children = []
        for magic in range(0, k, 2):
            p1, p2 = pop[magic], pop[magic + 1]
            child1 = cross(p1, p2, dimension)
            child2 = cross(p2, p1, dimension)
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            rewrite_score(child1, dimension)
            rewrite_score(child2, dimension)
            children.append(child1)
            children.append(child2)
        pop = children.copy()
    best_route = find_best(pop, k, dimension)
    true_form(best_route, dimension)
    return best_route



if __name__ == '__main__':
    cities_set = []
    cities_tups = []
    file_data = "ulysses16.tsp"
    k = 100
    z = 100
    #Stworzenie nie edytowalnej listy z miastami
    dimension = produce_final(file_data)
    dimension = int(dimension)
    #stworzenie listy dystansów
    distance_matrix = create_matrix_of_distance(dimension)
    with open('wyniki.txt', 'w') as f:
        sys.stdout = f
        for i in range(0, 10):
            print(route_finder(k, dimension))
        f.close()