"""
Unit tests for sound event metrics
"""

import nose.tools
import sed_eval
import os
import numpy
import dcase_util

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
        reference_event_list_for_current_file = reference_event_list.filter(filename=file)
        estimated_event_list_for_current_file = estimated_event_list.filter(filename=file)
        segment_based_metrics.evaluate(
            reference_event_list=reference_event_list_for_current_file,
            estimated_event_list=estimated_event_list_for_current_file
        )

    results = segment_based_metrics.results()
    nose.tools.assert_almost_equals(results['overall']['accuracy']['accuracy'], 0.84244791666)
    nose.tools.assert_almost_equals(results['overall']['error_rate']['error_rate'], 1.0616698292220115)

    # With specified evaluation length
    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(
        event_label_list=evaluated_event_labels,
        time_resolution=1.0
    )

    for file in evaluated_files:
        reference_event_list_for_current_file = reference_event_list.filter(filename=file)
        estimated_event_list_for_current_file = estimated_event_list.filter(filename=file)
        segment_based_metrics.evaluate(
            reference_event_list=reference_event_list_for_current_file,
            estimated_event_list=estimated_event_list_for_current_file,
            evaluated_length_seconds=1200.0
        )

    results = segment_based_metrics.results()

    nose.tools.assert_almost_equals(results['overall']['accuracy']['accuracy'], 0.9719907407407408)
    nose.tools.assert_almost_equals(results['overall']['error_rate']['error_rate'], 1.0616698292220115)


def test_dcase_style2():
    reference = os.path.join('data', 'sound_event', 'street_fold1_reference.txt')
    estimated = os.path.join('data', 'sound_event', 'street_fold1_detected.txt')

    reference_event_list = sed_eval.io.load_event_list(reference)
    estimated_event_list = sed_eval.io.load_event_list(estimated)

    evaluated_event_labels = reference_event_list.unique_event_labels
    files={}
    for event in reference_event_list:
        files[event['filename']] = event['filename']

    evaluated_files = sorted(list(files.keys()))

    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(
        event_label_list=evaluated_event_labels,
        time_resolution=1.0
    )

    for file in evaluated_files:
        reference_event_list_for_current_file = []
        for event in reference_event_list:
            if event['filename'] == file:
                reference_event_list_for_current_file.append(event)
                estimated_event_list_for_current_file = []
        for event in estimated_event_list:
            if event['filename'] == file:
                estimated_event_list_for_current_file.append(event)

        segment_based_metrics.evaluate(
            reference_event_list=reference_event_list_for_current_file,
            estimated_event_list=estimated_event_list_for_current_file
        )

    results = segment_based_metrics.results()
    nose.tools.assert_almost_equals(results['overall']['accuracy']['accuracy'], 0.84244791666)
    nose.tools.assert_almost_equals(results['overall']['error_rate']['error_rate'], 1.0616698292220115)

def test_csv():
    reference = os.path.join('data', 'sound_event', 'street_fold1_reference.csv')
    estimated = os.path.join('data', 'sound_event', 'street_fold1_detected.csv')

    reference_event_list = sed_eval.io.load_event_list(reference, delimiter='\t')
    estimated_event_list = sed_eval.io.load_event_list(estimated, delimiter='\t')

    evaluated_event_labels = reference_event_list.unique_event_labels
    files={}
    for event in reference_event_list:
        files[event['filename']] = event['filename']

    evaluated_files = sorted(list(files.keys()))

    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(
        event_label_list=evaluated_event_labels,
        time_resolution=1.0
    )

    for file in evaluated_files:
        reference_event_list_for_current_file = []
        for event in reference_event_list:
            if event['filename'] == file:
                reference_event_list_for_current_file.append(event)
                estimated_event_list_for_current_file = []
        for event in estimated_event_list:
            if event['filename'] == file:
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
    all_data = dcase_util.containers.MetaDataContainer()
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
    all_data = dcase_util.containers.MetaDataContainer()
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
            for filename in file_pair['reference_event_list'].unique_files:
                reference_event_list = file_pair['reference_event_list'].filter(filename=filename)
                estimated_event_list = file_pair['estimated_event_list'].filter(filename=filename)

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
    all_data = dcase_util.containers.MetaDataContainer()
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
                file_pair_event_lists['reference_event_list'].filter(filename=file),
                file_pair_event_lists['estimated_event_list'].filter(filename=file)
            )

    results = segment_based_metrics.results()

    nose.tools.assert_almost_equals(results['overall']['accuracy']['accuracy'], 1.0)
    nose.tools.eq_(results['overall']['accuracy']['balanced_accuracy'], 1.0)
    nose.tools.eq_(results['overall']['accuracy']['sensitivity'], 1.0)
    nose.tools.eq_(results['overall']['accuracy']['specificity'], 1.0)

    nose.tools.eq_(results['overall']['error_rate']['error_rate'], 0.0)

    nose.tools.eq_(results['overall']['f_measure']['f_measure'], 1.0)


