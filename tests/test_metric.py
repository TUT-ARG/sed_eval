'''
Unit tests for metrics
'''

import nose.tools
import sed_eval


def test_precision():
    nose.tools.assert_almost_equals(sed_eval.metric.precision(100, 100), 1)
    nose.tools.assert_almost_equals(sed_eval.metric.precision(10, 100), 0.1)
    nose.tools.assert_almost_equals(sed_eval.metric.precision(0, 100), 0)


def test_recall():
    nose.tools.assert_almost_equals(sed_eval.metric.recall(100, 100), 1)
    nose.tools.assert_almost_equals(sed_eval.metric.recall(10, 100), 0.1)
    nose.tools.assert_almost_equals(sed_eval.metric.recall(0, 100), 0)


def test_f_measure():
    nose.tools.assert_almost_equals(sed_eval.metric.f_measure(0, 0), 0.0)
    nose.tools.assert_almost_equals(sed_eval.metric.f_measure(0.1, 0), 0.0)
    nose.tools.assert_almost_equals(sed_eval.metric.f_measure(0.1, 0.1), 0.1)
    nose.tools.assert_almost_equals(sed_eval.metric.f_measure(0.1, 0.8), 0.17777777)
    nose.tools.assert_almost_equals(sed_eval.metric.f_measure(0.1, 0.5, 2), 0.27777777)


def test_sensitivity():
    nose.tools.assert_almost_equals(sed_eval.metric.sensitivity(10, 10), 0.5)
    nose.tools.assert_almost_equals(sed_eval.metric.sensitivity(1, 100), 0.00990099)
    nose.tools.assert_almost_equals(sed_eval.metric.sensitivity(0, 0), 0)


def test_specificity():
    nose.tools.assert_almost_equals(sed_eval.metric.specificity(10, 10), 0.5)
    nose.tools.assert_almost_equals(sed_eval.metric.specificity(1, 100), 0.00990099)
    nose.tools.assert_almost_equals(sed_eval.metric.specificity(0, 0), 0)


def test_balanced_accuracy():
    nose.tools.assert_almost_equals(sed_eval.metric.balanced_accuracy(0.1, 0.5), 0.3)
    nose.tools.assert_almost_equals(sed_eval.metric.balanced_accuracy(0, 0.5), 0.25)
    nose.tools.assert_almost_equals(sed_eval.metric.balanced_accuracy(0, 0), 0)


def test_substitution_rate():
    nose.tools.assert_almost_equals(sed_eval.metric.substitution_rate(100, 0), 0.0)
    nose.tools.assert_almost_equals(sed_eval.metric.substitution_rate(100, 10), 0.1)
    nose.tools.assert_almost_equals(sed_eval.metric.substitution_rate(100, 100), 1.0)


def test_deletion_rate():
    nose.tools.assert_almost_equals(sed_eval.metric.deletion_rate(100, 0), 0.0)
    nose.tools.assert_almost_equals(sed_eval.metric.deletion_rate(100, 10), 0.1)
    nose.tools.assert_almost_equals(sed_eval.metric.deletion_rate(100, 100), 1.0)


def test_insertion_rate():
    nose.tools.assert_almost_equals(sed_eval.metric.insertion_rate(100, 0), 0.0)
    nose.tools.assert_almost_equals(sed_eval.metric.insertion_rate(100, 10), 0.1)
    nose.tools.assert_almost_equals(sed_eval.metric.insertion_rate(100, 100), 1.0)


def test_error_rate():
    nose.tools.assert_almost_equals(sed_eval.metric.error_rate(0, 0, 0), 0.0)
    nose.tools.assert_almost_equals(sed_eval.metric.error_rate(0.2, 0.2, 0.2), 0.6)
    nose.tools.assert_almost_equals(sed_eval.metric.error_rate(1.5, 0.2, 0.2), 1.9)

