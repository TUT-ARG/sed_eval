'''
Unit tests for utils
'''

from __future__ import print_function, absolute_import
import numpy
import nose.tools
import sed_eval

event_list = [
    {'event_label': 'alert',  'event_offset': 17.1469, 'event_onset': 15.78237},
    {'event_label': 'clearthroat', 'event_offset': 5.32103, 'event_onset': 4.42416},
    {'event_label': 'cough', 'event_offset': 46.00705, 'event_onset': 44.90501},
    {'event_label': 'doorslam', 'event_offset': 44.46713, 'event_onset': 42.99847},
    {'event_label': 'doorslam', 'event_offset': 75.72066, 'event_onset': 74.79186},
    {'event_label': 'drawer', 'event_offset': 20.80981, 'event_onset': 19.08573},
    {'event_label': 'drawer', 'event_offset': 16.91668, 'event_onset': 14.92077},
    {'event_label': 'keyboard', 'event_offset': 85.67182, 'event_onset': 84.29222},
    {'event_label': 'keyboard', 'event_offset': 76.08911, 'event_onset': 74.84829},
    {'event_label': 'keys', 'event_offset': 69.44095, 'event_onset': 67.72667},
    {'event_label': 'keys', 'event_offset': 56.41965, 'event_onset': 54.70536},
    {'event_label': 'knock', 'event_offset': 5.48751, 'event_onset': 4.49323},
    {'event_label': 'knock', 'event_offset': 68.33579, 'event_onset': 67.3415},
    {'event_label': 'laughter', 'event_offset': 33.53816 ,'event_onset': 31.72691},
    {'event_label': 'laughter', 'event_offset': 60.12443, 'event_onset': 58.31318},
    {'event_label': 'mouse', 'event_offset': 60.96385, 'event_onset': 59.76997},
    {'event_label': 'mouse', 'event_offset': 39.17153, 'event_onset': 38.12083},
    {'event_label': 'pendrop', 'event_offset': 72.402, 'event_onset': 71.49642},
    {'event_label': 'pendrop', 'event_offset': 42.99936, 'event_onset': 42.09379},
    {'event_label': 'phone', 'event_offset': 31.90438, 'event_onset': 30.68533},
    {'event_label': 'phone', 'event_offset': 7.17349, 'event_onset': 5.11634},
    {'event_label': 'printer', 'event_offset': 83.35251, 'event_onset': 78.93727},
    {'event_label': 'printer', 'event_offset': 68.68035, 'event_onset': 64.30919},
    {'event_label': 'speech', 'event_offset': 67.13386, 'event_onset': 65.80452},
    {'event_label': 'speech', 'event_offset': 25.70843, 'event_onset': 23.69991},
    {'event_label': 'switch', 'event_offset': 52.52053, 'event_onset': 52.09387},
    {'event_label': 'switch', 'event_offset': 72.7728, 'event_onset': 72.35648}
]
event_labels = ['alert',
          'clearthroat',
          'cough',
          'doorslam',
          'drawer',
          'keyboard',
          'keys',
          'knock',
          'laughter',
          'mouse',
          'pendrop',
          'phone',
          'printer',
          'speech',
          'switch']


scene_list = [
    {'file': 'scenes_stereo/bus01.wav', 'scene_label': 'bus'},
    {'file': 'scenes_stereo/bus04.wav', 'scene_label': 'bus'},
    {'file': 'scenes_stereo/bus06.wav', 'scene_label': 'bus'},
    {'file': 'scenes_stereo/busystreet05.wav', 'scene_label': 'busystreet'},
    {'file': 'scenes_stereo/busystreet07.wav', 'scene_label': 'busystreet'},
    {'file': 'scenes_stereo/busystreet08.wav', 'scene_label': 'busystreet'},
    {'file': 'scenes_stereo/office07.wav', 'scene_label': 'office'},
    {'file': 'scenes_stereo/office08.wav', 'scene_label': 'office'},
    {'file': 'scenes_stereo/office10.wav', 'scene_label': 'office'},
    {'file': 'scenes_stereo/openairmarket01.wav', 'scene_label': 'openairmarket'},
    {'file': 'scenes_stereo/openairmarket04.wav', 'scene_label': 'openairmarket'},
    {'file': 'scenes_stereo/openairmarket05.wav', 'scene_label': 'openairmarket'},
    {'file': 'scenes_stereo/park04.wav', 'scene_label': 'park'},
    {'file': 'scenes_stereo/park09.wav', 'scene_label': 'park'},
    {'file': 'scenes_stereo/park10.wav', 'scene_label': 'park'},
    {'file': 'scenes_stereo/quietstreet01.wav', 'scene_label': 'quietstreet'},
    {'file': 'scenes_stereo/quietstreet05.wav', 'scene_label': 'quietstreet'},
    {'file': 'scenes_stereo/quietstreet08.wav', 'scene_label': 'quietstreet'},
    {'file': 'scenes_stereo/restaurant01.wav', 'scene_label': 'restaurant'},
    {'file': 'scenes_stereo/restaurant05.wav', 'scene_label': 'restaurant'},
    {'file': 'scenes_stereo/restaurant10.wav', 'scene_label': 'restaurant'},
    {'file': 'scenes_stereo/supermarket02.wav', 'scene_label': 'supermarket'},
    {'file': 'scenes_stereo/supermarket05.wav', 'scene_label': 'supermarket'},
    {'file': 'scenes_stereo/supermarket09.wav', 'scene_label': 'supermarket'},
    {'file': 'scenes_stereo/tube01.wav', 'scene_label': 'tube'},
    {'file': 'scenes_stereo/tube03.wav', 'scene_label': 'tube'},
    {'file': 'scenes_stereo/tube07.wav', 'scene_label': 'tube'},
    {'file': 'scenes_stereo/tubestation05.wav', 'scene_label': 'tubestation'},
    {'file': 'scenes_stereo/tubestation07.wav', 'scene_label': 'tubestation'},
    {'file': 'scenes_stereo/tubestation10.wav', 'scene_label': 'tubestation'},
]

