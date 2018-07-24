#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Event matching
"""

def bipartite_match(graph):
    """
    Find maximum cardinality matching of a bipartite graph (U,V,E).
    Function is borrowed from mir_eval toolbox (https://github.com/craffel/mir_eval).

    The input format is a dictionary mapping members of U to a list of their neighbors in V.
    The output is a dict M mapping members of V to their matches in U.

    Parameters
    ----------
    graph : dictionary : left-vertex -> list of right vertices
        The input bipartite graph.  Each edge need only be specified once.

    Returns
    -------
    matching : dictionary : right-vertex -> left vertex
        A maximal bipartite matching.

    """
    # Implementation is after _bipartite_match function in mir_eval toolbox:
    # Colin Raffel, Brian McFee, Eric J. Humphrey, Justin Salamon, Oriol Nieto, Dawen Liang,
    # and Daniel P. W. Ellis, "mir_eval: A Transparent Implementation of Common MIR Metrics",
    # Proceedings of the 15th International Conference on Music Information Retrieval, 2014.
    #
    # _bipartite_match function:
    # https://github.com/craffel/mir_eval/blob/master/mir_eval/util.py#L547
    #
    # Function is originally adapted from:
    #
    # Hopcroft-Karp bipartite max-cardinality matching and max independent set
    # David Eppstein, UC Irvine, 27 Apr 2002

    # initialize greedy matching (redundant, but faster than full search)
    matching = {}
    for u in graph:
        for v in graph[u]:
            if v not in matching:
                matching[v] = u
                break

    while True:
        # structure residual graph into layers
        # pred[u] gives the neighbor in the previous layer for u in U
        # preds[v] gives a list of neighbors in the previous layer for v in V
        # unmatched gives a list of unmatched vertices in final layer of V,
        # and is also used as a flag value for pred[u] when u is in the first
        # layer

        preds = {}
        unmatched = []
        pred = dict([(u, unmatched) for u in graph])

        for v in matching:
            del pred[matching[v]]

        layer = list(pred)

        # repeatedly extend layering structure by another pair of layers
        while layer and not unmatched:
            new_layer = {}
            for u in layer:
                for v in graph[u]:
                    if v not in preds:
                        new_layer.setdefault(v, []).append(u)

            layer = []
            for v in new_layer:
                preds[v] = new_layer[v]

                if v in matching:
                    layer.append(matching[v])
                    pred[matching[v]] = v

                else:
                    unmatched.append(v)

        # did we finish layering without finding any alternating paths?
        if not unmatched:
            unlayered = {}
            for u in graph:
                for v in graph[u]:
                    if v not in preds:
                        unlayered[v] = None

            return matching

        def recurse(v):
            """Recursively search backward through layers to find alternating
            paths.  recursion returns true if found path, false otherwise
            """

            if v in preds:
                L = preds[v]
                del preds[v]
                for u in L:
                    if u in pred:
                        pu = pred[u]
                        del pred[u]
                        if pu is unmatched or recurse(pu):
                            matching[v] = u
                            return True

            return False

        for v in unmatched:
            recurse(v)