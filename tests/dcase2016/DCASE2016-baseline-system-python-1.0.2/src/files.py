#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import wave
import numpy
import csv
import cPickle as pickle
import librosa
import yaml


def load_audio(filename, mono=True, fs=44100):
    """Load audio file into numpy array

    Supports 24-bit wav-format, and flac audio through librosa.

    Parameters
    ----------
    filename:  str
        Path to audio file

    mono : bool
        In case of multi-channel audio, channels are averaged into single channel.
        (Default value=True)

    fs : int > 0 [scalar]
        Target sample rate, if input audio does not fulfil this, audio is resampled.
        (Default value=44100)

    Returns
    -------
    audio_data : numpy.ndarray [shape=(signal_length, channel)]
        Audio

    sample_rate : integer
        Sample rate

    """

    file_base, file_extension = os.path.splitext(filename)
    if file_extension == '.wav':
        audio_file = wave.open(filename)

        # Audio info
        sample_rate = audio_file.getframerate()
        sample_width = audio_file.getsampwidth()
        number_of_channels = audio_file.getnchannels()
        number_of_frames = audio_file.getnframes()

        # Read raw bytes
        data = audio_file.readframes(number_of_frames)
        audio_file.close()

        # Convert bytes based on sample_width
        num_samples, remainder = divmod(len(data), sample_width * number_of_channels)
        if remainder > 0:
            raise ValueError('The length of data is not a multiple of sample size * number of channels.')
        if sample_width > 4:
            raise ValueError('Sample size cannot be bigger than 4 bytes.')

        if sample_width == 3:
            # 24 bit audio
            a = numpy.empty((num_samples, number_of_channels, 4), dtype=numpy.uint8)
            raw_bytes = numpy.fromstring(data, dtype=numpy.uint8)
            a[:, :, :sample_width] = raw_bytes.reshape(-1, number_of_channels, sample_width)
            a[:, :, sample_width:] = (a[:, :, sample_width - 1:sample_width] >> 7) * 255
            audio_data = a.view('<i4').reshape(a.shape[:-1]).T
        else:
            # 8 bit samples are stored as unsigned ints; others as signed ints.
            dt_char = 'u' if sample_width == 1 else 'i'
            a = numpy.fromstring(data, dtype='<%s%d' % (dt_char, sample_width))
            audio_data = a.reshape(-1, number_of_channels).T

        if mono:
            # Down-mix audio
            audio_data = numpy.mean(audio_data, axis=0)

        # Convert int values into float
        audio_data = audio_data / float(2 ** (sample_width * 8 - 1) + 1)

        # Resample
        if fs != sample_rate:
            audio_data = librosa.core.resample(audio_data, sample_rate, fs)
            sample_rate = fs

        return audio_data, sample_rate

    elif file_extension == '.flac':
        audio_data, sample_rate = librosa.load(filename, sr=fs, mono=mono)

        return audio_data, sample_rate

    return None, None


def load_event_list(file):
    """Load event list from tab delimited text file (csv-formated)

    Supported input formats:

        - [event_onset (float)][tab][event_offset (float)]
        - [event_onset (float)][tab][event_offset (float)][tab][event_label (string)]
        - [file(string)[tab][scene_label][tab][event_onset (float)][tab][event_offset (float)][tab][event_label (string)]

    Event dict format:

        {
            'file': 'filename',
            'scene_label': 'office',
            'event_onset': 0.0,
            'event_offset': 1.0,
            'event_label': 'people_walking',
        }

    Parameters
    ----------
    file : str
        Path to the event list in text format (csv)

    Returns
    -------
    data : list of event dicts
        List containing event dicts

    """
    data = []
    with open(file, 'rt') as f:
        for row in csv.reader(f, delimiter='\t'):
            if len(row) == 2:
                data.append(
                    {
                        'event_onset': float(row[0]),
                        'event_offset': float(row[1])
                    }
                )
            elif len(row) == 3:
                data.append(
                    {
                        'event_onset': float(row[0]),
                        'event_offset': float(row[1]),
                        'event_label': row[2]
                    }
                )
            elif len(row) == 5:
                data.append(
                    {
                        'file': row[0],
                        'scene_label': row[1],
                        'event_onset': float(row[2]),
                        'event_offset': float(row[3]),
                        'event_label': row[4]
                    }
                )
    return data


def save_data(filename, data):
    """Save variable into a pickle file

    Parameters
    ----------
    filename: str
        Path to file

    data: list or dict
        Data to be saved.

    Returns
    -------
    nothing

    """

    pickle.dump(data, open(filename, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)


def load_data(filename):
    """Load data from pickle file

    Parameters
    ----------
    filename: str
        Path to file

    Returns
    -------
    data: list or dict
        Loaded file.

    """

    return pickle.load(open(filename, "rb"))


def load_parameters(filename):
    """Load parameters from YAML-file

    Parameters
    ----------
    filename: str
        Path to file

    Returns
    -------
    parameters: dict
        Dict containing loaded parameters

    Raises
    -------
    IOError
        file is not found.

    """
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            return yaml.load(f)
    else:
        raise IOError("Parameter file not found [%s]" % filename)


def save_text(filename, text):
    """Save text into text file.

    Parameters
    ----------
    filename: str
        Path to file

    text: str
        String to be saved.

    Returns
    -------
    nothing

    """

    with open(filename, "w") as text_file:
        text_file.write(text)


def load_text(filename):
    """Load text file

    Parameters
    ----------
    filename: str
        Path to file

    Returns
    -------
    text: string
        Loaded text.

    """

    with open(filename, 'r') as f:
        return f.readlines()
