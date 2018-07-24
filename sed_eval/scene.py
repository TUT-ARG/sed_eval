#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Metrics
-------

Main functions:

* :func:`sed_eval.scene.SceneClassificationMetrics.evaluate`: Calculate intermediate values for evaluation and accumulate them.
* :func:`sed_eval.scene.SceneClassificationMetrics.results`: Calculate and return all metrics.
* :func:`sed_eval.scene.SceneClassificationMetrics.results_overall_metrics`: Calculate and return overall metrics (micro-averaged).
* :func:`sed_eval.scene.SceneClassificationMetrics.results_class_wise_metrics`: Calculate and return class-wise metrics.
* :func:`sed_eval.scene.SceneClassificationMetrics.results_class_wise_average_metrics`: Calculate and return class-wise average metrics (macro-averaged).

Function :func:`sed_eval.scene.SceneClassificationMetrics.evaluate` takes as a parameter scene lists,
use :func:`sed_eval.io.load_scene_list` to read them from a file.

Usage example to evaluate files:

.. code-block:: python
    :linenos:
    import sed_eval
    import dcase_util

    file_list = [
        {'reference_file': 'fold1_reference.txt', 'estimated_file': 'fold1_estimated.txt'}
    ]

    data = []

    # Get used scene labels and load data in
    all_data = []
    for file_pair in file_list:
        reference_scene_list = sed_eval.io.load_scene_list(
            filename=file_pair['reference_file'],
            csv_header=False,
            file_format=dcase_util.utils.FileFormat.CSV,
            fields=['filename', 'scene_label']
        )
        estimated_scene_list = sed_eval.io.load_scene_list(
            filename=file_pair['estimated_file'],
            csv_header=False,
            file_format=dcase_util.utils.FileFormat.CSV,
            fields=['filename', 'onset', 'offset', 'scene_label']
        )

        data.append(
            {
                'reference_scene_list': reference_scene_list,
                'estimated_scene_list': estimated_scene_list
            }
        )

        all_data += reference_scene_list

    scene_labels = sed_eval.sound_event.util.unique_scene_labels(all_data)

    # Create metrics class
    scene_metrics = sed_eval.scene.SceneClassificationMetrics(
        scene_labels=scene_labels
    )
    for file_pair in data:
        scene_metrics.evaluate(
            reference_scene_list=file_pair['reference_scene_list'],
            estimated_scene_list=file_pair['estimated_scene_list']
        )

    # Get only certain metrics
    overall_metrics_results = scene_metrics.results_overall_metrics()
    print("Accuracy:", overall_metrics_results['accuracy'])

    # Or print all metrics as reports
    print(scene_metrics)

Usage example to evaluate results stored in variables:

.. code-block:: python
    :linenos:

    import sed_eval
    import dcase_util

    reference = dcase_util.containers.MetaDataContainer([
        {
            'scene_label': 'supermarket',
            'file': 'supermarket09.wav'
        },
        {
            'scene_label': 'tubestation',
            'file': 'tubestation10.wav'
        },
        {
            'scene_label': 'quietstreet',
            'file': 'quietstreet08.wav'
        },
        {
            'scene_label': 'office',
            'file': 'office10.wav'
        },
        {
            'scene_label': 'bus',
            'file': 'bus01.wav'
        },
    ])

    estimated = dcase_util.containers.MetaDataContainer([
        {
            'scene_label': 'supermarket',
            'file': 'supermarket09.wav'
        },
        {
            'scene_label': 'bus',
            'file': 'tubestation10.wav'
        },
        {
            'scene_label': 'quietstreet',
            'file': 'quietstreet08.wav'
        },
        {
            'scene_label': 'park',
            'file': 'office10.wav'
        },
        {
            'scene_label': 'car',
            'file': 'bus01.wav'
        },
    ])

    scene_labels = sed_eval.sound_event.util.unique_scene_labels(reference)

    scene_metrics = sed_eval.scene.SceneClassificationMetrics(scene_labels)
    scene_metrics.evaluate(
        reference_scene_list=reference,
        estimated_scene_list=estimated
    )

    print(scene_metrics)

.. autosummary::
    :toctree: generated/

    SceneClassificationMetrics
    SceneClassificationMetrics.evaluate
    SceneClassificationMetrics.results
    SceneClassificationMetrics.results_overall_metrics
    SceneClassificationMetrics.results_class_wise_metrics
    SceneClassificationMetrics.results_class_wise_average_metrics
    SceneClassificationMetrics.result_report_parameters
    SceneClassificationMetrics.result_report_class_wise
    SceneClassificationMetrics.result_report_class_wise_average
    SceneClassificationMetrics.reset

