""" Unit tests for input/output functions """

import nose.tools
import sed_eval
import tempfile
import os


def test_load_event_list():
    # Tests for valid formats

    delimiters = [',', ';', '\t']
    for delimiter in delimiters:
        tmp = tempfile.NamedTemporaryFile('r+', suffix='.txt', dir='/tmp', delete=False)
        try:
            tmp.write('0.5'+delimiter+'0.7')
            tmp.close()
            data = sed_eval.io.load_event_list(tmp.name)
            nose.tools.eq_(data[0]['onset'], 0.5)
            nose.tools.eq_(data[0]['offset'], 0.7)

        finally:
            os.unlink(tmp.name)

        tmp = tempfile.NamedTemporaryFile('r+', suffix='.txt', dir='/tmp', delete=False)
        try:
            tmp.write('0.5'+delimiter+'0.7'+delimiter+'event')
            tmp.close()
            data = sed_eval.io.load_event_list(tmp.name)
            nose.tools.eq_(data[0]['event_label'], 'event')
            nose.tools.eq_(data[0]['onset'], 0.5)
            nose.tools.eq_(data[0]['offset'], 0.7)

        finally:
            os.unlink(tmp.name)

        tmp = tempfile.NamedTemporaryFile('r+', suffix='.txt', dir='/tmp', delete=False)
        try:
            tmp.write('file.wav'+delimiter+'scene'+delimiter+'0.5'+delimiter+'0.7'+delimiter+'event')
            tmp.close()
            data = sed_eval.io.load_event_list(tmp.name)

            nose.tools.eq_(data[0]['event_label'], 'event')
            nose.tools.eq_(data[0]['onset'], 0.5)
            nose.tools.eq_(data[0]['offset'], 0.7)
            nose.tools.eq_(data[0]['filename'], 'file.wav')
            nose.tools.eq_(data[0]['scene_label'], 'scene')

        finally:
            os.unlink(tmp.name)


def test_load_scene_list():
    delimiters = [',', ';', '\t']
    for delimiter in delimiters:
        # Tests for valid formats
        tmp = tempfile.NamedTemporaryFile('r+', suffix='.txt', dir='/tmp', delete=False)
        try:
            tmp.write('file.wav'+delimiter+'scene')
            tmp.close()
            data = sed_eval.io.load_scene_list(tmp.name)
            nose.tools.eq_(data[0]['filename'], 'file.wav')
            nose.tools.eq_(data[0]['scene_label'], 'scene')

        finally:
            os.unlink(tmp.name)


def test_load_file_pair_list():
    delimiters = [',', ';', '\t']
    for delimiter in delimiters:
        # Test for valid formats
        tmp = tempfile.NamedTemporaryFile('r+', suffix='.txt', dir='/tmp', delete=False)
        try:
            tmp.write('reference'+delimiter+'estimated')
            tmp.close()

            nose.tools.assert_dict_equal(
                sed_eval.io.load_file_pair_list(tmp.name)[0],
                {'reference_file': 'reference',
                 'estimated_file': 'estimated'}
            )
        finally:
            os.unlink(tmp.name)
