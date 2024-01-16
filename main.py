import numpy as np
import random

# Python Version: 3.11.5
# How to execute: python3 main.py

# Randomly colors nodes
# on each iterations there are 4 steps:
# 1) broadcast the permanent colors
# 2) randomly select color out of pool, that none of the neighbours have (in the previous iteration)
# 3) check if a neighbour has the same color as the node if so add to reset_v
# 4) resets colors if same color in the same iteration
def coloring_function(V, E, max_degree):
    permanent_C = np.zeros(V, dtype=int)

    counter = 0
    possible_value = np.empty(V, dtype=set)

    # For each vertex generate a set of all possible colors, that none of the neighbours has
    for i in range(V):
        possible_value[i] = set(range(1, max_degree + 2))

    while np.any(permanent_C == 0):
        CL = np.copy(permanent_C)

        # broadcast neighbours the permanent color
        for v, u_list in enumerate(E):
            for u in u_list:
                possible_value[u].discard(v)

        # Choose random color that none of the neighbours had in the previous iterations
        for v in range(0, V):
            if not permanent_C[v]:
                CL[v] = random.choice(list(possible_value[v]))

        # Compare color with neighbours
        reset_v = set()
        for v, u_list in enumerate(E):
            if not permanent_C[v]:
                for u in u_list:
                    if CL[v] == CL[u]:
                        reset_v.add(v)

        # Reset values
        for v in reset_v:
            CL[v] = 0

        # Make coloring permanent
        permanent_C = CL
        counter += 1

    print("It took " + str(counter) + " iterations to color the graph!")

    return permanent_C


# Checks if two neighbouring nodes have same color (share the same edge)
def check_coloring(E, C, max_degree):
    for v, u_list in enumerate(E):
        assert (C[v] <= max_degree + 1)
        for u in u_list:
            assert (C[u] != C[v])
    print("Test was successful\n")


# Dynamically generates random Testcases and checks coloring
def generate_test_cases():
    for i in range(1, 100, 10):
        # max possible degree in this iteration
        possible_max_degree = random.randint(i, 2 * i + 1)

        print("Possible Max Degree: " + str(possible_max_degree))

        # Nr. of vertices
        vertices = random.randint(possible_max_degree + 1, (possible_max_degree + 1) ** 2)

        #sets up edge datastructure
        edges = np.empty(vertices, dtype=set)
        for j in range(0, vertices):
            edges[j] = set()

        vertex_counter = np.zeros(vertices, dtype=int)
        edge_counter = 0

        #generates edges randomly
        for j in range(0, (i + 1) ** 3):
            v = random.randint(0, vertices - 1)
            u = random.randint(0, vertices - 1)

            # skip if edge is to itself
            if u == v:
                continue

            # add edge if edge count of u and v are below possible max degree and the edge is not already included
            if u not in edges[v] and vertex_counter[u] < possible_max_degree and vertex_counter[v] < possible_max_degree:
                edges[v].add(u)
                edges[u].add(v)
                vertex_counter[u] += 1
                vertex_counter[v] += 1
                edge_counter += 1

        # the maximum generate edge degree previously generated
        max_degree = max(vertex_counter)
        print("Max Degree: " + str(max_degree) + " | Vertices: " + str(vertices))
        print("Graph has in total: " + str(edge_counter) + " edges.")
        # Coloring
        C = coloring_function(vertices, edges, max_degree)

        # Check if coloring is correct
        check_coloring(edges, C, max_degree)

if __name__ == '__main__':
    generate_test_cases()

