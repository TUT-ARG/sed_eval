#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Metrics
-------

Main functions:

* :func:`sed_eval.audio_tag.AudioTaggingMetrics.evaluate`: Calculate intermediate values for evaluation and accumulate them.
* :func:`sed_eval.audio_tag.AudioTaggingMetrics.results`: Calculate and return all metrics.
* :func:`sed_eval.audio_tag.AudioTaggingMetrics.results_overall_metrics`: Calculate and return overall metrics (micro-averaged).
* :func:`sed_eval.audio_tag.AudioTaggingMetrics.results_class_wise_metrics`: Calculate and return class-wise metrics.
* :func:`sed_eval.audio_tag.AudioTaggingMetrics.results_class_wise_average_metrics`: Calculate and return class-wise average metrics (macro-averaged).

Function :func:`sed_eval.audio_tag.AudioTaggingMetrics.evaluate` takes as a parameter tag lists,
(use :func:`dcase_util.containers.MetaDataContainer` to read them from a file), and probability lists (use :func:`dcase_util.containers.ProbabilityContainer` to read them from a file).

Usage example:

.. code-block:: python
    :linenos:

    import sed_eval
    import dcase_util

    reference_tag_list = dcase_util.containers.MetaDataContainer([
        {
            'filename': 'test1.wav',
            'tags': 'cat,dog'
        },
        {
            'filename': 'test2.wav',
            'tags': 'dog'
        },
        {
            'filename': 'test3.wav',
            'tags': 'bird,cat'
        },
        {
            'filename': 'test4.wav',
            'tags': 'cat'
        },
        {
            'filename': 'test5.wav',
            'tags': 'bird,speech'
        },
        {
            'filename': 'test6.wav',
            'tags': 'dog,speech'
        },
        {
            'filename': 'test7.wav',
            'tags': 'speech'
        },
    ])

    estimated_tag_probabilities = dcase_util.containers.ProbabilityContainer([
        {
            'filename': 'test1.wav',
            'label': 'bird',
            'probability': 0.2
        },
        {
            'filename': 'test1.wav',
            'label': 'cat',
            'probability': 0.99
        },
        {
            'filename': 'test1.wav',
            'label': 'dog',
            'probability': 0.88
        },
        {
            'filename': 'test1.wav',
            'label': 'speech',
            'probability': 0.01
        },

        {
            'filename': 'test2.wav',
            'label': 'bird',
            'probability': 0.1
        },
        {
            'filename': 'test2.wav',
            'label': 'cat',
            'probability': 0.3
        },
        {
            'filename': 'test2.wav',
            'label': 'dog',
            'probability': 0.8
        },
        {
            'filename': 'test2.wav',
            'label': 'speech',
            'probability': 0.1
        },


        {
            'filename': 'test3.wav',
            'label': 'bird',
            'probability': 0.7
        },
        {
            'filename': 'test3.wav',
            'label': 'cat',
            'probability': 0.6
        },
        {
            'filename': 'test3.wav',
            'label': 'dog',
            'probability': 0.4
        },
        {
            'filename': 'test3.wav',
            'label': 'speech',
            'probability': 0.3
        },

        {
            'filename': 'test4.wav',
            'label': 'bird',
            'probability': 0.323
        },
        {
            'filename': 'test4.wav',
            'label': 'cat',
            'probability': 0.6
        },
        {
            'filename': 'test4.wav',
            'label': 'dog',
            'probability': 0.56
        },
        {
            'filename': 'test4.wav',
            'label': 'speech',
            'probability': 0.4
        },


        {
            'filename': 'test5.wav',
            'label': 'bird',
            'probability': 0.8
        },
        {
            'filename': 'test5.wav',
            'label': 'cat',
            'probability': 0.7
        },
        {
            'filename': 'test5.wav',
            'label': 'dog',
            'probability': 0.45
        },
        {
            'filename': 'test5.wav',
            'label': 'speech',
            'probability': 0.43
        },


        {
            'filename': 'test6.wav',
            'label': 'bird',
            'probability': 0.9
        },
        {
            'filename': 'test6.wav',
            'label': 'cat',
            'probability': 0.53
        },
        {
            'filename': 'test6.wav',
            'label': 'dog',
            'probability': 0.83
        },
        {
            'filename': 'test6.wav',
            'label': 'speech',
            'probability': 0.95
        },


        {
            'filename': 'test7.wav',
            'label': 'bird',
            'probability': 0.2
        },
        {
            'filename': 'test7.wav',
            'label': 'cat',
            'probability': 0.2
        },
        {
            'filename': 'test7.wav',
            'label': 'dog',
            'probability': 0.89
        },
        {
            'filename': 'test7.wav',
            'label': 'speech',
            'probability': 0.45
        },
    ])

    estimated_tag_list = dcase_util.containers.MetaDataContainer()
    for file in estimated_tag_probabilities.unique_files:
        k = estimated_tag_probabilities.filter(filename=file)
        tags = []
        for item in k:
            if item.probability > 0.5:
                tags.append(item.label)

        estimated_tag_list.append(
            {
                'filename': file,
                'tags': tags
            }
        )

    tag_evaluator = sed_eval.audio_tag.AudioTaggingMetrics(
        tags=reference_tag_list.unique_tags
    )

    tag_evaluator.evaluate(
        reference_tag_list=reference_tag_list,
        estimated_tag_list=estimated_tag_list,
        estimated_tag_probabilities=estimated_tag_probabilities
    )
    print(tag_evaluator)


