'''
Unit tests for scene classification
'''

import numpy
import nose.tools
import sed_eval
import dcase_util


def test_direct_use():
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

    results = scene_metrics.results()
    nose.tools.assert_almost_equals(results['overall']['accuracy'], 0.4)

    print(scene_metrics)


def test_direct_use2():
    reference = [
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
    ]

    estimated = [
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
    ]

    scene_labels = ['supermarket', 'tubestation', 'quietstreet', 'office', 'bus']

    scene_metrics = sed_eval.scene.SceneClassificationMetrics(scene_labels)
    scene_metrics.evaluate(
        reference_scene_list=reference,
        estimated_scene_list=estimated
    )

    results = scene_metrics.results()
    nose.tools.assert_almost_equals(results['overall']['accuracy'], 0.4)

    print(scene_metrics)

    scene_metrics.reset()
    results = scene_metrics.results()
    nose.tools.assert_almost_equals(results['overall']['count']['Nref'], 0)


@nose.tools.raises(ValueError)
def test_parameters_1():
    reference = [
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
    ]

    scene_labels = ['supermarket', 'tubestation', 'quietstreet', 'office', 'bus']

    scene_metrics = sed_eval.scene.SceneClassificationMetrics(scene_labels)
    scene_metrics.evaluate(
        reference_scene_list=reference
    )

