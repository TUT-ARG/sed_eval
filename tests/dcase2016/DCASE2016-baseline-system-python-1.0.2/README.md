DCASE2016 Baseline system
=========================
[Audio Research Group / Tampere University of Technology](http://arg.cs.tut.fi/)

*Python implementation*

Systems:
- Task 1 - Acoustic scene classification
- Task 3 - Sound event detection in real life audio

Authors
- Toni Heittola (<toni.heittola@tut.fi>, <http://www.cs.tut.fi/~heittolt/>)
- Annamaria Mesaros (<annamaria.mesaros@tut.fi>, <http://www.cs.tut.fi/~mesaros/>)
- Tuomas Virtanen (<tuomas.virtanen@tut.fi>, <http://www.cs.tut.fi/~tuomasv/>)

Table of Contents
=================
1. [Introduction](#1-introduction)
2. [Installation](#2-installation)
3. [Usage](#3-usage)
4. [System blocks](#4-system-blocks)
5. [System evaluation](#5-system-evaluation)
6. [System parameters](#6-system-parameters)
7. [Changelog](#7-changelog)
8. [License](#8-license)

1. Introduction
===============
This document describes the Python implementation of the baseline systems for the [Detection and Classification of Acoustic Scenes and Events 2016 (DCASE2016) challenge](http://www.cs.tut.fi/sgn/arg/dcase2016/) **[tasks 1](#11-acoustic-scene-classification)** and **[task 3](#12-sound-event-detection)**. The challenge consists of four tasks:

1. [Acoustic scene classification](http://www.cs.tut.fi/sgn/arg/dcase2016/task-acoustic-scene-classification)
2. [Sound event detection in synthetic audio](http://www.cs.tut.fi/sgn/arg/dcase2016/task-sound-event-detection-in-synthetic-audio)
3. [Sound event detection in real life audio](http://www.cs.tut.fi/sgn/arg/dcase2016/task-sound-event-detection-in-real-life-audio)
4. [Domestic audio tagging](http://www.cs.tut.fi/sgn/arg/dcase2016/task-audio-tagging)

The baseline systems for task 1 and 3 shares the same basic approach: [MFCC](https://en.wikipedia.org/wiki/Mel-frequency_cepstrum) based acoustic features and [GMM](https://en.wikipedia.org/wiki/Mixture_model) based classifier. The main motivation to have similar approaches for both tasks was to provide low entry level and allow easy switching between the tasks. 

The dataset handling is hidden behind dataset access class, which should help DCASE challenge participants implementing their own systems.

The [Matlab implementation](https://github.com/TUT-ARG/DCASE2016-baseline-system-matlab) is also available. 

#### 1.1. Acoustic scene classification

The acoustic features include MFCC static coefficients (with 0th coefficient), delta coefficients and acceleration coefficients. The system learns one acoustic model per acoustic scene class, and does the classification with maximum likelihood classification scheme. 

#### 1.2. Sound event detection

The acoustic features include MFCC static coefficients (0th coefficient omitted), delta coefficients and acceleration coefficients. The system has a binary classifier for each sound event class included. For the classifier, two acoustic models are trained from the mixture signals: one with positive examples (target sound event active) and one with negative examples (target sound event non-active). The classification is done between these two models as likelihood ratio. Post-processing is applied to get sound event detection output. 

2. Installation
===============

The systems are developed for [Python 2.7.0](https://www.python.org/). Currently, the baseline system is tested only with Linux operating system. 

Run to ensure that all external modules are installed

    pip install -r requirements.txt

**External modules required**

[*numpy*](http://www.numpy.org/), [*scipy*](http://www.scipy.org/), [*scikit-learn*](http://scikit-learn.org/)
`pip install numpy scipy scikit-learn`

Scikit-learn (version >= 0.16) is required for the machine learning implementations.

[*PyYAML*](http://pyyaml.org/)
`pip install pyyaml`

PyYAML is required for handling the configuration files.

[*librosa*](https://github.com/bmcfee/librosa)
`pip install librosa`

Librosa is required for the feature extraction.

3. Usage
========

For each task there is separate executable (.py file):

1. *task1_scene_classification.py*, Acoustic scene classification
3. *task3_sound_event_detection_in_real_life_audio.py*, Real life audio sound event detection

Each system has two operating modes: **Development mode** and **Challenge mode**. 

All the usage parameters are shown by `python task1_scene_classification.py -h` and `python task3_sound_event_detection_in_real_life_audio.py -h`

The system parameters are defined in `task1_scene_classification.yaml` and `task3_sound_event_detection_in_real_life_audio.yaml`. 

With default parameter settings, the system will download needed dataset from Internet and extract it under directory `data` (storage path is controlled with parameter `path->data`). 

#### Development mode

In this mode, the system is trained and evaluated with the development dataset. This is the default operating mode. 

To run the system in this mode:
`python task1_scene_classification.py` 
or `python task1_scene_classification.py -development`.

#### Challenge mode

In this mode, the system is trained with the provided development dataset and the evaluation dataset is run through the developed system. Output files are generated in correct format for the challenge submission. The system ouput is saved in the path specified with the parameter: `path->challenge_results`.

To run the system in this mode:
`python task1_scene_classification.py -challenge`.


4. System blocks
================

The system implements following blocks:

1. Dataset initialization 
  - Downloads the dataset from the Internet if needed
  - Extracts the dataset package if needed
  - Makes sure that the meta files are appropriately formated

2. Feature extraction (`do_feature_extraction`)
  - Goes through all the training material and extracts the acoustic features
  - Features are stored file-by-file on the local disk (pickle files)

3. Feature normalization (`do_feature_normalization`)
  - Goes through the training material in evaluation folds, and calculates global mean and std of the data.
  - Stores the normalization factors (pickle files)

4. System training (`do_system_training`)
  - Trains the system
  - Stores the trained models and feature normalization factors together on the local disk (pickle files)

5. System testing (`do_system_testing`)
  - Goes through the testing material and does the classification / detection 
  - Stores the results (text files)

6. System evaluation (`do_system_evaluation`)
  - Reads the ground truth and the output of the system and calculates evaluation metrics

5. System evaluation
====================

## Task 1 - Acoustic scene classification

###  Metrics

The scoring of acoustic scene classification will be based on classification accuracy: the number of correctly classified segments among the total number of segments. Each segment is considered an independent test sample. 

### Results

##### TUT Acoustic scenes 2016, development set

[Dataset](https://zenodo.org/record/45739)

*Evaluation setup*

- 4 cross-validation folds, average classification accuracy over folds
- 15 acoustic scene classes
- Classification unit: one file (30 seconds of audio).

*System parameters*

- Frame size: 40 ms (with 50% hop size)
- Number of Gaussians per acoustic scene class model: 16 
- Feature vector: 20 MFCC static coefficients (including 0th) + 20 delta MFCC coefficients + 20 acceleration MFCC coefficients = 60 values

| Scene                | Accuracy     |
|----------------------|--------------|
| Beach                |  90.6 %      |
| Bus                  |  81.4 %      |
| Cafe/restaurant      |  71.0 %      |
| Car                  |  94.1 %      |
| City center          |  76.7 %      |
| Forest path          |  96.4 %      |
| Grocery store        |  87.8 %      |
| Home                 |  79.4 %      |
| Library              |  64.9 %      |
| Metro station        |  80.3 %      |
| Office               |  96.5 %      |
| Park                 |  40.3 %      |
| Residential area     |  42.2 %      |
| Train                |  63.1 %      |
| Tram                 |  63.4 %      |
| **Overall accuracy** |  **75.2 %**  |

##### DCASE 2013 Scene classification, development set

[Dataset](http://c4dm.eecs.qmul.ac.uk/rdr/handle/123456789/29)

*Evaluation setup*

- 5 fold average
- 10 acoustic scene classes
- Classification unit: one file (30 seconds of audio).

*System parameters*

- Frame size: 40 ms (with 50% hop size)
- Number of Gaussians per acoustic scene class model: 16 
- Feature vector: 20 MFCC static coefficients (including 0th) + 20 delta MFCC coefficients + 20 acceleration MFCC coefficients = 60 values

| Scene                | Accuracy     |
|----------------------|--------------|
| Bus                  |  93.3 %      |
| Busy street          |  80.0 %      |
| Office               |  86.7 %      |
| Open air market      |  73.3 %      |
| Park                 |  26.7 %      |
| Quiet street         |  53.3 %      |
| Restaurant           |  40.0 %      |
| Supermarket          |  26.7 %      |
| Tube                 |  66.7 %      |
| Tube station         |  53.3 %      |
| **Overall accuracy** |  **60.0 %**  |


## Task 3 - Real life audio sound event detection

###  Metrics

**Segment-based metrics**

Segment based evaluation is done in a fixed time grid, using segments of one second length to compare the ground truth and the system output. 

- **Total error rate (ER)** is the main metric for this task. Error rate as defined in [Poliner2007](https://www.ee.columbia.edu/~dpwe/pubs/PoliE06-piano.pdf) will be evaluated in one-second segments over the entire test set. 

- **F-score** is calculated over all test data based on the total number of false positive, false negatives and true positives. 

**Event-based metrics**

Event-based evaluation considers true positives, false positives and false negatives with respect to event instances. 

**Definition**: An event in the system output is considered correctly detected if its temporal position is overlapping with the temporal position of an event with the same label in the ground truth. A tolerance is allowed for the onset and offset (200 ms for onset and 200 ms or half length for offset)

- **Error rate** calculated as described in [Poliner2007](https://www.ee.columbia.edu/~dpwe/pubs/PoliE06-piano.pdf) over all test data based on the total number of insertions, deletions and substitutions.

- **F-score** is calculated over all test data based on the total number of false positive, false negatives and true positives.

Detailed description of metrics can be found from [DCASE2016 website](http://www.cs.tut.fi/sgn/arg/dcase2016/sound-event-detection-metrics).

### Results

##### TUT Sound events 2016, development set

[Dataset](https://zenodo.org/record/45759)

*Evaluation setup*

- 4 cross-validation folds

*System parameters*

- Frame size: 40 ms (with 50% hop size)
- Number of Gaussians per sound event model (positive and negative): 16 
- Feature vector: 20 MFCC static coefficients (excluding 0th) + 20 delta MFCC coefficients + 20 acceleration MFCC coefficients = 60 values
- Decision_threshold: 140

*Segment based metrics - overall*

| Scene                 | ER          | ER / S      | ER / D      | ER / I      |  F1         |
|-----------------------|-------------|-------------|-------------|-------------|-------------|
| Home                  | 0.95        | 0.09        | 0.80        | 0.06        | 18.1 %      |
| Residential area      | 0.83        | 0.07        | 0.69        | 0.08        | 35.2 %      |
| **Average**           |  **0.89 **  |             |             |             | **26.6 %**  |

*Segment based metrics - class-wise*

| Scene                 | ER          | F1          | 
|-----------------------|-------------|-------------|
| Home                  | 1.05        | 11.6 %      |
| Residential area      | 1.04        | 20.2 %      | 
| **Average**           |  **1.05 **  | **15.9 %**  |

*Event based metrics - overall*

| Scene                 | ER          | F1          | 
|-----------------------|-------------|-------------|
| Home                  | 1.33        | 2.5 %       |
| Residential area      | 1.98        | 1.6 %       |
| **Average**           |  **1.66 **  | **2.0 %**   |

*Event based metrics - class-wise*

| Scene                 | ER          | F1          | 
|-----------------------|-------------|-------------|
| Home                  | 1.31        | 2.2 %       |
| Residential area      | 1.99        | 0.7 %       |
| **Average**           |  **1.65 **  | **1.4 %**   |


6. System parameters
====================
All the parameters are set in `task1_scene_classification.yaml`, and `task3_sound_event_detection_in_real_life_audio.yaml`.

**Controlling the system flow**

The blocks of the system can be controlled through the configuration file. Usually all of them can be kept on. 
    
    flow:
      initialize: true
      extract_features: true
      feature_normalizer: true
      train_system: true
      test_system: true
      evaluate_system: true

**General parameters**

The selection of used dataset.

    general:
      development_dataset: TUTSoundEvents_2016_DevelopmentSet
      challenge_dataset: TUTSoundEvents_2016_EvaluationSet

      overwrite: false                                          # Overwrite previously stored data 

`development_dataset: TUTSoundEvents_2016_DevelopmentSet`
: The dataset handler class used while running the system in development mode. If one wants to handle a new dataset, inherit a new class from the Dataset class (`src/dataset.py`).

`challenge_dataset: TUTSoundEvents_2016_EvaluationSet`
: The dataset handler class used while running the system in challenge mode. If one wants to handle a new dataset, inherit a new class from the Dataset class (`src/dataset.py`).

Available dataset handler classes:

**DCASE 2016**

- TUTAcousticScenes_2016_DevelopmentSet
- TUTAcousticScenes_2016_EvaluationSet
- TUTSoundEvents_2016_DevelopmentSet
- TUTSoundEvents_2016_EvaluationSet

**DCASE 2013**

- DCASE2013_Scene_DevelopmentSet
- DCASE2013_Scene_EvaluationSet
- DCASE2013_Event_DevelopmentSet
- DCASE2013_Event_EvaluationSet


`overwrite: false`
: Switch to allow the system always to overwrite existing data on disk. 

  
**System paths**

This section contains the storage paths.      
      
    path:
      data: data/

      base: system/baseline_dcase2016_task1/
      features: features/
      feature_normalizers: feature_normalizers/
      models: acoustic_models/
      results: evaluation_results/

      challenge_results: challenge_submission/task_1_acoustic_scene_classification/

These parameters defines the folder-structure to store acoustic features, feature normalization data, acoustic models and evaluation results.      

`data: data/`
: Defines the path where the dataset data is downloaded and stored. Path can be relative or absolute. 

`base: system/baseline_dcase2016_task1/`
: Defines the base path where the system stores the data. Other paths are stored under this path. If specified directory does not exist it is created. Path can be relative or absolute. 

`challenge_results: challenge_submission/task_1_acoustic_scene_classification/`
: Defines where the system output is stored while running the system in challenge mode. 
      
**Feature extraction**

This section contains the feature extraction related parameters. 

    features:
      fs: 44100
      win_length_seconds: 0.04
      hop_length_seconds: 0.02

      include_mfcc0: true           #
      include_delta: true           #
      include_acceleration: true    #

      mfcc:
        window: hamming_asymmetric  # [hann_asymmetric, hamming_asymmetric]
        n_mfcc: 20                  # Number of MFCC coefficients
        n_mels: 40                  # Number of MEL bands used
        n_fft: 2048                 # FFT length
        fmin: 0                     # Minimum frequency when constructing MEL bands
        fmax: 22050                 # Maximum frequency when constructing MEL band
        htk: false                  # Switch for HTK-styled MEL-frequency equation

      mfcc_delta:
        width: 9

      mfcc_acceleration:
        width: 9

`fs: 44100`
: Default sampling frequency. If given dataset does not fulfill this criteria the audio data is resampled.


`win_length_seconds: 0.04`
: Feature extraction frame length in seconds.
    

`hop_length_seconds: 0.02`
: Feature extraction frame hop-length in seconds.


`include_mfcc0: true`
: Switch to include zeroth coefficient of static MFCC in the feature vector


`include_delta: true`
: Switch to include delta coefficients to feature vector. Zeroth MFCC is always included in the delta coefficients. The width of delta-window is set in `mfcc_delta->width: 9` 


`include_acceleration: true`
: Switch to include acceleration (delta-delta) coefficients to feature vector. Zeroth MFCC is always included in the delta coefficients. The width of acceleration-window is set in `mfcc_acceleration->width: 9` 

`mfcc->n_mfcc: 16`
: Number of MFCC coefficients

`mfcc->fmax: 22050`
: Maximum frequency for MEL band. Usually, this is set to a half of the sampling frequency.
        
**Classification**

This section contains the frame classification related parameters. 

    classifier:
      method: gmm                   # The system supports only gmm
      parameters: !!null            # Parameters are copied from classifier_parameters based on defined method

    classifier_parameters:
      gmm:
        n_components: 16            # Number of Gaussian components
        covariance_type: diag       # Diagonal or full covariance matrix
        random_state: 0
        thresh: !!null
        tol: 0.001
        min_covar: 0.001
        n_iter: 40
        n_init: 1
        params: wmc
        init_params: wmc

`classifier_parameters->gmm->n_components: 16`
: Number of Gaussians used in the modeling.

In order to add new classifiers to the system, add parameters under classifier_parameters with new tag. Set `classifier->method` and add appropriate code where `classifier_method` variable is used system block API (look into `do_system_training` and `do_system_testing` methods). In addition to this, one might want to modify filename methods (`get_model_filename` and `get_result_filename`) to allow multiple classifier methods co-exist in the system.

**Detector**

This section contains the sound event detection related parameters.

    detector:
      decision_threshold: 140.0
      smoothing_window_length: 1.0  # seconds
      minimum_event_length: 0.1     # seconds
      minimum_event_gap: 0.1        # seconds

`decision_threshold: 140.0`
: Decision threshold used to do final classification. This can be used to control the sensitivity of the system. With log-likelihoods: `event_activity = (positive - negative) > decision_threshold`


`smoothing_window_length: 1.0`
: Size of sliding accumulation window (in seconds) used before frame-wise classification decision  


`minimum_event_length: 0.1`
: Minimum length (in seconds) of outputted events. Events with shorter length than given are filtered out from the system output.


`minimum_event_gap: 0.1`
: Minimum gap (in seconds) between events from same event class in the output. Consecutive events (event with same event label) having shorter gaps between them than set parameter are merged together.

7. Changelog
============
#### 1.0 / 2016-02-08
* Initial commit

8. License
==========

See file [EULA.pdf](EULA.pdf)
