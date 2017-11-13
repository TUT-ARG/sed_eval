"""
Unit tests for analysis tools
"""

import nose.tools
import sed_eval
import os


def test_mcnemar():
    ref = sed_eval.io.load_scene_list(
        os.path.join('data', 'scene', 'reference.txt')
    )
    est_a = sed_eval.io.load_scene_list(
        os.path.join('data', 'scene', 'estimated_a.txt')
    )
    est_b = sed_eval.io.load_scene_list(
        os.path.join('data', 'scene', 'estimated_b.txt')
    )

    y_true = []
    y_pred_a = []
    y_pred_b = []
    for item in ref:
        y_true.append(item['scene_label'])
        for est_a_item in est_a.filter(filename=item['filename']):
            y_pred_a.append(est_a_item['scene_label'])

        for est_b_item in est_b.filter(filename=item['filename']):
            y_pred_b.append(est_b_item['scene_label'])

    m = sed_eval.test.mcnemar(reference=y_true, estimated_a=y_pred_a, estimated_b=y_pred_b)

    nose.tools.assert_almost_equals(m, 1.33333333)
