"""
Unit tests for analysis tools
"""

import nose.tools
import sed_eval
import os

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

def test_mcnemar():
    ref = sed_eval.io.load_scene_list(os.path.join('data','scene','reference.txt'))
    est_a = sed_eval.io.load_scene_list(os.path.join('data', 'scene', 'estimated_a.txt'))
    est_b = sed_eval.io.load_scene_list(os.path.join('data', 'scene', 'estimated_b.txt'))

    y_true = []
    y_pred_a = []
    y_pred_b = []
    for item in ref:
        y_true.append(item['scene_label'])
        y_pred_a.append(est_a[find(est_a, 'file', item['file'])]['scene_label'])
        y_pred_b.append(est_b[find(est_b, 'file', item['file'])]['scene_label'])

    m = sed_eval.test.mcnemar(reference=y_true, estimated_a=y_pred_a, estimated_b=y_pred_b)

    nose.tools.assert_almost_equals(m, 1.33333333)
