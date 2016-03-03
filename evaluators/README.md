``sed_eval`` Evaluators
=======================

Evaluators are Python scripts which can be run from the command prompt and utilize ``sed_eval`` to compute metrics
according to reference and estimated annotations you provide.
To use the evaluators, you must first install ``sed_eval`` and its dependencies.

Currently there are two evaluators available, one for evaluating the sound event detection systems and one for
evaluating acoustic scene classification systems.

Sound event detection
---------------------

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
-----------------------------

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