scene_labels = [
    'bus',
    'busystreet',
    'office',
    'openairmarket',
    'park',
    'quietstreet',
    'restaurant',
    'supermarket',
    'tube',
    'tubestation',
]


def test_unique_event_labels():
    nose.tools.assert_list_equal(sed_eval.util.unique_event_labels(event_list), event_labels)


def test_max_event_offset():
    nose.tools.assert_equal(sed_eval.util.max_event_offset(event_list), 85.67182)


def test_unique_scene_labels():
    nose.tools.assert_list_equal(sed_eval.util.unique_scene_labels(scene_list), scene_labels)


def test_event_list_to_event_roll():
    minimal_event_list = [
        {'event_label': 'A', 'event_onset': 0, 'event_offset': 1, },
        {'event_label': 'A', 'event_onset': 5, 'event_offset': 15, },
        {'event_label': 'B', 'event_onset': 1, 'event_offset': 2, },
        {'event_label': 'B', 'event_onset': 4, 'event_offset': 5, },
        {'event_label': 'C', 'event_onset': 7, 'event_offset': 12, }
    ]

    target_event_roll = numpy.array([
       [1.,  0.,  0.],  # 0
       [0.,  1.,  0.],  # 1
       [0.,  0.,  0.],  # 2
       [0.,  0.,  0.],  # 3
       [0.,  1.,  0.],  # 4
       [1.,  0.,  0.],  # 5
       [1.,  0.,  0.],  # 6
       [1.,  0.,  1.],  # 7
       [1.,  0.,  1.],  # 8
       [1.,  0.,  1.],  # 9
       [1.,  0.,  1.],  # 10
       [1.,  0.,  1.],  # 11
       [1.,  0.,  0.],  # 12
       [1.,  0.,  0.],  # 13
       [1.,  0.,  0.],  # 14
    ])

    event_roll = sed_eval.util.event_list_to_event_roll(minimal_event_list,
                                                        event_label_list=['A', 'B', 'C'],
                                                        time_resolution=1.0)
    print(target_event_roll.T)
    print("")
    print(event_roll.T)
    numpy.testing.assert_array_equal(target_event_roll, event_roll)
    nose.tools.assert_equal(event_roll.shape[0], target_event_roll.shape[0])
    nose.tools.assert_equal(event_roll.shape[1], target_event_roll.shape[1])


def test_pad_event_roll():
    a = numpy.zeros((100, 10))
    nose.tools.assert_equal(sed_eval.util.pad_event_roll(a, 200).shape[0], 200)
    nose.tools.assert_equal(sed_eval.util.pad_event_roll(a, 100).shape[0], 100)
    nose.tools.assert_equal(sed_eval.util.pad_event_roll(a, 100).shape[0], 100)


def test_match_event_roll_lengths():
    a = numpy.zeros((100, 10))
    b = numpy.zeros((10, 10))

    a_, b_ = sed_eval.util.match_event_roll_lengths(a, b)
    nose.tools.assert_equal(a_.shape[0], b_.shape[0])
    nose.tools.assert_equal(a_.shape[1], b_.shape[1])
    nose.tools.assert_equal(b_.shape[0], a.shape[0])
    nose.tools.assert_equal(a_.shape[1], a.shape[1])
    nose.tools.assert_equal(b_.shape[1], b.shape[1])

