"""
Unit tests for sound event metrics
"""

import nose.tools
import sed_eval

def test_binary():
    file_list = [
        {'reference_file': 'data/sound_event/binary1.txt',
         'estimated_file': 'data/sound_event/binary1_detected.txt'},
        {'reference_file': 'data/sound_event/binary2.txt',
         'estimated_file': 'data/sound_event/binary2_detected.txt'},
    ]
    data = []
    all_data = sed_eval.util.event_list.EventList()
    for file_pair in file_list:
        reference_event_list = sed_eval.io.load_event_list(file_pair['reference_file'])
        estimated_event_list = sed_eval.io.load_event_list(file_pair['estimated_file'])
        data.append({'reference_event_list': reference_event_list, 'estimated_event_list': estimated_event_list})
        all_data += reference_event_list
    event_labels = all_data.unique_event_labels

    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(event_label_list=event_labels, time_resolution=1.0)
    for file_pair in data:
        segment_based_metrics.evaluate(file_pair['reference_event_list'], file_pair['estimated_event_list'])
    results = segment_based_metrics.results()

    nose.tools.assert_almost_equals(results['overall']['accuracy']['accuracy'], 0.666666666)
    nose.tools.eq_(results['overall']['accuracy']['balanced_accuracy'], 0.75)
    nose.tools.eq_(results['overall']['accuracy']['sensitivity'], 1.0)
    nose.tools.eq_(results['overall']['accuracy']['specificity'], 0.5)

    nose.tools.eq_(results['overall']['error_rate']['error_rate'], 1.0)

    nose.tools.assert_almost_equals(results['overall']['f_measure']['f_measure'], 0.66666666)

    event_based_metrics = sed_eval.sound_event.EventBasedMetrics(event_label_list=event_labels, t_collar=0.20)
    for file_pair in data:
        event_based_metrics.evaluate(file_pair['reference_event_list'], file_pair['estimated_event_list'])
    results = event_based_metrics.results()

    nose.tools.assert_almost_equals(results['overall']['error_rate']['error_rate'], 0.9999999999999999)
    nose.tools.assert_almost_equals(results['overall']['f_measure']['f_measure'], 0.6666666666666666666)

def test_audioset():
    file_list = [
        {'reference_file': 'data/sound_event/audioset1.txt',
         'estimated_file': 'data/sound_event/audioset1_detected.txt'}
    ]

    data = []
    all_data = sed_eval.util.event_list.EventList()
    for file_pair in file_list:
        reference_event_list = sed_eval.io.load_event_list(file_pair['reference_file'])
        estimated_event_list = sed_eval.io.load_event_list(file_pair['estimated_file'])
        data.append({'reference_event_list': reference_event_list, 'estimated_event_list': estimated_event_list})
        all_data += reference_event_list
    event_labels = all_data.unique_event_labels

    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(event_label_list=event_labels, time_resolution=1.0)
    for file_pair in data:
        segment_based_metrics.evaluate(file_pair['reference_event_list'], file_pair['estimated_event_list'])
    results = segment_based_metrics.results()

    nose.tools.assert_almost_equals(results['overall']['accuracy']['accuracy'], 1.0)
    nose.tools.eq_(results['overall']['accuracy']['balanced_accuracy'], 1.0)
    nose.tools.eq_(results['overall']['accuracy']['sensitivity'], 1.0)
    nose.tools.eq_(results['overall']['accuracy']['specificity'], 1.0)

    nose.tools.eq_(results['overall']['error_rate']['error_rate'], 0.0)

    nose.tools.eq_(results['overall']['f_measure']['f_measure'], 1.0)