"""

from __future__ import absolute_import
import numpy
import dcase_util
from . import metric


class SceneClassificationMetrics:
    def __init__(self, scene_labels=None):
        self.accuracies_per_class = None
        self.scene_label_list = scene_labels

        self.overall = {
            'Ncorr': 0.0,
            'Nref': 0.0,
            'Nsys': 0.0
        }

        self.scene_wise = {}
        for label in self.scene_label_list:
            self.scene_wise[label] = {
                'Ncorr': 0.0,
                'Nref': 0.0,
                'Nsys': 0.0
            }

        self.ui = dcase_util.ui.FancyStringifier()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self.results()

    def __str__(self):
        """Print result reports"""

        output = self.ui.section_header('Scene classification metrics') + '\n'
        output += self.result_report_parameters() + '\n'
        output += self.result_report_class_wise_average() + '\n'
        output += self.result_report_class_wise() + '\n'

        return output

    def evaluate(self, reference_scene_list, estimated_scene_list=None, estimated_scene_probabilities=None):
        """Evaluate file pair (reference and estimated)

        Parameters
        ----------

        reference_scene_list : list of dict or dcase_util.containers.MetaDataContainer
            Reference scene list.
            Default value None

        estimated_scene_list : list of dict or dcase_util.containers.MetaDataContainer
            Estimated scene list.
            Default value None

        estimated_scene_probabilities : dcase_util.containers.ProbabilityContainer
            Estimated scene probabilities. Currently not used.
            Default value None

        Returns
        -------
        self

        """

        if estimated_scene_list is None and estimated_scene_probabilities is None:
            raise ValueError("Nothing to evaluate, give at least estimated_scene_list or estimated_scene_probabilities")

        # Make sure reference_scene_list is dcase_util.containers.MetaDataContainer
        if not isinstance(estimated_scene_list, dcase_util.containers.MetaDataContainer):
            reference_scene_list = dcase_util.containers.MetaDataContainer(reference_scene_list)

        # Make sure estimated_scene_list is dcase_util.containers.MetaDataContainer
        if not isinstance(estimated_scene_list, dcase_util.containers.MetaDataContainer):
            estimated_scene_list = dcase_util.containers.MetaDataContainer(estimated_scene_list)

        # Make sure estimated_tag_probabilities is dcase_util.containers.ProbabilityContainer
        if estimated_scene_probabilities is not None:
            if not isinstance(estimated_scene_probabilities, dcase_util.containers.ProbabilityContainer):
                estimated_scene_probabilities = dcase_util.containers.ProbabilityContainer(estimated_scene_probabilities)

        # Translate "file" field to "filename"
        for item in reference_scene_list:
            if 'filename' not in item and 'file' in item:
                item['filename'] = item['file']

        for item in estimated_scene_list:
            if 'filename' not in item and 'file' in item:
                item['filename'] = item['file']

        y_true = []
        y_pred = []

        for estimated_item in estimated_scene_list:
            reference_item_matched = {}
            for reference_item in reference_scene_list:
                if estimated_item['filename'] == reference_item['filename']:
                    reference_item_matched = reference_item
                    break

            if not reference_item_matched:
                raise ValueError(
                    "Cannot find reference_item for estimated item [{item}]".format(item=estimated_item['file'])
                )

            y_true.append(reference_item_matched['scene_label'])
            y_pred.append(estimated_item['scene_label'])

        y_true = numpy.array(y_true)
        y_pred = numpy.array(y_pred)

        Ncorr_overall = 0
        for scene_id, scene_label in enumerate(self.scene_label_list):
            true_id = numpy.where(y_true == scene_label)[0]
            pred_id = numpy.where(y_pred == scene_label)[0]

            Ncorr = 0
            for id in true_id:
                if id in pred_id:
                    Ncorr += 1

            Ncorr_overall += Ncorr
            self.scene_wise[scene_label]['Ncorr'] += Ncorr
            self.scene_wise[scene_label]['Nref'] += true_id.shape[0]
            self.scene_wise[scene_label]['Nsys'] += pred_id.shape[0]

        self.overall['Ncorr'] += Ncorr_overall
        self.overall['Nref'] += y_true.shape[0]
        self.overall['Nsys'] += y_pred.shape[0]

        return self

    def reset(self):
        """Reset internal state
        """
        self.overall = {
            'Ncorr': 0.0,
            'Nref': 0.0,
            'Nsys': 0.0
        }

        self.scene_wise = {}
        for label in self.scene_label_list:
            self.scene_wise[label] = {
                'Ncorr': 0.0,
                'Nref': 0.0,
                'Nsys': 0.0
            }

    # Reports
    def result_report_parameters(self):
        """Report metric parameters

        Returns
        -------
        str
            result report in string format

        """

        output = self.ui.data(field='Scene labels', value=len(self.scene_label_list)) + '\n'
        output += self.ui.data(field='Evaluated units', value=int(self.overall['Nref'])) + '\n'

        return output

    def result_report_class_wise(self):
        """Report class-wise results

        Returns
        -------
        str
            result report in string format

        """

        results = self.results_class_wise_metrics()

        output = self.ui.section_header('Class-wise metrics', indent=2) + '\n'

        output += self.ui.row(
            'Scene label', 'Ncorr', 'Nref', 'Accuracy',
            widths=[20, 12, 12, 12],
            separators=[True, False, True, False],
            indent=4
        ) + '\n'

        output += self.ui.row('-', '-', '-', '-') + '\n'

        for scene_label in self.scene_label_list:
            output += self.ui.row(
                scene_label,
                results[scene_label]['count']['Ncorr'],
                results[scene_label]['count']['Nref'],
                results[scene_label]['accuracy']['accuracy'] * 100,
                types=['str', 'int', 'int', 'float1_percentage']
            ) + '\n'

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

        output += self.ui.line('Accuracy', indent=2) + '\n'
        output += self.ui.data(field='Accuracy',
                               value=float(results['accuracy']['accuracy']) * 100, unit='%', indent=4) + '\n'

        return output

    # Results
    def results(self):
        """All metrics

        Returns
        -------
        dict
            results in a dictionary format

        """

        results = {
            'overall': self.results_overall_metrics(),
            'class_wise': self.results_class_wise_metrics(),
            'class_wise_average': self.results_class_wise_average_metrics()
        }

        return results

    def results_overall_metrics(self):
        """Overall metrics

        Returns
        -------
        dict
            results in a dictionary format

        """

        if self.overall['Nsys'] != 0:
            accuracy = self.overall['Ncorr'] / float(self.overall['Nsys'])
        else:
            accuracy = None

        return {
            'count': self.overall,
            'accuracy': accuracy
        }

    def results_class_wise_metrics(self):
        """Class-wise metrics

        Returns
        -------
        dict
            results in a dictionary format

        """

        results = {}
        for scene_id, scene_label in enumerate(self.scene_label_list):
            if scene_label not in results:
                results[scene_label] = {}

            results[scene_label]['count'] = {}
            results[scene_label]['count']['Ncorr'] = self.scene_wise[scene_label]['Ncorr']
            results[scene_label]['count']['Nref'] = self.scene_wise[scene_label]['Nref']
            results[scene_label]['count']['Nsys'] = self.scene_wise[scene_label]['Nsys']
            results[scene_label]['accuracy'] = {
                'accuracy': metric.accuracy_corr(
                    Ncorr=self.scene_wise[scene_label]['Ncorr'],
                    N=self.scene_wise[scene_label]['Nref']
                )
            }

        return results

    def results_class_wise_average_metrics(self):
        """Class-wise averaged metrics

        Returns
        -------
        dict
            results in a dictionary format

        """

        scene_wise_results = self.results_class_wise_metrics()

        scene_wise_accuracy = []
        for scene_label in scene_wise_results:
            scene_wise_accuracy.append(scene_wise_results[scene_label]['accuracy']['accuracy'])

        return {
            'accuracy': {
                'accuracy': float(numpy.mean(scene_wise_accuracy))
            }
        }

    # Metrics
    def class_wise_accuracy(self, scene_label):
        """Class-wise accuracy

        Returns
        -------
        dict
            results in a dictionary format

        """

        if len(self.accuracies_per_class.shape) == 2:
            return {
                'accuracy': float(numpy.mean(self.accuracies_per_class[:, self.scene_label_list.index(scene_label)]))
            }

        else:
            return {
                'accuracy': float(numpy.mean(self.accuracies_per_class[self.scene_label_list.index(scene_label)]))
            }