def test_direct_use_segment():
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

    results = segment_based_metrics.results()
    nose.tools.assert_almost_equals(results['overall']['accuracy']['accuracy'], 0.5)
    nose.tools.assert_almost_equals(results['overall']['error_rate']['error_rate'], 0.555555555555)

    print(segment_based_metrics)


def test_direct_use_event():
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
                'event_onset': 0.2,
                'event_offset': 3.5,
                'file': 'audio/street/b099.wav',
                'scene_label': 'street'
            },
            {
                'event_label': 'car',
                'event_onset': 6.0,
                'event_offset': 8.0,
                'file': 'audio/street/b099.wav',
                'scene_label': 'street'
            }
        ]
    )
    event_based_metrics = sed_eval.sound_event.EventBasedMetrics(
        event_label_list=reference_event_list.unique_event_labels,
        t_collar=0.20
    )

    for filename in reference_event_list.unique_files:
        reference_event_list_for_current_file = reference_event_list.filter(
            filename=filename
        )

        estimated_event_list_for_current_file = estimated_event_list.filter(
            filename=filename
        )

        event_based_metrics.evaluate(
            reference_event_list=reference_event_list_for_current_file,
            estimated_event_list=estimated_event_list_for_current_file
        )

    results = event_based_metrics.results()
    nose.tools.assert_almost_equals(results['overall']['f_measure']['f_measure'], 0.8)
    nose.tools.assert_almost_equals(results['overall']['error_rate']['error_rate'], 0.3333333333333)

    print(event_based_metrics)


