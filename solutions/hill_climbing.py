from helpers import draw
from libraries.cg_lib import diagonal_difference, in_convex_square, Edge
from random import choice


def flip_edge(reconstructed_edges, edge):
    lr_edge = next(
        x_edge for x_edge in reconstructed_edges if x_edge.flat_eq(Edge(edge.tail, edge.incident_dots[1])))
    if len(lr_edge.incident_dots):
        lr_incident_dot_index = lr_edge.incident_dots.index(edge.head)
        lr_edge.incident_dots[lr_incident_dot_index] = edge.incident_dots[0]
    ll_edge = next(
        x_edge for x_edge in reconstructed_edges if x_edge.flat_eq(Edge(edge.tail, edge.incident_dots[0])))
    if len(ll_edge.incident_dots):
        ll_incident_dot_index = ll_edge.incident_dots.index(edge.head)
        ll_edge.incident_dots[ll_incident_dot_index] = edge.incident_dots[1]
    ul_edge = next(
        x_edge for x_edge in reconstructed_edges if x_edge.flat_eq(Edge(edge.head, edge.incident_dots[0])))
    if len(ul_edge.incident_dots):
        ul_incident_dot_index = ul_edge.incident_dots.index(edge.tail)
        ul_edge.incident_dots[ul_incident_dot_index] = edge.incident_dots[1]
    ur_edge = next(
        x_edge for x_edge in reconstructed_edges if x_edge.flat_eq(Edge(edge.head, edge.incident_dots[1])))
    if len(ur_edge.incident_dots):
        ur_incident_dot_index = ur_edge.incident_dots.index(edge.tail)
        ur_edge.incident_dots[ur_incident_dot_index] = edge.incident_dots[0]
    edge.tail, edge.incident_dots[0] = edge.incident_dots[0], edge.tail
    edge.head, edge.incident_dots[1] = edge.incident_dots[1], edge.head


def first_choice_hill_climbing(reconstructed_edges, init_weight):
    temp_mwt_weight = init_weight
    while True:
        solution_improved = False
        for edge in reconstructed_edges:
            if len(edge.incident_dots) == 0:
                continue
            # # Begin of debugging related
            # edge_flipped = False
            # draw.turtle.color('red')
            # edge.draw()
            # # End of debugging related
            diagonal_diff = diagonal_difference(edge)
            if in_convex_square(edge) and diagonal_diff >= 0:
                # # Begin of debugging related
                # edge_flipped = True
                # draw.turtle.color('white')
                # edge.draw()
                # # End of debugging related
                flip_edge(reconstructed_edges, edge)
                # # Begin of debugging related
                # draw.turtle.color('black')
                # edge.draw()
                # # End of debugging related
                temp_mwt_weight -= diagonal_diff
                solution_improved = True
            # # Begin of debugging related
            # if not edge_flipped:
            #     draw.turtle.color('black')
            #     edge.draw()
            # # End of debugging related
        if not solution_improved:
            break
    return temp_mwt_weight


def greedy_choice_hill_climbing(reconstructed_edges, init_weight):
    temp_mwt_weight = init_weight
    while True:
        diagonal_diff = 0
        greedy_edge = None
        for edge in reconstructed_edges:
            if len(edge.incident_dots) == 0:
                continue
            temp_diagonal_diff = diagonal_difference(edge)
            if in_convex_square(edge) and temp_diagonal_diff >= diagonal_diff:
                diagonal_diff = temp_diagonal_diff
                greedy_edge = edge
        if greedy_edge:
            flip_edge(reconstructed_edges, greedy_edge)
            temp_mwt_weight -= diagonal_diff
        else:
            break
    return temp_mwt_weight


def stochastic_choice_hill_climbing(reconstructed_edges, init_weight):
    temp_mwt_weight = init_weight
    while True:
        edge_candidates = []
        for edge in reconstructed_edges:
            if len(edge.incident_dots) == 0:
                continue
            diagonal_diff = diagonal_difference(edge)
            if in_convex_square(edge) and diagonal_diff >= 0:
                edge_candidates.append(edge)
        if len(edge_candidates):
            random_valid_edge = choice(edge_candidates)
            temp_mwt_weight -= diagonal_difference(random_valid_edge)
            flip_edge(reconstructed_edges, random_valid_edge)
        else:
            break
    return temp_mwt_weight
