"""
Unit tests for sound event metrics
"""

import nose.tools
import sed_eval
import os
import numpy


@nose.tools.raises(ValueError)
def test_parameters_1():
    reference = os.path.join('data', 'sound_event', 'street_fold1_reference.txt')
    estimated = os.path.join('data', 'sound_event', 'street_fold1_detected.txt')

    reference_event_list = sed_eval.io.load_event_list(reference)
    estimated_event_list = sed_eval.io.load_event_list(estimated)

    evaluated_event_labels = reference_event_list.unique_event_labels
    evaluated_files = reference_event_list.unique_files

    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(
        event_label_list=numpy.array(evaluated_event_labels),
        time_resolution=['test']
    )


@nose.tools.raises(ValueError)
def test_parameters_2():
    reference = os.path.join('data', 'sound_event', 'street_fold1_reference.txt')
    estimated = os.path.join('data', 'sound_event', 'street_fold1_detected.txt')

    reference_event_list = sed_eval.io.load_event_list(reference)
    estimated_event_list = sed_eval.io.load_event_list(estimated)

    evaluated_event_labels = reference_event_list.unique_event_labels
    evaluated_files = reference_event_list.unique_files

    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(
        event_label_list=numpy.array(evaluated_event_labels),
        time_resolution=['test']
    )

@nose.tools.raises(ValueError)
def test_parameters_3():
    reference = os.path.join('data', 'sound_event', 'street_fold1_reference.txt')
    estimated = os.path.join('data', 'sound_event', 'street_fold1_detected.txt')

    reference_event_list = sed_eval.io.load_event_list(reference)
    estimated_event_list = sed_eval.io.load_event_list(estimated)

    evaluated_event_labels = reference_event_list.unique_event_labels
    evaluated_files = reference_event_list.unique_files

    event_based_metrics = sed_eval.sound_event.EventBasedMetrics(
        event_label_list=evaluated_event_labels,
        t_collar=[2]
    )


@nose.tools.raises(ValueError)
def test_parameters_4():
    reference = os.path.join('data', 'sound_event', 'street_fold1_reference.txt')
    estimated = os.path.join('data', 'sound_event', 'street_fold1_detected.txt')

    reference_event_list = sed_eval.io.load_event_list(reference)
    estimated_event_list = sed_eval.io.load_event_list(estimated)

    evaluated_event_labels = reference_event_list.unique_event_labels
    evaluated_files = reference_event_list.unique_files

    event_based_metrics = sed_eval.sound_event.EventBasedMetrics(
        event_label_list=evaluated_event_labels,
        t_collar=0.2,
        percentage_of_length='test',
    )


def test_dcase_style():
    reference = os.path.join('data', 'sound_event', 'street_fold1_reference.txt')
    estimated = os.path.join('data', 'sound_event', 'street_fold1_detected.txt')

    reference_event_list = sed_eval.io.load_event_list(reference)
    estimated_event_list = sed_eval.io.load_event_list(estimated)

    evaluated_event_labels = reference_event_list.unique_event_labels
    evaluated_files = reference_event_list.unique_files

    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(
        event_label_list=evaluated_event_labels,
        time_resolution=1.0
    )

    for file in evaluated_files:
        reference_event_list_for_current_file = reference_event_list.filter(file=file)
        estimated_event_list_for_current_file = estimated_event_list.filter(file=file)
        segment_based_metrics.evaluate(
            reference_event_list=reference_event_list_for_current_file,
            estimated_event_list=estimated_event_list_for_current_file
        )
    results = segment_based_metrics.results()
    nose.tools.assert_almost_equals(results['overall']['accuracy']['accuracy'], 0.84244791666)
    nose.tools.assert_almost_equals(results['overall']['error_rate']['error_rate'], 1.0616698292220115)


def test_dcase_style2():
    reference = os.path.join('data', 'sound_event', 'street_fold1_reference.txt')
    estimated = os.path.join('data', 'sound_event', 'street_fold1_detected.txt')

    reference_event_list = sed_eval.io.load_event_list(reference)
    estimated_event_list = sed_eval.io.load_event_list(estimated)

    evaluated_event_labels = reference_event_list.unique_event_labels
    files={}
    for event in reference_event_list:
        files[event['file']] = event['file']

    evaluated_files = sorted(list(files.keys()))

    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(
        event_label_list=evaluated_event_labels,
        time_resolution=1.0
    )

    for file in evaluated_files:
        reference_event_list_for_current_file = []
        for event in reference_event_list:
            if event['file'] == file:
                reference_event_list_for_current_file.append(event)
                estimated_event_list_for_current_file = []
        for event in estimated_event_list:
            if event['file'] == file:
                estimated_event_list_for_current_file.append(event)

        segment_based_metrics.evaluate(
            reference_event_list=reference_event_list_for_current_file,
            estimated_event_list=estimated_event_list_for_current_file
        )

    results = segment_based_metrics.results()
    nose.tools.assert_almost_equals(results['overall']['accuracy']['accuracy'], 0.84244791666)
    nose.tools.assert_almost_equals(results['overall']['error_rate']['error_rate'], 1.0616698292220115)


