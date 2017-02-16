#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Event roll handling

"""
from __future__ import absolute_import
import math
import numpy
from . import event_list


def event_list_to_event_roll(source_event_list, event_label_list=None, time_resolution=0.01):
    """Convert event list into event roll, binary activity matrix

    Parameters
    ----------
    source_event_list : list, shape=(n,)
        A list containing event dicts
    event_label_list : list, shape=(k,) or None
        A list of containing unique labels in alphabetical order
        (Default value = None)
    time_resolution : float > 0
        Time resolution in seconds of the event roll
        (Default value = 0.01)

    Returns
    -------
    event_roll: np.ndarray, shape=(m,k)
        Event roll

    """

    max_offset_value = event_list.max_event_offset(source_event_list)

    if event_label_list is None:
        event_label_list = event_list.unique_event_labels(source_event_list)

    # Initialize event roll
    event_roll = numpy.zeros((int(math.ceil(max_offset_value * 1 / time_resolution)), len(event_label_list)))

    # Fill-in event_roll
    for event in source_event_list:
        pos = event_label_list.index(event['event_label'])

        onset = int(math.floor(event['event_onset'] * 1 / time_resolution))
        offset = int(math.ceil(event['event_offset'] * 1 / time_resolution))

        event_roll[onset:offset, pos] = 1

    return event_roll


def pad_event_roll(event_roll, length):
    """Pad event roll's length to given length

    Parameters
    ----------
    event_roll: np.ndarray, shape=(m,k)
        Event roll
    length : int
        Length to be padded

    Returns
    -------
    event_roll: np.ndarray, shape=(m,k)
        Padded event roll

    """

    if length > event_roll.shape[0]:
        padding = numpy.zeros((length-event_roll.shape[0], event_roll.shape[1]))
        event_roll = numpy.vstack((event_roll, padding))

    return event_roll


def match_event_roll_lengths(event_roll_a, event_roll_b):
    """Fix the length of two event rolls

    Parameters
    ----------
    event_roll_a: np.ndarray, shape=(m1,k)
        Event roll A
    event_roll_b: np.ndarray, shape=(m2,k)
        Event roll B

    Returns
    -------
    event_roll_a: np.ndarray, shape=(max(m1,m2),k)
        Padded event roll A
    event_roll_b: np.ndarray, shape=(max(m1,m2),k)
        Padded event roll B

    """

    # Fix durations of both event_rolls to be equal
    event_roll_a = pad_event_roll(event_roll=event_roll_a, length=event_roll_b.shape[0])
    event_roll_b = pad_event_roll(event_roll=event_roll_b, length=event_roll_a.shape[0])

    return event_roll_a, event_roll_b

