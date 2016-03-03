Tutorial
========

.. _sed_eval:

``sed_eval`` -- Evaluation toolbox for Sound Event Detection
------------------------------------------------------------

The structure of the ``sed_eval`` toolbox is as follows:

* For evaluating the **sound event detection system** (SED system later), there are two types of metrics available: segment-based and event-based. For both types, there is a metric class ``SegmentBasedMetrics`` and ``EventBasedMetrics``. A member function ``evaluate()`` is used to go through system output (estimated event list) and ground truth (reference event list) pairs. The ``results()`` function is used to get the metric values in dictionary. There are also functions to return results as a formatted string for convenience (e.g. ``result_report_overall()``), or one can just print class instance.
* For evaluating the **acoustic scene classification system**, there is similar evaluation class, ``SceneClassificationMetrics``, as for SED system evaluation.

``sed_eval`` also includes the following additional submodules:

* ``io`` which contains convenience functions for loading annotations
* ``util`` which includes miscellaneous functions to handle event lists (list of event items), event roll (event activity indicator matrix used in evaluation), and scene list.


.. _evaluators:

Quickstart: Using the evaluators
--------------------------------

The easiest way to evaluate systems with ``sed_eval`` is to use provided evaluators.
Evaluators are Python scripts which can be run from the command prompt and utilize ``sed_eval`` to compute metrics
according to reference and estimated annotations you provide.
To use the evaluators, you must first install ``sed_eval`` and its dependencies (see :ref:`installation`).
The evaluator scripts can be found in the ``sed_eval`` repository in the ``evaluators`` folder:

https://github.com/TUT-ARG/sed_eval/tree/master/evaluators

Currently there are two evaluators available, one for evaluating the sound event detection systems and one for
evaluating acoustic scene classification systems.

Sound event detection
^^^^^^^^^^^^^^^^^^^^^

To get usage help:

``./sound_event_eval.py --help``

Evaluator takes as argument a csv-formatted file-list. The list contains pairs of filenames, one pair per row: first the filename of the reference event list
file and the second the estimated event list file. Format is [reference_file][delimiter][estimated_file], and supported delimiters are ``,``, ``;``, ``tab``.

Example of file-list::

    office_snr0_high_v2.txt	office_snr0_high_v2_detected.txt
    office_snr0_med_v2.txt	office_snr0_med_v2_detected.txt

Event list is csv-formatted text-file. Supported formats for the file are:

- [event onset (float >= 0)][delimiter][event offset (float >= 0)]
- [event onset (float >= 0)][delimiter][event offset (float >= 0)][delimiter][label]
- [filename][delimiter][scene_label][delimiter][event onset (float >= 0)][delimiter][event offset (float >= 0)][delimiter][event label]

Supported delimiters: ``,``, ``;``, ``tab``

Example of event list file::

    21.64715	23.00552	alert
    36.91184	38.27021	alert
    69.72575	71.09029	alert
    63.53990	64.89827	alert
    84.25553	84.83920	alert
    20.92974	21.82661	clearthroat
    28.39992	29.29679	clearthroat
    80.47837	81.95937	clearthroat
    44.48363	45.96463	clearthroat
    78.13073	79.05953	clearthroat
    15.17031	16.27235	cough
    20.54931	21.65135	cough
    27.79964	28.90168	cough
    75.45959	76.32490	cough
    70.81708	71.91912	cough
    21.23203	22.55902	doorslam
    7.546220	9.014880	doorslam
    34.11303	35.04183	doorslam
    45.86001	47.32867	doorslam

To get segment-based and event-based metrics report printed, run:

``./sound_event_eval.py file_list.txt``

To get segment-based and event-based metrics saved in YAML-format, run:

``./sound_event_eval.py file_list.txt -o results.yaml``

Acoustic scene classification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``./scene_eval.py --help``

Evaluator takes as argument a csv-formatted file-list. The list contains pairs of filenames, one pair per row: first the filename of the reference scene list
file and the second the estimated scene list file. Format is [reference_file][delimiter][estimated_file], and supported delimiters are ``,``, ``;``, ``tab``.

Example of file-list::

    fold1_reference.txt	fold1_estimated.txt
    fold2_reference.txt	fold2_estimated.txt
    fold3_reference.txt	fold3_estimated.txt
    fold4_reference.txt	fold4_estimated.txt
    fold5_reference.txt	fold5_estimated.txt


Scene list is csv-formatted text-file. Supported formats for the file are:

- [filename][delimiter][scene label]
- [filename][delimiter][segment start (float >= 0)][delimiter][segment stop (float >= 0)][delimiter][scene label]

Supported delimiters: ``,``, ``;``, ``tab``

