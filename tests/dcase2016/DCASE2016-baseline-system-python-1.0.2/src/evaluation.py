#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy
import math
from sklearn import metrics

class DCASE2016_SceneClassification_Metrics():
    """DCASE 2016 scene classification metrics

    Examples
    --------

        >>> dcase2016_scene_metric = DCASE2016_SceneClassification_Metrics(class_list=dataset.scene_labels)
        >>> for fold in dataset.folds(mode=dataset_evaluation_mode):
        >>>     results = []
        >>>     result_filename = get_result_filename(fold=fold, path=result_path)
        >>>
        >>>     if os.path.isfile(result_filename):
        >>>         with open(result_filename, 'rt') as f:
        >>>             for row in csv.reader(f, delimiter='\t'):
        >>>                 results.append(row)
        >>>
        >>>     y_true = []
        >>>     y_pred = []
        >>>     for result in results:
        >>>         y_true.append(dataset.file_meta(result[0])[0]['scene_label'])
        >>>         y_pred.append(result[1])
        >>>
        >>>     dcase2016_scene_metric.evaluate(system_output=y_pred, annotated_ground_truth=y_true)
        >>>
        >>> results = dcase2016_scene_metric.results()

    """

    def __init__(self, class_list):
        """__init__ method.

        Parameters
        ----------
        class_list : list
            Evaluated scene labels in the list

        """
        self.accuracies_per_class = None
        self.Nsys = None
        self.Nref = None
        self.class_list = class_list
        self.eps = numpy.spacing(1)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self.results()

    def accuracies(self, y_true, y_pred, labels):
        """Calculate accuracy

        Parameters
        ----------
        y_true : numpy.array
            Ground truth array, list of scene labels

        y_pred : numpy.array
            System output array, list of scene labels

        labels : list
            list of scene labels

        Returns
        -------
        array : numpy.array [shape=(number of scene labels,)]
            Accuracy per scene label class

        """

        confusion_matrix = metrics.confusion_matrix(y_true=y_true, y_pred=y_pred, labels=labels).astype(float)
        return numpy.divide(numpy.diag(confusion_matrix), numpy.sum(confusion_matrix, 1)+self.eps)

    def evaluate(self, annotated_ground_truth, system_output):
        """Evaluate system output and annotated ground truth pair.

        Use results method to get results.

        Parameters
        ----------
        annotated_ground_truth : numpy.array
            Ground truth array, list of scene labels

        system_output : numpy.array
            System output array, list of scene labels

        Returns
        -------
        nothing

        """

        accuracies_per_class = self.accuracies(y_true=system_output, y_pred=annotated_ground_truth, labels=self.class_list)

        if self.accuracies_per_class is None:
            self.accuracies_per_class = accuracies_per_class
        else:
            self.accuracies_per_class = numpy.vstack((self.accuracies_per_class, accuracies_per_class))

        Nref = numpy.zeros(len(self.class_list))
        Nsys = numpy.zeros(len(self.class_list))

        for class_id, class_label in enumerate(self.class_list):
            for item in system_output:
                if item == class_label:
                    Nsys[class_id] += 1

            for item in annotated_ground_truth:
                if item == class_label:
                    Nref[class_id] += 1

        if self.Nref is None:
            self.Nref = Nref
        else:
            self.Nref = numpy.vstack((self.Nref, Nref))

        if self.Nsys is None:
            self.Nsys = Nsys
        else:
            self.Nsys = numpy.vstack((self.Nsys, Nsys))

    def results(self):
        """Get results

        Outputs results in dict, format:

            {
                'class_wise_data':
                    {
                        'office': {
                            'Nsys': 10,
                            'Nref': 7,
                        },
                    }
                'class_wise_accuracy':
                    {
                        'office': 0.6,
                        'home': 0.4,
                    }
                'overall_accuracy': numpy.mean(self.accuracies_per_class)
                'Nsys': 100,
                'Nref': 100,
            }

        Parameters
        ----------
        nothing

        Returns
        -------
        results : dict
            Results dict

        """

        results = {
            'class_wise_data': {},
            'class_wise_accuracy': {},
            'overall_accuracy': numpy.mean(self.accuracies_per_class)
        }
        if len(self.Nsys.shape) == 2:
            results['Nsys'] = int(sum(sum(self.Nsys)))
            results['Nref'] = int(sum(sum(self.Nref)))
        else:
            results['Nsys'] = int(sum(self.Nsys))
            results['Nref'] = int(sum(self.Nref))

        for class_id, class_label in enumerate(self.class_list):
            if len(self.accuracies_per_class.shape) == 2:
                results['class_wise_accuracy'][class_label] = numpy.mean(self.accuracies_per_class[:, class_id])
                results['class_wise_data'][class_label] = {
                   'Nsys': int(sum(self.Nsys[:, class_id])),
                    'Nref': int(sum(self.Nref[:, class_id])),
                }
            else:
                results['class_wise_accuracy'][class_label] = numpy.mean(self.accuracies_per_class[class_id])
                results['class_wise_data'][class_label] = {
                   'Nsys': int(self.Nsys[class_id]),
                    'Nref': int(self.Nref[class_id]),
                }

        return results


