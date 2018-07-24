#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

.. autosummary::
    :toctree: generated/

    f_measure
    precision
    recall
    
    accuracy
    accuracy2
    balanced_accuracy
    sensitivity
    specificity

    error_rate
    substitution_rate
    deletion_rate
    insertion_rate

    equal_error_rate

"""

import numpy


# -- F-measure -- #
def precision(Ntp, Nsys, eps=numpy.spacing(1)):
    """Precision.

    Wikipedia entry https://en.wikipedia.org/wiki/Precision_and_recall

    Parameters
    ----------
    Ntp : int >=0
        Number of true positives.

    Nsys : int >=0
        Amount of system output.

    eps : float
        eps.
        Default value numpy.spacing(1)

    Returns
    -------
    precision: float
        Precision

    """

    if Nsys == 0:
        return numpy.nan
    else:
        return float(Ntp / float(Nsys))


def recall(Ntp, Nref, eps=numpy.spacing(1)):
    """Recall.

    Wikipedia entry https://en.wikipedia.org/wiki/Precision_and_recall

    Parameters
    ----------
    Ntp : int >=0
        Number of true positives.

    Nref : int >=0
        Amount of reference.

    eps : float
        eps.
        Default value numpy.spacing(1)

    Returns
    -------
    recall: float
        Recall

    """

    if Nref == 0:
        return numpy.nan
    else:
        return float(Ntp / float(Nref))


def f_measure(precision, recall, beta=1.0):
    """F-measure from precision and recall scores.

    Wikipedia entry https://en.wikipedia.org/wiki/F1_score

    Parameters
    ----------
    precision : float in (0, 1]
        Precision.

    recall : float in (0, 1]
        Recall.

    beta : float > 0
        Weighting factor for f-measure.
        Default value 1.0

    Returns
    -------
    f_measure: float
        The weighted f-measure

    """

    if precision == 0 and recall == 0:
        return 0.0

    return float((1 + beta**2)*precision*recall/((beta**2)*precision + recall))


# -- Accuracy -- #
def sensitivity(Ntp, Nfn, eps=numpy.spacing(1)):
    """Sensitivity

    Wikipedia entry https://en.wikipedia.org/wiki/Sensitivity_and_specificity

    Parameters
    ----------
    Ntp : int >=0
        Number of true positives.

    Nfn : int >=0
        Number of false negatives.

    eps : float
        eps.
        Default value numpy.spacing(1)

    Returns
    -------
    sensitivity: float
        Sensitivity

    """

    return float(Ntp / (Ntp + Nfn + eps))


def specificity(Ntn, Nfp, eps=numpy.spacing(1)):
    """Specificity

    Wikipedia entry https://en.wikipedia.org/wiki/Sensitivity_and_specificity

    Parameters
    ----------
    Ntn : int >= 0
        Number of true negatives.

    Nfp : int >= 0
        Number of false positives.
    
    eps : float
        eps.
        Default value numpy.spacing(1)

    Returns
    -------
    specificity: float
        Specificity

    """

    return float(Ntn / (Ntn + Nfp + eps))


def balanced_accuracy(sensitivity, specificity, factor=0.5):
    """Balanced accuracy

    Wikipedia entry https://en.wikipedia.org/wiki/Accuracy_and_precision

    Parameters
    ----------
    sensitivity : float in [0, 1]
        sensitivity.

    specificity : float in [0, 1]
        specificity.

    factor : float in [0, 1]
        Balancing factor multiplying true positive rate (sensitivity).
        Default value 0.5

    Returns
    -------
    bacc: float
        Balanced accuracy

    """

    return float(((1-factor) * sensitivity) + (factor * specificity))


def accuracy(Ntp, Ntn, Nfp, Nfn, eps=numpy.spacing(1)):
    """Accuracy

    Parameters
    ----------
    Ntp : int >= 0
        Number of true positives.

    Ntn : int >= 0
        Number of true negatives.

    Nfp : int >= 0
        Number of false positives.

    Nfn : int >= 0
        Number of false negatives.

    eps : float
        eps.
        Default value numpy.spacing(1)

    Returns
    -------
    acc: float
        Accuracy

    """

    return float((Ntp + Ntn) / (Ntp + Ntn + Nfn + Nfp + eps))


def accuracy_corr(Ncorr, N, eps=numpy.spacing(1)):
    """Accuracy

    Parameters
    ----------
    Ncorr : int >= 0
        Number of correct items.

    N : int >= 0
        Number of all items.

    eps : float
        eps.
        Default value numpy.spacing(1)

    Returns
    -------
    acc: float
        Accuracy.

    """

    return float((Ncorr) / (N + eps))


def accuracy2(Ntp, Nfp, Nfn, eps=numpy.spacing(1)):
    """Accuracy

    Implements metric described by [1]_.

    .. [1] Dixon, S.
           "On the computer recognition of solo piano music".
           Proceedings of Australasian Computer Music Conference, July 2000, Brisbane, Australia, pp. 31–37.
           http://www.eecs.qmul.ac.uk/~simond/pub/2000/acmc.pdf

    Parameters
    ----------
    Ntp : int >= 0
        Number of true positives.

    Nfp : int >= 0
        Number of false positives.

    Nfn : int >= 0
        Number of false negatives.

    eps : float
        eps.
        Default value numpy.spacing(1)

    Returns
    -------
    acc: float
        Accuracy

    """

    return float((Ntp) / (Ntp + Nfn + Nfp + eps))


def substitution_rate(Nref, Nsubstitutions, eps=numpy.spacing(1)):
    """Substitution rate

    Parameters
    ----------
    Nref : int >=0
        Number of entries in the reference.

    Nsubstitutions : int >=0
        Number of substitutions.

    eps : float
        eps.
        Default value numpy.spacing(1)

    Returns
    -------
    substitution_rate: float
        Substitution rate

    """

    return float(Nsubstitutions / (Nref + eps))


def deletion_rate(Nref, Ndeletions, eps=numpy.spacing(1)):
    """Deletion rate

    Parameters
    ----------
    Nref : int >=0
        Number of entries in the reference.

    Ndeletions : int >=0
        Number of deletions.

    eps : float
        eps.
        Default value numpy.spacing(1)

    Returns
    -------
    deletion_rate: float
        Deletion rate
        
    """

    return float(Ndeletions / (Nref + eps))


def insertion_rate(Nref, Ninsertions, eps=numpy.spacing(1)):
    """Insertion rate

    Parameters
    ----------
    Nref : int >=0
        Number of entries in the reference.

    Ninsertions : int >=0
        Number of insertions.

    eps : float
        eps.
        Default value numpy.spacing(1)

    Returns
    -------
    insertion_rate: float
        Insertion rate

    """

    return float(Ninsertions / (Nref + eps))


def error_rate(substitution_rate_value=0.0, deletion_rate_value=0.0, insertion_rate_value=0.0):
    """Error rate

    Parameters
    ----------
    substitution_rate_value : float >=0
        Substitution rate.
        Default value 0

    deletion_rate_value : float >=0
        Deletion rate.
        Default value 0

    insertion_rate_value : float >=0
        Insertion rate.
        Default value 0

    Returns
    -------
    error_rate: float
        Error rate

    """

    return float(substitution_rate_value + deletion_rate_value + insertion_rate_value)


def equal_error_rate(y_true, y_score, eps=numpy.spacing(1)):
    """Equal error rate (EER)

    EER is calculated from the curve of the false negative rate versus the false positive rate.
    Implementation is based on https://github.com/pafoster/dcase2016_task4/blob/master/evaluation_scripts/eer.py

    Parameters
    ----------
    y_true : numpy.array or list
        True binary labels in range {0, 1} or {-1, 1}.

    y_score : numpy.array or list
        Target scores, can either be probability estimates of the positive
        class or confidence values.

    eps : float
        Minimum difference considered equal.
        Default value numpy.spacing(1)

    Returns
    -------
    float

    """

    from sklearn import metrics

    if numpy.any(y_true):
        false_positive_rate, true_positive_rate, thresholds = metrics.roc_curve(
            y_true=y_true,
            y_score=y_score,
            drop_intermediate=True
        )

        points = [(0, 0)] + list(zip(false_positive_rate, true_positive_rate))
        for i, point in enumerate(points):
            if point[0] + eps >= 1 - point[1]:
                break

        point1 = points[i - 1]
        point2 = points[i]

        # Interpolate between point1 and point2
        if abs(point2[0] - point1[0]) < eps:
            eer = point1[0]

        else:
            m = (point2[1] - point1[1]) / (point2[0] - point1[0])
            o = point1[1] - m * point1[0]
            eer = (1 - o) / (1 + m)

    else:
        eer = numpy.nan

    return eer
