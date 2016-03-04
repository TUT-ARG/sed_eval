#!/usr/bin/env python

import sed_eval

file_list = [
    {'reference_file': 'data/scene/fold1_reference.txt', 'estimated_file': 'data/scene/fold1_estimated.txt'},
    {'reference_file': 'data/scene/fold2_reference.txt', 'estimated_file': 'data/scene/fold2_estimated.txt'},
    {'reference_file': 'data/scene/fold3_reference.txt', 'estimated_file': 'data/scene/fold3_estimated.txt'},
    {'reference_file': 'data/scene/fold4_reference.txt', 'estimated_file': 'data/scene/fold4_estimated.txt'},
    {'reference_file': 'data/scene/fold5_reference.txt', 'estimated_file': 'data/scene/fold5_estimated.txt'},
]


data = []
all_data = []
for file_pair in file_list:
    reference_scene_list = sed_eval.io.load_scene_list(file_pair['reference_file'])
    estimated_scene_list = sed_eval.io.load_scene_list(file_pair['estimated_file'])
    data.append({'reference_scene_list': reference_scene_list, 'estimated_scene_list': estimated_scene_list})
    all_data += reference_scene_list

scene_labels = sed_eval.sound_event.util.unique_scene_labels(all_data)
scene_metrics = sed_eval.scene.SceneClassificationMetrics(scene_labels)
for file_pair in data:
    scene_metrics.evaluate(file_pair['reference_scene_list'], file_pair['estimated_scene_list'])

overall_metrics_results = scene_metrics.results_overall_metrics()
print "Accuracy:", overall_metrics_results['accuracy']

print scene_metrics
