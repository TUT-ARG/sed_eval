#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# DCASE 2016::Sound Event Detection in Real-life Audio / Baseline System

from src.ui import *
from src.general import *
from src.files import *

from src.features import *
from src.sound_event_detection import *
from src.dataset import *
from src.evaluation import *

import numpy
import csv
import warnings
import argparse
import textwrap
import math

from sklearn import mixture

__version_info__ = ('1', '0', '1')
__version__ = '.'.join(__version_info__)


def main(argv):
    numpy.random.seed(123456)  # let's make randomization predictable

    parser = argparse.ArgumentParser(
        prefix_chars='-+',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            DCASE 2016
            Task 3: Sound Event Detection in Real-life Audio 
            Baseline System
            ---------------------------------------------
                Tampere University of Technology / Audio Research Group
                Author:  Toni Heittola ( toni.heittola@tut.fi )

            System description
                This is an baseline implementation for the D-CASE 2016, task 3 - Sound event detection in real life audio.
                The system has binary classifier for each included sound event class. The GMM classifier is trained with
                the positive and negative examples from the mixture signals, and classification is done between these
                two models as likelihood ratio. Acoustic features are MFCC+Delta+Acceleration (MFCC0 omitted).

        '''))

    parser.add_argument("-development", help="Use the system in the development mode", action='store_true',
                        default=False, dest='development')
    parser.add_argument("-challenge", help="Use the system in the challenge mode", action='store_true',
                        default=False, dest='challenge')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    args = parser.parse_args()

    # Load parameters from config file
    params = load_parameters('task3_sound_event_detection_in_real_life_audio.yaml')
    params = process_parameters(params)

    title("DCASE 2016::Sound Event Detection in Real-life Audio / Baseline System")

    # Check if mode is defined
    if not (args.development or args.challenge):
        args.development = True
        args.challenge = False

    dataset_evaluation_mode = 'folds'
    if args.development and not args.challenge:
        print "Running system in development mode"
        dataset_evaluation_mode = 'folds'
    elif not args.development and args.challenge:
        print "Running system in challenge mode"
        dataset_evaluation_mode = 'full'

    # Get dataset container class
    dataset = eval(params['general']['development_dataset'])(data_path=params['path']['data'])

    # Fetch data over internet and setup the data
    # ==================================================
    if params['flow']['initialize']:
        dataset.fetch()

    # Extract features for all audio files in the dataset
    # ==================================================
    if params['flow']['extract_features']:
        section_header('Feature extraction [Development data]')

        # Collect files from evaluation sets
        files = []
        for fold in dataset.folds(mode=dataset_evaluation_mode):
            for item_id, item in enumerate(dataset.train(fold)):
                if item['file'] not in files:
                    files.append(item['file'])
            for item_id, item in enumerate(dataset.test(fold)):
                if item['file'] not in files:
                    files.append(item['file'])

        # Go through files and make sure all features are extracted
        do_feature_extraction(files=files,
                              dataset=dataset,
                              feature_path=params['path']['features'],
                              params=params['features'],
                              overwrite=params['general']['overwrite'])

        foot()

    # Prepare feature normalizers
    # ==================================================
    if params['flow']['feature_normalizer']:
        section_header('Feature normalizer [Development data]')

        do_feature_normalization(dataset=dataset,
                                 feature_normalizer_path=params['path']['feature_normalizers'],
                                 feature_path=params['path']['features'],
                                 dataset_evaluation_mode=dataset_evaluation_mode,
                                 overwrite=params['general']['overwrite'])

        foot()

    # System training
    # ==================================================
    if params['flow']['train_system']:
        section_header('System training    [Development data]')

        do_system_training(dataset=dataset,
                           model_path=params['path']['models'],
                           feature_normalizer_path=params['path']['feature_normalizers'],
                           feature_path=params['path']['features'],
                           hop_length_seconds=params['features']['hop_length_seconds'],
                           classifier_params=params['classifier']['parameters'],
                           dataset_evaluation_mode=dataset_evaluation_mode,
                           classifier_method=params['classifier']['method'],
                           overwrite=params['general']['overwrite']
                           )

        foot()

    # System evaluation in development mode
    if args.development and not args.challenge:

        # System testing
        # ==================================================
        if params['flow']['test_system']:
            section_header('System testing     [Development data]')

            do_system_testing(dataset=dataset,                              
                              result_path=params['path']['results'],
                              feature_path=params['path']['features'],
                              model_path=params['path']['models'],
                              feature_params=params['features'],
                              detector_params=params['detector'],
                              dataset_evaluation_mode=dataset_evaluation_mode,
                              classifier_method=params['classifier']['method'],
                              overwrite=params['general']['overwrite']
                              )
            foot()

        # System evaluation
        # ==================================================
        if params['flow']['evaluate_system']:
            section_header('System evaluation  [Development data]')

            do_system_evaluation(dataset=dataset,
                                 dataset_evaluation_mode=dataset_evaluation_mode,
                                 result_path=params['path']['results'])

            foot()

    # System evaluation with challenge data
    elif not args.development and args.challenge:
        # Fetch data over internet and setup the data
        challenge_dataset = eval(params['general']['challenge_dataset'])()

        if params['flow']['initialize']:
            challenge_dataset.fetch()

        # System testing
        if params['flow']['test_system']:
            section_header('System testing     [Challenge data]')

            do_system_testing(dataset=challenge_dataset,                              
                              result_path=params['path']['challenge_results'],
                              feature_path=params['path']['features'],
                              model_path=params['path']['models'],
                              feature_params=params['features'],
                              detector_params=params['detector'],
                              dataset_evaluation_mode=dataset_evaluation_mode,
                              classifier_method=params['classifier']['method'],
                              overwrite=True
                              )
            foot()

            print " "
            print "Your results for the challenge data are stored at ["+params['path']['challenge_results']+"]"
            print " "


def process_parameters(params):
    """Parameter post-processing.

    Parameters
    ----------
    params : dict
        parameters in dict

    Returns
    -------
    params : dict
        processed parameters

    """

    params['features']['mfcc']['win_length'] = int(params['features']['win_length_seconds'] * params['features']['fs'])
    params['features']['mfcc']['hop_length'] = int(params['features']['hop_length_seconds'] * params['features']['fs'])

    # Copy parameters for current classifier method
    params['classifier']['parameters'] = params['classifier_parameters'][params['classifier']['method']]

    params['features']['hash'] = get_parameter_hash(params['features'])
    params['classifier']['hash'] = get_parameter_hash(params['classifier'])
    params['detector']['hash'] = get_parameter_hash(params['detector'])

    params['path']['features'] = os.path.join(params['path']['base'], params['path']['features'], params['features']['hash'])
    params['path']['feature_normalizers'] = os.path.join(params['path']['base'], params['path']['feature_normalizers'], params['features']['hash'])
    params['path']['models'] = os.path.join(params['path']['base'], params['path']['models'], params['features']['hash'], params['classifier']['hash'])
    params['path']['results'] = os.path.join(params['path']['base'], params['path']['results'], params['features']['hash'], params['classifier']['hash'], params['detector']['hash'])
    return params


def get_feature_filename(audio_file, path, extension='cpickle'):
    """Get feature filename

    Parameters
    ----------
    audio_file : str
        audio file name from which the features are extracted

    path :  str
        feature path

    extension : str
        file extension
        (Default value='cpickle')

    Returns
    -------
    feature_filename : str
        full feature filename

    """

    return os.path.join(path, 'sequence_' + os.path.splitext(audio_file)[0] + '.' + extension)


def get_feature_normalizer_filename(fold, scene_label, path, extension='cpickle'):
    """Get normalizer filename

    Parameters
    ----------
    fold : int >= 0
        evaluation fold number

    scene_label : str
        scene label

    path :  str
        normalizer path

    extension : str
        file extension
        (Default value='cpickle')

    Returns
    -------
    normalizer_filename : str
        full normalizer filename

    """

    return os.path.join(path, 'scale_fold' + str(fold) + '_' + str(scene_label) + '.' + extension)


def get_model_filename(fold, scene_label, path, extension='cpickle'):
    """Get model filename

    Parameters
    ----------
    fold : int >= 0
        evaluation fold number

    scene_label : str
        scene label

    path :  str
        model path

    extension : str
        file extension
        (Default value='cpickle')

    Returns
    -------
    model_filename : str
        full model filename

    """

    return os.path.join(path, 'model_fold' + str(fold) + '_' + str(scene_label) + '.' + extension)


def get_result_filename(fold, scene_label, path, extension='txt'):
    """Get result filename

    Parameters
    ----------
    fold : int >= 0
        evaluation fold number

    scene_label : str
        scene label

    path :  str
        result path

    extension : str
        file extension
        (Default value='cpickle')

    Returns
    -------
    result_filename : str
        full result filename

    """

    if fold == 0:
        return os.path.join(path, 'results_' + str(scene_label) + '.' + extension)
    else:
        return os.path.join(path, 'results_fold' + str(fold) + '_' + str(scene_label) + '.' + extension)


def do_feature_extraction(files, dataset, feature_path, params, overwrite=False):
    """Feature extraction

    Parameters
    ----------
    files : list
        file list

    dataset : class
        dataset class

    feature_path : str
        path where the features are saved

    params : dict
        parameter dict

    overwrite : bool
        overwrite existing feature files
        (Default value=False)

    Returns
    -------
    nothing

    Raises
    -------
    IOError
        Audio file not found.

    """

    # Check that target path exists, create if not
    check_path(feature_path)

    for file_id, audio_filename in enumerate(files):
        # Get feature filename
        current_feature_file = get_feature_filename(audio_file=os.path.split(audio_filename)[1], path=feature_path)

        progress(title_text='Extracting [sequences]',
                 percentage=(float(file_id) / len(files)),
                 note=os.path.split(audio_filename)[1])

        if not os.path.isfile(current_feature_file) or overwrite:
            # Load audio
            if os.path.isfile(dataset.relative_to_absolute_path(audio_filename)):
                y, fs = load_audio(filename=dataset.relative_to_absolute_path(audio_filename), mono=True, fs=params['fs'])
            else:
                raise IOError("Audio file not found [%s]" % audio_filename)

            # Extract features
            feature_data = feature_extraction(y=y,
                                              fs=fs,
                                              include_mfcc0=params['include_mfcc0'],
                                              include_delta=params['include_delta'],
                                              include_acceleration=params['include_acceleration'],
                                              mfcc_params=params['mfcc'],
                                              delta_params=params['mfcc_delta'],
                                              acceleration_params=params['mfcc_acceleration'])
            # Save
            save_data(current_feature_file, feature_data)


def do_feature_normalization(dataset, feature_normalizer_path, feature_path, dataset_evaluation_mode='folds', overwrite=False):
    """Feature normalization

    Calculated normalization factors for each evaluation fold based on the training material available.

    Parameters
    ----------
    dataset : class
        dataset class

    feature_normalizer_path : str
        path where the feature normalizers are saved.

    feature_path : str
        path where the features are saved.

    dataset_evaluation_mode : str ['folds', 'full']
        evaluation mode, 'full' all material available is considered to belong to one fold.
        (Default value='folds')

    overwrite : bool
        overwrite existing normalizers
        (Default value=False)

    Returns
    -------
    nothing

    Raises
    -------
    IOError
        Feature file not found.

    """

    # Check that target path exists, create if not
    check_path(feature_normalizer_path)

    for fold in dataset.folds(mode=dataset_evaluation_mode):
        for scene_id, scene_label in enumerate(dataset.scene_labels):
            current_normalizer_file = get_feature_normalizer_filename(fold=fold, scene_label=scene_label, path=feature_normalizer_path)
            
            if not os.path.isfile(current_normalizer_file) or overwrite:
                # Collect sequence files from scene class
                files = []                
                for item_id, item in enumerate(dataset.train(fold, scene_label=scene_label)):
                    if item['file'] not in files:
                        files.append(item['file'])

                file_count = len(files)

                # Initialize statistics
                normalizer = FeatureNormalizer()

                for file_id, audio_filename in enumerate(files):
                    progress(title_text='Collecting data',
                             fold=fold,
                             percentage=(float(file_id) / file_count),
                             note=os.path.split(audio_filename)[1])

                    # Load features
                    feature_filename = get_feature_filename(audio_file=os.path.split(audio_filename)[1], path=feature_path)
                    if os.path.isfile(feature_filename):
                        feature_data = load_data(feature_filename)['stat']
                    else:
                        raise IOError("Feature file not found [%s]" % audio_filename)

                    # Accumulate statistics
                    normalizer.accumulate(feature_data)

                # Calculate normalization factors
                normalizer.finalize()

                # Save
                save_data(current_normalizer_file, normalizer)


def do_system_training(dataset, model_path, feature_normalizer_path, feature_path, hop_length_seconds, classifier_params,
                       dataset_evaluation_mode='folds', classifier_method='gmm', overwrite=False):
    """System training

    Train a model pair for each sound event class, one for activity and one for inactivity.

    model container format:

    {
        'normalizer': normalizer class
        'models' :
            {
                'mouse click' :
                    {
                        'positive': mixture.GMM class,
                        'negative': mixture.GMM class
                    }
                'keyboard typing' :
                    {
                        'positive': mixture.GMM class,
                        'negative': mixture.GMM class
                    }
                ...
            }
    }

    Parameters
    ----------
    dataset : class
        dataset class

    model_path : str
        path where the models are saved.

    feature_normalizer_path : str
        path where the feature normalizers are saved.

    feature_path : str
        path where the features are saved.

    hop_length_seconds : float > 0
        feature frame hop length in seconds

    classifier_params : dict
        parameter dict

    dataset_evaluation_mode : str ['folds', 'full']
        evaluation mode, 'full' all material available is considered to belong to one fold.
        (Default value='folds')

    classifier_method : str ['gmm']
        classifier method, currently only GMM supported
        (Default value='gmm')

    overwrite : bool
        overwrite existing models
        (Default value=False)

    Returns
    -------
    nothing

    Raises
    -------
    ValueError
        classifier_method is unknown.

    IOError
        Feature normalizer not found.
        Feature file not found.

    """

    if classifier_method != 'gmm':
        raise ValueError("Unknown classifier method ["+classifier_method+"]")

    # Check that target path exists, create if not
    check_path(model_path)

    for fold in dataset.folds(mode=dataset_evaluation_mode):
        for scene_id, scene_label in enumerate(dataset.scene_labels):
            current_model_file = get_model_filename(fold=fold, scene_label=scene_label, path=model_path)
            if not os.path.isfile(current_model_file) or overwrite:

                # Load normalizer
                feature_normalizer_filename = get_feature_normalizer_filename(fold=fold, scene_label=scene_label, path=feature_normalizer_path)
                if os.path.isfile(feature_normalizer_filename):
                    normalizer = load_data(feature_normalizer_filename)
                else:
                    raise IOError("Feature normalizer not found [%s]" % feature_normalizer_filename)

                # Initialize model container
                model_container = {'normalizer': normalizer, 'models': {}}

                # Restructure training data in to structure[files][events]
                ann = {}
                for item_id, item in enumerate(dataset.train(fold=fold, scene_label=scene_label)):
                    filename = os.path.split(item['file'])[1]
                    if filename not in ann:
                        ann[filename] = {}
                    if item['event_label'] not in ann[filename]:
                        ann[filename][item['event_label']] = []
                    ann[filename][item['event_label']].append((item['event_onset'], item['event_offset']))

                # Collect training examples
                data_positive = {}
                data_negative = {}
                file_count = len(ann)
                for item_id, audio_filename in enumerate(ann):
                    progress(title_text='Collecting data',
                             fold=fold,
                             percentage=(float(item_id) / file_count),
                             note=scene_label+" / "+os.path.split(audio_filename)[1])

                    # Load features
                    feature_filename = get_feature_filename(audio_file=audio_filename, path=feature_path)
                    if os.path.isfile(feature_filename):
                        feature_data = load_data(feature_filename)['feat']
                    else:
                        raise IOError("Feature file not found [%s]" % feature_filename)

                    # Normalize features
                    feature_data = model_container['normalizer'].normalize(feature_data)

                    for event_label in ann[audio_filename]:
                        positive_mask = numpy.zeros((feature_data.shape[0]), dtype=bool)

                        for event in ann[audio_filename][event_label]:
                            start_frame = int(math.floor(event[0] / hop_length_seconds))
                            stop_frame = int(math.ceil(event[1] / hop_length_seconds))

                            if stop_frame > feature_data.shape[0]:
                                stop_frame = feature_data.shape[0]

                            positive_mask[start_frame:stop_frame] = True

                        # Store positive examples
                        if event_label not in data_positive:
                            data_positive[event_label] = feature_data[positive_mask, :]
                        else:
                            data_positive[event_label] = numpy.vstack((data_positive[event_label], feature_data[positive_mask, :]))

                        # Store negative examples
                        if event_label not in data_negative:
                            data_negative[event_label] = feature_data[~positive_mask, :]
                        else:
                            data_negative[event_label] = numpy.vstack((data_negative[event_label], feature_data[~positive_mask, :]))

                # Train models for each class
                for event_label in data_positive:
                    progress(title_text='Train models',
                             fold=fold,
                             note=scene_label+" / "+event_label)
                    if classifier_method == 'gmm':
                        model_container['models'][event_label] = {}
                        model_container['models'][event_label]['positive'] = mixture.GMM(**classifier_params).fit(data_positive[event_label])
                        model_container['models'][event_label]['negative'] = mixture.GMM(**classifier_params).fit(data_negative[event_label])
                    else:
                        raise ValueError("Unknown classifier method ["+classifier_method+"]")

                # Save models
                save_data(current_model_file, model_container)


def do_system_testing(dataset, result_path, feature_path, model_path, feature_params, detector_params,
                      dataset_evaluation_mode='folds', classifier_method='gmm', overwrite=False):
    """System testing.

    If extracted features are not found from disk, they are extracted but not saved.

    Parameters
    ----------
    dataset : class
        dataset class

    result_path : str
        path where the results are saved.

    feature_path : str
        path where the features are saved.

    model_path : str
        path where the models are saved.

    feature_params : dict
        parameter dict

    dataset_evaluation_mode : str ['folds', 'full']
        evaluation mode, 'full' all material available is considered to belong to one fold.
        (Default value='folds')

    classifier_method : str ['gmm']
        classifier method, currently only GMM supported
        (Default value='gmm')

    overwrite : bool
        overwrite existing models
        (Default value=False)

    Returns
    -------
    nothing

    Raises
    -------
    ValueError
        classifier_method is unknown.

    IOError
        Model file not found.
        Audio file not found.

    """

    if classifier_method != 'gmm':
        raise ValueError("Unknown classifier method ["+classifier_method+"]")

    # Check that target path exists, create if not
    check_path(result_path)
    for fold in dataset.folds(mode=dataset_evaluation_mode):
        for scene_id, scene_label in enumerate(dataset.scene_labels):
            current_result_file = get_result_filename(fold=fold, scene_label=scene_label, path=result_path)
            if not os.path.isfile(current_result_file) or overwrite:
                results = []

                # Load class model container
                model_filename = get_model_filename(fold=fold, scene_label=scene_label, path=model_path)
                if os.path.isfile(model_filename):
                    model_container = load_data(model_filename)
                else:
                    raise IOError("Model file not found [%s]" % model_filename)

                file_count = len(dataset.test(fold, scene_label=scene_label))
                for file_id, item in enumerate(dataset.test(fold=fold, scene_label=scene_label)):
                    progress(title_text='Testing',
                             fold=fold,
                             percentage=(float(file_id) / file_count),
                             note=scene_label+" / "+os.path.split(item['file'])[1])

                    # Load features
                    feature_filename = get_feature_filename(audio_file=item['file'], path=feature_path)

                    if os.path.isfile(feature_filename):
                        feature_data = load_data(feature_filename)['feat']
                    else:
                        # Load audio
                        if os.path.isfile(dataset.relative_to_absolute_path(item['file'])):
                            y, fs = load_audio(filename=item['file'], mono=True, fs=feature_params['fs'])
                        else:
                            raise IOError("Audio file not found [%s]" % item['file'])

                        # Extract features
                        feature_data = feature_extraction(y=y,
                                                          fs=fs,
                                                          include_mfcc0=feature_params['include_mfcc0'],
                                                          include_delta=feature_params['include_delta'],
                                                          include_acceleration=feature_params['include_acceleration'],
                                                          mfcc_params=feature_params['mfcc'],
                                                          delta_params=feature_params['mfcc_delta'],
                                                          acceleration_params=feature_params['mfcc_acceleration'],
                                                          statistics=False)['feat']

                    # Normalize features
                    feature_data = model_container['normalizer'].normalize(feature_data)

                    current_results = event_detection(feature_data=feature_data,
                                                      model_container=model_container,
                                                      hop_length_seconds=feature_params['hop_length_seconds'],
                                                      smoothing_window_length_seconds=detector_params['smoothing_window_length'],
                                                      decision_threshold=detector_params['decision_threshold'],
                                                      minimum_event_length=detector_params['minimum_event_length'],
                                                      minimum_event_gap=detector_params['minimum_event_gap'])

                    # Store the result
                    for event in current_results:
                        results.append((dataset.absolute_to_relative(item['file']), event[0], event[1], event[2] ))

                # Save testing results
                with open(current_result_file, 'wt') as f:
                    writer = csv.writer(f, delimiter='\t')
                    for result_item in results:
                        writer.writerow(result_item)


def do_system_evaluation(dataset, result_path, dataset_evaluation_mode='folds'):
    """System evaluation. Testing outputs are collected and evaluated. Evaluation results are printed.

    Parameters
    ----------
    dataset : class
        dataset class

    result_path : str
        path where the results are saved.

    dataset_evaluation_mode : str ['folds', 'full']
        evaluation mode, 'full' all material available is considered to belong to one fold.
        (Default value='folds')

    Returns
    -------
    nothing

    Raises
    -------
    IOError
        Result file not found

    """

    # Set warnings off, sklearn metrics will trigger warning for classes without
    # predicted samples in F1-scoring. This is just to keep printing clean.
    warnings.simplefilter("ignore")

    overall_metrics_per_scene = {}

    for scene_id, scene_label in enumerate(dataset.scene_labels):
        if scene_label not in overall_metrics_per_scene:
            overall_metrics_per_scene[scene_label] = {}

        dcase2016_segment_based_metric = DCASE2016_EventDetection_SegmentBasedMetrics(class_list=dataset.event_labels(scene_label=scene_label))
        dcase2016_event_based_metric = DCASE2016_EventDetection_EventBasedMetrics(class_list=dataset.event_labels(scene_label=scene_label))

        for fold in dataset.folds(mode=dataset_evaluation_mode):
            results = []
            result_filename = get_result_filename(fold=fold, scene_label=scene_label, path=result_path)

            if os.path.isfile(result_filename):
                with open(result_filename, 'rt') as f:
                    for row in csv.reader(f, delimiter='\t'):
                        results.append(row)
            else:
                raise IOError("Result file not found [%s]" % result_filename)

            for file_id, item in enumerate(dataset.test(fold, scene_label=scene_label)):
                current_file_results = []
                for result_line in results:
                    if len(result_line) != 0 and result_line[0] == dataset.absolute_to_relative(item['file']):
                        current_file_results.append(
                            {'file': result_line[0],
                             'event_onset': float(result_line[1]),
                             'event_offset': float(result_line[2]),
                             'event_label': result_line[3].rstrip()
                             }
                        )
                meta = dataset.file_meta(dataset.absolute_to_relative(item['file']))

                dcase2016_segment_based_metric.evaluate(system_output=current_file_results, annotated_ground_truth=meta)
                dcase2016_event_based_metric.evaluate(system_output=current_file_results, annotated_ground_truth=meta)

        overall_metrics_per_scene[scene_label]['segment_based_metrics'] = dcase2016_segment_based_metric.results()
        overall_metrics_per_scene[scene_label]['event_based_metrics'] = dcase2016_event_based_metric.results()

    print "  Evaluation over %d folds" % dataset.fold_count
    print " "
    print "  Results per scene "
    print "  {:18s} | {:5s} |  | {:39s}  ".format('', 'Main', 'Secondary metrics')
    print "  {:18s} | {:5s} |  | {:38s} | {:14s} | {:14s} |  {:14s} ".format('', '', 'Seg/Overall','Seg/Class', 'Event/Overall','Event/Class')
    print "  {:18s} | {:5s} |  | {:6s} : {:5s} : {:5s} : {:5s} : {:5s} | {:6s} : {:5s} | {:6s} : {:5s} | {:6s} : {:5s} |".format('Scene', 'ER', 'F1', 'ER', 'ER/S', 'ER/D', 'ER/I', 'F1', 'ER', 'F1', 'ER', 'F1', 'ER')
    print "  -------------------+-------+  +--------+-------+-------+-------+-------+--------+-------+--------+-------+--------+-------+"
    averages = {
        'segment_based_metrics': {
            'overall': {
                'ER': [],
                'F': [],
            },
            'class_wise_average': {
                'ER': [],
                'F': [],
            }
        },
        'event_based_metrics': {
            'overall': {
                'ER': [],
                'F': [],
            },
            'class_wise_average': {
                'ER': [],
                'F': [],
            }
        },
    }
    for scene_id, scene_label in enumerate(dataset.scene_labels):
        print "  {:18s} | {:5.2f} |  | {:4.1f} % : {:5.2f} : {:5.2f} : {:5.2f} : {:5.2f} | {:4.1f} % : {:5.2f} | {:4.1f} % : {:5.2f} | {:4.1f} % : {:5.2f} |".format(scene_label,
                                        overall_metrics_per_scene[scene_label]['segment_based_metrics']['overall']['ER'],
                                        overall_metrics_per_scene[scene_label]['segment_based_metrics']['overall']['F'] * 100,
                                        overall_metrics_per_scene[scene_label]['segment_based_metrics']['overall']['ER'],
                                        overall_metrics_per_scene[scene_label]['segment_based_metrics']['overall']['S'],
                                        overall_metrics_per_scene[scene_label]['segment_based_metrics']['overall']['D'],
                                        overall_metrics_per_scene[scene_label]['segment_based_metrics']['overall']['I'],
                                        overall_metrics_per_scene[scene_label]['segment_based_metrics']['class_wise_average']['F']*100,
                                        overall_metrics_per_scene[scene_label]['segment_based_metrics']['class_wise_average']['ER'],
                                        overall_metrics_per_scene[scene_label]['event_based_metrics']['overall']['F']*100,
                                        overall_metrics_per_scene[scene_label]['event_based_metrics']['overall']['ER'],
                                        overall_metrics_per_scene[scene_label]['event_based_metrics']['class_wise_average']['F']*100,
                                        overall_metrics_per_scene[scene_label]['event_based_metrics']['class_wise_average']['ER'],
                                                                     )
        averages['segment_based_metrics']['overall']['ER'].append(overall_metrics_per_scene[scene_label]['segment_based_metrics']['overall']['ER'])
        averages['segment_based_metrics']['overall']['F'].append(overall_metrics_per_scene[scene_label]['segment_based_metrics']['overall']['F'])
        averages['segment_based_metrics']['class_wise_average']['ER'].append(overall_metrics_per_scene[scene_label]['segment_based_metrics']['class_wise_average']['ER'])
        averages['segment_based_metrics']['class_wise_average']['F'].append(overall_metrics_per_scene[scene_label]['segment_based_metrics']['class_wise_average']['F'])
        averages['event_based_metrics']['overall']['ER'].append(overall_metrics_per_scene[scene_label]['event_based_metrics']['overall']['ER'])
        averages['event_based_metrics']['overall']['F'].append(overall_metrics_per_scene[scene_label]['event_based_metrics']['overall']['F'])
        averages['event_based_metrics']['class_wise_average']['ER'].append(overall_metrics_per_scene[scene_label]['event_based_metrics']['class_wise_average']['ER'])
        averages['event_based_metrics']['class_wise_average']['F'].append(overall_metrics_per_scene[scene_label]['event_based_metrics']['class_wise_average']['F'])

    print "  -------------------+-------+  +--------+-------+-------+-------+-------+--------+-------+--------+-------+--------+-------+"
    print "  {:18s} | {:5.2f} |  | {:4.1f} % : {:5.2f} : {:21s} | {:4.1f} % : {:5.2f} | {:4.1f} % : {:5.2f} | {:4.1f} % : {:5.2f} |".format('Average',
                                        numpy.mean(averages['segment_based_metrics']['overall']['ER']),
                                        numpy.mean(averages['segment_based_metrics']['overall']['F'])*100,
                                        numpy.mean(averages['segment_based_metrics']['overall']['ER']),
                                        ' ',
                                        numpy.mean(averages['segment_based_metrics']['class_wise_average']['F'])*100,
                                        numpy.mean(averages['segment_based_metrics']['class_wise_average']['ER']),
                                        numpy.mean(averages['event_based_metrics']['overall']['F'])*100,
                                        numpy.mean(averages['event_based_metrics']['overall']['ER']),
                                        numpy.mean(averages['event_based_metrics']['class_wise_average']['F'])*100,
                                        numpy.mean(averages['event_based_metrics']['class_wise_average']['ER']),
                                                    )

    print "  "
    # Restore warnings to default settings
    warnings.simplefilter("default")
    print "  Results per events "

    for scene_id, scene_label in enumerate(dataset.scene_labels):
        print "  "
        print "  "+scene_label.upper()
        print "  {:20s} | {:30s} |  | {:15s} ".format('', 'Segment-based', 'Event-based')
        print "  {:20s} | {:5s} : {:5s} : {:6s} : {:5s} |  | {:5s} : {:5s} : {:6s} : {:5s} |".format('Event', 'Nref', 'Nsys', 'F1', 'ER', 'Nref', 'Nsys', 'F1', 'ER')
        print "  ---------------------+-------+-------+--------+-------+  +-------+-------+--------+-------+"
        seg_Nref = 0
        seg_Nsys = 0

        event_Nref = 0
        event_Nsys = 0
        for event_label in sorted(overall_metrics_per_scene[scene_label]['segment_based_metrics']['class_wise']):
            print "  {:20s} | {:5d} : {:5d} : {:4.1f} % : {:5.2f} |  | {:5d} : {:5d} : {:4.1f} % : {:5.2f} |".format(event_label,
                                                                        int(overall_metrics_per_scene[scene_label]['segment_based_metrics']['class_wise'][event_label]['Nref']),
                                                                        int(overall_metrics_per_scene[scene_label]['segment_based_metrics']['class_wise'][event_label]['Nsys']),
                                                                        overall_metrics_per_scene[scene_label]['segment_based_metrics']['class_wise'][event_label]['F']*100,
                                                                        overall_metrics_per_scene[scene_label]['segment_based_metrics']['class_wise'][event_label]['ER'],
                                                                        int(overall_metrics_per_scene[scene_label]['event_based_metrics']['class_wise'][event_label]['Nref']),
                                                                        int(overall_metrics_per_scene[scene_label]['event_based_metrics']['class_wise'][event_label]['Nsys']),
                                                                        overall_metrics_per_scene[scene_label]['event_based_metrics']['class_wise'][event_label]['F']*100,
                                                                        overall_metrics_per_scene[scene_label]['event_based_metrics']['class_wise'][event_label]['ER'])
            seg_Nref += int(overall_metrics_per_scene[scene_label]['segment_based_metrics']['class_wise'][event_label]['Nref'])
            seg_Nsys += int(overall_metrics_per_scene[scene_label]['segment_based_metrics']['class_wise'][event_label]['Nsys'])

            event_Nref += int(overall_metrics_per_scene[scene_label]['event_based_metrics']['class_wise'][event_label]['Nref'])
            event_Nsys += int(overall_metrics_per_scene[scene_label]['event_based_metrics']['class_wise'][event_label]['Nsys'])
        print "  ---------------------+-------+-------+--------+-------+  +-------+-------+--------+-------+"
        print "  {:20s} | {:5d} : {:5d} : {:14s} |  | {:5d} : {:5d} : {:14s} |".format('Sum',
                                                                        seg_Nref,
                                                                        seg_Nsys,
                                                                        '',
                                                                        event_Nref,
                                                                        event_Nsys,
                                                                        '')
        print "  {:20s} | {:5s}   {:5s} : {:4.1f} % : {:5.2f} |  | {:5s}   {:5s} : {:4.1f} % : {:5.2f} |".format('Average',
                                                                        '', '',
                                                                        overall_metrics_per_scene[scene_label]['segment_based_metrics']['class_wise_average']['F']*100,
                                                                        overall_metrics_per_scene[scene_label]['segment_based_metrics']['class_wise_average']['ER'],
                                                                        '', '',
                                                                        overall_metrics_per_scene[scene_label]['event_based_metrics']['class_wise_average']['F']*100,
                                                                        overall_metrics_per_scene[scene_label]['event_based_metrics']['class_wise_average']['ER'])
        print "  "

if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except (ValueError, IOError) as e:
        sys.exit(e)