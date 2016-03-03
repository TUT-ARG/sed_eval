#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Scene list handling
"""

__all__ = ['SceneList',
           'unique_scene_labels']

class SceneList(list):
    def __init__(self, *args):
        """Constructor

        This class is inherited from list class.

        Returns
        -------
            Nothing

        """
        list.__init__(self, *args)

    @property
    def valid_scene_list(self):
        if 'scene_label' in self[0]:
            return True
        else:
            return False

    @property
    def scene_count(self):
        """Get number of scene segments

        Returns
        -------
        scene_count: integer > 0

        """

        if self.valid_scene_list:
            return len(self)

    @property
    def scene_label_count(self):
        """Get number of unique scene labels

        Returns
        -------
        scene_label_count: float > 0

        """

        if self.valid_scene_list:
            return len(self.unique_scene_labels)

    @property
    def unique_scene_labels(self):
        """Get unique scene labels

        Returns
        -------
        labels: list, shape=(n,)
            Unique labels in alphabetical order

        """

        if self.valid_scene_list:
            return unique_scene_labels(self)


def unique_scene_labels(scene_list):
    """Find the unique scene labels

    Parameters
    ----------
    scene_list : list, shape=(n,)
        A list containing scene dicts

    Returns
    -------
    labels: list, shape=(n,)
        Unique labels in alphabetical order

    """

    labels = []
    for item in scene_list:
        if 'scene_label' in item and item['scene_label'] not in labels:
            labels.append(item['scene_label'])

    labels.sort()
    return labels

