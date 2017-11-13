"""
Unit tests for audio tag metrics
"""

import nose.tools
import sed_eval
import os
import numpy
import dcase_util


def test_direct_use():

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

    results = tag_evaluator.results()

    nose.tools.eq_(results['overall']['count']['Nref'], 11)
    nose.tools.eq_(results['overall']['count']['Nsys'], 14)
    nose.tools.assert_almost_equals(results['overall']['eer']['eer'], 0.181818181818181)

    nose.tools.assert_almost_equals(results['overall']['f_measure']['f_measure'], 0.72)
    nose.tools.assert_almost_equals(results['overall']['f_measure']['precision'], 0.6428571428571429)
    nose.tools.assert_almost_equals(results['overall']['f_measure']['recall'], 0.8181818181818182)

    nose.tools.eq_(results['class_wise_average']['eer']['eer'], 0.175)
    nose.tools.assert_almost_equals(results['class_wise_average']['f_measure']['f_measure'], 0.7)
    nose.tools.assert_almost_equals(results['class_wise_average']['f_measure']['precision'], 0.7166666666666667)
    nose.tools.assert_almost_equals(results['class_wise_average']['f_measure']['recall'], 0.8333333333333333)

    print(tag_evaluator)


def test_direct_use2():

    reference_tag_list = [
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
    ]

    estimated_tag_probabilities = [
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
    ]

    tag_evaluator = sed_eval.audio_tag.AudioTaggingMetrics(
        tags=['cat', 'dog', 'bird', 'speech']
    )

    tag_evaluator.evaluate(
        reference_tag_list=reference_tag_list,
        estimated_tag_probabilities=estimated_tag_probabilities
    )

    results = tag_evaluator.results()

    nose.tools.assert_almost_equals(results['overall']['eer']['eer'], 0.181818181818181)

    nose.tools.eq_(results['class_wise_average']['eer']['eer'], 0.175)

    tag_evaluator.reset()

    results = tag_evaluator.results()

    nose.tools.eq_(results['overall']['count']['Nsys'], 0)
    nose.tools.eq_(results['overall']['count']['Nref'], 0)


@nose.tools.raises(ValueError)
def test_parameters_1():

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

    tag_evaluator = sed_eval.audio_tag.AudioTaggingMetrics(
        tags=reference_tag_list.unique_tags
    )

    tag_evaluator.evaluate(
        reference_tag_list=reference_tag_list
    )
