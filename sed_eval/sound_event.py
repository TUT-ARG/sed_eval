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


Usage example when reading event lists from disk:

.. code-block:: python
    :linenos:

    import sed_eval

    file_list = [
        {
         'reference_file': 'office_snr0_high_v2.txt',
         'estimated_file': 'office_snr0_high_out.txt'
        },
        {
         'reference_file': 'office_snr0_low_v2.txt',
         'estimated_file': 'office_snr0_low_out.txt'
        },
        {
         'reference_file': 'office_snr0_med_v2.txt',
         'estimated_file': 'office_snr0_med_out.txt'
        },
        {
         'reference_file': 'office_snr-6_high_v2.txt',
         'estimated_file': 'office_snr-6_high_out.txt'
        }
    ]

    data = []

    # Get used event labels
    all_data = sed_eval.util.event_list.EventList()
    for file_pair in file_list:
        reference_event_list = sed_eval.io.load_event_list(file_pair['reference_file'])
        estimated_event_list = sed_eval.io.load_event_list(file_pair['estimated_file'])
        data.append({'reference_event_list': reference_event_list,
                     'estimated_event_list': estimated_event_list})
        all_data += reference_event_list
    event_labels = all_data.unique_event_labels

    # Start evaluating

    # Create metrics classes, define parameters
    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(event_label_list=event_labels,
                                                                     time_resolution=1)
    event_based_metrics = sed_eval.sound_event.EventBasedMetrics(event_label_list=event_labels,
                                                                 t_collar=0.250)

    # Go through files
    for file_pair in data:
        segment_based_metrics.evaluate(file_pair['reference_event_list'],
                                       file_pair['estimated_event_list'])
        event_based_metrics.evaluate(file_pair['reference_event_list'],
                                     file_pair['estimated_event_list'])

    # Get only certain metrics
    overall_segment_based_metrics = segment_based_metrics.results_overall_metrics()
    print "Accuracy:", overall_segment_based_metrics['accuracy']['accuracy']

    # Or print all metrics as reports
    print segment_based_metrics
    print event_based_metrics

Usage example:

