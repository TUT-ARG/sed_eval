#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Metrics
-------

Segment-based metrics, main functions:

* :func:`sed_eval.scene.SceneClassificationMetrics.evaluate`: Calculate intermediate values for evaluation and accumulate them.
* :func:`sed_eval.scene.SceneClassificationMetrics.results`: Calculate and return all metrics.
* :func:`sed_eval.scene.SceneClassificationMetrics.results_overall_metrics`: Calculate and return overall metrics (micro-averaged).
* :func:`sed_eval.scene.SceneClassificationMetrics.results_class_wise_metrics`: Calculate and return class-wise metrics.
* :func:`sed_eval.scene.SceneClassificationMetrics.results_class_wise_average_metrics`: Calculate and return class-wise average metrics (macro-averaged).

Function :func:`sed_eval.scene.SceneClassificationMetrics.evaluate` takes as a parameter scene lists, use :func:`sed_eval.io.load_scene_list` to read them from a file.

Usage example:

.. code-block:: python
    :linenos:

    import sed_eval

    file_list = [
        {'reference_file': 'fold1_reference.txt', 'estimated_file': 'fold1_estimated.txt'},
        {'reference_file': 'fold2_reference.txt', 'estimated_file': 'fold2_estimated.txt'},
        {'reference_file': 'fold3_reference.txt', 'estimated_file': 'fold3_estimated.txt'},
        {'reference_file': 'fold4_reference.txt', 'estimated_file': 'fold4_estimated.txt'},
        {'reference_file': 'fold5_reference.txt', 'estimated_file': 'fold5_estimated.txt'},
    ]

    data = []

    # Get used scene labels
    all_data = []
    for file_pair in file_list:
        reference_scene_list = sed_eval.io.load_scene_list(file_pair['reference_file'])
        estimated_scene_list = sed_eval.io.load_scene_list(file_pair['estimated_file'])
        data.append({'reference_scene_list': reference_scene_list,
                     'estimated_scene_list': estimated_scene_list})
        all_data += reference_scene_list

    scene_labels = sed_eval.sound_event.util.unique_scene_labels(all_data)

    # Create metrics class
    scene_metrics = sed_eval.scene.SceneClassificationMetrics(scene_labels)
    for file_pair in data:
        scene_metrics.evaluate(file_pair['reference_scene_list'],
                               file_pair['estimated_scene_list'])

    # Get only certain metrics
    overall_metrics_results = scene_metrics.results_overall_metrics()
    print "Accuracy:", overall_metrics_results['accuracy']

    # Or print all metrics as reports
    print scene_metrics

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
from . import metric


