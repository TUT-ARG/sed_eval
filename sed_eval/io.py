#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
I/O
==================
Functions for loading annotations from files in various formats.

.. autosummary::
    :toctree: generated/

    load_event_list
    load_scene_list
    load_file_pair_list

"""

from __future__ import absolute_import
from . import util
import csv
import os


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def load_event_list(filename):
    """Load event list from csv formatted text-file

    Supported formats:

    - [event onset (float >= 0)][delimiter][event offset (float >= 0)]
    - [event onset (float >= 0)][delimiter][event offset (float >= 0)][delimiter][label]
    - [filename][delimiter][event onset (float >= 0)][delimiter][event offset (float >= 0)][delimiter][event label]
    - [filename][delimiter][scene_label][delimiter][event onset (float >= 0)][delimiter][event offset (float >= 0)][delimiter][event label]
    - [filename]

    Supported delimiters: ``,``, ``;``, ``tab``

    Example of event list file::

        21.64715	23.00552	alert
        36.91184	38.27021	alert
        69.72575	71.09029	alert
        63.53990	64.89827	alert
        84.25553	84.83920	alert
        20.92974	21.82661	clearthroat
        28.39992	29.29679	clearthroat
        80.47837	81.95937	clearthroat
        44.48363	45.96463	clearthroat
        78.13073	79.05953	clearthroat
        15.17031	16.27235	cough
        20.54931	21.65135	cough
        27.79964	28.90168	cough
        75.45959	76.32490	cough
        70.81708	71.91912	cough
        21.23203	22.55902	doorslam
        7.546220	9.014880	doorslam
        34.11303	35.04183	doorslam
        45.86001	47.32867	doorslam


    Parameters
    ----------
    filename : str
        Path to the csv-file

    Returns
    -------
    event_list: list
        Event list

    """

    data = []
    file_open = False
    if hasattr(filename, 'read'):
        input_file = filename
    else:
        input_file = open(filename, 'rt')
        file_open = True
        if os.path.getsize(filename) == 0:
            return util.event_list.EventList(data)

    try:
        dialect = csv.Sniffer().sniff(input_file.readline(), [',', ';', '\t'])
    except csv.Error:
        raise ValueError('Unknown delimiter in file [{file}].'.format(file=filename))

    input_file.seek(0)

    for row in csv.reader(input_file, dialect):
        if len(row):
            if len(row) == 2:
                if not isfloat(row[0]) or not isfloat(row[1]):
                    raise ValueError('Event onset and event offset needs to be float in file [{file}].'.format(file=filename))

                data.append(
                    {
                        'event_onset': float(row[0]),
                        'event_offset': float(row[1])
                    }
                )

            elif len(row) == 3:
                if not isfloat(row[0]) or not isfloat(row[1]):
                    raise ValueError('Event onset and event offset needs to be float in file [{file}].'.format(file=filename))

                data.append(
                    {
                        'event_onset': float(row[0]),
                        'event_offset': float(row[1]),
                        'event_label': row[2]
                    }
                )

            elif len(row) == 4:
                if not isfloat(row[1]) or not isfloat(row[2]):
                    raise ValueError('Event onset and event offset needs to be float in file [{file}].'.format(file=filename))

                data.append(
                    {
                        'file': row[0],
                        'event_onset': float(row[1]),
                        'event_offset': float(row[2]),
                        'event_label': row[3]
                    }
                )

            elif len(row) == 5:
                if not isfloat(row[2]) or not isfloat(row[3]):
                    raise ValueError('Event onset and event offset needs to be float in file [{file}].'.format(file=filename))

                data.append(
                    {
                        'file': row[0],
                        'scene_label': row[1],
                        'event_onset': float(row[2]),
                        'event_offset': float(row[3]),
                        'event_label': row[4]
                    }
                )

            elif len(row) == 1 and not isfloat(row[0]):
                data.append(
                    {
                        'file': row[0]
                    }
                )

            else:
                raise ValueError('Unknown event list format in file [{file}].'.format(file=filename))

    if file_open:
        input_file.close()

    return util.event_list.EventList(data)


def load_scene_list(filename):
    """Load scene list from csv formatted text-file

    Supported formats:

    - [filename][delimiter][scene label]
    - [filename][delimiter][segment start (float >= 0)][delimiter][segment stop (float >= 0)][delimiter][scene label]

    Supported delimiters: ``,``, ``;``, ``tab``

    Example of scene list file::

        scenes_stereo/supermarket09.wav	supermarket
        scenes_stereo/tubestation10.wav	tubestation
        scenes_stereo/quietstreet08.wav	quietstreet
        scenes_stereo/restaurant05.wav	restaurant
        scenes_stereo/busystreet05.wav	busystreet
        scenes_stereo/openairmarket04.wav	openairmarket
        scenes_stereo/quietstreet01.wav	quietstreet
        scenes_stereo/supermarket05.wav	supermarket
        scenes_stereo/openairmarket01.wav	openairmarket

    Parameters
    ----------
    filename : str
        Path to the csv-file

    Returns
    -------
    scene_list: list
        Scene list

    """

    data = []
    file_open = False
    if hasattr(filename, 'read'):
        input_file = filename
    else:
        input_file = open(filename, 'rt')
        file_open = True

    try:
        dialect = csv.Sniffer().sniff(input_file.readline(), [',', ';', '\t'])
    except csv.Error:
        raise ValueError('Unknown delimiter in file [{file}].'.format(file=filename))
    input_file.seek(0)  

    for row in csv.reader(input_file, dialect):
        if len(row) == 2:
            data.append(
                {
                    'file': row[0],
                    'scene_label': row[1],
                }
            )
        elif len(row) == 4:
            if not isfloat(row[1]) or not isfloat(row[2]):
                raise ValueError('Segment start and segment end needs to be float in file [{file}].'.format(file=filename))
            data.append(
                {
                    'file': row[0],
                    'segment_start': float(row[1]),
                    'segment_end': float(row[2]),
                    'scene_label': row[3]
                }
            )
        else:
            raise ValueError('Unknown scene list format in file [{file}].'.format(file=filename))
    if file_open:
        input_file.close()

    return util.scene_list.SceneList(data)


def load_file_pair_list(filename):
    """Load file pair list csv formated text-file

    Format is [reference_file][delimiter][estimated_file]

    Supported delimiters: ``,``, ``;``, ``tab``

    Example of file-list::

        office_snr0_high_v2.txt	office_snr0_high_v2_detected.txt
        office_snr0_med_v2.txt	office_snr0_med_v2_detected.txt

    Parameters
    ----------
    filename : str
        Path to the csv-file

    Returns
    -------
    file_list: list
        File pair dicts in a list

    """

    data = []
    file_open = False
    if hasattr(filename, 'read'):
        input_file = filename
    else:
        input_file = open(filename, 'rt')
        file_open = True

    try:
        dialect = csv.Sniffer().sniff(input_file.readline(), [',', ';', '\t'])
    except csv.Error:
        raise ValueError('Unknown delimiter in file [{file}].'.format(file=filename))
    input_file.seek(0)  

    for row in csv.reader(input_file, dialect):
        if len(row) == 2:
            data.append(
                {
                    'reference_file': row[0],
                    'estimated_file': row[1]
                }
            )
        else:
            raise ValueError('Unknown file pair list format in file [{file}].'.format(file=filename))
    if file_open:
        input_file.close()
    return data