.. autosummary::
    :toctree: generated/

    AudioTaggingMetrics
    AudioTaggingMetrics.evaluate
    AudioTaggingMetrics.results
    AudioTaggingMetrics.results_overall_metrics
    AudioTaggingMetrics.results_class_wise_metrics
    AudioTaggingMetrics.results_class_wise_average_metrics
    AudioTaggingMetrics.result_report_parameters
    AudioTaggingMetrics.result_report_class_wise
    AudioTaggingMetrics.result_report_class_wise_average
    AudioTaggingMetrics.reset

"""

from __future__ import absolute_import
import numpy
from . import metric
import dcase_util


class AudioTaggingMetrics:
    def __init__(self, tags=None):
        self.tag_label_list = tags

        self.overall = {
            'Ncorr': 0.0,
            'Nref': 0.0,
            'Nsys': 0.0,
            'Ntp': 0.0,
            'Ntn': 0.0,
            'Nfp': 0.0,
            'Nfn': 0.0,
        }

        self.tag_wise = {}
        self.y_true = {}
        self.y_pred = {}
        self.y_pred_score = {}

        for label in self.tag_label_list:
            self.tag_wise[label] = {
                'Nref': 0.0,
                'Nsys': 0.0,
                'Ntp': 0.0,
                'Ntn': 0.0,
                'Nfp': 0.0,
                'Nfn': 0.0,
            }
            self.y_true[label] = []
            self.y_pred[label] = []
            self.y_pred_score[label] = []

        self.ui = dcase_util.ui.FancyStringifier()

    def __str__(self):
        """Print result reports"""

        output = self.ui.section_header('Audio tagging metrics') + '\n'
        output += self.result_report_parameters() + '\n'
        output += self.result_report_overall() + '\n'
        output += self.result_report_class_wise_average() + '\n'
        output += self.result_report_class_wise() + '\n'

        return output

    def evaluate(self, reference_tag_list, estimated_tag_list=None, estimated_tag_probabilities=None):
        """Evaluate estimated against reference

        Parameters
        ----------

        reference_tag_list : list of dict or dcase_util.containers.MetaDataContainer
            Reference tag list

        estimated_tag_list : list of dict or dcase_util.containers.MetaDataContainer
            Estimated tag list

        estimated_tag_probabilities : list of dict or dcase_util.containers.ProbabilityContainer
            Estimated tag probabilities

        Returns
        -------
        self

        """

        if estimated_tag_list is None and estimated_tag_probabilities is None:
            raise ValueError("Nothing to evaluate, give at least estimated_tag_list or estimated_tag_probabilities")

        # Make sure reference_tag_list is dcase_util.containers.MetaDataContainer
        if not isinstance(reference_tag_list, dcase_util.containers.MetaDataContainer):
            reference_tag_list = dcase_util.containers.MetaDataContainer(reference_tag_list)

        # Make sure estimated_tag_list is dcase_util.containers.MetaDataContainer
        if estimated_tag_list is not None:
            if not isinstance(estimated_tag_list, dcase_util.containers.MetaDataContainer):
                estimated_tag_list = dcase_util.containers.MetaDataContainer(estimated_tag_list)

        # Make sure estimated_tag_probabilities is dcase_util.containers.ProbabilityContainer
        if estimated_tag_probabilities is not None:
            if not isinstance(estimated_tag_probabilities, dcase_util.containers.ProbabilityContainer):
                estimated_tag_probabilities = dcase_util.containers.ProbabilityContainer(estimated_tag_probabilities)

        y_true = []
        y_pred = []

        # Go though reference and estimated list label by label, and file by file
        for label in self.tag_label_list:
            for filename in reference_tag_list.unique_files:
                reference_item = reference_tag_list.filter(filename=filename)[0]

                # Populate y_true based on reference_item
                if label in reference_item.tags:
                    self.y_true[label].append(1)
                    y_true.append(1)

                else:
                    self.y_true[label].append(0)
                    y_true.append(0)

                if estimated_tag_list is not None:
                    # Evaluate based on estimated tags

                    estimated_item = estimated_tag_list.filter(filename=filename)[0]

                    if not estimated_item:
                        raise ValueError(
                            "Not all reference files estimated, please check [{file}]".format(
                                file=filename
                            )
                        )
                    # Store nref
                    if label in reference_item.tags:
                        self.tag_wise[label]['Nref'] += 1

                    # Populate y_pred based estimated_item
                    if label in estimated_item.tags:
                        self.y_pred[label].append(1)
                        y_pred.append(1)
                        self.tag_wise[label]['Nsys'] += 1

                    else:
                        self.y_pred[label].append(0)
                        y_pred.append(0)

                    # Accumulate intermediate values
                    # True positives (TP)
                    if label in reference_item.tags and label in estimated_item.tags:
                        self.tag_wise[label]['Ntp'] += 1

                    # True negatives (TN)
                    if label not in reference_item.tags and label not in estimated_item.tags:
                        self.tag_wise[label]['Ntn'] += 1

                    # False positives (FP)
                    if label not in reference_item.tags and label in estimated_item.tags:
                        self.tag_wise[label]['Nfp'] += 1

                    # False negatives (FN)
                    if label in reference_item.tags and label not in estimated_item.tags:
                        self.tag_wise[label]['Nfn'] += 1

                if estimated_tag_probabilities is not None:
                    # Evaluate based on per tag probabilities

                    estimated_item = estimated_tag_probabilities.filter(filename=filename, label=label)[0]
                    self.y_pred_score[label].append(float(estimated_item['probability']))

        if estimated_tag_list is not None:
            # Evaluate based on estimated tags

            self.overall['Nref'] += sum(y_true)
            self.overall['Nsys'] += sum(y_pred)

            y_true = numpy.array(y_true)
            y_pred = numpy.array(y_pred)

            self.overall['Ntp'] += sum(y_pred + y_true > 1)
            self.overall['Ntn'] += sum(y_pred + y_true == 0)
            self.overall['Nfp'] += sum(y_pred - y_true > 0)
            self.overall['Nfn'] += sum(y_true - y_pred > 0)

        return self

    def reset(self):
        """Reset internal state
        """
        self.overall = {
            'Nref': 0.0,
            'Nsys': 0.0,
            'Ntp': 0.0,
            'Ntn': 0.0,
            'Nfp': 0.0,
            'Nfn': 0.0,
        }

        self.tag_wise = {}
        for label in self.tag_label_list:
            self.tag_wise[label] = {
                'Nref': 0.0,
                'Nsys': 0.0,
                'Ntp': 0.0,
                'Ntn': 0.0,
                'Nfp': 0.0,
                'Nfn': 0.0,
            }

        return self

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
            'class_wise_average': self.results_class_wise_average_metrics(),
        }

        return results

    def results_overall_metrics(self):
        """Overall metrics

        Returns
        -------
        dict
            results in a dictionary format

        """

        # F-measure
        if self.overall['Nref'] > 0:
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

        else:
            precision = None
            recall = None
            f_measure = None

        y_true = []
        y_score = []
        for tag_id, tag_label in enumerate(self.tag_label_list):
            y_true += self.y_true[tag_label]
            y_score += self.y_pred_score[tag_label]

        if y_score:
            eer = metric.equal_error_rate(
                y_true=y_true,
                y_score=y_score
            )

        else:
            eer = None

        return {
                'count': {
                    'Nref': self.overall['Nref'],
                    'Nsys': self.overall['Nsys'],
                },
                'f_measure': {
                    'f_measure': f_measure,
                    'precision': precision,
                    'recall': recall,
                },
                'eer': {
                    'eer': eer
                }

        }

    def results_class_wise_metrics(self):
        """Class-wise metrics

        Returns
        -------
        dict
            results in a dictionary format

        """

        results = {}
        for tag_id, tag_label in enumerate(self.tag_label_list):
            if tag_label not in results:
                results[tag_label] = {}

            # Counts
            results[tag_label]['count'] = {
                'Nref': self.tag_wise[tag_label]['Nref'],
                'Nsys': self.tag_wise[tag_label]['Nsys'],
                'Ntp': self.tag_wise[tag_label]['Ntp'],
                'Ntn': self.tag_wise[tag_label]['Ntn'],
                'Nfp': self.tag_wise[tag_label]['Nfp'],
                'Nfn': self.tag_wise[tag_label]['Nfn'],
            }

            # Equal error rate
            if self.y_pred_score[tag_label]:
                results[tag_label]['eer'] = {
                    'eer': metric.equal_error_rate(
                        y_true=self.y_true[tag_label],
                        y_score=self.y_pred_score[tag_label]
                    )
                }

            else:
                results[tag_label]['eer'] = {
                    'eer': None
                }

            # F-measure
            if self.tag_wise[tag_label]['Nref'] > 0:

                precision = metric.precision(
                    Ntp=self.tag_wise[tag_label]['Ntp'],
                    Nsys=self.tag_wise[tag_label]['Nsys']
                )

                recall = metric.recall(
                    Ntp=self.tag_wise[tag_label]['Ntp'],
                    Nref=self.tag_wise[tag_label]['Nref']
                )

                f_measure = metric.f_measure(precision=precision, recall=recall)

            else:
                precision = None
                recall = None
                f_measure = None

            results[tag_label]['f_measure'] = {
                'f_measure': f_measure,
                'precision': precision,
                'recall': recall,
            }

        return results

    def results_class_wise_average_metrics(self):
        """Class-wise averaged metrics

        Returns
        -------
        dict
            results in a dictionary format

        """

        class_wise_results = self.results_class_wise_metrics()

        class_wise_eer = []
        class_wise_fmeasure = []
        class_wise_precision = []
        class_wise_recall = []

        for class_label in class_wise_results:
            if class_wise_results[class_label]['eer']['eer'] is not None:
                class_wise_eer.append(class_wise_results[class_label]['eer']['eer'])

            if class_wise_results[class_label]['f_measure']['f_measure'] is not None:
                class_wise_fmeasure.append(class_wise_results[class_label]['f_measure']['f_measure'])
                class_wise_precision.append(class_wise_results[class_label]['f_measure']['precision'])
                class_wise_recall.append(class_wise_results[class_label]['f_measure']['recall'])

        if class_wise_eer:
            eer = float(numpy.nanmean(class_wise_eer))

        else:
            eer = None

        if class_wise_fmeasure:
            f_measure = float(numpy.nanmean(class_wise_fmeasure))

        else:
            f_measure = None

        if class_wise_precision:
            precision = float(numpy.nanmean(class_wise_precision))

        else:
            precision = None

        if class_wise_recall:
            recall = float(numpy.nanmean(class_wise_recall))

        else:
            recall = None

        return {
            'eer': {
                'eer': eer
            },
            'f_measure': {
                'f_measure': f_measure,
                'precision': precision,
                'recall': recall,
            }
        }

    # Reports
    def result_report_parameters(self):
        """Report metric parameters

        Returns
        -------
        str
            result report in string format

        """

        output = self.ui.data(field='Tags', value=len(self.tag_label_list)) + '\n'
        output += self.ui.data(field='Evaluated units', value=int(self.overall['Nref'])) + '\n'

        return output

    def result_report_overall(self):
        """Report overall results

        Returns
        -------
        str
            result report in string format

        """

        results = self.results_overall_metrics()

        output = self.ui.section_header('Overall metrics (micro-average)', indent=2) + '\n'

        if 'f_measure' in results and results['f_measure']:

            if results['f_measure']['f_measure'] is not None:
                f_measure = results['f_measure']['f_measure'] * 100

            else:
                f_measure = None

            if results['f_measure']['precision'] is not None:
                precision = results['f_measure']['precision'] * 100

            else:
                precision = None

            if results['f_measure']['recall'] is not None:
                recall = results['f_measure']['recall'] * 100

            else:
                recall = None

            output += self.ui.line('F-measure', indent=2) + '\n'
            output += self.ui.data(field='F-measure (F1)', value=f_measure, unit='%', indent=4) + '\n'
            output += self.ui.data(field='Precision', value=precision, unit='%', indent=4) + '\n'
            output += self.ui.data(field='Recall', value=recall, unit='%', indent=4) + '\n'

        if 'eer' in results and results['eer']:
            if results['eer']['eer'] is not None:
                eer = results['eer']['eer'] * 100

            else:
                eer = None

            output += self.ui.line('Equal error rate', indent=2) + '\n'
            output += self.ui.data(field='Equal error rate (EER)', value=eer, unit='%', indent=4) + '\n'

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

        if 'f_measure' in results and results['f_measure']:
            if results['f_measure']['f_measure'] is not None:
                f_measure = results['f_measure']['f_measure'] * 100

            else:
                f_measure = None

            if results['f_measure']['precision'] is not None:
                precision = results['f_measure']['precision'] * 100

            else:
                precision = None

            if results['f_measure']['recall'] is not None:
                recall = results['f_measure']['recall'] * 100

            else:
                recall = None

            output += self.ui.line('F-measure', indent=2) + '\n'
            output += self.ui.data(field='F-measure (F1)', value=f_measure, unit='%', indent=4) + '\n'
            output += self.ui.data(field='Precision', value=precision, unit='%', indent=4) + '\n'
            output += self.ui.data(field='Recall', value=recall, unit='%', indent=4) + '\n'

        if 'eer' in results and results['eer']:
            if results['eer']['eer'] is not None:
                eer = results['eer']['eer'] * 100

            else:
                eer = None

            output += self.ui.line('Equal error rate', indent=2) + '\n'
            output += self.ui.data(field='Equal error rate (EER)', value=eer, unit='%', indent=4) + '\n'

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
            'Tag', 'Nref', 'Nsys', 'F-score', 'Pre', 'Rec', 'EER',
            widths=[20, 12, 12, 12, 12, 12, 12],
            separators=[True, False, True, False, False, True, False],
            indent=4
        ) + '\n'
        output += self.ui.row('-', '-', '-', '-', '-', '-', '-') + '\n'

        for tag_label in self.tag_label_list:
            if results[tag_label]['f_measure']['f_measure'] is not None:
                f_measure = results[tag_label]['f_measure']['f_measure'] * 100

            else:
                f_measure = None

            if results[tag_label]['f_measure']['precision'] is not None:
                precision = results[tag_label]['f_measure']['precision'] * 100

            else:
                precision = None

            if results[tag_label]['f_measure']['recall'] is not None:
                recall = results[tag_label]['f_measure']['recall'] * 100

            else:
                recall = None

            if results[tag_label]['eer']['eer'] is not None:
                eer = results[tag_label]['eer']['eer'] * 100

            else:
                eer = None

            output += self.ui.row(
                tag_label,
                results[tag_label]['count']['Nref'],
                results[tag_label]['count']['Nsys'],
                f_measure,
                precision,
                recall,
                eer,
                types=['str', 'int', 'int', 'float1_percentage', 'float1', 'float1', 'float1_percentage']
            ) + '\n'

        return output
