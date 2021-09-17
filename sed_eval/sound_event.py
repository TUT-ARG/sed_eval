#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Segment-based metrics, main functions:

* :func:`sed_eval.sound_event.SegmentBasedMetrics.evaluate`: Calculate intermediate values for evaluation and accumulate them.
* :func:`sed_eval.sound_event.SegmentBasedMetrics.results`: Calculate and return all metrics.
* :func:`sed_eval.sound_event.SegmentBasedMetrics.results_overall_metrics`: Calculate and return overall metrics (micro-averaged).
* :func:`sed_eval.sound_event.SegmentBasedMetrics.results_class_wise_metrics`: Calculate and return class-wise metrics.
* :func:`sed_eval.sound_event.SegmentBasedMetrics.results_class_wise_average_metrics`: Calculate and return class-wise average metrics (macro-averaged).

Event-based metrics, main functions:

* :func:`sed_eval.sound_event.EventBasedMetrics.evaluate`: Calculate intermediate values for evaluation and accumulate them.
* :func:`sed_eval.sound_event.EventBasedMetrics.results`: Calculate and return all metrics.
* :func:`sed_eval.sound_event.EventBasedMetrics.results_overall_metrics`: Calculate and return overall metrics (micro-averaged).
* :func:`sed_eval.sound_event.EventBasedMetrics.results_class_wise_metrics`: Calculate and return class-wise metrics.
* :func:`sed_eval.sound_event.EventBasedMetrics.results_class_wise_average_metrics`: Calculate and return class-wise average metrics (macro-averaged).

Functions :func:`sed_eval.sound_event.SegmentBasedMetrics.evaluate` and :func:`sed_eval.sound_event.EventBasedMetrics.evaluate`
take as a parameter event lists, use :func:`sed_eval.io.load_event_list` to read them from a file.


Usage example when reading event lists from disk (you can run example in path ``tests/data/sound_event``):

.. code-block:: python
    :linenos:

    import sed_eval
    import dcase_util

    file_list = [
        {
         'reference_file': 'office_snr0_high_v2.txt',
         'estimated_file': 'office_snr0_high_v2_detected.txt'
        },
        {
         'reference_file': 'office_snr0_med_v2.txt',
         'estimated_file': 'office_snr0_med_v2_detected.txt'
        }
    ]

    data = []

    # Get used event labels
    all_data = dcase_util.containers.MetaDataContainer()
    for file_pair in file_list:
        reference_event_list = sed_eval.io.load_event_list(
            filename=file_pair['reference_file']
        )
        estimated_event_list = sed_eval.io.load_event_list(
            filename=file_pair['estimated_file']
        )

        data.append({'reference_event_list': reference_event_list,
                     'estimated_event_list': estimated_event_list})

        all_data += reference_event_list

    event_labels = all_data.unique_event_labels

    # Start evaluating

    # Create metrics classes, define parameters
    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(
        event_label_list=event_labels,
        time_resolution=1.0
    )

    event_based_metrics = sed_eval.sound_event.EventBasedMetrics(
        event_label_list=event_labels,
        t_collar=0.250
    )

    # Go through files
    for file_pair in data:
        segment_based_metrics.evaluate(
            reference_event_list=file_pair['reference_event_list'],
            estimated_event_list=file_pair['estimated_event_list']
        )

        event_based_metrics.evaluate(
            reference_event_list=file_pair['reference_event_list'],
            estimated_event_list=file_pair['estimated_event_list']
        )

    # Get only certain metrics
    overall_segment_based_metrics = segment_based_metrics.results_overall_metrics()
    print("Accuracy:", overall_segment_based_metrics['accuracy']['accuracy'])

    # Or print all metrics as reports
    print(segment_based_metrics)
    print(event_based_metrics)

Usage example to evaluate results stored in variables:

.. code-block:: python
    :linenos:

    import sed_eval
    import dcase_util

    reference_event_list = dcase_util.containers.MetaDataContainer(
        [
            {
                'event_label': 'car',
                'event_onset': 0.0,
                'event_offset': 2.5,
                'file': 'audio/street/b099.wav',
                'scene_label': 'street'
            },
            {
                'event_label': 'car',
                'event_onset': 2.8,
                'event_offset': 4.5,
                'file': 'audio/street/b099.wav',
                'scene_label': 'street'
            },
            {
                'event_label': 'car',
                'event_onset': 6.0,
                'event_offset': 10.0,
                'file': 'audio/street/b099.wav',
                'scene_label': 'street'
            }
        ]
    )

    estimated_event_list = dcase_util.containers.MetaDataContainer(
        [
            {
                'event_label': 'car',
                'event_onset': 1.0,
                'event_offset': 3.5,
                'file': 'audio/street/b099.wav',
                'scene_label': 'street'
            },
            {
                'event_label': 'car',
                'event_onset': 7.0,
                'event_offset': 8.0,
                'file': 'audio/street/b099.wav',
                'scene_label': 'street'
            }
        ]
    )

    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(
        event_label_list=reference_event_list.unique_event_labels,
        time_resolution=1.0
    )
    event_based_metrics = sed_eval.sound_event.EventBasedMetrics(
        event_label_list=reference_event_list.unique_event_labels,
        t_collar=0.250
    )

    for filename in reference_event_list.unique_files:
        reference_event_list_for_current_file = reference_event_list.filter(
            filename=filename
        )

        estimated_event_list_for_current_file = estimated_event_list.filter(
            filename=filename
        )

        segment_based_metrics.evaluate(
            reference_event_list=reference_event_list_for_current_file,
            estimated_event_list=estimated_event_list_for_current_file
        )

        event_based_metrics.evaluate(
            reference_event_list=reference_event_list_for_current_file,
            estimated_event_list=estimated_event_list_for_current_file
        )

    # Get only certain metrics
    overall_segment_based_metrics = segment_based_metrics.results_overall_metrics()
    print("Accuracy:", overall_segment_based_metrics['accuracy']['accuracy'])

    # Or print all metrics as reports
    print(segment_based_metrics)
    print(event_based_metrics)

Segment based metrics
^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
    :toctree: generated/

    SegmentBasedMetrics
    SegmentBasedMetrics.evaluate
    SegmentBasedMetrics.results
    SegmentBasedMetrics.results_overall_metrics
    SegmentBasedMetrics.results_class_wise_metrics
    SegmentBasedMetrics.results_class_wise_average_metrics
    SegmentBasedMetrics.result_report_parameters
    SegmentBasedMetrics.result_report_overall
    SegmentBasedMetrics.result_report_class_wise
    SegmentBasedMetrics.result_report_class_wise_average
    SegmentBasedMetrics.reset

.. autoclass:: SegmentBasedMetrics
   :members:

Event based metrics
^^^^^^^^^^^^^^^^^^^

.. autosummary::
    :toctree: generated/

    EventBasedMetrics
    EventBasedMetrics.evaluate
    EventBasedMetrics.results
    EventBasedMetrics.results_overall_metrics
    EventBasedMetrics.results_class_wise_metrics
    EventBasedMetrics.results_class_wise_average_metrics
    EventBasedMetrics.result_report_parameters
    EventBasedMetrics.result_report_overall
    EventBasedMetrics.result_report_class_wise
    EventBasedMetrics.result_report_class_wise_average
    EventBasedMetrics.reset