class SceneClassificationMetrics:
    def __init__(self, scene_labels=None):
        self.accuracies_per_class = None
        self.scene_label_list = scene_labels

        self.overall = {
            'Ncorr': 0.0,
            'Nref': 0.0,
            'Nsys': 0.0,
        }

        self.scene_wise = {}
        for label in self.scene_label_list:
            self.scene_wise[label] = {
                'Ncorr': 0.0,
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
        report: str
            result report in string format
        """
        output = "\nScene classification metrics \n"
        output += "----------------------------------------------------------------------\n"
        output += self.result_report_parameters()
        output += self.result_report_class_wise_average()
        output += self.result_report_class_wise()
        return output

    def evaluate(self, reference_scene_list, estimated_scene_list):
        """Evaluate file pair (reference and estimated)

        Parameters
        ----------

        reference_scene_list : scene list
            Reference scene list

        estimated_scene_list : scene list
            Estimated scene list

        Returns
        -------
            Nothing

        """

        y_true = []
        y_pred = []
        for estimated_item in estimated_scene_list:
            reference_item_matched = {}
            for reference_item in reference_scene_list:
                if estimated_item['file'] == reference_item['file']:
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

    def reset(self):
        """Reset internal state
        """
        self.overall = {
            'Ncorr': 0.0,
            'Nref': 0.0,
            'Nsys': 0.0,
        }

        self.scene_wise = {}
        for label in self.scene_label_list:
            self.scene_wise[label] = {
                'Ncorr': 0.0,
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
        report: str
            result report in string format
        """

        output = "    {:17s} : {:5.0f}\n".format('Scene labels', len(self.scene_label_list))
        output += "    {:17s} : {:5.0f}\n".format('Evaluated units', self.overall['Nref'])
        output += "  \n"
        return output

    def result_report_class_wise(self):
        """Report class-wise results

        Parameters
        ----------
            Nothing

        Returns
        -------
        report: str
            result report in string format
        """

        results = self.results_class_wise_metrics()
        output = "  Class-wise metrics\n"
        output += "  ===============\n"
        output += "    {:17s} | {:^4s} | {:^4s} | {:^8s} |\n".format('Scene label', 'Ncorr', 'Nref', 'Accuracy')

        output += "    ------------------+-------+------+----------+\n"
        for scene_label in self.scene_label_list:
            output += "    {:17s} |  {:4.0f} | {:4.0f} | {:5.1f} %  | \n".format(scene_label,
                                                                                results[scene_label]['count']['Ncorr'],
                                                                                results[scene_label]['count']['Nref'],
                                                                                results[scene_label]['accuracy']['accuracy']*100)
        output += "  \n"
        return output

    def result_report_class_wise_average(self):
        """Report class-wise averages

        Parameters
        ----------
            Nothing

        Returns
        -------
        report: str
            result report in string format
        """

        results = self.results_class_wise_average_metrics()
        output = "  Class-wise average metrics (macro-average)\n"
        output += "  ===============\n"

        output += "  Accuracy\n"
        output += "    {:17s} : {:5.1f} %\n".format('Accuracy', results['accuracy']['accuracy']*100)

        output += "  \n"
        return output

    # Results
    def results(self):
        """All metrics

        Parameters
        ----------
        Nothing

        Returns
        -------
        results: dict
            results in a dictionary format
        """
        results = {
            'overall': self.results_overall_metrics(),
            'class_wise': self.results_class_wise_metrics(),
            'class_wise_average': self.results_class_wise_average_metrics(),
        }

        return results

    def results_overall_metrics(self):
        """Overall metrics

        Parameters
        ----------
        Nothing

        Returns
        -------
        results: dict
            results in a dictionary format
        """

        return {
                'count': self.overall,
                'accuracy': self.overall['Ncorr']/self.overall['Nsys'],
               }

    def results_class_wise_metrics(self):
        """Class-wise metrics

        Parameters
        ----------
        Nothing

        Returns
        -------
        results: dict
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
            results[scene_label]['accuracy'] = {}
            results[scene_label]['accuracy']['accuracy'] = metric.accuracy_corr(Ncorr=self.scene_wise[scene_label]['Ncorr'],
                                                                                N=self.scene_wise[scene_label]['Nref'])
        return results

    def results_class_wise_average_metrics(self):
        """Class-wise averaged metrics

        Parameters
        ----------
        Nothing

        Returns
        -------
        results: dict
            results in a dictionary format
        """

        scene_wise_results = self.results_class_wise_metrics()

        scene_wise_accuracy = []
        for scene_label in scene_wise_results:
            scene_wise_accuracy.append(scene_wise_results[scene_label]['accuracy']['accuracy'])

        return {'accuracy': {
                    'accuracy': float(numpy.mean(scene_wise_accuracy))
               }}

    # Metrics
    def class_wise_accuracy(self, scene_label):
        """Class-wise accuracy

        Parameters
        ----------
        Nothing

        Returns
        -------
        results: dict
            results in a dictionary format
        """

        if len(self.accuracies_per_class.shape) == 2:
            return {'accuracy': float(numpy.mean(self.accuracies_per_class[:, self.scene_label_list.index(scene_label)]))}
        else:
            return {'accuracy': float(numpy.mean(self.accuracies_per_class[self.scene_label_list.index(scene_label)]))}