def test_binary():
    file_list = [
        {'reference_file': os.path.join('data', 'sound_event', 'binary1.txt'),
         'estimated_file': os.path.join('data', 'sound_event', 'binary1_detected.txt')},
        {'reference_file': os.path.join('data', 'sound_event', 'binary2.txt'),
         'estimated_file': os.path.join('data', 'sound_event', 'binary2_detected.txt')},
    ]
    data = []
    all_data = sed_eval.util.event_list.EventList()
    for file_pair in file_list:
        reference_event_list = sed_eval.io.load_event_list(file_pair['reference_file'])
        estimated_event_list = sed_eval.io.load_event_list(file_pair['estimated_file'])
        data.append({'reference_event_list': reference_event_list, 'estimated_event_list': estimated_event_list})
        all_data += reference_event_list
    event_labels = all_data.unique_event_labels

    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(
        event_label_list=event_labels,
        time_resolution=1.0
    )

    for file_pair in data:
        segment_based_metrics.evaluate(file_pair['reference_event_list'], file_pair['estimated_event_list'])
    results = segment_based_metrics.results()

    nose.tools.assert_almost_equals(results['overall']['accuracy']['accuracy'], 0.666666666)
    nose.tools.eq_(results['overall']['accuracy']['balanced_accuracy'], 0.75)
    nose.tools.eq_(results['overall']['accuracy']['sensitivity'], 1.0)
    nose.tools.eq_(results['overall']['accuracy']['specificity'], 0.5)

    nose.tools.eq_(results['overall']['error_rate']['error_rate'], 1.0)

    nose.tools.assert_almost_equals(results['overall']['f_measure']['f_measure'], 0.66666666)

    event_based_metrics = sed_eval.sound_event.EventBasedMetrics(
        event_label_list=event_labels,
        t_collar=0.20
    )

    for file_pair in data:
        event_based_metrics.evaluate(file_pair['reference_event_list'], file_pair['estimated_event_list'])
    results = event_based_metrics.results()

    nose.tools.assert_almost_equals(results['overall']['error_rate']['error_rate'], 0.9999999999999999)
    nose.tools.assert_almost_equals(results['overall']['f_measure']['f_measure'], 0.6666666666666666666)

    file_list = [
        {'reference_file': os.path.join('data', 'sound_event', 'binary5.txt'),
         'estimated_file': os.path.join('data', 'sound_event', 'binary5_detected.txt')},
    ]
    data = []
    all_data = sed_eval.util.event_list.EventList()
    for file_pair in file_list:
        reference_event_list = sed_eval.io.load_event_list(file_pair['reference_file'])
        estimated_event_list = sed_eval.io.load_event_list(file_pair['estimated_file'])
        data.append({'reference_event_list': reference_event_list, 'estimated_event_list': estimated_event_list})
        all_data += reference_event_list
    event_labels = all_data.unique_event_labels

    event_based_metrics = sed_eval.sound_event.EventBasedMetrics(
        event_label_list=event_labels
    )

    for file_pair in data:
        if len(file_pair['reference_event_list'].unique_files) > 1:
            for file in file_pair['reference_event_list'].unique_files:
                reference_event_list = file_pair['reference_event_list'].filter(file=file)
                estimated_event_list = file_pair['estimated_event_list'].filter(file=file)

                event_based_metrics.evaluate(reference_event_list, estimated_event_list)

    results = event_based_metrics.results()

    nose.tools.assert_almost_equals(results['overall']['error_rate']['error_rate'], 1.5)
    nose.tools.assert_almost_equals(results['overall']['f_measure']['f_measure'], 0.0)


def test_audioset():
    file_list = [
        {
            'reference_file': os.path.join('data', 'sound_event', 'audioset1.txt'),
            'estimated_file': os.path.join('data', 'sound_event', 'audioset1_detected.txt')
        }
    ]

    data = []
    all_data = sed_eval.util.event_list.EventList()
    for file_pair in file_list:
        reference_event_list = sed_eval.io.load_event_list(file_pair['reference_file'])
        estimated_event_list = sed_eval.io.load_event_list(file_pair['estimated_file'])
        data.append(
            {
                'reference_event_list': reference_event_list,
                'estimated_event_list': estimated_event_list
            }
        )
        all_data += reference_event_list

    event_labels = all_data.unique_event_labels

    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(
        event_label_list=event_labels,
        time_resolution=1.0
    )

    for file_pair_event_lists in data:
        evaluated_files = file_pair_event_lists['reference_event_list'].unique_files
        for file in evaluated_files:
            segment_based_metrics.evaluate(
                file_pair_event_lists['reference_event_list'].filter(file=file),
                file_pair_event_lists['estimated_event_list'].filter(file=file)
            )

    results = segment_based_metrics.results()

    nose.tools.assert_almost_equals(results['overall']['accuracy']['accuracy'], 1.0)
    nose.tools.eq_(results['overall']['accuracy']['balanced_accuracy'], 1.0)
    nose.tools.eq_(results['overall']['accuracy']['sensitivity'], 1.0)
    nose.tools.eq_(results['overall']['accuracy']['specificity'], 1.0)

    nose.tools.eq_(results['overall']['error_rate']['error_rate'], 0.0)

    nose.tools.eq_(results['overall']['f_measure']['f_measure'], 1.0)
