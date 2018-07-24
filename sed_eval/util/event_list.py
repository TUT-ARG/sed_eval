#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Event list handling
"""

import dcase_util

__all__ = ['filter_event_list',
           'unique_files',
           'unique_event_labels',
           'max_event_offset']


def filter_event_list(event_list, scene_label=None, event_label=None, filename=None):
    """Filter event list based on given fields

    Parameters
    ----------
    event_list : list, shape=(n,)
        A list containing event dicts

    scene_label : str
        Scene label

    event_label : str
        Event label

    filename : str
        Filename

    Returns
    -------
    event_list: list, shape=(n,)
        A list containing event dicts

    """

    return dcase_util.containers.MetaDataContainer(event_list).filter(
        filename=filename,
        scene_label=scene_label,
        event_label=event_label
    )


def unique_files(event_list):
    """Find the unique files

    Parameters
    ----------
    event_list : list or dcase_util.containers.MetaDataContainer
        A list containing event dicts

    Returns
    -------
    list
        Unique filenames in alphabetical order

    """

    if isinstance(event_list, dcase_util.containers.MetaDataContainer):
        return event_list.unique_files

    else:
        files = {}
        for event in event_list:
            if 'file' in event:
                files[event['file']] = event['file']

            elif 'filename' in event:
                files[event['filename']] = event['filename']

        files = list(files.keys())
        files.sort()
        return files


def unique_event_labels(event_list):
    """Find the unique event labels

    Parameters
    ----------
    event_list : list or dcase_util.containers.MetaDataContainer
        A list containing event dicts

    Returns
    -------
    list
        Unique labels in alphabetical order

    """

    if isinstance(event_list, dcase_util.containers.MetaDataContainer):
        return event_list.unique_event_labels

    else:
        labels = []
        for event in event_list:
            if 'event_label' in event and event['event_label'] not in labels:
                labels.append(event['event_label'])

        labels.sort()
        return labels


def max_event_offset(event_list):
    """Find the offset (end-time) of last event

    Parameters
    ----------
    event_list : list or dcase_util.containers.MetaDataContainer
        A list containing event dicts

    Returns
    -------
    float > 0
        maximum offset

    """

    if isinstance(event_list, dcase_util.containers.MetaDataContainer):
        return event_list.max_offset

    else:
        max_offset = 0
        for event in event_list:
            if 'event_offset' in event:
                if event['event_offset'] > max_offset:
                    max_offset = event['event_offset']

            elif 'offset' in event:
                if event['offset'] > max_offset:
                    max_offset = event['offset']

        return max_offset