class EventDetectionMetrics(object):
    """Baseclass for sound event metric classes.
    """

    def __init__(self, class_list):
        """__init__ method.

        Parameters
        ----------
        class_list : list
            List of class labels to be evaluated.

        """

        self.class_list = class_list
        self.eps = numpy.spacing(1)

    def max_event_offset(self, data):
        """Get maximum event offset from event list

        Parameters
        ----------
        data : list
            Event list, list of event dicts

        Returns
        -------
        max : float > 0
            Maximum event offset
        """

        max = 0
        for event in data:
            if event['event_offset'] > max:
                max = event['event_offset']
        return max

    def list_to_roll(self, data, time_resolution=0.01):
        """Convert event list into event roll.
        Event roll is binary matrix indicating event activity withing time segment defined by time_resolution.

        Parameters
        ----------
        data : list
            Event list, list of event dicts

        time_resolution : float > 0
            Time resolution used when converting event into event roll.

        Returns
        -------
        event_roll : numpy.ndarray [shape=(math.ceil(data_length * 1 / time_resolution) + 1, amount of classes)]
            Event roll
        """

        # Initialize
        data_length = self.max_event_offset(data)
        event_roll = numpy.zeros((math.ceil(data_length * 1 / time_resolution) + 1, len(self.class_list)))

        # Fill-in event_roll
        for event in data:
            pos = self.class_list.index(event['event_label'].rstrip())

            onset = math.floor(event['event_onset'] * 1 / time_resolution)
            offset = math.ceil(event['event_offset'] * 1 / time_resolution) + 1

            event_roll[onset:offset, pos] = 1

        return event_roll