Example of scene list file::

    scenes_stereo/supermarket09.wav	supermarket
    scenes_stereo/tubestation10.wav	tubestation
    scenes_stereo/quietstreet08.wav	quietstreet
    scenes_stereo/restaurant05.wav	restaurant
    scenes_stereo/busystreet05.wav	busystreet
    scenes_stereo/openairmarket04.wav	openairmarket
    scenes_stereo/quietstreet01.wav	quietstreet
    scenes_stereo/supermarket05.wav	supermarket
    scenes_stereo/openairmarket01.wav	openairmarket


To get metrics printed, run:

``./scene_eval.py file_list.txt``

To get metrics saved in YAML-format, run:

``./scene_eval.py file_list.txt -o results.yaml``


.. _sed_eval_quickstart:

Quickstart: Using ``sed_eval`` in Python code
---------------------------------------------

After ``sed_eval`` is installed (see :ref:`installation`), it can be imported to your Python code as follows:

``import sed_eval``

Sound event detection
^^^^^^^^^^^^^^^^^^^^^

Usage example to evaluate files:

.. code-block:: python
    :linenos:

    import sed_eval

    file_list = [
        {
         'reference_file': 'office_snr0_high_v2.txt',
         'estimated_file': 'office_snr0_high_out.txt'
        },
        {
         'reference_file': 'office_snr0_low_v2.txt',
         'estimated_file': 'office_snr0_low_out.txt'
        },
        {
         'reference_file': 'office_snr0_med_v2.txt',
         'estimated_file': 'office_snr0_med_out.txt'
        },
        {
         'reference_file': 'office_snr-6_high_v2.txt',
         'estimated_file': 'office_snr-6_high_out.txt'
        }
    ]

    data = []

    # Get used event labels
    all_data = sed_eval.util.event_list.EventList()
    for file_pair in file_list:
        reference_event_list = sed_eval.io.load_event_list(file_pair['reference_file'])
        estimated_event_list = sed_eval.io.load_event_list(file_pair['estimated_file'])
        data.append({'reference_event_list': reference_event_list,
                     'estimated_event_list': estimated_event_list})
        all_data += reference_event_list
    event_labels = all_data.unique_event_labels

    # Start evaluating

    # Create metrics classes, define parameters
    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(event_label_list=event_labels,
                                                                     time_resolution=1)
    event_based_metrics = sed_eval.sound_event.EventBasedMetrics(event_label_list=event_labels,
                                                                 t_collar=0.250)

    # Go through files
    for file_pair in data:
        segment_based_metrics.evaluate(file_pair['reference_event_list'],
                                       file_pair['estimated_event_list'])
        event_based_metrics.evaluate(file_pair['reference_event_list'],
                                     file_pair['estimated_event_list'])

    # Get only certain metrics
    overall_segment_based_metrics = segment_based_metrics.results_overall_metrics()
    print "Accuracy:", overall_segment_based_metrics['accuracy']['accuracy']

    # Or print all metrics as reports
    print segment_based_metrics
    print event_based_metrics

Acoustic scene classification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Usage example to evaluate files:

.. code-block:: python
    :linenos:

    import sed_eval

    file_list = [
        {'reference_file': 'fold1_reference.txt', 'estimated_file': 'fold1_estimated.txt'},
        {'reference_file': 'fold2_reference.txt', 'estimated_file': 'fold2_estimated.txt'},
        {'reference_file': 'fold3_reference.txt', 'estimated_file': 'fold3_estimated.txt'},
        {'reference_file': 'fold4_reference.txt', 'estimated_file': 'fold4_estimated.txt'},
        {'reference_file': 'fold5_reference.txt', 'estimated_file': 'fold5_estimated.txt'},
    ]

    data = []

    # Get used scene labels
    all_data = []
    for file_pair in file_list:
        reference_scene_list = sed_eval.io.load_scene_list(file_pair['reference_file'])
        estimated_scene_list = sed_eval.io.load_scene_list(file_pair['estimated_file'])
        data.append({'reference_scene_list': reference_scene_list,
                     'estimated_scene_list': estimated_scene_list})
        all_data += reference_scene_list

    scene_labels = sed_eval.sound_event.util.unique_scene_labels(all_data)

    # Create metrics class
    scene_metrics = sed_eval.scene.SceneClassificationMetrics(scene_labels)
    for file_pair in data:
        scene_metrics.evaluate(file_pair['reference_scene_list'],
                               file_pair['estimated_scene_list'])

    # Get only certain metrics
    overall_metrics_results = scene_metrics.results_overall_metrics()
    print "Accuracy:", overall_metrics_results['accuracy']

    # Or print all metrics as reports
    print scene_metrics