#!/usr/bin/env python
"""
Evaluator for computing all acoustic scene classification related metrics.

Usage:
./scene_eval.py FILE_PAIR_LIST.TXT

Evaluator takes as argument a csv-formatted file-list. The list contains pairs of filenames, one pair per row:
first the filename of the reference scene list file and the second the estimated scene list file.
Format is [reference_file][delimiter][estimated_file], and supported delimiters are ``,``, ``;``, ``tab``.

Example of file-list::

    fold1_reference.txt	fold1_estimated.txt
    fold2_reference.txt	fold2_estimated.txt
    fold3_reference.txt	fold3_estimated.txt
    fold4_reference.txt	fold4_estimated.txt
    fold5_reference.txt	fold5_estimated.txt


Scene list is csv-formatted text-file. Supported formats for the file are:

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


To get metrics printed, run:

./scene_eval.py file_list.txt

To get metrics saved in YAML-format, run:

./scene_eval.py file_list.txt -o results.yaml

"""
from __future__ import print_function, absolute_import
import sys
import os
import argparse
import textwrap
import yaml
import sed_eval
import dcase_util

__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)


def process_arguments(argv):

    # Argparse function to get the program parameters
    parser = argparse.ArgumentParser(
        prefix_chars='-+',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Acoustic scene classification evaluator
        '''))

    # Setup argument handling
    parser.add_argument('-o',
                        dest='output_file',
                        default=None,
                        type=str,
                        action='store',
                        help='Store results in yaml format')

    parser.add_argument('file_list',
                        action='store',
                        help='path to the file list in csv format having two fields: reference annotation file[tab]estimated annotation file')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    return vars(parser.parse_args(argv[1:]))


def main(argv):
    """
    """
    parameters = process_arguments(argv)
    file_list = sed_eval.io.load_file_pair_list(parameters['file_list'])
    path = os.path.dirname(parameters['file_list'])

    data = []
    all_data = dcase_util.containers.MetaDataContainer()
    for file_pair in file_list:
        reference_scene_list = sed_eval.io.load_scene_list(os.path.abspath(os.path.join(path, file_pair['reference_file'])))
        estimated_scene_list = sed_eval.io.load_scene_list(os.path.abspath(os.path.join(path, file_pair['estimated_file'])))
        data.append({'reference_scene_list': reference_scene_list, 'estimated_scene_list': estimated_scene_list})
        all_data += reference_scene_list
    scene_labels = all_data.unique_scene_labels

    metrics = sed_eval.scene.SceneClassificationMetrics(scene_labels=scene_labels)
    for file_pair in data:
        metrics.evaluate(file_pair['reference_scene_list'], file_pair['estimated_scene_list'])

    if parameters['output_file']:
        results = {
            'metrics': metrics.results(),
        }

        with open(parameters['output_file'], 'w') as result_file:
            result_file.write(yaml.dump(results, default_flow_style=False))
    else:
        print(metrics)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except (ValueError, IOError) as e:
        sys.exit(e)