class DCASE2016_EventDetection_SegmentBasedMetrics(EventDetectionMetrics):
    """DCASE2016 Segment based metrics for sound event detection

    Supported metrics:
    - Overall
        - Error rate (ER), Substitutions (S), Insertions (I), Deletions (D)
        - F-score (F1)
    - Class-wise
        - Error rate (ER), Insertions (I), Deletions (D)
        - F-score (F1)

    Examples
    --------

    >>> overall_metrics_per_scene = {}
    >>> for scene_id, scene_label in enumerate(dataset.scene_labels):
    >>>     dcase2016_segment_based_metric = DCASE2016_EventDetection_SegmentBasedMetrics(class_list=dataset.event_labels(scene_label=scene_label))
    >>>     for fold in dataset.folds(mode=dataset_evaluation_mode):
    >>>         results = []
    >>>         result_filename = get_result_filename(fold=fold, scene_label=scene_label, path=result_path)
    >>>
    >>>         if os.path.isfile(result_filename):
    >>>             with open(result_filename, 'rt') as f:
    >>>                 for row in csv.reader(f, delimiter='\t'):
    >>>                     results.append(row)
    >>>
    >>>         for file_id, item in enumerate(dataset.test(fold,scene_label=scene_label)):
    >>>             current_file_results = []
    >>>             for result_line in results:
    >>>                 if result_line[0] == dataset.absolute_to_relative(item['file']):
    >>>                     current_file_results.append(
    >>>                         {'file': result_line[0],
    >>>                          'event_onset': float(result_line[1]),
    >>>                          'event_offset': float(result_line[2]),
    >>>                          'event_label': result_line[3]
    >>>                          }
    >>>                     )
    >>>             meta = dataset.file_meta(dataset.absolute_to_relative(item['file']))
    >>>         dcase2016_segment_based_metric.evaluate(system_output=current_file_results, annotated_ground_truth=meta)
    >>> overall_metrics_per_scene[scene_label]['segment_based_metrics'] = dcase2016_segment_based_metric.results()

    """

    def __init__(self, class_list, time_resolution=1.0):
        """__init__ method.

        Parameters
        ----------
        class_list : list
            List of class labels to be evaluated.

        time_resolution : float > 0
            Time resolution used when converting event into event roll.
            (Default value = 1.0)

        """

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

        for class_label in class_list:
            self.class_wise[class_label] = {
                'Ntp': 0.0,
                'Ntn': 0.0,
                'Nfp': 0.0,
                'Nfn': 0.0,
                'Nref': 0.0,
                'Nsys': 0.0,
            }

        EventDetectionMetrics.__init__(self, class_list=class_list)

    def __enter__(self):
        # Initialize class and return it
        return self

    def __exit__(self, type, value, traceback):
        # Finalize evaluation and return results
        return self.results()

    def evaluate(self, annotated_ground_truth, system_output):
        """Evaluate system output and annotated ground truth pair.

        Use results method to get results.

        Parameters
        ----------
        annotated_ground_truth : numpy.array
            Ground truth array, list of scene labels

        system_output : numpy.array
            System output array, list of scene labels

        Returns
        -------
        nothing

        """

        # Convert event list into frame-based representation
        system_event_roll = self.list_to_roll(data=system_output, time_resolution=self.time_resolution)
        annotated_event_roll = self.list_to_roll(data=annotated_ground_truth, time_resolution=self.time_resolution)

        # Fix durations of both event_rolls to be equal
        if annotated_event_roll.shape[0] > system_event_roll.shape[0]:
            padding = numpy.zeros((annotated_event_roll.shape[0] - system_event_roll.shape[0], len(self.class_list)))
            system_event_roll = numpy.vstack((system_event_roll, padding))

        if system_event_roll.shape[0] > annotated_event_roll.shape[0]:
            padding = numpy.zeros((system_event_roll.shape[0] - annotated_event_roll.shape[0], len(self.class_list)))
            annotated_event_roll = numpy.vstack((annotated_event_roll, padding))

        # Compute segment-based overall metrics
        for segment_id in range(0, annotated_event_roll.shape[0]):
            annotated_segment = annotated_event_roll[segment_id, :]
            system_segment = system_event_roll[segment_id, :]

            Ntp = sum(system_segment + annotated_segment > 1)
            Ntn = sum(system_segment + annotated_segment == 0)
            Nfp = sum(system_segment - annotated_segment > 0)
            Nfn = sum(annotated_segment - system_segment > 0)

            Nref = sum(annotated_segment)
            Nsys = sum(system_segment)

            S = min(Nref, Nsys) - Ntp
            D = max(0, Nref - Nsys)
            I = max(0, Nsys - Nref)
            ER = max(Nref, Nsys) - Ntp

            self.overall['Ntp'] += Ntp
            self.overall['Ntn'] += Ntn
            self.overall['Nfp'] += Nfp
            self.overall['Nfn'] += Nfn
            self.overall['Nref'] += Nref
            self.overall['Nsys'] += Nsys
            self.overall['S'] += S
            self.overall['D'] += D
            self.overall['I'] += I
            self.overall['ER'] += ER

        for class_id, class_label in enumerate(self.class_list):
            annotated_segment = annotated_event_roll[:, class_id]
            system_segment = system_event_roll[:, class_id]

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

    def results(self):
        """Get results

        Outputs results in dict, format:

            {
                'overall':
                    {
                        'Pre':
                        'Rec':
                        'F':
                        'ER':
                        'S':
                        'D':
                        'I':
                    }
                'class_wise':
                    {
                        'office': {
                            'Pre':
                            'Rec':
                            'F':
                            'ER':
                            'D':
                            'I':
                            'Nref':
                            'Nsys':
                            'Ntp':
                            'Nfn':
                            'Nfp':
                        },
                    }
                'class_wise_average':
                    {
                        'F':
                        'ER':
                    }
            }

        Parameters
        ----------
        nothing

        Returns
        -------
        results : dict
            Results dict

        """

        results = {'overall': {},
                   'class_wise': {},
                   'class_wise_average': {},
                   }

        # Overall metrics
        results['overall']['Pre'] = self.overall['Ntp'] / (self.overall['Nsys'] + self.eps)
        results['overall']['Rec'] = self.overall['Ntp'] / self.overall['Nref']
        results['overall']['F'] = 2 * ((results['overall']['Pre'] * results['overall']['Rec']) / (results['overall']['Pre'] + results['overall']['Rec'] + self.eps))

        results['overall']['ER'] = self.overall['ER'] / self.overall['Nref']
        results['overall']['S'] = self.overall['S'] / self.overall['Nref']
        results['overall']['D'] = self.overall['D'] / self.overall['Nref']
        results['overall']['I'] = self.overall['I'] / self.overall['Nref']

        # Class-wise metrics
        class_wise_F = []
        class_wise_ER = []
        for class_id, class_label in enumerate(self.class_list):
            if class_label not in results['class_wise']:
                results['class_wise'][class_label] = {}
            results['class_wise'][class_label]['Pre'] = self.class_wise[class_label]['Ntp'] / (self.class_wise[class_label]['Nsys'] + self.eps)
            results['class_wise'][class_label]['Rec'] = self.class_wise[class_label]['Ntp'] / (self.class_wise[class_label]['Nref'] + self.eps)
            results['class_wise'][class_label]['F'] = 2 * ((results['class_wise'][class_label]['Pre'] * results['class_wise'][class_label]['Rec']) / (results['class_wise'][class_label]['Pre'] + results['class_wise'][class_label]['Rec'] + self.eps))

            results['class_wise'][class_label]['ER'] = (self.class_wise[class_label]['Nfn'] + self.class_wise[class_label]['Nfp']) / (self.class_wise[class_label]['Nref'] + self.eps)
            results['class_wise'][class_label]['D'] = self.class_wise[class_label]['Nfn'] / (self.class_wise[class_label]['Nref'] + self.eps)
            results['class_wise'][class_label]['I'] = self.class_wise[class_label]['Nfp'] / (self.class_wise[class_label]['Nref'] + self.eps)

            results['class_wise'][class_label]['Nref'] = self.class_wise[class_label]['Nref']
            results['class_wise'][class_label]['Nsys'] = self.class_wise[class_label]['Nsys']
            results['class_wise'][class_label]['Ntp'] = self.class_wise[class_label]['Ntp']
            results['class_wise'][class_label]['Nfn'] = self.class_wise[class_label]['Nfn']
            results['class_wise'][class_label]['Nfp'] = self.class_wise[class_label]['Nfp']

            class_wise_F.append(results['class_wise'][class_label]['F'])
            class_wise_ER.append(results['class_wise'][class_label]['ER'])

        results['class_wise_average']['F'] = numpy.mean(class_wise_F)
        results['class_wise_average']['ER'] = numpy.mean(class_wise_ER)

        return results


