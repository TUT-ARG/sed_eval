#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy


def event_detection(feature_data, model_container, hop_length_seconds=0.01, smoothing_window_length_seconds=1.0, decision_threshold=0.0, minimum_event_length=0.1, minimum_event_gap=0.1):
    """Sound event detection

    Parameters
    ----------
    feature_data : numpy.ndarray [shape=(n_features, t)]
        Feature matrix

    model_container : dict
        Sound event model pairs [positive and negative] in dict

    hop_length_seconds : float > 0.0
        Feature hop length in seconds, used to convert feature index into time-stamp
        (Default value=0.01)

    smoothing_window_length_seconds : float > 0.0
        Accumulation window (look-back) length, withing the window likelihoods are accumulated.
        (Default value=1.0)

    decision_threshold : float > 0.0
        Likelihood ratio threshold for making the decision.
        (Default value=0.0)

    minimum_event_length : float > 0.0
        Minimum event length in seconds, shorten than given are filtered out from the output.
        (Default value=0.1)

    minimum_event_gap : float > 0.0
        Minimum allowed gap between events in seconds from same event label class.
        (Default value=0.1)

    Returns
    -------
    results : list (event dicts)
        Detection result, event list

    """

    smoothing_window = int(smoothing_window_length_seconds / hop_length_seconds)

    results = []
    for event_label in model_container['models']:
        positive = model_container['models'][event_label]['positive'].score_samples(feature_data)[0]
        negative = model_container['models'][event_label]['negative'].score_samples(feature_data)[0]

        # Lets keep the system causal and use look-back while smoothing (accumulating) likelihoods
        for stop_id in range(0, feature_data.shape[0]):
            start_id = stop_id - smoothing_window
            if start_id < 0:
                start_id = 0
            positive[start_id] = sum(positive[start_id:stop_id])
            negative[start_id] = sum(negative[start_id:stop_id])

        likelihood_ratio = positive - negative
        event_activity = likelihood_ratio > decision_threshold

        # Find contiguous segments and convert frame-ids into times
        event_segments = contiguous_regions(event_activity) * hop_length_seconds

        # Preprocess the event segments
        event_segments = postprocess_event_segments(event_segments=event_segments,
                                                   minimum_event_length=minimum_event_length,
                                                   minimum_event_gap=minimum_event_gap)

        for event in event_segments:
            results.append((event[0], event[1], event_label))

    return results


def contiguous_regions(activity_array):
    """Find contiguous regions from bool valued numpy.array.
    Transforms boolean values for each frame into pairs of onsets and offsets.

    Parameters
    ----------
    activity_array : numpy.array [shape=(t)]
        Event activity array, bool values

    Returns
    -------
    change_indices : numpy.ndarray [shape=(2, number of found changes)]
        Onset and offset indices pairs in matrix

    """

    # Find the changes in the activity_array
    change_indices = numpy.diff(activity_array).nonzero()[0]

    # Shift change_index with one, focus on frame after the change.
    change_indices += 1

    if activity_array[0]:
        # If the first element of activity_array is True add 0 at the beginning
        change_indices = numpy.r_[0, change_indices]

    if activity_array[-1]:
        # If the last element of activity_array is True, add the length of the array
        change_indices = numpy.r_[change_indices, activity_array.size]

    # Reshape the result into two columns
    return change_indices.reshape((-1, 2))


def postprocess_event_segments(event_segments, minimum_event_length=0.1, minimum_event_gap=0.1):
    """Post process event segment list. Makes sure that minimum event length and minimum event gap conditions are met.

    Parameters
    ----------
    event_segments : numpy.ndarray [shape=(2, number of event)]
        Event segments, first column has the onset, second has the offset.

    minimum_event_length : float > 0.0
        Minimum event length in seconds, shorten than given are filtered out from the output.
        (Default value=0.1)

    minimum_event_gap : float > 0.0
        Minimum allowed gap between events in seconds from same event label class.
        (Default value=0.1)

    Returns
    -------
    event_results : numpy.ndarray [shape=(2, number of event)]
        postprocessed event segments

    """

    # 1. remove short events
    event_results_1 = []
    for event in event_segments:
        if event[1]-event[0] >= minimum_event_length:
            event_results_1.append((event[0], event[1]))

    if len(event_results_1):
        # 2. remove small gaps between events
        event_results_2 = []

        # Load first event into event buffer
        buffered_event_onset = event_results_1[0][0]
        buffered_event_offset = event_results_1[0][1]
        for i in range(1,len(event_results_1)):
            if event_results_1[i][0] - buffered_event_offset > minimum_event_gap:
                # The gap between current event and the buffered is bigger than minimum event gap,
                # store event, and replace buffered event
                event_results_2.append((buffered_event_onset, buffered_event_offset))
                buffered_event_onset = event_results_1[i][0]
                buffered_event_offset = event_results_1[i][1]
            else:
                # The gap between current event and the buffered is smalle than minimum event gap,
                # extend the buffered event until the current offset
                buffered_event_offset = event_results_1[i][1]

        # Store last event from buffer
        event_results_2.append((buffered_event_onset, buffered_event_offset))

        return event_results_2
    else:
        return event_results_1
