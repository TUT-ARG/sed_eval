'''
Unit tests for scene classification
'''

import numpy
import nose.tools
import sed_eval


def test_direct_use():
    reference = sed_eval.util.SceneList([
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

    estimated = sed_eval.util.SceneList([
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