class DCASE2016_EventDetection_EventBasedMetrics(EventDetectionMetrics):
    """DCASE2016 Event based metrics for sound event detection

    Supported metrics:
    - Overall
        - Error rate (ER), Substitutions (S), Insertions (I), Deletions (D)
        - F-score (F1)
    - Class-wise
        - Error rate (ER), Insertions (I), Deletions (D)
        - F-score (F1)

    Examples
    --------

    >>> overall_metrics_per_scene = {}
    >>> for scene_id, scene_label in enumerate(dataset.scene_labels):
    >>>     dcase2016_event_based_metric = DCASE2016_EventDetection_EventBasedMetrics(class_list=dataset.event_labels(scene_label=scene_label))
    >>>     for fold in dataset.folds(mode=dataset_evaluation_mode):
    >>>         results = []
    >>>         result_filename = get_result_filename(fold=fold, scene_label=scene_label, path=result_path)
    >>>
    >>>         if os.path.isfile(result_filename):
    >>>             with open(result_filename, 'rt') as f:
    >>>                 for row in csv.reader(f, delimiter='\t'):
    >>>                     results.append(row)
    >>>
    >>>         for file_id, item in enumerate(dataset.test(fold,scene_label=scene_label)):
    >>>             current_file_results = []
    >>>             for result_line in results:
    >>>                 if result_line[0] == dataset.absolute_to_relative(item['file']):
    >>>                     current_file_results.append(
    >>>                         {'file': result_line[0],
    >>>                          'event_onset': float(result_line[1]),
    >>>                          'event_offset': float(result_line[2]),
    >>>                          'event_label': result_line[3]
    >>>                          }
    >>>                     )
    >>>             meta = dataset.file_meta(dataset.absolute_to_relative(item['file']))
    >>>         dcase2016_event_based_metric.evaluate(system_output=current_file_results, annotated_ground_truth=meta)
    >>> overall_metrics_per_scene[scene_label]['event_based_metrics'] = dcase2016_event_based_metric.results()

    """

    def __init__(self, class_list, time_resolution=1.0, t_collar=0.2):
        """__init__ method.

        Parameters
        ----------
        class_list : list
            List of class labels to be evaluated.

        time_resolution : float > 0
            Time resolution used when converting event into event roll.
            (Default value = 1.0)

        t_collar : float > 0
            Time collar for event onset and offset condition
            (Default value = 0.2)

        """

        self.time_resolution = time_resolution
        self.t_collar = t_collar

        self.overall = {
            'Nref': 0.0,
            'Nsys': 0.0,
            'Nsubs': 0.0,
            'Ntp': 0.0,
            'Nfp': 0.0,
            'Nfn': 0.0,
        }
        self.class_wise = {}

        for class_label in class_list:
            self.class_wise[class_label] = {
                'Nref': 0.0,
                'Nsys': 0.0,
                'Ntp': 0.0,
                'Ntn': 0.0,
                'Nfp': 0.0,
                'Nfn': 0.0,
            }

        EventDetectionMetrics.__init__(self, class_list=class_list)

    def __enter__(self):
        # Initialize class and return it
        return self

    def __exit__(self, type, value, traceback):
        # Finalize evaluation and return results
        return self.results()

    def evaluate(self, annotated_ground_truth, system_output):
        """Evaluate system output and annotated ground truth pair.

        Use results method to get results.

        Parameters
        ----------
        annotated_ground_truth : numpy.array
            Ground truth array, list of scene labels

        system_output : numpy.array
            System output array, list of scene labels

        Returns
        -------
        nothing

        """

        # Overall metrics

        # Total number of detected and reference events
        Nsys = len(system_output)
        Nref = len(annotated_ground_truth)

        sys_correct = numpy.zeros(Nsys, dtype=bool)
        ref_correct = numpy.zeros(Nref, dtype=bool)

        # Number of correctly transcribed events, onset/offset within a t_collar range
        for j in range(0, len(annotated_ground_truth)):
            for i in range(0, len(system_output)):
                label_condition = annotated_ground_truth[j]['event_label'] == system_output[i]['event_label']
                onset_condition = self.onset_condition(annotated_event=annotated_ground_truth[j],
                                                       system_event=system_output[i],
                                                       t_collar=self.t_collar)

                offset_condition = self.offset_condition(annotated_event=annotated_ground_truth[j],
                                                         system_event=system_output[i],
                                                         t_collar=self.t_collar)

                if label_condition and onset_condition and offset_condition:
                    ref_correct[j] = True
                    sys_correct[i] = True
                    break

        Ntp = numpy.sum(sys_correct)

        sys_leftover = numpy.nonzero(numpy.negative(sys_correct))[0]
        ref_leftover = numpy.nonzero(numpy.negative(ref_correct))[0]

        # Substitutions
        Nsubs = 0
        for j in ref_leftover:
            for i in sys_leftover:
                onset_condition = self.onset_condition(annotated_event=annotated_ground_truth[j],
                                                       system_event=system_output[i],
                                                       t_collar=self.t_collar)

                offset_condition = self.offset_condition(annotated_event=annotated_ground_truth[j],
                                                         system_event=system_output[i],
                                                         t_collar=self.t_collar)

                if onset_condition and offset_condition:
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
        for class_id, class_label in enumerate(self.class_list):
            Nref = 0.0
            Nsys = 0.0
            Ntp = 0.0

            # Count event frequencies in the ground truth
            for i in range(0, len(annotated_ground_truth)):
                if annotated_ground_truth[i]['event_label'] == class_label:
                    Nref += 1

            # Count event frequencies in the system output
            for i in range(0, len(system_output)):
                if system_output[i]['event_label'] == class_label:
                    Nsys += 1

            for j in range(0, len(annotated_ground_truth)):
                for i in range(0, len(system_output)):
                    if annotated_ground_truth[j]['event_label'] == class_label and system_output[i]['event_label'] == class_label:
                        onset_condition = self.onset_condition(annotated_event=annotated_ground_truth[j],
                                                               system_event=system_output[i],
                                                               t_collar=self.t_collar)

                        offset_condition = self.offset_condition(annotated_event=annotated_ground_truth[j],
                                                                 system_event=system_output[i],
                                                                 t_collar=self.t_collar)

                        if onset_condition and offset_condition:
                            Ntp += 1
                            break

            Nfp = Nsys - Ntp
            Nfn = Nref - Ntp

            self.class_wise[class_label]['Nref'] += Nref
            self.class_wise[class_label]['Nsys'] += Nsys

            self.class_wise[class_label]['Ntp'] += Ntp
            self.class_wise[class_label]['Nfp'] += Nfp
            self.class_wise[class_label]['Nfn'] += Nfn

    def onset_condition(self, annotated_event, system_event, t_collar=0.200):
        """Onset condition, checked does the event pair fulfill condition

        Condition:

        - event onsets are within t_collar each other

        Parameters
        ----------
        annotated_event : dict
            Event dict

        system_event : dict
            Event dict

        t_collar : float > 0
            Defines how close event onsets have to be in order to be considered match. In seconds.
            (Default value = 0.2)

        Returns
        -------
        result : bool
            Condition result

        """

        return math.fabs(annotated_event['event_onset'] - system_event['event_onset']) <= t_collar

    def offset_condition(self, annotated_event, system_event, t_collar=0.200, percentage_of_length=0.5):
        """Offset condition, checking does the event pair fulfill condition

        Condition:

        - event offsets are within t_collar each other
        or
        - system event offset is within the percentage_of_length*annotated event_length

        Parameters
        ----------
        annotated_event : dict
            Event dict

        system_event : dict
            Event dict

        t_collar : float > 0
            Defines how close event onsets have to be in order to be considered match. In seconds.
            (Default value = 0.2)

        percentage_of_length : float [0-1]


        Returns
        -------
        result : bool
            Condition result

        """
        annotated_length = annotated_event['event_offset'] - annotated_event['event_onset']
        return math.fabs(annotated_event['event_offset'] - system_event['event_offset']) <= max(t_collar, percentage_of_length * annotated_length)

    def results(self):
        """Get results

        Outputs results in dict, format:

            {
                'overall':
                    {
                        'Pre':
                        'Rec':
                        'F':
                        'ER':
                        'S':
                        'D':
                        'I':
                    }
                'class_wise':
                    {
                        'office': {
                            'Pre':
                            'Rec':
                            'F':
                            'ER':
                            'D':
                            'I':
                            'Nref':
                            'Nsys':
                            'Ntp':
                            'Nfn':
                            'Nfp':
                        },
                    }
                'class_wise_average':
                    {
                        'F':
                        'ER':
                    }
            }

        Parameters
        ----------
        nothing

        Returns
        -------
        results : dict
            Results dict

        """

        results = {
            'overall': {},
            'class_wise': {},
            'class_wise_average': {},
        }

        # Overall metrics
        results['overall']['Pre'] = self.overall['Ntp'] / (self.overall['Nsys'] + self.eps)
        results['overall']['Rec'] = self.overall['Ntp'] / self.overall['Nref']
        results['overall']['F'] = 2 * ((results['overall']['Pre'] * results['overall']['Rec']) / (results['overall']['Pre'] + results['overall']['Rec'] + self.eps))

        results['overall']['ER'] = (self.overall['Nfn'] + self.overall['Nfp'] + self.overall['Nsubs']) / self.overall['Nref']
        results['overall']['S'] = self.overall['Nsubs'] / self.overall['Nref']
        results['overall']['D'] = self.overall['Nfn'] / self.overall['Nref']
        results['overall']['I'] = self.overall['Nfp'] / self.overall['Nref']

        # Class-wise metrics
        class_wise_F = []
        class_wise_ER = []
        
        for class_label in self.class_list:
            if class_label not in results['class_wise']:
                results['class_wise'][class_label] = {}

            results['class_wise'][class_label]['Pre'] = self.class_wise[class_label]['Ntp'] / (self.class_wise[class_label]['Nsys'] + self.eps)
            results['class_wise'][class_label]['Rec'] = self.class_wise[class_label]['Ntp'] / (self.class_wise[class_label]['Nref'] + self.eps)
            results['class_wise'][class_label]['F'] = 2 * ((results['class_wise'][class_label]['Pre'] * results['class_wise'][class_label]['Rec']) / (results['class_wise'][class_label]['Pre'] + results['class_wise'][class_label]['Rec'] + self.eps))

            results['class_wise'][class_label]['ER'] = (self.class_wise[class_label]['Nfn']+self.class_wise[class_label]['Nfp']) / (self.class_wise[class_label]['Nref'] + self.eps)
            results['class_wise'][class_label]['D'] = self.class_wise[class_label]['Nfn'] / (self.class_wise[class_label]['Nref'] + self.eps)
            results['class_wise'][class_label]['I'] = self.class_wise[class_label]['Nfp'] / (self.class_wise[class_label]['Nref'] + self.eps)

            results['class_wise'][class_label]['Nref'] = self.class_wise[class_label]['Nref']
            results['class_wise'][class_label]['Nsys'] = self.class_wise[class_label]['Nsys']
            results['class_wise'][class_label]['Ntp'] = self.class_wise[class_label]['Ntp']
            results['class_wise'][class_label]['Nfn'] = self.class_wise[class_label]['Nfn']
            results['class_wise'][class_label]['Nfp'] = self.class_wise[class_label]['Nfp']

            class_wise_F.append(results['class_wise'][class_label]['F'])
            class_wise_ER.append(results['class_wise'][class_label]['ER'])

        # Class-wise average
        results['class_wise_average']['F'] = numpy.mean(class_wise_F)
        results['class_wise_average']['ER'] = numpy.mean(class_wise_ER)

        return results


