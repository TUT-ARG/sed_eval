#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Scene list handling
"""

import dcase_util

__all__ = ['unique_scene_labels']


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
    if isinstance(scene_list, dcase_util.containers.MetaDataContainer):
        return scene_list.unique_scene_labels

    else:
        labels = []
        for item in scene_list:
            if 'scene_label' in item and item['scene_label'] not in labels:
                labels.append(item['scene_label'])

        labels.sort()
        return labels