.. code-block:: python
    :linenos:

    import sed_eval

    reference_event_list = sed_eval.util.EventList(
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

    estimated_event_list = sed_eval.util.EventList(
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

    # Go through files
    for file in reference_event_list.unique_files:
        # Get reference event list for file by filtering reference_event_list
        reference_event_list_for_current_file = reference_event_list.filter(file=file)

        # Get estimated event list for file by filtering estimated_event_list
        estimated_event_list_for_current_file = estimated_event_list.filter(file=file)

        segment_based_metrics.evaluate(
            reference_event_list=reference_event_list_for_current_file,
            estimated_event_list=estimated_event_list_for_current_file
        )

    # Get only certain metrics
    overall_segment_based_metrics = segment_based_metrics.results_overall_metrics()
    print "Accuracy:", overall_segment_based_metrics['accuracy']['accuracy']

    # Or print all metrics as reports
    print segment_based_metrics

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
from . import metric
from . import util
from .util.event_list import EventList


class SoundEventMetrics(object):
    """Base class for sound event detection metrics.

    """
    def __init__(self):
        self.event_label_list = []

    # Reports
    def result_report_overall(self):
        """Report overall results

        Parameters
        ----------
        Nothing

        Returns
        -------
        report : str
            result report in string format

        """

        results = self.results_overall_metrics()
        output = "  Overall metrics (micro-average)\n"
        output += "  ===============\n"
        if results['f_measure']:
            output += "  F-measure\n"
            output += "    {:17s} : {:5.1f} %\n".format('F-measure (F)', float(results['f_measure']['f_measure'])*100)
            output += "    {:17s} : {:5.1f} %\n".format('Precision', float(results['f_measure']['precision'])*100)
            output += "    {:17s} : {:5.1f} %\n".format('Recall', float(results['f_measure']['recall'])*100)
        if results['error_rate']:
            output += "  Error rate\n"
            output += "    {:17s} :  {:3.2f}\n".format('Error rate (ER)', float(results['error_rate']['error_rate']))
            output += "    {:17s} :  {:3.2f}\n".format('Substitution rate', float(results['error_rate']['substitution_rate']))
            output += "    {:17s} :  {:3.2f}\n".format('Deletion rate', float(results['error_rate']['deletion_rate']))
            output += "    {:17s} :  {:3.2f}\n".format('Insertion rate', float(results['error_rate']['insertion_rate']))
        if results['accuracy']:
            output += "  Accuracy\n"
            output += "    {:17s} : {:5.1f} %\n".format('Sensitivity', float(results['accuracy']['sensitivity'])*100)
            output += "    {:17s} : {:5.1f} %\n".format('Specificity', float(results['accuracy']['specificity'])*100)
            output += "    {:17s} : {:5.1f} %\n".format('Balanced accuracy', float(results['accuracy']['balanced_accuracy'])*100)
            output += "    {:17s} : {:5.1f} %\n".format('Accuracy', float(results['accuracy']['accuracy'])*100)
        output += "  \n"
        return output

    def result_report_class_wise_average(self):
        """Report class-wise averages

        Parameters
        ----------
        Nothing

        Returns
        -------
        report : str
            result report in string format

        """

        results = self.results_class_wise_average_metrics()
        output = "  Class-wise average metrics (macro-average)\n"
        output += "  ===============\n"
        if results['f_measure']:
            output += "  F-measure\n"
            output += "    {:17s} : {:5.1f} %\n".format('F-measure (F)', float(results['f_measure']['f_measure'])*100)
            output += "    {:17s} : {:5.1f} %\n".format('Precision', float(results['f_measure']['precision'])*100)
            output += "    {:17s} : {:5.1f} %\n".format('Recall', float(results['f_measure']['recall'])*100)
        if results['error_rate']:
            output += "  Error rate\n"
            output += "    {:17s} :  {:3.2f}\n".format('Error rate (ER)', float(results['error_rate']['error_rate']))
            output += "    {:17s} :  {:3.2f}\n".format('Deletion rate', float(results['error_rate']['deletion_rate']))
            output += "    {:17s} :  {:3.2f}\n".format('Insertion rate', float(results['error_rate']['insertion_rate']))
        if results['accuracy']:
            output += "  Accuracy\n"
            output += "    {:17s} : {:5.1f} %\n".format('Sensitivity', float(results['accuracy']['sensitivity'])*100)
            output += "    {:17s} : {:5.1f} %\n".format('Specificity', float(results['accuracy']['specificity'])*100)
            output += "    {:17s} : {:5.1f} %\n".format('Balanced accuracy', float(results['accuracy']['balanced_accuracy'])*100)
            output += "    {:17s} : {:5.1f} %\n".format('Accuracy', float(results['accuracy']['accuracy'])*100)

        output += "  \n"
        return output

    def result_report_class_wise(self):
        """Report class-wise results

        Parameters
        ----------
        Nothing

        Returns
        -------
        report : str
            result report in string format

        """

        results = self.results_class_wise_metrics()

        accuracy_present = True
        for event_label in self.event_label_list:
            if 'accuracy' not in results[event_label]['accuracy']:
                accuracy_present = False

        output = "  Class-wise metrics\n"
        output += "  ===============\n"

        output += "    {:17s} | {:^4s} | {:^4s} | {:^7s} : {:^7s} : {:^7s} | {:^5s} : {:^5s} : {:^5s} |".format('Event label',
                                                                                                                  'Nref',
                                                                                                                  'Nsys',
                                                                                                                  'F',
                                                                                                                  'Pre',
                                                                                                                  'Rec',
                                                                                                                  'ER',
                                                                                                                  'Del',
                                                                                                                  'Ins')
        if accuracy_present:
            output += " {:^7s} : {:^7s} : {:^7s} | {:^7s} |".format('Sens', 'Spec', 'Bacc', 'Acc')
        output += "\n"

        output += "    ------------------+------+------+---------+---------+---------+-------+-------+-------+"
        if accuracy_present:
            output += "---------+---------+---------+---------+"
        output += "\n"

        for event_label in self.event_label_list:
            output += "    {:17s} | {:4.0f} | {:4.0f} | {:5.1f} %   {:5.1f} %   {:5.1f} % |  {:3.2f}    {:3.2f}    {:3.2f} |".format(event_label,
                                                                    results[event_label]['count']['Nref'],
                                                                    results[event_label]['count']['Nsys'],
                                                                    results[event_label]['f_measure']['f_measure']*100,
                                                                    results[event_label]['f_measure']['precision']*100,
                                                                    results[event_label]['f_measure']['recall']*100,
                                                                    results[event_label]['error_rate']['error_rate'],
                                                                    results[event_label]['error_rate']['deletion_rate'],
                                                                    results[event_label]['error_rate']['insertion_rate'])
            if accuracy_present:
                output += " {:5.1f} %   {:5.1f} %   {:5.1f} % | {:5.1f} % |".format(results[event_label]['accuracy']['sensitivity']*100,
                                                                                    results[event_label]['accuracy']['specificity']*100,
                                                                                    results[event_label]['accuracy']['balanced_accuracy']*100,
                                                                                    results[event_label]['accuracy']['accuracy']*100)
            output += "\n"
        output += "  \n"
        return output

    # Metrics / overall
    def overall_f_measure(self):
        return {}

    def overall_error_rate(self):
        return {}

    def overall_accuracy(self, factor=0.5):
        return {}
    
    # Metrics / class-wise
    def class_wise_count(self, event_label):
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

        Parameters
        ----------
        Nothing

        Returns
        -------
        results : dict
            results in a dictionary format

        """

        return {'f_measure': self.overall_f_measure(),
                'error_rate': self.overall_error_rate(),
                'accuracy': self.overall_accuracy()}

    def results_class_wise_metrics(self):
        """Class-wise metrics

        Parameters
        ----------
        Nothing

        Returns
        -------
        results : dict
            results in a dictionary format

        """

        results = {}
        for event_label in self.event_label_list:
            if event_label not in results:
                results[event_label] = {}

            results[event_label]['f_measure'] = self.class_wise_f_measure(event_label)
            results[event_label]['accuracy'] = self.class_wise_accuracy(event_label)
            results[event_label]['error_rate'] = self.class_wise_error_rate(event_label)
            results[event_label]['count'] = self.class_wise_count(event_label)
        return results

    def results_class_wise_average_metrics(self):
        """Class-wise averaged metrics

        Parameters
        ----------
        Nothing

        Returns
        -------
        results : dict
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
            event_wise_accuracy_dict = {'sensitivity': float(numpy.nanmean(event_wise_sensitivity)),
                                        'specificity': float(numpy.nanmean(event_wise_specificity)),
                                        'balanced_accuracy': float(numpy.nanmean(event_wise_balanced_accuracy)),
                                        'accuracy': float(numpy.nanmean(event_wise_accuracy))}
        else:
            event_wise_accuracy_dict = {}

        return {'f_measure': event_wise_f_measure_dict,
                'error_rate': event_wise_error_rate_dict,
                'accuracy':event_wise_accuracy_dict
                }

    def results(self):
        """All metrics

        Parameters
        ----------
        Nothing

        Returns
        -------
        results : dict
            results in a dictionary format

        """

        return {'overall': self.results_overall_metrics(),
                'class_wise': self.results_class_wise_metrics(),
                'class_wise_average': self.results_class_wise_average_metrics()}


class SegmentBasedMetrics(SoundEventMetrics):
    def __init__(self,
                 event_label_list,
                 time_resolution=1.0):
        """Constructor

        Parameters
        ----------
        event_label_list : list, numpy.array
            List of unique event labels
        time_resolution : float (0,]
            Segment size used in the evaluation, in seconds
            (Default value=1.0)

        Returns
        -------
        Nothing

        """

        SoundEventMetrics.__init__(self)

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
        self.evaluated_length = 0.0
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
        """Print result reports

        Parameters
        ----------
            Nothing

        Returns
        -------
        report : str
            result report in string format

        """

        output = "\nSegment based metrics \n"
        output += "----------------------------------------------------------------------\n"
        output += self.result_report_parameters()
        output += self.result_report_overall()
        output += self.result_report_class_wise_average()
        output += self.result_report_class_wise()
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
            Nothing

        """

        # Check that input event list have event only from one file
        reference_files = EventList(reference_event_list).unique_files
        if len(reference_files) > 1:
            raise ValueError(
                "reference_event_list contains events from multiple files. Evaluate only file by file."
            )

        estimated_files = EventList(estimated_event_list).unique_files
        if len(estimated_files) > 1:
            raise ValueError(
                "estimated_event_list contains events from multiple files. Evaluate only file by file."
            )

        # Evaluate only valid events
        valid_reference_event_list = EventList()
        for item in reference_event_list:
            if 'event_onset' in item and 'event_offset' in item and 'event_label' in item:
                valid_reference_event_list.append(item)
        reference_event_list = valid_reference_event_list

        valid_estimated_event_list = EventList()
        for item in estimated_event_list:
            if 'event_onset' in item and 'event_offset' in item and 'event_label' in item:
                valid_estimated_event_list.append(item)
        estimated_event_list = valid_estimated_event_list


        # Convert event list into frame-based representation
        reference_event_roll = util.event_list_to_event_roll(source_event_list=reference_event_list,
                                                             event_label_list=self.event_label_list,
                                                             time_resolution=self.time_resolution)

        estimated_event_roll = util.event_list_to_event_roll(source_event_list=estimated_event_list,
                                                             event_label_list=self.event_label_list,
                                                             time_resolution=self.time_resolution)

        self.evaluated_length += max(util.max_event_offset(reference_event_list), util.max_event_offset(estimated_event_list))
        self.evaluated_files += 1

        reference_event_roll, estimated_event_roll = util.match_event_roll_lengths(reference_event_roll, estimated_event_roll)

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
        """Reset internal state
        """

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

    # Reports
    def result_report_parameters(self):
        """Report metric parameters

        Parameters
        ----------
            Nothing

        Returns
        -------
        report : str
            result report in string format
        
        """

        output = ''
        output += "    {:17s} : {:<5.1f} sec\n".format('Evaluated length', self.evaluated_length)
        output += "    {:17s} : {:<5d} files\n".format('Evaluated files', self.evaluated_files)

        if self.time_resolution < 1:
            output += "    {:17s} : {:<5.0f} ms\n".format('Segment length', self.time_resolution*1000)
        else:
            output += "    {:17s} : {:<5.2f} sec\n".format('Segment length', self.time_resolution)

        output += "  \n"
        return output

    # Metrics
    def overall_f_measure(self):
        """Overall f-measure metrics (f_measure, precision, and recall)

        Parameters
        ----------
        Nothing

        Returns
        -------
        results : dict
            results in a dictionary format

        """

        precision = metric.precision(self.overall['Ntp'], self.overall['Nsys'])
        recall = metric.recall(self.overall['Ntp'], self.overall['Nref'])
        f_measure = metric.f_measure(precision=precision, recall=recall)
        return {'f_measure': f_measure,
                'precision': precision,
                'recall': recall}

    def overall_error_rate(self):
        """Overall error rate metrics (error_rate, substitution_rate, deletion_rate, and insertion_rate)

        Parameters
        ----------
        Nothing

        Returns
        -------
        results : dict
            results in a dictionary format

        """

        substitution_rate = metric.substitution_rate(Nref=self.overall['Nref'],
                                                     Nsubstitutions=self.overall['S'])
        deletion_rate = metric.deletion_rate(Nref=self.overall['Nref'],
                                             Ndeletions=self.overall['D'])
        insertion_rate = metric.insertion_rate(Nref=self.overall['Nref'],
                                               Ninsertions=self.overall['I'])
        error_rate = metric.error_rate(substitution_rate_value=substitution_rate,
                                       deletion_rate_value=deletion_rate,
                                       insertion_rate_value=insertion_rate)

        return {'error_rate': error_rate,
                'substitution_rate': substitution_rate,
                'deletion_rate': deletion_rate,
                'insertion_rate': insertion_rate}

    def overall_accuracy(self, factor=0.5):
        """Overall accuracy metrics (sensitivity, specificity, accuracy, and balanced_accuracy)

        Parameters
        ----------
        factor : float [0-1]
            balance factor
            (Default value=0.5)

        Returns
        -------
        results : dict
            results in a dictionary format

        """

        sensitivity = metric.sensitivity(Ntp=self.overall['Ntp'], Nfn=self.overall['Nfn'])
        specificity = metric.specificity(Ntn=self.overall['Ntn'], Nfp=self.overall['Nfp'])
        balanced_accuracy = metric.balanced_accuracy(sensitivity=sensitivity,
                                                     specificity=specificity,
                                                     factor=factor)
        accuracy = metric.accuracy(Ntp=self.overall['Ntp'], Ntn=self.overall['Ntn'], Nfp=self.overall['Nfp'], Nfn=self.overall['Nfn'])
        return {
                'accuracy': accuracy,
                'balanced_accuracy': balanced_accuracy,            
                'sensitivity': sensitivity,
                'specificity': specificity
                }

    def class_wise_count(self, event_label):
        """Class-wise counts (Nref and Nsys)

        Parameters
        ----------
        Nothing

        Returns
        -------
        results : dict
            results in a dictionary format

        """

        return {'Nref': float(self.class_wise[event_label]['Nref']),
                'Nsys': float(self.class_wise[event_label]['Nsys'])}

    def class_wise_f_measure(self, event_label):
        """Class-wise f-measure metrics (f_measure, precision, and recall)

        Parameters
        ----------
        Nothing

        Returns
        -------
        results : dict
            results in a dictionary format

        """

        precision = metric.precision(self.class_wise[event_label]['Ntp'], self.class_wise[event_label]['Nsys'])
        recall = metric.recall(self.class_wise[event_label]['Ntp'], self.class_wise[event_label]['Nref'])
        f_measure = metric.f_measure(precision=precision, recall=recall)
        return {'f_measure': f_measure,
                'precision': precision,
                'recall': recall}

    def class_wise_error_rate(self, event_label):
        """Class-wise error rate metrics (error_rate, deletion_rate, and insertion_rate)

        Parameters
        ----------
        Nothing

        Returns
        -------
        results : dict
            results in a dictionary format

        """

        deletion_rate = metric.deletion_rate(Nref=self.class_wise[event_label]['Nref'],
                                             Ndeletions=self.class_wise[event_label]['Nfn'])
        insertion_rate = metric.insertion_rate(Nref=self.class_wise[event_label]['Nref'],
                                               Ninsertions=self.class_wise[event_label]['Nfp'])
        error_rate = metric.error_rate(deletion_rate_value=deletion_rate,
                                       insertion_rate_value=insertion_rate)
        return {'error_rate': error_rate,
                'deletion_rate': deletion_rate,
                'insertion_rate': insertion_rate}

    def class_wise_accuracy(self, event_label, factor=0.5):
        """Class-wise accuracy metrics (sensitivity, specificity, accuracy, and balanced_accuracy)

        Parameters
        ----------
        Nothing

        Returns
        -------
        results : dict
            results in a dictionary format

        """

        sensitivity = metric.sensitivity(Ntp=self.class_wise[event_label]['Ntp'], Nfn=self.class_wise[event_label]['Nfn'])
        specificity = metric.specificity(Ntn=self.class_wise[event_label]['Ntn'], Nfp=self.class_wise[event_label]['Nfp'])
        balanced_accuracy = metric.balanced_accuracy(sensitivity=sensitivity,
                                                     specificity=specificity,
                                                     factor=factor)

        accuracy = metric.accuracy(Ntp=self.class_wise[event_label]['Ntp'],
                                   Ntn=self.class_wise[event_label]['Ntn'],
                                   Nfp=self.class_wise[event_label]['Nfp'],
                                   Nfn=self.class_wise[event_label]['Nfn'])

        return {
                'accuracy': accuracy,
                'balanced_accuracy': balanced_accuracy,
                'sensitivity': sensitivity,
                'specificity': specificity
                }


class EventBasedMetrics(SoundEventMetrics):
    def __init__(self,
                 event_label_list,
                 evaluate_onset=True,
                 evaluate_offset=True,
                 t_collar=0.200,
                 percentage_of_length=0.5):
        """Constructor

        Parameters
        ----------
        event_label_list : list
            List of unique event labels

        evaluate_onset : bool
            Evaluate onset
            (Default value=True)

        evaluate_offset : bool
            Evaluate offset
            (Default value=True)

        t_collar : float (0,]
            Time collar used when evaluating validty of the onset and offset, in seconds
            (Default value=0.2)

        percentage_of_length : float in [0, 1]
            Second condition, percentage of the length within which the estimated offset has to be in order to be consider valid estimation
            (Default value = 0.5)

        Returns
        -------
            Nothing

        """

        SoundEventMetrics.__init__(self)

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

    @staticmethod
    def validate_onset(reference_event, estimated_event, t_collar=0.200):
        """Validate estimated event based on event onset

        Parameters
        ----------
        reference_event : dict
            Reference event
        estimated_event: dict
            Estimated event
        t_collar : float > 0, seconds
            Time collar with which the estimated onset has to be in order to be consider valid estimation
            (Default value = 0.2)

        Returns
        -------
        validity: bool

        """

        return math.fabs(reference_event['event_onset'] - estimated_event['event_onset']) <= t_collar

    @staticmethod
    def validate_offset(reference_event, estimated_event, t_collar=0.200, percentage_of_length=0.5):
        """Validate estimated event based on event offset

        Parameters
        ----------
        reference_event : dict
            Reference event

        estimated_event : dict
            Estimated event

        t_collar : float > 0, seconds
            First condition, Time collar with which the estimated offset has to be in order to be consider valid estimation
            (Default value = 0.2)

        percentage_of_length : float in [0, 1]
            Second condition, percentage of the length within which the estimated offset has to be in order to be consider valid estimation
            (Default value = 0.5)

        Returns
        -------
        validity : bool

        """

        annotated_length = reference_event['event_offset'] - reference_event['event_onset']
        return math.fabs(reference_event['event_offset'] - estimated_event['event_offset']) <= max(t_collar, percentage_of_length * annotated_length)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self.results()

    def __str__(self):
        """Print result reports

        Parameters
        ----------
            Nothing

        Returns
        -------
        report: str
            result report in string format
        """
        if self.evaluate_onset and self.evaluate_offset:
            output = "\nEvent based metrics (onset-offset)\n"
        elif self.evaluate_onset and not self.evaluate_offset:
            output = "\nEvent based metrics (onset only)\n"
        elif not self.evaluate_onset and self.evaluate_offset:
            output = "\nEvent based metrics (offset only)\n"
        else:
            output = "\nEvent based metrics\n"

        output += "----------------------------------------------------------------------\n"
        output += self.result_report_parameters()
        output += self.result_report_overall()
        output += self.result_report_class_wise_average()
        output += self.result_report_class_wise()
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
            Nothing

        """

        # Check that input event list have event only from one file
        reference_files = EventList(reference_event_list).unique_files
        if len(reference_files) > 1:
            raise ValueError(
                "reference_event_list contains events from multiple files. Evaluate only file by file."
            )

        estimated_files = EventList(estimated_event_list).unique_files
        if len(estimated_files) > 1:
            raise ValueError(
                "estimated_event_list contains events from multiple files. Evaluate only file by file."
            )

        # Evaluate only valid events
        valid_reference_event_list = EventList()
        for item in reference_event_list:
            if 'event_onset' in item and 'event_offset' in item and 'event_label' in item:
                valid_reference_event_list.append(item)
        reference_event_list = valid_reference_event_list

        valid_estimated_event_list = EventList()
        for item in estimated_event_list:
            if 'event_onset' in item and 'event_offset' in item and 'event_label' in item:
                valid_estimated_event_list.append(item)
        estimated_event_list = valid_estimated_event_list

        self.evaluated_length += util.max_event_offset(reference_event_list)
        self.evaluated_files += 1

        # Overall metrics

        # Total number of detected and reference events
        Nsys = len(estimated_event_list)
        Nref = len(reference_event_list)

        sys_correct = numpy.zeros(Nsys, dtype=bool)
        ref_correct = numpy.zeros(Nref, dtype=bool)

        # Number of correctly detected events
        for j in range(0, len(reference_event_list)):
            for i in range(0, len(estimated_event_list)):
                if not sys_correct[i]:  # skip already matched events
                    label_condition = reference_event_list[j]['event_label'] == estimated_event_list[i]['event_label']

                    if self.evaluate_onset:
                        onset_condition = self.validate_onset(reference_event=reference_event_list[j],
                                                              estimated_event=estimated_event_list[i],
                                                              t_collar=self.t_collar)
                    else:
                        onset_condition = True

                    if self.evaluate_offset:
                        offset_condition = self.validate_offset(reference_event=reference_event_list[j],
                                                                estimated_event=estimated_event_list[i],
                                                                t_collar=self.t_collar,
                                                                percentage_of_length=self.percentage_of_length)
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
                        onset_condition = self.validate_onset(reference_event=reference_event_list[j],
                                                              estimated_event=estimated_event_list[i],
                                                              t_collar=self.t_collar)
                    else:
                        onset_condition = True

                    if self.evaluate_offset:
                        offset_condition = self.validate_offset(reference_event=reference_event_list[j],
                                                                estimated_event=estimated_event_list[i],
                                                                t_collar=self.t_collar,
                                                                percentage_of_length=self.percentage_of_length)
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

            sys_counted = numpy.zeros(len(estimated_event_list), dtype=bool)
            for j in range(0, len(reference_event_list)):
                if reference_event_list[j]['event_label'] == class_label:
                    for i in range(0, len(estimated_event_list)):
                        if estimated_event_list[i]['event_label'] == class_label and not sys_counted[i]:
                            if self.evaluate_onset:
                                onset_condition = self.validate_onset(reference_event=reference_event_list[j],
                                                                      estimated_event=estimated_event_list[i],
                                                                      t_collar=self.t_collar)
                            else:
                                onset_condition = True

                            if self.evaluate_offset:
                                offset_condition = self.validate_offset(reference_event=reference_event_list[j],
                                                                        estimated_event=estimated_event_list[i],
                                                                        t_collar=self.t_collar,
                                                                        percentage_of_length=self.percentage_of_length)
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

    # Reports
    def result_report_parameters(self):
        """Report metric parameters

        Parameters
        ----------
        Nothing

        Returns
        -------
        report : str
            result report in string format

        """

        output = ''
        output += "    {:17s} : {:5.1f} sec\n".format('Evaluated length', self.evaluated_length)
        output += "    {:17s} : {:<5d} files\n".format('Evaluated files', self.evaluated_files)

        output += "    {:17s} : {} \n".format('Evaluate onset', self.evaluate_onset)
        output += "    {:17s} : {} \n".format('Evaluate offset', self.evaluate_offset)
        if self.t_collar < 1:
            output += "    {:17s} : {:<5.0f} ms\n".format('T collar', self.t_collar*1000)
        else:
            output += "    {:17s} : {:<5.1f} sec\n".format('T collar', self.t_collar)

        output += "    {:17s} : {:<5.0f} %\n".format('Offset (length)', self.percentage_of_length*100)
        output += "  \n"
        return output

    # Metrics
    def overall_f_measure(self):
        """Overall f-measure metrics (f_measure, precision, and recall)

        Parameters
        ----------
        Nothing

        Returns
        -------
        results : dict
            results in a dictionary format
        """
        precision = metric.precision(self.overall['Ntp'], self.overall['Nsys'])
        recall = metric.recall(self.overall['Ntp'], self.overall['Nref'])
        f_measure = metric.f_measure(precision=precision, recall=recall)
        return {'f_measure': f_measure,
                'precision': precision,
                'recall': recall}

    def overall_error_rate(self):
        """Overall error rate metrics (error_rate, substitution_rate, deletion_rate, and insertion_rate)

        Parameters
        ----------
        Nothing

        Returns
        -------
        results : dict
            results in a dictionary format

        """

        substitution_rate = metric.substitution_rate(Nref=self.overall['Nref'],
                                                     Nsubstitutions=self.overall['Nsubs'])
        deletion_rate = metric.deletion_rate(Nref=self.overall['Nref'],
                                             Ndeletions=self.overall['Nfn'])
        insertion_rate = metric.insertion_rate(Nref=self.overall['Nref'],
                                               Ninsertions=self.overall['Nfp'])
        error_rate = metric.error_rate(substitution_rate_value=substitution_rate,
                                       deletion_rate_value=deletion_rate,
                                       insertion_rate_value=insertion_rate)

        return {'error_rate': error_rate,
                'substitution_rate': substitution_rate,
                'deletion_rate': deletion_rate,
                'insertion_rate': insertion_rate}

    def class_wise_count(self, event_label):
        """Class-wise counts (Nref and Nsys)

        Parameters
        ----------
        Nothing

        Returns
        -------
        results : dict
            results in a dictionary format

        """

        return {'Nref': self.class_wise[event_label]['Nref'],
                'Nsys': self.class_wise[event_label]['Nsys']}

    def class_wise_f_measure(self, event_label):
        """Class-wise f-measure metrics (f_measure, precision, and recall)

        Parameters
        ----------
        Nothing

        Returns
        -------
        results : dict
            results in a dictionary format

        """

        precision = metric.precision(self.class_wise[event_label]['Ntp'], self.class_wise[event_label]['Nsys'])
        recall = metric.recall(self.class_wise[event_label]['Ntp'], self.class_wise[event_label]['Nref'])
        f_measure = metric.f_measure(precision=precision, recall=recall)
        return {'f_measure': f_measure,
                'precision': precision,
                'recall': recall}

    def class_wise_error_rate(self, event_label):
        """Class-wise error rate metrics (error_rate, deletion_rate, and insertion_rate)

        Parameters
        ----------
        Nothing

        Returns
        -------
        results : dict
            results in a dictionary format

        """

        deletion_rate = metric.deletion_rate(Nref=self.class_wise[event_label]['Nref'],
                                             Ndeletions=self.class_wise[event_label]['Nfn'])
        insertion_rate = metric.insertion_rate(Nref=self.class_wise[event_label]['Nref'],
                                               Ninsertions=self.class_wise[event_label]['Nfp'])
        error_rate = metric.error_rate(deletion_rate_value=deletion_rate,
                                       insertion_rate_value=insertion_rate)
        return {'error_rate': error_rate,
                'deletion_rate': deletion_rate,
                'insertion_rate': insertion_rate}