class DCASE2013_EventDetection_Metrics(EventDetectionMetrics):
    """Lecagy DCASE2013 metrics, converted from the provided Matlab implementation

    Supported metrics:
    - Frame based
        - F-score (F)
        - AEER
    - Event based
        - Onset
            - F-Score (F)
            - AEER
        - Onset-offset
            - F-Score (F)
            - AEER
    - Class based
        - Onset
            - F-Score (F)
            - AEER
        - Onset-offset
            - F-Score (F)
            - AEER
    """

    #

    def frame_based(self, annotated_ground_truth, system_output, resolution=0.01):
        # Convert event list into frame-based representation
        system_event_roll = self.list_to_roll(data=system_output, time_resolution=resolution)
        annotated_event_roll = self.list_to_roll(data=annotated_ground_truth, time_resolution=resolution)

        # Fix durations of both event_rolls to be equal
        if annotated_event_roll.shape[0] > system_event_roll.shape[0]:
            padding = numpy.zeros((annotated_event_roll.shape[0] - system_event_roll.shape[0], len(self.class_list)))
            system_event_roll = numpy.vstack((system_event_roll, padding))

        if system_event_roll.shape[0] > annotated_event_roll.shape[0]:
            padding = numpy.zeros((system_event_roll.shape[0] - annotated_event_roll.shape[0], len(self.class_list)))
            annotated_event_roll = numpy.vstack((annotated_event_roll, padding))

        # Compute frame-based metrics
        Nref = sum(sum(annotated_event_roll))
        Ntot = sum(sum(system_event_roll))
        Ntp = sum(sum(system_event_roll + annotated_event_roll > 1))
        Nfp = sum(sum(system_event_roll - annotated_event_roll > 0))
        Nfn = sum(sum(annotated_event_roll - system_event_roll > 0))
        Nsubs = min(Nfp, Nfn)

        eps = numpy.spacing(1)

        results = dict()
        results['Rec'] = Ntp / (Nref + eps)
        results['Pre'] = Ntp / (Ntot + eps)
        results['F'] = 2 * ((results['Pre'] * results['Rec']) / (results['Pre'] + results['Rec'] + eps))
        results['AEER'] = (Nfn + Nfp + Nsubs) / (Nref + eps)

        return results

    def event_based(self, annotated_ground_truth, system_output):
        # Event-based evaluation for event detection task
        # outputFile: the output of the event detection system
        # GTFile: the ground truth list of events

        # Total number of detected and reference events
        Ntot = len(system_output)
        Nref = len(annotated_ground_truth)

        # Number of correctly transcribed events, onset within a +/-100 ms range
        Ncorr = 0
        NcorrOff = 0
        for j in range(0, len(annotated_ground_truth)):
            for i in range(0, len(system_output)):
                if annotated_ground_truth[j]['event_label'] == system_output[i]['event_label'] and (math.fabs(annotated_ground_truth[j]['event_onset'] - system_output[i]['event_onset']) <= 0.1):
                    Ncorr += 1

                    # If offset within a +/-100 ms range or within 50% of ground-truth event's duration
                    if math.fabs(annotated_ground_truth[j]['event_offset'] - system_output[i]['event_offset']) <= max(0.1, 0.5 * (annotated_ground_truth[j]['event_offset'] - annotated_ground_truth[j]['event_onset'])):
                        NcorrOff += 1

                    break  # In order to not evaluate duplicates

        # Compute onset-only event-based metrics
        eps = numpy.spacing(1)
        results = {
            'onset': {},
            'onset-offset': {},
        }

        Nfp = Ntot - Ncorr
        Nfn = Nref - Ncorr
        Nsubs = min(Nfp, Nfn)
        results['onset']['Rec'] = Ncorr / (Nref + eps)
        results['onset']['Pre'] = Ncorr / (Ntot + eps)
        results['onset']['F'] = 2 * (
            (results['onset']['Pre'] * results['onset']['Rec']) / (
                results['onset']['Pre'] + results['onset']['Rec'] + eps))
        results['onset']['AEER'] = (Nfn + Nfp + Nsubs) / (Nref + eps)

        # Compute onset-offset event-based metrics
        NfpOff = Ntot - NcorrOff
        NfnOff = Nref - NcorrOff
        NsubsOff = min(NfpOff, NfnOff)
        results['onset-offset']['Rec'] = NcorrOff / (Nref + eps)
        results['onset-offset']['Pre'] = NcorrOff / (Ntot + eps)
        results['onset-offset']['F'] = 2 * ((results['onset-offset']['Pre'] * results['onset-offset']['Rec']) / (
            results['onset-offset']['Pre'] + results['onset-offset']['Rec'] + eps))
        results['onset-offset']['AEER'] = (NfnOff + NfpOff + NsubsOff) / (Nref + eps)

        return results

    def class_based(self, annotated_ground_truth, system_output):
        # Class-wise event-based evaluation for event detection task
        # outputFile: the output of the event detection system
        # GTFile: the ground truth list of events

        # Total number of detected and reference events per class
        Ntot = numpy.zeros((len(self.class_list), 1))
        for event in system_output:
            pos = self.class_list.index(event['event_label'])
            Ntot[pos] += 1

        Nref = numpy.zeros((len(self.class_list), 1))
        for event in annotated_ground_truth:
            pos = self.class_list.index(event['event_label'])
            Nref[pos] += 1

        I = (Nref > 0).nonzero()[0]  # index for classes present in ground-truth

        # Number of correctly transcribed events per class, onset within a +/-100 ms range
        Ncorr = numpy.zeros((len(self.class_list), 1))
        NcorrOff = numpy.zeros((len(self.class_list), 1))

        for j in range(0, len(annotated_ground_truth)):
            for i in range(0, len(system_output)):
                if annotated_ground_truth[j]['event_label'] == system_output[i]['event_label'] and (
                            math.fabs(
                                    annotated_ground_truth[j]['event_onset'] - system_output[i]['event_onset']) <= 0.1):
                    pos = self.class_list.index(system_output[i]['event_label'])
                    Ncorr[pos] += 1

                    # If offset within a +/-100 ms range or within 50% of ground-truth event's duration
                    if math.fabs(annotated_ground_truth[j]['event_offset'] - system_output[i]['event_offset']) <= max(
                            0.1, 0.5 * (
                                        annotated_ground_truth[j]['event_offset'] - annotated_ground_truth[j][
                                        'event_onset'])):
                        pos = self.class_list.index(system_output[i]['event_label'])
                        NcorrOff[pos] += 1

                    break  # In order to not evaluate duplicates

        # Compute onset-only class-wise event-based metrics
        eps = numpy.spacing(1)
        results = {
            'onset': {},
            'onset-offset': {},
        }

        Nfp = Ntot - Ncorr
        Nfn = Nref - Ncorr
        Nsubs = numpy.minimum(Nfp, Nfn)
        tempRec = Ncorr[I] / (Nref[I] + eps)
        tempPre = Ncorr[I] / (Ntot[I] + eps)
        results['onset']['Rec'] = numpy.mean(tempRec)
        results['onset']['Pre'] = numpy.mean(tempPre)
        tempF = 2 * ((tempPre * tempRec) / (tempPre + tempRec + eps))
        results['onset']['F'] = numpy.mean(tempF)
        tempAEER = (Nfn[I] + Nfp[I] + Nsubs[I]) / (Nref[I] + eps)
        results['onset']['AEER'] = numpy.mean(tempAEER)

        # Compute onset-offset class-wise event-based metrics
        NfpOff = Ntot - NcorrOff
        NfnOff = Nref - NcorrOff
        NsubsOff = numpy.minimum(NfpOff, NfnOff)
        tempRecOff = NcorrOff[I] / (Nref[I] + eps)
        tempPreOff = NcorrOff[I] / (Ntot[I] + eps)
        results['onset-offset']['Rec'] = numpy.mean(tempRecOff)
        results['onset-offset']['Pre'] = numpy.mean(tempPreOff)
        tempFOff = 2 * ((tempPreOff * tempRecOff) / (tempPreOff + tempRecOff + eps))
        results['onset-offset']['F'] = numpy.mean(tempFOff)
        tempAEEROff = (NfnOff[I] + NfpOff[I] + NsubsOff[I]) / (Nref[I] + eps)
        results['onset-offset']['AEER'] = numpy.mean(tempAEEROff)

        return results


