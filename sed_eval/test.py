#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

.. autosummary::
    :toctree: generated/

    mcnemar

"""

import numpy


def mcnemar(reference, estimated_a, estimated_b):
    """McNemar's test

    Wikipedia entry https://en.wikipedia.org/wiki/McNemar%27s_test

    Parameters
    ----------
    reference : list
        Reference value

    estimated_a : list
        System output A

    estimated_b : list
        System output B

    Returns
    -------
    float
        exact P-value

    """

    if len(reference) != len(estimated_a) or len(reference) != len(estimated_b):
        raise ValueError('Input arrays needs to be same length.')

    # Convert lists into numpy.array
    reference = numpy.array(reference)
    estimated_a = numpy.array(estimated_a)
    estimated_b = numpy.array(estimated_b)

    # Intermediate values
    correct_a = estimated_a == reference
    correct_b = estimated_b == reference

    incorrect_a = estimated_a != reference
    incorrect_b = estimated_b != reference

    # Contingency table values
    b = float( numpy.sum( numpy.logical_and(incorrect_a, correct_b) ) )
    c = float( numpy.sum( numpy.logical_and(correct_a, incorrect_b) ) )

    # Continuity corrected version of the McNemar test to approximate the binomial exact-P-value
    # Edwards, A (1948). "Note on the "correction for continuity" in testing the significance of the difference
    # between correlated proportions". Psychometrika. 13: 185–187
    if b + c > 0:
        return (numpy.abs(b - c) - 1)**2 / (b + c)
    else:
        return 0
