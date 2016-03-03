""" Unit tests for input/output functions """

import nose.tools
import sed_eval
import tempfile


def test_load_event_list():
    # Tests for valid formats

    delimiters = [',', ';', '\t']
    for delimiter in delimiters:
        tmp = tempfile.TemporaryFile('r+')
        tmp.write('0.5'+delimiter+'0.7')
        tmp.seek(0)
        nose.tools.assert_dict_equal(sed_eval.io.load_event_list(tmp)[0], {'event_offset': 0.7,
                                                                           'event_onset': 0.5})

        tmp = tempfile.TemporaryFile('r+')
        tmp.write('0.5'+delimiter+'0.7'+delimiter+'event')
        tmp.seek(0)
        nose.tools.assert_dict_equal(sed_eval.io.load_event_list(tmp)[0], {'event_label': 'event',
                                                                           'event_offset': 0.7,
                                                                           'event_onset': 0.5})

        tmp = tempfile.TemporaryFile('r+')
        tmp.write('file'+delimiter+'scene'+delimiter+'0.5'+delimiter+'0.7'+delimiter+'event')
        tmp.seek(0)
        nose.tools.assert_dict_equal(sed_eval.io.load_event_list(tmp)[0], {'event_label': 'event',
                                                                           'event_offset': 0.7,
                                                                           'event_onset': 0.5,
                                                                           'file': 'file',
                                                                           'scene_label': 'scene'})

    # Tests for raised errors when invalid delimiter is used
    tmp = tempfile.TemporaryFile('r+')
    tmp.write('10.0-12.0-Test')
    tmp.seek(0)
    nose.tools.assert_raises(ValueError, sed_eval.io.load_event_list, tmp)

    tmp = tempfile.TemporaryFile('r+')
    tmp.write('10.0 12.0 Test')
    tmp.seek(0)
    nose.tools.assert_raises(ValueError, sed_eval.io.load_event_list, tmp)

    # Tests for raised errors when invalid events lists are supplied
    tmp = tempfile.TemporaryFile('r+')
    tmp.write('A\tA\t')
    tmp.seek(0)
    nose.tools.assert_raises(ValueError, sed_eval.io.load_event_list, tmp)

    tmp = tempfile.TemporaryFile('r+')
    tmp.write('a 12.0')
    tmp.seek(0)
    nose.tools.assert_raises(ValueError, sed_eval.io.load_event_list, tmp)

    tmp = tempfile.TemporaryFile('r+')
    tmp.write('10.0\tA\tTest\tTest')
    tmp.seek(0)
    nose.tools.assert_raises(ValueError, sed_eval.io.load_event_list, tmp)

    tmp = tempfile.TemporaryFile('r+')
    tmp.write('10.0\t10.0\tTest\tTest')
    tmp.seek(0)
    nose.tools.assert_raises(ValueError, sed_eval.io.load_event_list, tmp)

    tmp = tempfile.TemporaryFile('r+')
    tmp.write('10.0\t12\tTest\t12\ttest')
    tmp.seek(0)
    nose.tools.assert_raises(ValueError, sed_eval.io.load_event_list, tmp)


def test_load_scene_list():
    delimiters = [',', ';', '\t']
    for delimiter in delimiters:
        # Tests for valid formats
        tmp = tempfile.TemporaryFile('r+')
        tmp.write('file'+delimiter+'scene')
        tmp.seek(0)
        nose.tools.assert_dict_equal(sed_eval.io.load_scene_list(tmp)[0], {'file': 'file',
                                                                            'scene_label': 'scene'})

        tmp = tempfile.TemporaryFile('r+')
        tmp.write('file'+delimiter+'0'+delimiter+'30'+delimiter+'scene')
        tmp.seek(0)
        nose.tools.assert_dict_equal(sed_eval.io.load_scene_list(tmp)[0], {'file': 'file',
                                                                            'segment_start': 0,
                                                                            'segment_end': 30,
                                                                            'scene_label': 'scene'})

    # Tests for raised errors when invalid delimiter is used
    tmp = tempfile.TemporaryFile('r+')
    tmp.write('test_file-test_scene')
    tmp.seek(0)
    nose.tools.assert_raises(ValueError, sed_eval.io.load_scene_list, tmp)

    tmp = tempfile.TemporaryFile('r+')
    tmp.write('test_file test_scene')
    tmp.seek(0)
    nose.tools.assert_raises(ValueError, sed_eval.io.load_scene_list, tmp)

    # Tests for raised errors when invalid scene lists are supplied
    tmp = tempfile.TemporaryFile('r+')
    tmp.write('A\tA\tA\tA\t')
    tmp.seek(0)
    nose.tools.assert_raises(ValueError, sed_eval.io.load_scene_list, tmp)

    tmp = tempfile.TemporaryFile('r+')
    tmp.write('A\tA\tA\t')
    tmp.seek(0)
    nose.tools.assert_raises(ValueError, sed_eval.io.load_scene_list, tmp)


def test_load_file_pair_list():
    delimiters = [',', ';', '\t']
    for delimiter in delimiters:
        # Test for valid formats
        tmp = tempfile.TemporaryFile('r+')
        tmp.write('reference'+delimiter+'estimated')
        tmp.seek(0)
        nose.tools.assert_dict_equal(sed_eval.io.load_file_pair_list(tmp)[0], {'reference_file': 'reference',
                                                                                'estimated_file': 'estimated'})

    # Tests for raised errors when invalid delimiter is used
    tmp = tempfile.TemporaryFile('r+')
    tmp.write('test_file1-test_file2')
    tmp.seek(0)
    nose.tools.assert_raises(ValueError, sed_eval.io.load_file_pair_list, tmp)

    tmp = tempfile.TemporaryFile('r+')
    tmp.write('test_file1 test_file2')
    tmp.seek(0)
    nose.tools.assert_raises(ValueError, sed_eval.io.load_file_pair_list, tmp)

    # Test for raised errors when invalid scene lists are supplied
    tmp = tempfile.TemporaryFile('r+')
    tmp.write('A\tA\tA\tA\t')
    tmp.seek(0)
    nose.tools.assert_raises(ValueError, sed_eval.io.load_file_pair_list, tmp)

