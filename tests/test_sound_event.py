"""
Unit tests for sound event metrics
"""

import nose.tools
import sed_eval

# add DCASE2016 baseline system
import sys
sys.path.insert(0, 'dcase2016/DCASE2016-baseline-system-python-1.0.6/src')
from evaluation import DCASE2016_EventDetection_SegmentBasedMetrics, DCASE2016_EventDetection_EventBasedMetrics

file_list = [
    {'reference_file': 'data/sound_event/office_snr0_med_v2.txt',  'estimated_file': 'data/sound_event/office_snr0_med_v2_detected.txt'},
    {'reference_file': 'data/sound_event/office_snr0_high_v2.txt', 'estimated_file': 'data/sound_event/office_snr0_high_v2_detected.txt'},
]

def test_compare_dcase2016_metrics_segment():
    data = []
    all_data = sed_eval.util.event_list.EventList()
    for file_pair in file_list:
        reference_event_list = sed_eval.io.load_event_list(file_pair['reference_file'])
        estimated_event_list = sed_eval.io.load_event_list(file_pair['estimated_file'])
        data.append({'reference_event_list': reference_event_list, 'estimated_event_list': estimated_event_list})
        all_data += reference_event_list
    event_labels = all_data.unique_event_labels

    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(event_label_list=event_labels, time_resolution=1.0)
    dcase2016_segment_based_metric = DCASE2016_EventDetection_SegmentBasedMetrics(class_list=event_labels)

    for file_pair in data:
        segment_based_metrics.evaluate(file_pair['reference_event_list'], file_pair['estimated_event_list'])
        dcase2016_segment_based_metric.evaluate(annotated_ground_truth=file_pair['reference_event_list'],
                                                system_output=file_pair['estimated_event_list'])

    results = segment_based_metrics.results()
    dcase2016_results = dcase2016_segment_based_metric.results()

    # F-measure
    nose.tools.assert_almost_equals(dcase2016_results['overall']['F'], results['overall']['f_measure']['f_measure'])
    nose.tools.assert_almost_equals(dcase2016_results['overall']['Pre'], results['overall']['f_measure']['precision'])
    nose.tools.assert_almost_equals(dcase2016_results['overall']['Rec'], results['overall']['f_measure']['recall'])

    # Error rate
    nose.tools.assert_almost_equals(dcase2016_results['overall']['ER'], results['overall']['error_rate']['error_rate'])
    nose.tools.assert_almost_equals(dcase2016_results['overall']['D'], results['overall']['error_rate']['deletion_rate'])
    nose.tools.assert_almost_equals(dcase2016_results['overall']['I'], results['overall']['error_rate']['insertion_rate'])
    nose.tools.assert_almost_equals(dcase2016_results['overall']['S'], results['overall']['error_rate']['substitution_rate'])


def test_compare_dcase2016_metrics_event():
    data = []
    all_data = sed_eval.util.event_list.EventList()
    for file_pair in file_list:
        reference_event_list = sed_eval.io.load_event_list(file_pair['reference_file'])
        estimated_event_list = sed_eval.io.load_event_list(file_pair['estimated_file'])
        data.append({'reference_event_list': reference_event_list, 'estimated_event_list': estimated_event_list})
        all_data += reference_event_list
    event_labels = all_data.unique_event_labels

    event_based_metrics = sed_eval.sound_event.EventBasedMetrics(event_label_list=event_labels, t_collar=0.20)
    dcase2016_event_based_metric = DCASE2016_EventDetection_EventBasedMetrics(class_list=event_labels)

    for file_pair in data:
        event_based_metrics.evaluate(file_pair['reference_event_list'], file_pair['estimated_event_list'])
        dcase2016_event_based_metric.evaluate(annotated_ground_truth=file_pair['reference_event_list'],
                                              system_output=file_pair['estimated_event_list'])

    results = event_based_metrics.results()
    dcase2016_results = dcase2016_event_based_metric.results()

    # F-measure
    nose.tools.assert_almost_equals(dcase2016_results['overall']['F'], results['overall']['f_measure']['f_measure'])
    nose.tools.assert_almost_equals(dcase2016_results['overall']['Pre'], results['overall']['f_measure']['precision'])
    nose.tools.assert_almost_equals(dcase2016_results['overall']['Rec'], results['overall']['f_measure']['recall'])

    # Error rate
    nose.tools.assert_almost_equals(dcase2016_results['overall']['ER'], results['overall']['error_rate']['error_rate'])
    nose.tools.assert_almost_equals(dcase2016_results['overall']['D'], results['overall']['error_rate']['deletion_rate'])
    nose.tools.assert_almost_equals(dcase2016_results['overall']['I'], results['overall']['error_rate']['insertion_rate'])
    nose.tools.assert_almost_equals(dcase2016_results['overall']['S'], results['overall']['error_rate']['substitution_rate'])