def main(argv):
    # Examples to show usage and required data structures
    class_list = ['class1', 'class2', 'class3']
    system_output = [
        {
            'event_label': 'class1',
            'event_onset': 0.1,
            'event_offset': 1.0
        },
        {
            'event_label': 'class2',
            'event_onset': 4.1,
            'event_offset': 4.7
        },
        {
            'event_label': 'class3',
            'event_onset': 5.5,
            'event_offset': 6.7
        }
    ]
    annotated_groundtruth = [
        {
            'event_label': 'class1',
            'event_onset': 0.1,
            'event_offset': 1.0
        },
        {
            'event_label': 'class2',
            'event_onset': 4.2,
            'event_offset': 5.4
        },
        {
            'event_label': 'class3',
            'event_onset': 5.5,
            'event_offset': 6.7
        }
    ]
    dcase2013metric = DCASE2013_EventDetection_Metrics(class_list=class_list)

    print 'DCASE2013'
    print 'Frame-based:', dcase2013metric.frame_based(system_output=system_output,
                                                      annotated_ground_truth=annotated_groundtruth)
    print 'Event-based:', dcase2013metric.event_based(system_output=system_output,
                                                      annotated_ground_truth=annotated_groundtruth)
    print 'Class-based:', dcase2013metric.class_based(system_output=system_output,
                                                      annotated_ground_truth=annotated_groundtruth)

    dcase2016_metric = DCASE2016_EventDetection_SegmentBasedMetrics(class_list=class_list)
    print 'DCASE2016'
    print dcase2016_metric.evaluate(system_output=system_output, annotated_ground_truth=annotated_groundtruth).results()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