.. autoclass:: EventBasedMetrics
   :members:
   :undoc-members:
   :inherited-members:

"""

from __future__ import absolute_import
import numpy
import math
import dcase_util
from . import metric
from . import util


class SoundEventMetrics(object):
    """Base class for sound event detection metrics.

    """
    def __init__(self,
                 empty_system_output_handling=None):
        """Constructor

        Parameters
        ----------

        empty_system_output_handling : str
            Controls how empty system output is handled, i.e. when Nsys = 0. Default behaviour is to show NaN when e.g.
            computing precision (Ntp / Nsys).
            Use 'zero_score' to force these score to zero.
            Default value None

        """

        self.event_label_list = []
        self.ui = dcase_util.ui.FancyStringifier()
        self.empty_system_output_handling = empty_system_output_handling

    # Reports
    def result_report_overall(self):
        """Report overall results

        Returns
        -------
        str
            result report in string format

        """

        results = self.results_overall_metrics()

        output = self.ui.section_header('Overall metrics (micro-average)', indent=2) + '\n'

        if results['f_measure']:
            output += self.ui.line('F-measure', indent=2) + '\n'
            output += self.ui.data(field='F-measure (F1)', value=float(results['f_measure']['f_measure']) * 100,
                                   unit='%', indent=4) + '\n'
            output += self.ui.data(field='Precision', value=float(results['f_measure']['precision']) * 100,
                                   unit='%', indent=4) + '\n'
            output += self.ui.data(field='Recall', value=float(results['f_measure']['recall']) * 100,
                                   unit='%', indent=4) + '\n'

        if results['error_rate']:
            output += self.ui.line('Error rate', indent=2) + '\n'
            output += self.ui.data(field='Error rate (ER)', value=float(results['error_rate']['error_rate']),
                                   indent=4) + '\n'
            output += self.ui.data(field='Substitution rate', value=float(results['error_rate']['substitution_rate']),
                                   indent=4) + '\n'
            output += self.ui.data(field='Deletion rate', value=float(results['error_rate']['deletion_rate']),
                                   indent=4) + '\n'
            output += self.ui.data(field='Insertion rate', value=float(results['error_rate']['insertion_rate']),
                                   indent=4) + '\n'

        if results['accuracy']:
            output += self.ui.line('Accuracy', indent=2) + '\n'
            output += self.ui.data(field='Sensitivity', value=float(results['accuracy']['sensitivity']*100),
                                   unit='%', indent=4) + '\n'
            output += self.ui.data(field='Specificity', value=float(results['accuracy']['specificity'] * 100),
                                   unit='%', indent=4) + '\n'
            output += self.ui.data(field='Balanced accuracy', value=float(results['accuracy']['balanced_accuracy'] * 100),
                                   unit='%', indent=4) + '\n'
            output += self.ui.data(field='Accuracy', value=float(results['accuracy']['accuracy'] * 100),
                                   unit='%', indent=4) + '\n'

        return output

    def result_report_class_wise_average(self):
        """Report class-wise averages

        Returns
        -------
        str
            result report in string format

        """

        results = self.results_class_wise_average_metrics()

        output = self.ui.section_header('Class-wise average metrics (macro-average)', indent=2) + '\n'

        if results['f_measure']:
            output += self.ui.line('F-measure', indent=2) + '\n'
            output += self.ui.data(field='F-measure (F1)', value=float(results['f_measure']['f_measure']) * 100,
                                   unit='%', indent=4) + '\n'
            output += self.ui.data(field='Precision', value=float(results['f_measure']['precision']) * 100,
                                   unit='%', indent=4) + '\n'
            output += self.ui.data(field='Recall', value=float(results['f_measure']['recall']) * 100,
                                   unit='%', indent=4) + '\n'

        if results['error_rate']:
            output += self.ui.line('Error rate', indent=2) + '\n'
            output += self.ui.data(field='Error rate (ER)', value=float(results['error_rate']['error_rate']),
                                   indent=4) + '\n'
            output += self.ui.data(field='Deletion rate', value=float(results['error_rate']['deletion_rate']),
                                   indent=4) + '\n'
            output += self.ui.data(field='Insertion rate', value=float(results['error_rate']['insertion_rate']),
                                   indent=4) + '\n'

        if results['accuracy']:
            output += self.ui.line('Accuracy', indent=2) + '\n'
            output += self.ui.data(field='Sensitivity', value=float(results['accuracy']['sensitivity']*100),
                                   unit='%', indent=4) + '\n'
            output += self.ui.data(field='Specificity', value=float(results['accuracy']['specificity'] * 100),
                                   unit='%', indent=4) + '\n'
            output += self.ui.data(field='Balanced accuracy', value=float(results['accuracy']['balanced_accuracy'] * 100),
                                   unit='%', indent=4) + '\n'
            output += self.ui.data(field='Accuracy', value=float(results['accuracy']['accuracy'] * 100),
                                   unit='%', indent=4) + '\n'

        output += "  \n"

        return output

    def result_report_class_wise(self):
        """Report class-wise results

        Returns
        -------
        str
            result report in string format

        """

        results = self.results_class_wise_metrics()

        accuracy_present = True
        for event_label in self.event_label_list:
            if 'accuracy' not in results[event_label]['accuracy']:
                accuracy_present = False

        output = self.ui.section_header('Class-wise metrics', indent=2) + '\n'

        headers = ['Event label', 'Nref', 'Nsys', 'F', 'Pre', 'Rec', 'ER', 'Del', 'Ins']
        sep = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
        widths = [15, 8, 8, 9, 9, 9, 9, 9, 9]
        separators = [True, False, True, False, False, True, False, False, True]
        if accuracy_present:
            headers += ['Sens', 'Spec', 'Bacc', 'Acc']
            sep += ['-', '-', '-', '-']
            widths += [9, 9, 9, 9]
            separators += [False, False, False, False]

        output += self.ui.row(*headers, widths=widths, indent=4, separators=separators) + '\n'
        output += self.ui.row(*sep) + '\n'
        for event_label in self.event_label_list:
            data = [
                event_label,
                results[event_label]['count']['Nref'],
                results[event_label]['count']['Nsys'],
                results[event_label]['f_measure']['f_measure'] * 100,
                results[event_label]['f_measure']['precision'] * 100,
                results[event_label]['f_measure']['recall'] * 100,
                results[event_label]['error_rate']['error_rate'],
                results[event_label]['error_rate']['deletion_rate'],
                results[event_label]['error_rate']['insertion_rate']
            ]

            types = [
                'str15',
                'int',
                'int',
                'float1_percentage',
                'float1_percentage',
                'float1_percentage',
                'float2',
                'float2',
                'float2',
            ]

            if accuracy_present:
                data += [
                    results[event_label]['accuracy']['sensitivity'] * 100,
                    results[event_label]['accuracy']['specificity'] * 100,
                    results[event_label]['accuracy']['balanced_accuracy'] * 100,
                    results[event_label]['accuracy']['accuracy'] * 100
                ]

                types += [
                    'float1_percentage',
                    'float1_percentage',
                    'float1_percentage',
                    'float1_percentage',
                ]

            output += self.ui.row(*data, types=types) + '\n'

        return output

    # Metrics / overall
    def overall_f_measure(self):
        return {}

    def overall_error_rate(self):
        return {}

    def overall_accuracy(self, factor=0.5):
        return {}
    
    def overall_intermediate_counts(self):
        return {}
    
    # Metrics / class-wise
    def class_wise_intermediate_counts(self, event_label):
        return {}
    
    def class_wise_f_measure(self, event_label):
        return {}

    def class_wise_error_rate(self, event_label):
        return {}

    def class_wise_accuracy(self, event_label):
        return {}

    # Results
    def results_overall_metrics(self):
        """Overall metrics

        Returns
        -------
        dict
            results in a dictionary format

        """

        return {
            'f_measure': self.overall_f_measure(),
            'error_rate': self.overall_error_rate(),
            'accuracy': self.overall_accuracy(),
            'counts': self.overall_intermediate_counts()
        }

    def results_class_wise_metrics(self):
        """Class-wise metrics

        Returns
        -------
        dict
            results in a dictionary format

        """

        results = {}
        for event_label in self.event_label_list:
            if event_label not in results:
                results[event_label] = {}

            results[event_label]['f_measure'] = self.class_wise_f_measure(event_label)
            results[event_label]['accuracy'] = self.class_wise_accuracy(event_label)
            results[event_label]['error_rate'] = self.class_wise_error_rate(event_label)
            results[event_label]['count'] = self.class_wise_intermediate_counts(event_label)

        return results

    def results_class_wise_average_metrics(self):
        """Class-wise averaged metrics

        Returns
        -------
        dict
            results in a dictionary format

        """

        event_wise_results = self.results_class_wise_metrics()

        event_wise_f_measure = []
        event_wise_precision = []
        event_wise_recall = []
        
        event_wise_error_rate = []
        event_wise_deletion_rate = []
        event_wise_insertion_rate = []
        
        event_wise_sensitivity = []
        event_wise_specificity = []
        event_wise_balanced_accuracy = []
        event_wise_accuracy = []

        for event_label in event_wise_results:
            # F-measure
            event_wise_f_measure.append(event_wise_results[event_label]['f_measure']['f_measure'])
            event_wise_precision.append(event_wise_results[event_label]['f_measure']['precision'])
            event_wise_recall.append(event_wise_results[event_label]['f_measure']['recall'])
            
            # Error rate
            event_wise_error_rate.append(event_wise_results[event_label]['error_rate']['error_rate'])
            event_wise_deletion_rate.append(event_wise_results[event_label]['error_rate']['deletion_rate'])
            event_wise_insertion_rate.append(event_wise_results[event_label]['error_rate']['insertion_rate'])

            # Accuracy
            if 'sensitivity' in event_wise_results[event_label]['accuracy']:
                event_wise_sensitivity.append(event_wise_results[event_label]['accuracy']['sensitivity'])

            if 'specificity' in event_wise_results[event_label]['accuracy']:
                event_wise_specificity.append(event_wise_results[event_label]['accuracy']['specificity'])

            if 'balanced_accuracy' in event_wise_results[event_label]['accuracy']:
                event_wise_balanced_accuracy.append(event_wise_results[event_label]['accuracy']['balanced_accuracy'])

            if 'accuracy' in event_wise_results[event_label]['accuracy']:
                event_wise_accuracy.append(event_wise_results[event_label]['accuracy']['accuracy'])

        if event_wise_f_measure:
            event_wise_f_measure_dict = {
                'f_measure': float(numpy.nanmean(event_wise_f_measure)),
                'precision': float(numpy.nanmean(event_wise_precision)),
                'recall': float(numpy.nanmean(event_wise_recall))
            }

        else:
            event_wise_f_measure_dict = {}

        if event_wise_error_rate:
            event_wise_error_rate_dict = {
                'error_rate': float(numpy.nanmean(event_wise_error_rate)),
                'deletion_rate': float(numpy.nanmean(event_wise_deletion_rate)),
                'insertion_rate': float(numpy.nanmean(event_wise_insertion_rate))
            }

        else:
            event_wise_error_rate_dict = {}

        if event_wise_accuracy:
            event_wise_accuracy_dict = {
                'sensitivity': float(numpy.nanmean(event_wise_sensitivity)),
                'specificity': float(numpy.nanmean(event_wise_specificity)),
                'balanced_accuracy': float(numpy.nanmean(event_wise_balanced_accuracy)),
                'accuracy': float(numpy.nanmean(event_wise_accuracy))
            }

        else:
            event_wise_accuracy_dict = {}

        return {
            'f_measure': event_wise_f_measure_dict,
            'error_rate': event_wise_error_rate_dict,
            'accuracy': event_wise_accuracy_dict
        }

    def results(self):
        """All metrics

        Returns
        -------
        dict
            results in a dictionary format

        """

        return {
            'overall': self.results_overall_metrics(),
            'class_wise': self.results_class_wise_metrics(),
            'class_wise_average': self.results_class_wise_average_metrics()
        }


class SegmentBasedMetrics(SoundEventMetrics):
    def __init__(self,
                 event_label_list,
                 time_resolution=1.0,
                 **kwargs):
        """Constructor

        Parameters
        ----------
        event_label_list : list, numpy.array
            List of unique event labels

        time_resolution : float (0,]
            Segment size used in the evaluation, in seconds.
            Default value 1.0

        """

        SoundEventMetrics.__init__(self, **kwargs)

        if isinstance(event_label_list, numpy.ndarray) and len(event_label_list.shape) == 1:
            # We have numpy array, convert it to list
            event_label_list = event_label_list.tolist()

        if not isinstance(event_label_list, list):
            raise ValueError(
                "event_label_list needs to be list or numpy.array"
            )

        if not isinstance(time_resolution, float) or time_resolution <= 0.0:
            raise ValueError(
                "time_resolution needs to be float > 0"
            )

        self.event_label_list = event_label_list
        self.evaluated_length_seconds = 0.0
        self.evaluated_files = 0

        self.time_resolution = time_resolution

        self.overall = {
            'Ntp': 0.0,
            'Ntn': 0.0,
            'Nfp': 0.0,
            'Nfn': 0.0,
            'Nref': 0.0,
            'Nsys': 0.0,
            'ER': 0.0,
            'S': 0.0,
            'D': 0.0,
            'I': 0.0,
        }

        self.class_wise = {}
        for class_label in self.event_label_list:
            self.class_wise[class_label] = {
                'Ntp': 0.0,
                'Ntn': 0.0,
                'Nfp': 0.0,
                'Nfn': 0.0,
                'Nref': 0.0,
                'Nsys': 0.0,
            }

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self.results()

    def __str__(self):
        """Print result reports"""

        output = self.ui.section_header('Segment based metrics') + '\n'
        output += self.result_report_parameters() + '\n'
        output += self.result_report_overall() + '\n'
        output += self.result_report_class_wise_average() + '\n'
        output += self.result_report_class_wise() + '\n'

        return output

    def evaluate(self, reference_event_list, estimated_event_list, evaluated_length_seconds=None):
        """Evaluate file pair (reference and estimated)

        Parameters
        ----------

        reference_event_list : list of dict or dcase_util.containers.MetaDataContainer
            Reference event list.

        estimated_event_list : list of dict or dcase_util.containers.MetaDataContainer
            Estimated event list.

        evaluated_length_seconds : float, optional
            Evaluated length. If none given, maximum offset is used.
            Default value None

        Returns
        -------
        self

        """

        # Make sure input is dcase_util.containers.MetaDataContainer
        if not isinstance(reference_event_list, dcase_util.containers.MetaDataContainer):
            reference_event_list = dcase_util.containers.MetaDataContainer(reference_event_list)

        if not isinstance(estimated_event_list, dcase_util.containers.MetaDataContainer):
            estimated_event_list = dcase_util.containers.MetaDataContainer(estimated_event_list)

        # Check that input event list have event only from one file
        reference_files = reference_event_list.unique_files
        if len(reference_files) > 1:
            raise ValueError(
                "reference_event_list contains events from multiple files. Evaluate only file by file."
            )

        estimated_files = estimated_event_list.unique_files
        if len(estimated_files) > 1:
            raise ValueError(
                "estimated_event_list contains events from multiple files. Evaluate only file by file."
            )

        # Evaluate only valid events
        valid_reference_event_list = dcase_util.containers.MetaDataContainer()
        for item in reference_event_list:
            if 'event_onset' in item and 'event_offset' in item and 'event_label' in item:
                valid_reference_event_list.append(item)

            elif 'onset' in item and 'offset' in item and 'event_label' in item:
                valid_reference_event_list.append(item)

        reference_event_list = valid_reference_event_list

        valid_estimated_event_list = dcase_util.containers.MetaDataContainer()
        for item in estimated_event_list:
            if 'event_onset' in item and 'event_offset' in item and 'event_label' in item:
                valid_estimated_event_list.append(item)

            elif 'onset' in item and 'offset' in item and 'event_label' in item:
                valid_estimated_event_list.append(item)

        estimated_event_list = valid_estimated_event_list

        # Convert event list into frame-based representation
        reference_event_roll = util.event_list_to_event_roll(
            source_event_list=reference_event_list,
            event_label_list=self.event_label_list,
            time_resolution=self.time_resolution
        )

        estimated_event_roll = util.event_list_to_event_roll(
            source_event_list=estimated_event_list,
            event_label_list=self.event_label_list,
            time_resolution=self.time_resolution
        )

        if evaluated_length_seconds is None:
            evaluated_length_seconds = max(reference_event_list.max_offset, estimated_event_list.max_offset)
            evaluated_length_segments = int(math.ceil(evaluated_length_seconds * 1 / float(self.time_resolution)))

        else:
            evaluated_length_segments = int(math.ceil(evaluated_length_seconds * 1 / float(self.time_resolution)))

        self.evaluated_length_seconds += evaluated_length_seconds
        self.evaluated_files += 1

        reference_event_roll, estimated_event_roll = util.match_event_roll_lengths(
            reference_event_roll,
            estimated_event_roll,
            evaluated_length_segments
        )

        # Compute segment-based overall metrics
        for segment_id in range(0, reference_event_roll.shape[0]):
            annotated_segment = reference_event_roll[segment_id, :]
            system_segment = estimated_event_roll[segment_id, :]

            Ntp = sum(system_segment + annotated_segment > 1)
            Ntn = sum(system_segment + annotated_segment == 0)
            Nfp = sum(system_segment - annotated_segment > 0)
            Nfn = sum(annotated_segment - system_segment > 0)

            Nref = sum(annotated_segment)
            Nsys = sum(system_segment)

            S = min(Nref, Nsys) - Ntp
            D = max(0, Nref - Nsys)
            I = max(0, Nsys - Nref)

            self.overall['Ntp'] += Ntp
            self.overall['Ntn'] += Ntn
            self.overall['Nfp'] += Nfp
            self.overall['Nfn'] += Nfn
            self.overall['Nref'] += Nref
            self.overall['Nsys'] += Nsys
            self.overall['S'] += S
            self.overall['D'] += D
            self.overall['I'] += I

        # Compute segment-based class-wise metrics
        for class_id, class_label in enumerate(self.event_label_list):
            annotated_segment = reference_event_roll[:, class_id]
            system_segment = estimated_event_roll[:, class_id]

            Ntp = sum(system_segment + annotated_segment > 1)
            Ntn = sum(system_segment + annotated_segment == 0)
            Nfp = sum(system_segment - annotated_segment > 0)
            Nfn = sum(annotated_segment - system_segment > 0)

            Nref = sum(annotated_segment)
            Nsys = sum(system_segment)

            self.class_wise[class_label]['Ntp'] += Ntp
            self.class_wise[class_label]['Ntn'] += Ntn
            self.class_wise[class_label]['Nfp'] += Nfp
            self.class_wise[class_label]['Nfn'] += Nfn
            self.class_wise[class_label]['Nref'] += Nref
            self.class_wise[class_label]['Nsys'] += Nsys

        return self

    def reset(self):
        """Reset internal state"""

        self.overall = {
            'Ntp': 0.0,
            'Ntn': 0.0,
            'Nfp': 0.0,
            'Nfn': 0.0,
            'Nref': 0.0,
            'Nsys': 0.0,
            'ER': 0.0,
            'S': 0.0,
            'D': 0.0,
            'I': 0.0,
        }

        self.class_wise = {}
        for class_label in self.event_label_list:
            self.class_wise[class_label] = {
                'Ntp': 0.0,
                'Ntn': 0.0,
                'Nfp': 0.0,
                'Nfn': 0.0,
                'Nref': 0.0,
                'Nsys': 0.0,
            }

        return self

    # Metrics
    def overall_f_measure(self):
        """Overall f-measure metrics (f_measure, precision, and recall)

        Returns
        -------
        dict
            results in a dictionary format

        """
        if self.overall['Nsys'] == 0 and self.empty_system_output_handling == 'zero_score':
            precision = 0

        else:
            precision = metric.precision(
                Ntp=self.overall['Ntp'],
                Nsys=self.overall['Nsys']
            )

        recall = metric.recall(
            Ntp=self.overall['Ntp'],
            Nref=self.overall['Nref']
        )

        f_measure = metric.f_measure(
            precision=precision,
            recall=recall
        )

        return {
            'f_measure': f_measure,
            'precision': precision,
            'recall': recall
        }

    def overall_error_rate(self):
        """Overall error rate metrics (error_rate, substitution_rate, deletion_rate, and insertion_rate)

        Returns
        -------
        dict
            results in a dictionary format

        """

        substitution_rate = metric.substitution_rate(
            Nref=self.overall['Nref'],
            Nsubstitutions=self.overall['S']
        )

        deletion_rate = metric.deletion_rate(
            Nref=self.overall['Nref'],
            Ndeletions=self.overall['D']
        )

        insertion_rate = metric.insertion_rate(
            Nref=self.overall['Nref'],
            Ninsertions=self.overall['I']
        )

        error_rate = metric.error_rate(
            substitution_rate_value=substitution_rate,
            deletion_rate_value=deletion_rate,
            insertion_rate_value=insertion_rate
        )

        return {
            'error_rate': error_rate,
            'substitution_rate': substitution_rate,
            'deletion_rate': deletion_rate,
            'insertion_rate': insertion_rate
        }

    def overall_accuracy(self, factor=0.5):
        """Overall accuracy metrics (sensitivity, specificity, accuracy, and balanced_accuracy)

        Parameters
        ----------
        factor : float [0-1]
            Balance factor.
            Default value 0.5

        Returns
        -------
        dict
            results in a dictionary format

        """

        sensitivity = metric.sensitivity(
            Ntp=self.overall['Ntp'],
            Nfn=self.overall['Nfn']
        )

        specificity = metric.specificity(
            Ntn=self.overall['Ntn'],
            Nfp=self.overall['Nfp']
        )

        balanced_accuracy = metric.balanced_accuracy(
            sensitivity=sensitivity,
            specificity=specificity,
            factor=factor
        )

        accuracy = metric.accuracy(
            Ntp=self.overall['Ntp'],
            Ntn=self.overall['Ntn'],
            Nfp=self.overall['Nfp'],
            Nfn=self.overall['Nfn']
        )

        return {
            'accuracy': accuracy,
            'balanced_accuracy': balanced_accuracy,
            'sensitivity': sensitivity,
            'specificity': specificity
        }

    def overall_intermediate_counts(self):
        """Overall intermediate counts (Ntp, Ntn, Nfp, Nfn, Nref, and Nsys)

        Returns
        -------
        dict
            results in a dictionary format

        """

        return {
            'Ntp': float(self.overall['Ntp']),
            'Ntn': float(self.overall['Ntn']),
            'Nfp': float(self.overall['Nfp']),
            'Nfn': float(self.overall['Nfn']),
            'Nref': float(self.overall['Nref']),
            'Nsys': float(self.overall['Nsys']),
        }

    def class_wise_intermediate_counts(self, event_label):
        """Class-wise counts (Nref and Nsys)

        Returns
        -------
        dict
            results in a dictionary format

        """

        return {
            'Ntp': float(self.class_wise[event_label]['Ntp']),
            'Ntn': float(self.class_wise[event_label]['Ntn']),
            'Nfp': float(self.class_wise[event_label]['Nfp']),
            'Nfn': float(self.class_wise[event_label]['Nfn']),

            'Nref': float(self.class_wise[event_label]['Nref']),
            'Nsys': float(self.class_wise[event_label]['Nsys'])
        }

    def class_wise_f_measure(self, event_label):
        """Class-wise f-measure metrics (f_measure, precision, and recall)

        Returns
        -------
        dict
            results in a dictionary format

        """
        if self.class_wise[event_label]['Nsys'] == 0 and self.empty_system_output_handling == 'zero_score':
            precision = 0

        else:
            precision = metric.precision(
                Ntp=self.class_wise[event_label]['Ntp'],
                Nsys=self.class_wise[event_label]['Nsys']
            )

        recall = metric.recall(
            Ntp=self.class_wise[event_label]['Ntp'],
            Nref=self.class_wise[event_label]['Nref']
        )

        f_measure = metric.f_measure(
            precision=precision,
            recall=recall
        )

        return {
            'f_measure': f_measure,
            'precision': precision,
            'recall': recall
        }

    def class_wise_error_rate(self, event_label):
        """Class-wise error rate metrics (error_rate, deletion_rate, and insertion_rate)

        Returns
        -------
        dict
            results in a dictionary format

        """

        deletion_rate = metric.deletion_rate(
            Nref=self.class_wise[event_label]['Nref'],
            Ndeletions=self.class_wise[event_label]['Nfn']
        )

        insertion_rate = metric.insertion_rate(
            Nref=self.class_wise[event_label]['Nref'],
            Ninsertions=self.class_wise[event_label]['Nfp']
        )

        error_rate = metric.error_rate(
            deletion_rate_value=deletion_rate,
            insertion_rate_value=insertion_rate
        )

        return {
            'error_rate': error_rate,
            'deletion_rate': deletion_rate,
            'insertion_rate': insertion_rate
        }

    def class_wise_accuracy(self, event_label, factor=0.5):
        """Class-wise accuracy metrics (sensitivity, specificity, accuracy, and balanced_accuracy)

        Returns
        -------
        dict
            results in a dictionary format

        """

        sensitivity = metric.sensitivity(
            Ntp=self.class_wise[event_label]['Ntp'],
            Nfn=self.class_wise[event_label]['Nfn']
        )

        specificity = metric.specificity(
            Ntn=self.class_wise[event_label]['Ntn'],
            Nfp=self.class_wise[event_label]['Nfp']
        )

        balanced_accuracy = metric.balanced_accuracy(
            sensitivity=sensitivity,
            specificity=specificity,
            factor=factor
        )

        accuracy = metric.accuracy(
            Ntp=self.class_wise[event_label]['Ntp'],
            Ntn=self.class_wise[event_label]['Ntn'],
            Nfp=self.class_wise[event_label]['Nfp'],
            Nfn=self.class_wise[event_label]['Nfn']
        )

        return {
            'accuracy': accuracy,
            'balanced_accuracy': balanced_accuracy,
            'sensitivity': sensitivity,
            'specificity': specificity
        }

    # Reports
    def result_report_parameters(self):
        """Report metric parameters

        Returns
        -------
        str
            result report in string format

        """

        output = self.ui.data(field='Evaluated length', value=self.evaluated_length_seconds, unit='sec') + '\n'
        output += self.ui.data(field='Evaluated files', value=self.evaluated_files) + '\n'

        if self.time_resolution < 1:
            output += self.ui.data(field='Segment length', value=self.time_resolution * 1000, unit='ms') + '\n'

        else:
            output += self.ui.data(field='Segment length', value=self.time_resolution, unit='sec') + '\n'

        return output


class EventBasedMetrics(SoundEventMetrics):
    def __init__(self,
                 event_label_list,
                 evaluate_onset=True,
                 evaluate_offset=True,
                 t_collar=0.200,
                 percentage_of_length=0.5,
                 event_matching_type='optimal',
                 **kwargs):
        """Constructor

        Parameters
        ----------
        event_label_list : list
            List of unique event labels

        evaluate_onset : bool
            Evaluate onset.
            Default value True

        evaluate_offset : bool
            Evaluate offset.
            Default value True

        t_collar : float (0,]
            Time collar used when evaluating validity of the onset and offset, in seconds.
            Default value 0.2

        percentage_of_length : float in [0, 1]
            Second condition, percentage of the length within which the estimated offset has to be in order to be
            consider valid estimation.
            Default value 0.5

        event_matching_type : str
            Event matching type. Set 'optimal' for graph-based matching, or 'greedy' for always select first found match.
            Greedy type of event matching is kept for backward compatibility. Both event matching types produce
            very similar results, however, greedy matching can be sensitive to the order of reference events.
            Use default 'optimal' event matching, if you do not intend to compare your results to old results.
            Default value 'optimal'

        """

        SoundEventMetrics.__init__(self, **kwargs)

        if isinstance(event_label_list, numpy.ndarray) and len(event_label_list.shape) == 1:
            # We have numpy array, convert it to list
            event_label_list = event_label_list.tolist()

        if not isinstance(event_label_list, list):
            raise ValueError(
                "event_label_list needs to be list or numpy.array"
            )

        if not isinstance(t_collar, float) or t_collar <= 0.0:
            raise ValueError(
                "t_collar needs to be float > 0"
            )

        if not isinstance(percentage_of_length, float) or percentage_of_length < 0.0 or percentage_of_length > 1.0:
            raise ValueError(
                "t_collar percentage_of_length to be float in [0, 1]"
            )

        self.event_label_list = event_label_list
        self.evaluated_length = 0.0
        self.evaluated_files = 0
        if not evaluate_onset and not evaluate_offset:
            raise ValueError("Both evaluate_onset and evaluate_offset cannot be set to False")

        self.evaluate_onset = evaluate_onset
        self.evaluate_offset = evaluate_offset

        self.t_collar = t_collar
        self.percentage_of_length = percentage_of_length
        self.event_matching_type = event_matching_type
        self.overall = {
            'Nref': 0.0,
            'Nsys': 0.0,
            'Nsubs': 0.0,
            'Ntp': 0.0,
            'Nfp': 0.0,
            'Nfn': 0.0,
        }
        self.class_wise = {}

        for class_label in self.event_label_list:
            self.class_wise[class_label] = {
                'Nref': 0.0,
                'Nsys': 0.0,
                'Ntp': 0.0,
                'Ntn': 0.0,
                'Nfp': 0.0,
                'Nfn': 0.0,
            }

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self.results()

    def __str__(self):
        """Print result reports"""

        if self.evaluate_onset and self.evaluate_offset:
            title = "Event based metrics (onset-offset)"

        elif self.evaluate_onset and not self.evaluate_offset:
            title = "Event based metrics (onset only)"

        elif not self.evaluate_onset and self.evaluate_offset:
            title = "Event based metrics (offset only)"

        else:
            title = "Event based metrics"

        output = self.ui.section_header(title) + '\n'

        output += self.result_report_parameters() + '\n'
        output += self.result_report_overall() + '\n'
        output += self.result_report_class_wise_average() + '\n'
        output += self.result_report_class_wise() + '\n'

        return output

    def evaluate(self, reference_event_list, estimated_event_list):
        """Evaluate file pair (reference and estimated)

        Parameters
        ----------

        reference_event_list : event list
            Reference event list

        estimated_event_list : event list
            Estimated event list

        Returns
        -------
        self

        """

        # Make sure input is dcase_util.containers.MetaDataContainer
        if not isinstance(reference_event_list, dcase_util.containers.MetaDataContainer):
            reference_event_list = dcase_util.containers.MetaDataContainer(reference_event_list)

        if not isinstance(estimated_event_list, dcase_util.containers.MetaDataContainer):
            estimated_event_list = dcase_util.containers.MetaDataContainer(estimated_event_list)

        # Check that input event list have event only from one file
        reference_files = reference_event_list.unique_files
        if len(reference_files) > 1:
            raise ValueError(
                "reference_event_list contains events from multiple files. Evaluate only file by file."
            )

        estimated_files = estimated_event_list.unique_files
        if len(estimated_files) > 1:
            raise ValueError(
                "estimated_event_list contains events from multiple files. Evaluate only file by file."
            )

        # Evaluate only valid events
        valid_reference_event_list = dcase_util.containers.MetaDataContainer()
        for item in reference_event_list:
            if 'event_onset' in item and 'event_offset' in item and 'event_label' in item:
                valid_reference_event_list.append(item)

            elif 'onset' in item and 'offset' in item and 'event_label' in item:
                valid_reference_event_list.append(item)

        reference_event_list = valid_reference_event_list

        valid_estimated_event_list = dcase_util.containers.MetaDataContainer()
        for item in estimated_event_list:
            if 'event_onset' in item and 'event_offset' in item and 'event_label' in item:
                valid_estimated_event_list.append(item)

            elif 'onset' in item and 'offset' in item and 'event_label' in item:
                valid_estimated_event_list.append(item)

        estimated_event_list = valid_estimated_event_list

        evaluated_length_seconds = max(reference_event_list.max_offset, estimated_event_list.max_offset)
        self.evaluated_length += evaluated_length_seconds
        self.evaluated_files += 1

        # Overall metrics

        # Total number of detected and reference events
        Nsys = len(estimated_event_list)
        Nref = len(reference_event_list)

        if self.event_matching_type == 'optimal':
            label_hit_matrix = numpy.zeros((len(reference_event_list), len(estimated_event_list)), dtype=bool)
            for j in range(0, len(reference_event_list)):
                for i in range(0, len(estimated_event_list)):
                    label_hit_matrix[j, i] = reference_event_list[j]['event_label'] == estimated_event_list[i]['event_label']

            hit_matrix = label_hit_matrix
            if self.evaluate_onset:
                onset_hit_matrix = numpy.zeros((len(reference_event_list), len(estimated_event_list)), dtype=bool)
                for j in range(0, len(reference_event_list)):
                    for i in range(0, len(estimated_event_list)):
                        onset_hit_matrix[j, i] = self.validate_onset(
                            reference_event=reference_event_list[j],
                            estimated_event=estimated_event_list[i],
                            t_collar=self.t_collar
                        )

                hit_matrix *= onset_hit_matrix

            if self.evaluate_offset:
                offset_hit_matrix = numpy.zeros((len(reference_event_list), len(estimated_event_list)), dtype=bool)
                for j in range(0, len(reference_event_list)):
                    for i in range(0, len(estimated_event_list)):
                        offset_hit_matrix[j, i] = self.validate_offset(
                            reference_event=reference_event_list[j],
                            estimated_event=estimated_event_list[i],
                            t_collar=self.t_collar,
                            percentage_of_length=self.percentage_of_length
                        )

                hit_matrix *= offset_hit_matrix

            hits = numpy.where(hit_matrix)
            G = {}
            for ref_i, est_i in zip(*hits):
                if est_i not in G:
                    G[est_i] = []

                G[est_i].append(ref_i)

            matching = sorted(util.bipartite_match(G).items())

            ref_correct = numpy.zeros(Nref, dtype=bool)
            sys_correct = numpy.zeros(Nsys, dtype=bool)
            for item in matching:
                ref_correct[item[0]] = True
                sys_correct[item[1]] = True

            Ntp = len(matching)
            # Substitutions
            Nsubs = 0

            ref_leftover = numpy.nonzero(numpy.logical_not(ref_correct))[0]
            sys_leftover = numpy.nonzero(numpy.logical_not(sys_correct))[0]
            sys_counted = numpy.zeros(Nsys, dtype=bool)
            for j in ref_leftover:
                for i in sys_leftover:
                    if not sys_counted[i]:
                        if self.evaluate_onset:
                            onset_condition = self.validate_onset(
                                reference_event=reference_event_list[j],
                                estimated_event=estimated_event_list[i],
                                t_collar=self.t_collar
                            )

                        else:
                            onset_condition = True

                        if self.evaluate_offset:
                            offset_condition = self.validate_offset(
                                reference_event=reference_event_list[j],
                                estimated_event=estimated_event_list[i],
                                t_collar=self.t_collar,
                                percentage_of_length=self.percentage_of_length
                            )

                        else:
                            offset_condition = True

                        if onset_condition and offset_condition:
                            sys_counted[i] = True
                            Nsubs += 1
                            break

        elif self.event_matching_type == 'greedy':
            sys_correct = numpy.zeros(Nsys, dtype=bool)
            ref_correct = numpy.zeros(Nref, dtype=bool)

            # Number of correctly detected events
            for j in range(0, len(reference_event_list)):
                for i in range(0, len(estimated_event_list)):
                    if not sys_correct[i]:  # skip already matched events
                        label_condition = reference_event_list[j]['event_label'] == estimated_event_list[i]['event_label']

                        if self.evaluate_onset:
                            onset_condition = self.validate_onset(
                                reference_event=reference_event_list[j],
                                estimated_event=estimated_event_list[i],
                                t_collar=self.t_collar
                            )

                        else:
                            onset_condition = True

                        if self.evaluate_offset:
                            offset_condition = self.validate_offset(
                                reference_event=reference_event_list[j],
                                estimated_event=estimated_event_list[i],
                                t_collar=self.t_collar,
                                percentage_of_length=self.percentage_of_length
                            )

                        else:
                            offset_condition = True

                        if label_condition and onset_condition and offset_condition:
                            ref_correct[j] = True
                            sys_correct[i] = True
                            break

            Ntp = numpy.sum(sys_correct)

            ref_leftover = numpy.nonzero(numpy.logical_not(ref_correct))[0]
            sys_leftover = numpy.nonzero(numpy.logical_not(sys_correct))[0]

            # Substitutions
            Nsubs = 0
            sys_counted = numpy.zeros(Nsys, dtype=bool)
            for j in ref_leftover:
                for i in sys_leftover:
                    if not sys_counted[i]:
                        if self.evaluate_onset:
                            onset_condition = self.validate_onset(
                                reference_event=reference_event_list[j],
                                estimated_event=estimated_event_list[i],
                                t_collar=self.t_collar
                            )

                        else:
                            onset_condition = True

                        if self.evaluate_offset:
                            offset_condition = self.validate_offset(
                                reference_event=reference_event_list[j],
                                estimated_event=estimated_event_list[i],
                                t_collar=self.t_collar,
                                percentage_of_length=self.percentage_of_length
                            )

                        else:
                            offset_condition = True

                        if onset_condition and offset_condition:
                            sys_counted[i] = True
                            Nsubs += 1
                            break

        Nfp = Nsys - Ntp - Nsubs
        Nfn = Nref - Ntp - Nsubs

        self.overall['Nref'] += Nref
        self.overall['Nsys'] += Nsys
        self.overall['Ntp'] += Ntp
        self.overall['Nsubs'] += Nsubs
        self.overall['Nfp'] += Nfp
        self.overall['Nfn'] += Nfn

        # Class-wise metrics
        for class_id, class_label in enumerate(self.event_label_list):
            Nref = 0.0
            Nsys = 0.0
            Ntp = 0.0

            # Count event frequencies in the ground truth
            for i in range(0, len(reference_event_list)):
                if reference_event_list[i]['event_label'] == class_label:
                    Nref += 1

            # Count event frequencies in the system output
            for i in range(0, len(estimated_event_list)):
                if estimated_event_list[i]['event_label'] == class_label:
                    Nsys += 1

            if self.event_matching_type == 'optimal':
                class_reference_event_list = reference_event_list.filter(event_label=class_label)
                class_estimated_event_list = estimated_event_list.filter(event_label=class_label)

                hit_matrix = numpy.ones((len(class_reference_event_list), len(class_estimated_event_list)), dtype=bool)
                if self.evaluate_onset:
                    onset_hit_matrix = numpy.zeros((len(class_reference_event_list), len(class_estimated_event_list)), dtype=bool)
                    for j in range(0, len(class_reference_event_list)):
                        for i in range(0, len(class_estimated_event_list)):
                            onset_hit_matrix[j, i] = self.validate_onset(
                                reference_event=class_reference_event_list[j],
                                estimated_event=class_estimated_event_list[i],
                                t_collar=self.t_collar
                            )

                    hit_matrix *= onset_hit_matrix

                if self.evaluate_offset:
                    offset_hit_matrix = numpy.zeros((len(class_reference_event_list), len(class_estimated_event_list)), dtype=bool)
                    for j in range(0, len(class_reference_event_list)):
                        for i in range(0, len(class_estimated_event_list)):
                            offset_hit_matrix[j, i] = self.validate_offset(
                                reference_event=class_reference_event_list[j],
                                estimated_event=class_estimated_event_list[i],
                                t_collar=self.t_collar,
                                percentage_of_length=self.percentage_of_length
                            )

                    hit_matrix *= offset_hit_matrix

                hits = numpy.where(hit_matrix)
                G = {}
                for ref_i, est_i in zip(*hits):
                    if est_i not in G:
                        G[est_i] = []

                    G[est_i].append(ref_i)

                matching = sorted(util.bipartite_match(G).items())

                ref_correct = numpy.zeros(int(Nref), dtype=bool)
                sys_correct = numpy.zeros(int(Nsys), dtype=bool)

                for item in matching:
                    ref_correct[item[0]] = True
                    sys_correct[item[1]] = True

                Ntp = len(matching)

            elif self.event_matching_type == 'greedy':
                sys_counted = numpy.zeros(len(estimated_event_list), dtype=bool)
                for j in range(0, len(reference_event_list)):
                    if reference_event_list[j]['event_label'] == class_label:
                        for i in range(0, len(estimated_event_list)):
                            if estimated_event_list[i]['event_label'] == class_label and not sys_counted[i]:
                                if self.evaluate_onset:
                                    onset_condition = self.validate_onset(
                                        reference_event=reference_event_list[j],
                                        estimated_event=estimated_event_list[i],
                                        t_collar=self.t_collar
                                    )

                                else:
                                    onset_condition = True

                                if self.evaluate_offset:
                                    offset_condition = self.validate_offset(
                                        reference_event=reference_event_list[j],
                                        estimated_event=estimated_event_list[i],
                                        t_collar=self.t_collar,
                                        percentage_of_length=self.percentage_of_length
                                    )

                                else:
                                    offset_condition = True

                                if onset_condition and offset_condition:
                                    sys_counted[i] = True
                                    Ntp += 1
                                    break

            Nfp = Nsys - Ntp
            Nfn = Nref - Ntp

            self.class_wise[class_label]['Nref'] += Nref
            self.class_wise[class_label]['Nsys'] += Nsys

            self.class_wise[class_label]['Ntp'] += Ntp
            self.class_wise[class_label]['Nfp'] += Nfp
            self.class_wise[class_label]['Nfn'] += Nfn

        return self

    def reset(self):
        """Reset internal state
        """

        self.overall = {
            'Nref': 0.0,
            'Nsys': 0.0,
            'Nsubs': 0.0,
            'Ntp': 0.0,
            'Nfp': 0.0,
            'Nfn': 0.0,
        }
        self.class_wise = {}

        for class_label in self.event_label_list:
            self.class_wise[class_label] = {
                'Nref': 0.0,
                'Nsys': 0.0,
                'Ntp': 0.0,
                'Ntn': 0.0,
                'Nfp': 0.0,
                'Nfn': 0.0,
            }

        return self

    @staticmethod
    def validate_onset(reference_event, estimated_event, t_collar=0.200):
        """Validate estimated event based on event onset

        Parameters
        ----------
        reference_event : dict
            Reference event.

        estimated_event: dict
            Estimated event.

        t_collar : float > 0, seconds
            Time collar with which the estimated onset has to be in order to be consider valid estimation.
            Default value 0.2

        Returns
        -------
        bool

        """

        # Detect field naming style used and validate onset
        if 'event_onset' in reference_event and 'event_onset' in estimated_event:
            return math.fabs(reference_event['event_onset'] - estimated_event['event_onset']) <= t_collar

        elif 'onset' in reference_event and 'onset' in estimated_event:
            return math.fabs(reference_event['onset'] - estimated_event['onset']) <= t_collar

    @staticmethod
    def validate_offset(reference_event, estimated_event, t_collar=0.200, percentage_of_length=0.5):
        """Validate estimated event based on event offset

        Parameters
        ----------
        reference_event : dict
            Reference event.

        estimated_event : dict
            Estimated event.

        t_collar : float > 0, seconds
            First condition, Time collar with which the estimated offset has to be in order to be consider valid estimation.
            Default value 0.2

        percentage_of_length : float in [0, 1]
            Second condition, percentage of the length within which the estimated offset has to be in order to be
            consider valid estimation.
            Default value 0.5

        Returns
        -------
        bool

        """

        # Detect field naming style used and validate onset
        if 'event_offset' in reference_event and 'event_offset' in estimated_event:
            annotated_length = reference_event['event_offset'] - reference_event['event_onset']

            return math.fabs(reference_event['event_offset'] - estimated_event['event_offset']) <= max(t_collar, percentage_of_length * annotated_length)

        elif 'offset' in reference_event and 'offset' in estimated_event:
            annotated_length = reference_event['offset'] - reference_event['onset']

            return math.fabs(reference_event['offset'] - estimated_event['offset']) <= max(t_collar, percentage_of_length * annotated_length)

    # Metrics
    def overall_f_measure(self):
        """Overall f-measure metrics (f_measure, precision, and recall)

        Returns
        -------
        dict
            results in a dictionary format
        """

        if self.overall['Nsys'] == 0 and self.empty_system_output_handling == 'zero_score':
            precision = 0

        else:
            precision = metric.precision(
                Ntp=self.overall['Ntp'],
                Nsys=self.overall['Nsys']
            )

        recall = metric.recall(
            Ntp=self.overall['Ntp'],
            Nref=self.overall['Nref']
        )

        f_measure = metric.f_measure(
            precision=precision,
            recall=recall
        )

        return {
            'f_measure': f_measure,
            'precision': precision,
            'recall': recall
        }

    def overall_error_rate(self):
        """Overall error rate metrics (error_rate, substitution_rate, deletion_rate, and insertion_rate)

        Returns
        -------
        dict
            results in a dictionary format

        """

        substitution_rate = metric.substitution_rate(
            Nref=self.overall['Nref'],
            Nsubstitutions=self.overall['Nsubs']
        )

        deletion_rate = metric.deletion_rate(
            Nref=self.overall['Nref'],
            Ndeletions=self.overall['Nfn']
        )

        insertion_rate = metric.insertion_rate(
            Nref=self.overall['Nref'],
            Ninsertions=self.overall['Nfp']
        )

        error_rate = metric.error_rate(
            substitution_rate_value=substitution_rate,
            deletion_rate_value=deletion_rate,
            insertion_rate_value=insertion_rate
        )

        return {
            'error_rate': error_rate,
            'substitution_rate': substitution_rate,
            'deletion_rate': deletion_rate,
            'insertion_rate': insertion_rate
        }

    def class_wise_intermediate_counts(self, event_label):
        """Class-wise counts (Nref and Nsys)

        Returns
        -------
        dict
            results in a dictionary format

        """

        return {
            'Nref': self.class_wise[event_label]['Nref'],
            'Nsys': self.class_wise[event_label]['Nsys']
        }

    def class_wise_f_measure(self, event_label):
        """Class-wise f-measure metrics (f_measure, precision, and recall)

        Returns
        -------
        dict
            results in a dictionary format

        """
        if self.class_wise[event_label]['Nsys'] == 0 and self.empty_system_output_handling == 'zero_score':
            precision = 0

        else:
            precision = metric.precision(
                Ntp=self.class_wise[event_label]['Ntp'],
                Nsys=self.class_wise[event_label]['Nsys']
            )

        recall = metric.recall(
            Ntp=self.class_wise[event_label]['Ntp'],
            Nref=self.class_wise[event_label]['Nref']
        )

        f_measure = metric.f_measure(
            precision=precision,
            recall=recall
        )

        return {
            'f_measure': f_measure,
            'precision': precision,
            'recall': recall
        }

    def class_wise_error_rate(self, event_label):
        """Class-wise error rate metrics (error_rate, deletion_rate, and insertion_rate)

        Returns
        -------
        dict
            results in a dictionary format

        """

        deletion_rate = metric.deletion_rate(
            Nref=self.class_wise[event_label]['Nref'],
            Ndeletions=self.class_wise[event_label]['Nfn']
        )

        insertion_rate = metric.insertion_rate(
            Nref=self.class_wise[event_label]['Nref'],
            Ninsertions=self.class_wise[event_label]['Nfp']
        )

        error_rate = metric.error_rate(
            deletion_rate_value=deletion_rate,
            insertion_rate_value=insertion_rate
        )

        return {
            'error_rate': error_rate,
            'deletion_rate': deletion_rate,
            'insertion_rate': insertion_rate
        }

    # Reports
    def result_report_parameters(self):
        """Report metric parameters

        Returns
        -------
        str
            result report in string format

        """

        output = self.ui.data(field='Evaluated length', value=self.evaluated_length, unit='sec') + '\n'
        output += self.ui.data(field='Evaluated files', value=self.evaluated_files) + '\n'

        output += self.ui.data(field='Evaluate onset', value=self.evaluate_onset) + '\n'
        output += self.ui.data(field='Evaluate offset', value=self.evaluate_offset) + '\n'

        if self.t_collar < 1:
            output += self.ui.data(field='T collar', value=self.t_collar*1000, unit='ms') + '\n'

        else:
            output += self.ui.data(field='T collar', value=self.t_collar, unit='sec') + '\n'

        output += self.ui.data(field='Offset (length)', value=self.percentage_of_length*100, unit='%') + '\n'

        return output
