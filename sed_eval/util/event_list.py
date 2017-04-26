#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Event list handling
"""

__all__ = ['EventList',
           'unique_event_labels',
           'max_event_offset']


class EventList(list):
    def __init__(self, *args):
        """Constructor

        This class is inherited from list class.

        Returns
        -------
            Nothing

        """
        list.__init__(self, *args)

    @property
    def valid_event_list(self):
        if len(self) > 0:
            if 'event_label' in self[0] and 'event_onset' in self[0] and 'event_offset' in self[0]:
                return True
            else:
                return False
        else:
            return False

    @property
    def event_count(self):
        """Get number of events

        Returns
        -------
        event_count: integer > 0

        """

        if self.valid_event_list:
            return len(self)

    @property
    def event_label_count(self):
        """Get number of unique event labels

        Returns
        -------
        event_label_count: float > 0

        """

        if self.valid_event_list:
            return len(self.unique_event_labels)

    @property
    def unique_event_labels(self):
        """Get unique event labels

        Returns
        -------
        labels: list, shape=(n,)
            Unique labels in alphabetical order

        """

        if self.valid_event_list:
            return unique_event_labels(event_list=self)
        else:
            return []

    @property
    def unique_files(self):
        """Get unique files

        Returns
        -------
        labels: list, shape=(n,)
            Unique files in alphabetical order

        """

        if self.valid_event_list:
            return unique_files(event_list=self)
        else:
            return []

    @property
    def max_event_offset(self):
        """Find the offset (end-time) of last event

        Returns
        -------
        max_offset: float > 0
            maximum offset

        """

        if self.valid_event_list:
            return max_event_offset(event_list=self)

    def filter(self, scene_label=None, event_label=None, file=None):
        """Filter event list based on given fields

        Parameters
        ----------
        event_list : list, shape=(n,)
            A list containing event dicts
        scene_label : str
            Scene label
        event_label : str
            Event label
        file : str
            Filename

        Returns
        -------
        event_list: list, shape=(n,)
            A list containing event dicts

        """

        if self.valid_event_list:
            return filter_event_list(
                event_list=self,
                scene_label=scene_label,
                event_label=event_label,
                file=file
            )

    def filter_event_list(self, scene_label=None, event_label=None, file=None):
        self.filter(scene_label=scene_label, event_label=event_label, file=file)

def filter_event_list(event_list, scene_label=None, event_label=None, file=None):
    """Filter event list based on given fields

    Parameters
    ----------
    event_list : list, shape=(n,)
        A list containing event dicts
    scene_label : str
        Scene label
    event_label : str
        Event label
    file : str
        Filename

    Returns
    -------
    event_list: list, shape=(n,)
        A list containing event dicts

    """

    filtered_event_list = EventList()
    for event in event_list:
        matched = False
        if event_label is not None and 'event_label' in event and event['event_label'] == event_label:
            matched = True
        if scene_label is not None and 'scene_label' in event and event['scene_label'] == scene_label:
            matched = True
        if file is not None and 'file' in event and event['file'] == file:
            matched = True
        if matched:
            filtered_event_list.append(event)
    return filtered_event_list

def unique_files(event_list):
    """Find the unique files

    Parameters
    ----------
    event_list : list, shape=(n,)
        A list containing event dicts

    Returns
    -------
    file_list: list, shape=(n,)
        Unique filenames in alphabetical order

    """

    files = {}
    for event in event_list:
        if 'file' in event:
            files[event['file']] = event['file']

    files = list(files.keys())
    files.sort()
    return files


def unique_event_labels(event_list):
    """Find the unique event labels

    Parameters
    ----------
    event_list : list, shape=(n,)
        A list containing event dicts

    Returns
    -------
    labels: list, shape=(n,)
        Unique labels in alphabetical order

    """

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
    event_list : list, shape=(n,)
        A list containing event dicts

    Returns
    -------
    max_offset: float > 0
        maximum offset

    """

    max_offset = 0
    for event in event_list:
        if event['event_offset'] > max_offset:
            max_offset = event['event_offset']
    return max_offset