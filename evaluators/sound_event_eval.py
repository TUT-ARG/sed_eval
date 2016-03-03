#!/usr/bin/env python
"""
Evaluator for computing all sound event detection related metrics.

Usage:
./sound_event_eval.py FILE_PAIR_LIST.TXT

Evaluator takes as argument a csv-formatted file-list. The list contains pairs of filenames, one pair per row:
first the filename of the reference event list file and the second the estimated event list file.
Format is [reference_file][delimiter][estimated_file], and supported delimiters are ``,``, ``;``, ``tab``.

Example of file-list::

    office_snr0_high_v2.txt	office_snr0_high_v2_detected.txt
    office_snr0_med_v2.txt	office_snr0_med_v2_detected.txt

Event list is csv-formatted text-file. Supported formats for the file are:

- [event onset (float >= 0)][delimiter][event offset (float >= 0)]
- [event onset (float >= 0)][delimiter][event offset (float >= 0)][delimiter][label]
- [filename][delimiter][scene_label][delimiter][event onset (float >= 0)][delimiter][event offset (float >= 0)][delimiter][event label]

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

To get segment-based and event-based metrics report printed, run:

./sound_event_eval.py file_list.txt

To get segment-based and event-based metrics saved in YAML-format, run:

./sound_event_eval.py file_list.txt -o results.yaml

"""

import sys
import os
import argparse
import textwrap
import yaml
import sed_eval


__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)


def process_arguments(argv):

    # Argparse function to get the program parameters
    parser = argparse.ArgumentParser(
        prefix_chars='-+',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Sound event detection evaluator
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
    all_data = sed_eval.util.EventList([])
    for file_pair in file_list:
        reference_event_list = sed_eval.io.load_event_list(os.path.abspath(os.path.join(path, file_pair['reference_file'])))
        estimated_event_list = sed_eval.io.load_event_list(os.path.abspath(os.path.join(path, file_pair['estimated_file'])))
        data.append({'reference_event_list': reference_event_list, 'estimated_event_list': estimated_event_list})
        all_data += reference_event_list
    event_labels = all_data.unique_event_labels

    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(event_labels)
    event_based_metrics = sed_eval.sound_event.EventBasedMetrics(event_labels)
    for file_pair in data:
        segment_based_metrics.evaluate(file_pair['reference_event_list'], file_pair['estimated_event_list'])
        event_based_metrics.evaluate(file_pair['reference_event_list'], file_pair['estimated_event_list'])

    if parameters['output_file']:
        results = {
            'segment_based_metrics': segment_based_metrics.results(),
            'event_based_metrics': event_based_metrics.results()
        }

        with open(parameters['output_file'], 'w') as result_file:
            result_file.write(yaml.dump(results, default_flow_style=False))
    else:
        print segment_based_metrics
        print event_based_metrics

if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except (ValueError, IOError) as e:
        sys.exit(e)