def test_event_matching():
    reference = os.path.join('data', 'sound_event', 'street_fold1_reference.txt')
    estimated = os.path.join('data', 'sound_event', 'street_fold1_detected.txt')

    reference_event_list = sed_eval.io.load_event_list(reference)
    estimated_event_list = sed_eval.io.load_event_list(estimated)

    event_based_metrics_optimal = sed_eval.sound_event.EventBasedMetrics(
        event_label_list=reference_event_list.unique_event_labels,
        t_collar=0.20,
        event_matching_type='optimal'
    )
    event_based_metrics_greedy = sed_eval.sound_event.EventBasedMetrics(
        event_label_list=reference_event_list.unique_event_labels,
        t_collar=0.20,
        event_matching_type='greedy'
    )
    for filename in reference_event_list.unique_files:
        reference_event_list_for_current_file = reference_event_list.filter(
            filename=filename
        )

        estimated_event_list_for_current_file = estimated_event_list.filter(
            filename=filename
        )

        event_based_metrics_optimal.evaluate(
            reference_event_list=reference_event_list_for_current_file,
            estimated_event_list=estimated_event_list_for_current_file
        )
        event_based_metrics_greedy.evaluate(
            reference_event_list=reference_event_list_for_current_file,
            estimated_event_list=estimated_event_list_for_current_file
        )

    results_optimal = event_based_metrics_optimal.results()
    results_greedy = event_based_metrics_greedy.results()

    nose.tools.assert_almost_equals(
        results_optimal['overall']['f_measure']['f_measure'],
        results_greedy['overall']['f_measure']['f_measure']
    )
    nose.tools.assert_almost_equals(
        results_optimal['overall']['error_rate']['error_rate'],
        results_greedy['overall']['error_rate']['error_rate']
    )
    nose.tools.assert_almost_equals(
        results_optimal['class_wise_average']['error_rate']['error_rate'],
        results_greedy['class_wise_average']['error_rate']['error_rate']
    )


    reference = os.path.join('data', 'sound_event', 'mini_reference.txt')
    estimated_a = os.path.join('data', 'sound_event', 'mini_detected_a.txt')
    estimated_b = os.path.join('data', 'sound_event', 'mini_detected_b.txt')

    reference_event_list = sed_eval.io.load_event_list(reference)
    estimated_event_list_a = sed_eval.io.load_event_list(estimated_a)
    estimated_event_list_b = sed_eval.io.load_event_list(estimated_b)

    event_based_metrics_optimal_a = sed_eval.sound_event.EventBasedMetrics(
        event_label_list=reference_event_list.unique_event_labels,
        t_collar=0.25,
        event_matching_type='optimal'
    )
    event_based_metrics_optimal_b = sed_eval.sound_event.EventBasedMetrics(
        event_label_list=reference_event_list.unique_event_labels,
        t_collar=0.25,
        event_matching_type='optimal'
    )
    event_based_metrics_greedy_a = sed_eval.sound_event.EventBasedMetrics(
        event_label_list=reference_event_list.unique_event_labels,
        t_collar=0.25,
        event_matching_type='greedy'
    )
    event_based_metrics_greedy_b = sed_eval.sound_event.EventBasedMetrics(
        event_label_list=reference_event_list.unique_event_labels,
        t_collar=0.25,
        event_matching_type='greedy'
    )

    event_based_metrics_optimal_a.evaluate(
        reference_event_list=reference_event_list,
        estimated_event_list=estimated_event_list_a
    )
    event_based_metrics_optimal_b.evaluate(
        reference_event_list=reference_event_list,
        estimated_event_list=estimated_event_list_b
    )

    event_based_metrics_greedy_a.evaluate(
        reference_event_list=reference_event_list,
        estimated_event_list=estimated_event_list_a
    )
    event_based_metrics_greedy_b.evaluate(
        reference_event_list=reference_event_list,
        estimated_event_list=estimated_event_list_b
    )

    results_optimal_a = event_based_metrics_optimal_a.results()
    results_optimal_b = event_based_metrics_optimal_b.results()

    results_greedy_a = event_based_metrics_greedy_a.results()
    results_greedy_b = event_based_metrics_greedy_b.results()

    nose.tools.assert_almost_equals(
        results_optimal_a['overall']['f_measure']['f_measure'],
        results_optimal_b['overall']['f_measure']['f_measure']
    )

    nose.tools.assert_almost_equals(
        results_greedy_a['overall']['f_measure']['f_measure'],
        results_greedy_b['overall']['f_measure']['f_measure']
    )

    nose.tools.assert_almost_equals(
        results_optimal_a['overall']['error_rate']['error_rate'],
        results_optimal_b['overall']['error_rate']['error_rate']
    )
    nose.tools.assert_almost_equals(
        results_optimal_a['class_wise_average']['error_rate']['error_rate'],
        results_optimal_b['class_wise_average']['error_rate']['error_rate']
    )

def test_empty_system_output_handling():
    reference = [
        {
            'filename': 'f1.wav',
            'onset': 0.3,
            'offset': 0.8,
            'event_label': 'event A'
        },
        {
            'filename': 'f2.wav',
            'onset': 0.1,
            'offset': 0.8,
            'event_label': 'event B'
        }
    ]
    estimated = [
        {
            'filename': 'f1.wav',
            'onset': 0.2,
            'offset': 0.9,
            'event_label': 'event A'
        }
    ]
    event_based_metric = sed_eval.sound_event.EventBasedMetrics(
        event_label_list=['event A', 'event B'],
        t_collar=0.200,
        percentage_of_length=0.2
    )
    event_based_metric_zero = sed_eval.sound_event.EventBasedMetrics(
        event_label_list=['event A', 'event B'],
        t_collar=0.200,
        percentage_of_length=0.2,
        empty_system_output_handling='zero_score'
    )

    for filename in sed_eval.util.event_list.unique_files(reference):
        reference_event_list_for_current_file = sed_eval.util.event_list.filter_event_list(
            event_list=reference,
            filename=filename
        )

        estimated_event_list_for_current_file = sed_eval.util.event_list.filter_event_list(
            event_list=estimated,
            filename=filename
        )
        event_based_metric.evaluate(
            reference_event_list=reference_event_list_for_current_file,
            estimated_event_list=estimated_event_list_for_current_file
        )
        event_based_metric_zero.evaluate(
            reference_event_list=reference_event_list_for_current_file,
            estimated_event_list=estimated_event_list_for_current_file
        )

    results = event_based_metric.results()
    results_zero = event_based_metric_zero.results()

    nose.tools.eq_(
        results['class_wise_average']['f_measure']['f_measure'],
        1.0
    )
    nose.tools.eq_(
        results_zero['class_wise_average']['f_measure']['f_measure'],
        0.5
    )
