#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib2
import socket
import locale
import zipfile
import tarfile
from sklearn.cross_validation import StratifiedShuffleSplit, KFold

from ui import *
from general import *
from files import *


class Dataset(object):
    """Dataset base class.

    The specific dataset classes are inherited from this class, and only needed methods are reimplemented.

    """

    def __init__(self, data_path='data', name='dataset'):
        """__init__ method.

        Parameters
        ----------
        data_path : str
            Basepath where the dataset is stored.
            (Default value='data')

        """

        # Folder name for dataset
        self.name = name

        # Path to the dataset
        self.local_path = os.path.join(data_path, self.name)

        # Create the dataset path if does not exist
        if not os.path.isdir(self.local_path):
            os.makedirs(self.local_path)

        # Evaluation setup folder
        self.evaluation_setup_folder = 'evaluation_setup'

        # Path to the folder containing evaluation setup files
        self.evaluation_setup_path = os.path.join(self.local_path, self.evaluation_setup_folder)

        # Meta data file, csv-format
        self.meta_filename = 'meta.txt'

        # Path to meta data file
        self.meta_file = os.path.join(self.local_path, self.meta_filename)

        # Hash file to detect removed or added files
        self.filelisthash_filename = 'filelist.hash'

        # Number of evaluation folds
        self.evaluation_folds = 1

        # List containing dataset package items
        # Define this in the inherited class.
        # Format:
        # {
        #        'remote_package': download_url,
        #        'local_package': os.path.join(self.local_path, 'name_of_downloaded_package'),
        #        'local_audio_path': os.path.join(self.local_path, 'name_of_folder_containing_audio_files'),
        # }
        self.package_list = []

        # List of audio files
        self.files = None

        # List of meta data dict
        self.meta_data = None

        # Training meta data for folds
        self.evaluation_data_train = {}

        # Testing meta data for folds
        self.evaluation_data_test = {}

        # Recognized audio extensions
        self.audio_extensions = {'wav', 'flac'}

        # Info fields for dataset
        self.authors = ''
        self.name_remote = ''
        self.url = ''
        self.audio_source = ''
        self.audio_type = ''
        self.recording_device_model = ''
        self.microphone_model = ''

    @property
    def audio_files(self):
        """Get all audio files in the dataset

        Parameters
        ----------
        Nothing

        Returns
        -------
        filelist : list
            File list with absolute paths

        """

        if self.files is None:
            self.files = []
            for item in self.package_list:
                path = item['local_audio_path']
                if path:
                    l = os.listdir(path)
                    for f in l:
                        file_name, file_extension = os.path.splitext(f)
                        if file_extension[1:] in self.audio_extensions:
                            self.files.append(os.path.abspath(os.path.join(path, f)))
            self.files.sort()
        return self.files

    @property
    def audio_file_count(self):
        """Get number of audio files in dataset

        Parameters
        ----------
        Nothing

        Returns
        -------
        filecount : int
            Number of audio files

        """

        return len(self.audio_files)

    @property
    def meta(self):
        """Get meta data for dataset. If not already read from disk, data is read and returned.

        Parameters
        ----------
        Nothing

        Returns
        -------
        meta_data : list
            List containing meta data as dict.

        Raises
        -------
        IOError
            meta file not found.

        """

        if self.meta_data is None:
            self.meta_data = []
            meta_id = 0
            if os.path.isfile(self.meta_file):
                f = open(self.meta_file, 'rt')
                try:
                    reader = csv.reader(f, delimiter='\t')
                    for row in reader:
                        if len(row) == 2:
                            # Scene meta
                            self.meta_data.append({'file': row[0], 'scene_label': row[1].rstrip()})
                        elif len(row) == 4:
                            # Audio tagging meta
                            self.meta_data.append(
                                {'file': row[0], 'scene_label': row[1].rstrip(), 'tag_string': row[2].rstrip(),
                                 'tags': row[3].split(';')})
                        elif len(row) == 6:
                            # Event meta
                            self.meta_data.append({'file': row[0],
                                                   'scene_label': row[1].rstrip(),
                                                   'event_onset': float(row[2]),
                                                   'event_offset': float(row[3]),
                                                   'event_label': row[4].rstrip(),
                                                   'event_type': row[5].rstrip(),
                                                   'id': meta_id
                                                   })
                        meta_id += 1
                finally:
                    f.close()
            else:
                raise IOError("Meta file not found [%s]" % self.meta_file)

        return self.meta_data

    @property
    def meta_count(self):
        """Number of meta data items.

        Parameters
        ----------
        Nothing

        Returns
        -------
        meta_item_count : int
            Meta data item count

        """

        return len(self.meta)

    @property
    def fold_count(self):
        """Number of fold in the evaluation setup.

        Parameters
        ----------
        Nothing

        Returns
        -------
        fold_count : int
            Number of folds

        """

        return self.evaluation_folds

    @property
    def scene_labels(self):
        """List of unique scene labels in the meta data.

        Parameters
        ----------
        Nothing

        Returns
        -------
        labels : list
            List of scene labels in alphabetical order.

        """

        labels = []
        for item in self.meta:
            if 'scene_label' in item and item['scene_label'] not in labels:
                labels.append(item['scene_label'])
        labels.sort()
        return labels

    @property
    def scene_label_count(self):
        """Number of unique scene labels in the meta data.

        Parameters
        ----------
        Nothing

        Returns
        -------
        scene_label_count : int
            Number of unique scene labels.

        """

        return len(self.scene_labels)

    @property
    def event_labels(self):
        """List of unique event labels in the meta data.

        Parameters
        ----------
        Nothing

        Returns
        -------
        labels : list
            List of event labels in alphabetical order.

        """

        labels = []
        for item in self.meta:
            if 'event_label' in item and item['event_label'].rstrip() not in labels:
                labels.append(item['event_label'].rstrip())
        labels.sort()
        return labels

    @property
    def event_label_count(self):
        """Number of unique event labels in the meta data.

        Parameters
        ----------
        Nothing

        Returns
        -------
        event_label_count : int
            Number of unique event labels

        """

        return len(self.event_labels)

    @property
    def audio_tags(self):
        """List of unique audio tags in the meta data.

        Parameters
        ----------
        Nothing

        Returns
        -------
        labels : list
            List of audio tags in alphabetical order.

        """

        tags = []
        for item in self.meta:
            if 'tags' in item:
                for tag in item['tags']:
                    if tag and tag not in tags:
                        tags.append(tag)
        tags.sort()
        return tags

    @property
    def audio_tag_count(self):
        """Number of unique audio tags in the meta data.

        Parameters
        ----------
        Nothing

        Returns
        -------
        audio_tag_count : int
            Number of unique audio tags

        """

        return len(self.audio_tags)

    def __getitem__(self, i):
        """Getting meta data item

        Parameters
        ----------
        i : int
            item id

        Returns
        -------
        meta_data : dict
            Meta data item
        """
        if i < len(self.meta):
            return self.meta[i]
        else:
            return None

    def __iter__(self):
        """Iterator for meta data items

        Parameters
        ----------
        Nothing

        Returns
        -------
        Nothing

        """

        i = 0
        meta = self[i]

        # yield window while it's valid
        while meta is not None:
            yield meta
            # get next item
            i += 1
            meta = self[i]

    @staticmethod
    def print_bytes(num_bytes):
        """Output number of bytes according to locale and with IEC binary prefixes

        Parameters
        ----------
        num_bytes : int > 0 [scalar]
            Bytes

        Returns
        -------
        bytes : str
            Human readable string
        """

        KiB = 1024
        MiB = KiB * KiB
        GiB = KiB * MiB
        TiB = KiB * GiB
        PiB = KiB * TiB
        EiB = KiB * PiB
        ZiB = KiB * EiB
        YiB = KiB * ZiB
        locale.setlocale(locale.LC_ALL, '')
        output = locale.format("%d", num_bytes, grouping=True) + ' bytes'
        if num_bytes > YiB:
            output += ' (%.4g YiB)' % (num_bytes / YiB)
        elif num_bytes > ZiB:
            output += ' (%.4g ZiB)' % (num_bytes / ZiB)
        elif num_bytes > EiB:
            output += ' (%.4g EiB)' % (num_bytes / EiB)
        elif num_bytes > PiB:
            output += ' (%.4g PiB)' % (num_bytes / PiB)
        elif num_bytes > TiB:
            output += ' (%.4g TiB)' % (num_bytes / TiB)
        elif num_bytes > GiB:
            output += ' (%.4g GiB)' % (num_bytes / GiB)
        elif num_bytes > MiB:
            output += ' (%.4g MiB)' % (num_bytes / MiB)
        elif num_bytes > KiB:
            output += ' (%.4g KiB)' % (num_bytes / KiB)
        return output

    def download(self):
        """Download dataset over the internet to the local path

        Parameters
        ----------
        Nothing

        Returns
        -------
        Nothing

        Raises
        -------
        IOError
            Download failed.

        """

        section_header('Download dataset')
        for item in self.package_list:
            try:
                if item['remote_package'] and not os.path.isfile(item['local_package']):
                    data = None
                    req = urllib2.Request(item['remote_package'], data, {})
                    handle = urllib2.urlopen(req)

                    if "Content-Length" in handle.headers.items():
                        size = int(handle.info()["Content-Length"])
                    else:
                        size = None
                    actualSize = 0
                    blocksize = 64 * 1024
                    tmp_file = os.path.join(self.local_path, 'tmp_file')
                    fo = open(tmp_file, "wb")
                    terminate = False
                    while not terminate:
                        block = handle.read(blocksize)
                        actualSize += len(block)
                        if size:
                            progress(title_text=os.path.split(item['local_package'])[1],
                                     percentage=actualSize / float(size),
                                     note=self.print_bytes(actualSize))
                        else:
                            progress(title_text=os.path.split(item['local_package'])[1],
                                     note=self.print_bytes(actualSize))

                        if len(block) == 0:
                            break
                        fo.write(block)
                    fo.close()
                    os.rename(tmp_file, item['local_package'])

            except (urllib2.URLError, socket.timeout), e:
                try:
                    fo.close()
                except:
                    raise IOError('Download failed [%s]' % (item['remote_package']))
        foot()

    def extract(self):
        """Extract the dataset packages

        Parameters
        ----------
        Nothing

        Returns
        -------
        Nothing

        """

        section_header('Extract dataset')
        for item_id, item in enumerate(self.package_list):
            if item['local_package']:
                if item['local_package'].endswith('.zip'):

                    with zipfile.ZipFile(item['local_package'], "r") as z:
                        # Trick to omit first level folder
                        parts = []
                        for name in z.namelist():
                            if not name.endswith('/'):
                                parts.append(name.split('/')[:-1])
                        prefix = os.path.commonprefix(parts) or ''

                        if prefix:
                            if len(prefix) > 1:
                                prefix_ = list()
                                prefix_.append(prefix[0])
                                prefix = prefix_

                            prefix = '/'.join(prefix) + '/'
                        offset = len(prefix)

                        # Start extraction
                        members = z.infolist()
                        file_count = 1
                        for i, member in enumerate(members):
                            if len(member.filename) > offset:
                                member.filename = member.filename[offset:]

                                if not os.path.isfile(os.path.join(self.local_path, member.filename)):
                                    z.extract(member, self.local_path)

                                progress(title_text='Extracting ['+str(item_id)+'/'+str(len(self.package_list))+']', percentage=(file_count / float(len(members))),
                                         note=member.filename)
                                file_count += 1

                elif item['local_package'].endswith('.tar.gz'):
                    tar = tarfile.open(item['local_package'], "r:gz")
                    for i, tar_info in enumerate(tar):
                        if not os.path.isfile(os.path.join(self.local_path, tar_info.name)):
                            tar.extract(tar_info, self.local_path)
                        progress(title_text='Extracting ['+str(item_id)+'/'+str(len(self.package_list))+']', note=tar_info.name)
                        tar.members = []
                    tar.close()
        foot()

    def on_after_extract(self):
        """Dataset meta data preparation, this will be overloaded in dataset specific classes

        Parameters
        ----------
            Nothing

        Returns
        -------
            Nothing
        """

        pass

    def get_filelist(self):
        """List of files under local_path

        Parameters
        ----------
        Nothing

        Returns
        -------
        filelist: list
            File list
        """

        filelist = []
        for path, subdirs, files in os.walk(self.local_path):
            for name in files:
                filelist.append(os.path.join(path, name))
        return filelist

    def check_filelist(self):
        """Generates hash from file list and check does it matches with one saved in filelist.hash.
        If some files have been deleted or added, checking will result False.

        Parameters
        ----------
        Nothing

        Returns
        -------
        result: bool
            Result
        """

        if os.path.isfile(os.path.join(self.local_path, self.filelisthash_filename)):
            hash = load_text(os.path.join(self.local_path, self.filelisthash_filename))[0]
            if hash != get_parameter_hash(sorted(self.get_filelist())):
                return False
            else:
                return True
        else:
            return False

    def save_filelist_hash(self):
        """Generates file list hash, and saves it as filelist.hash under local_path.

        Parameters
        ----------
        Nothing

        Returns
        -------
        Nothing

        """

        filelist = self.get_filelist()

        filelist_hash_not_found = True
        for file in filelist:
            if self.filelisthash_filename in file:
                filelist_hash_not_found = False

        if filelist_hash_not_found:
            filelist.append(os.path.join(self.local_path, self.filelisthash_filename))

        save_text(os.path.join(self.local_path, self.filelisthash_filename), get_parameter_hash(sorted(filelist)))

    def fetch(self):
        """Download, extract and prepare the dataset.

        Parameters
        ----------
        Nothing

        Returns
        -------
        Nothing

        """

        if not self.check_filelist():
            self.download()
            self.extract()
            self.on_after_extract()
            self.save_filelist_hash()

        return self

    def train(self, fold=0):
        """List of training items.

        Parameters
        ----------
        fold : int > 0 [scalar]
            Fold id, if zero all meta data is returned.
            (Default value=0)

        Returns
        -------
        list : list of dicts
            List containing all meta data assigned to training set for given fold.

        """

        if fold not in self.evaluation_data_train:
            self.evaluation_data_train[fold] = []
            if fold > 0:
                with open(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_train.txt'), 'rt') as f:
                    for row in csv.reader(f, delimiter='\t'):
                        if len(row) == 2:
                            # Scene meta
                            self.evaluation_data_train[fold].append({
                                'file': self.relative_to_absolute_path(row[0]),
                                'scene_label': row[1]
                            })
                        elif len(row) == 4:
                            # Audio tagging meta
                            self.evaluation_data_train[fold].append({
                                'file': self.relative_to_absolute_path(row[0]),
                                'scene_label': row[1],
                                'tag_string': row[2],
                                'tags': row[3].split(';')
                            })
                        elif len(row) == 5:
                            # Event meta
                            self.evaluation_data_train[fold].append({
                                'file': self.relative_to_absolute_path(row[0]),
                                'scene_label': row[1],
                                'event_onset': float(row[2]),
                                'event_offset': float(row[3]),
                                'event_label': row[4]
                            })
            else:
                data = []
                for item in self.meta:
                    if 'event_label' in item:
                        data.append({'file': self.relative_to_absolute_path(item['file']),
                                     'scene_label': item['scene_label'],
                                     'event_onset': item['event_onset'],
                                     'event_offset': item['event_offset'],
                                     'event_label': item['event_label'],
                                     })
                    else:
                        data.append({'file': self.relative_to_absolute_path(item['file']),
                                     'scene_label': item['scene_label']
                                     })
                self.evaluation_data_train[0] = data

        return self.evaluation_data_train[fold]

    def test(self, fold=0):
        """List of testing items.

        Parameters
        ----------
        fold : int > 0 [scalar]
            Fold id, if zero all meta data is returned.
            (Default value=0)

        Returns
        -------
        list : list of dicts
            List containing all meta data assigned to testing set for given fold.

        """

        if fold not in self.evaluation_data_test:
            self.evaluation_data_test[fold] = []
            if fold > 0:
                with open(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_test.txt'), 'rt') as f:
                    for row in csv.reader(f, delimiter='\t'):
                        self.evaluation_data_test[fold].append({'file': self.relative_to_absolute_path(row[0])})
            else:
                data = []
                files = []
                for item in self.meta:
                    if self.relative_to_absolute_path(item['file']) not in files:
                        data.append({'file': self.relative_to_absolute_path(item['file'])})
                        files.append(self.relative_to_absolute_path(item['file']))

                self.evaluation_data_test[fold] = data

        return self.evaluation_data_test[fold]

    def folds(self, mode='folds'):
        """List of fold ids

        Parameters
        ----------
        mode : str {'folds','full'}
            Fold setup type, possible values are 'folds' and 'full'. In 'full' mode fold number is set 0 and all data is used for training.
            (Default value=folds)

        Returns
        -------
        list : list of integers
            Fold ids

        """

        if mode == 'folds':
            return range(1, self.evaluation_folds + 1)
        elif mode == 'full':
            return [0]

    def file_meta(self, file):
        """Meta data for given file

        Parameters
        ----------
        file : str
            File name

        Returns
        -------
        list : list of dicts
            List containing all meta data related to given file.

        """

        file = self.absolute_to_relative(file)
        file_meta = []
        for item in self.meta:
            if item['file'] == file:
                file_meta.append(item)

        return file_meta

    def relative_to_absolute_path(self, path):
        """Converts relative path into absolute path.

        Parameters
        ----------
        path : str
            Relative path

        Returns
        -------
        path : str
            Absolute path

        """

        return os.path.abspath(os.path.join(self.local_path, path))

    def absolute_to_relative(self, path):
        """Converts absolute path into relative path.

        Parameters
        ----------
        path : str
            Absolute path

        Returns
        -------
        path : str
            Relative path

        """

        if path.startswith(os.path.abspath(self.local_path)):
            return os.path.relpath(path, self.local_path)
        else:
            return path


# =====================================================
# DCASE 2016
# =====================================================
class TUTAcousticScenes_2016_DevelopmentSet(Dataset):
    """TUT Acoustic scenes 2016 development dataset

    This dataset is used in DCASE2016 - Task 1, Acoustic scene classification

    """

    def __init__(self, data_path='data'):
        Dataset.__init__(self, data_path=data_path, name='TUT-acoustic-scenes-2016-development')

        self.authors = 'Annamaria Mesaros, Toni Heittola, and Tuomas Virtanen'
        self.name_remote = 'TUT Acoustic Scenes 2016, development dataset'
        self.url = 'https://zenodo.org/record/45739'
        self.audio_source = 'Field recording'
        self.audio_type = 'Natural'
        self.recording_device_model = 'Roland Edirol R-09'
        self.microphone_model = 'Soundman OKM II Klassik/studio A3 electret microphone'

        self.evaluation_folds = 4

        self.package_list = [
            {
                'remote_package': None,
                'local_package': None,
                'local_audio_path': os.path.join(self.local_path, 'audio'),
            },
            {
                'remote_package': 'https://zenodo.org/record/45739/files/TUT-acoustic-scenes-2016-development.doc.zip',
                'local_package': os.path.join(self.local_path, 'TUT-acoustic-scenes-2016-development.doc.zip'),
                'local_audio_path': os.path.join(self.local_path, 'audio'),
            },
            {
                'remote_package': 'https://zenodo.org/record/45739/files/TUT-acoustic-scenes-2016-development.meta.zip',
                'local_package': os.path.join(self.local_path, 'TUT-acoustic-scenes-2016-development.meta.zip'),
                'local_audio_path': os.path.join(self.local_path, 'audio'),
            },
            {
                'remote_package': 'https://zenodo.org/record/45739/files/TUT-acoustic-scenes-2016-development.audio.1.zip',
                'local_package': os.path.join(self.local_path, 'TUT-acoustic-scenes-2016-development.audio.1.zip'),
                'local_audio_path': os.path.join(self.local_path, 'audio'),
            },
            {
                'remote_package': 'https://zenodo.org/record/45739/files/TUT-acoustic-scenes-2016-development.audio.2.zip',
                'local_package': os.path.join(self.local_path, 'TUT-acoustic-scenes-2016-development.audio.2.zip'),
                'local_audio_path': os.path.join(self.local_path, 'audio'),
            },
            {
                'remote_package': 'https://zenodo.org/record/45739/files/TUT-acoustic-scenes-2016-development.audio.3.zip',
                'local_package': os.path.join(self.local_path, 'TUT-acoustic-scenes-2016-development.audio.3.zip'),
                'local_audio_path': os.path.join(self.local_path, 'audio'),
            },
            {
                'remote_package': 'https://zenodo.org/record/45739/files/TUT-acoustic-scenes-2016-development.audio.4.zip',
                'local_package': os.path.join(self.local_path, 'TUT-acoustic-scenes-2016-development.audio.4.zip'),
                'local_audio_path': os.path.join(self.local_path, 'audio'),
            },
            {
                'remote_package': 'https://zenodo.org/record/45739/files/TUT-acoustic-scenes-2016-development.audio.5.zip',
                'local_package': os.path.join(self.local_path, 'TUT-acoustic-scenes-2016-development.audio.5.zip'),
                'local_audio_path': os.path.join(self.local_path, 'audio'),
            },
            {
                'remote_package': 'https://zenodo.org/record/45739/files/TUT-acoustic-scenes-2016-development.audio.6.zip',
                'local_package': os.path.join(self.local_path, 'TUT-acoustic-scenes-2016-development.audio.6.zip'),
                'local_audio_path': os.path.join(self.local_path, 'audio'),
            },
            {
                'remote_package': 'https://zenodo.org/record/45739/files/TUT-acoustic-scenes-2016-development.audio.7.zip',
                'local_package': os.path.join(self.local_path, 'TUT-acoustic-scenes-2016-development.audio.7.zip'),
                'local_audio_path': os.path.join(self.local_path, 'audio'),
            },
            {
                'remote_package': 'https://zenodo.org/record/45739/files/TUT-acoustic-scenes-2016-development.audio.8.zip',
                'local_package': os.path.join(self.local_path, 'TUT-acoustic-scenes-2016-development.audio.8.zip'),
                'local_audio_path': os.path.join(self.local_path, 'audio'),
            }
        ]

    def on_after_extract(self):
        """After dataset packages are downloaded and extracted, meta-files are checked.

        Parameters
        ----------
        nothing

        Returns
        -------
        nothing

        """

        if not os.path.isfile(self.meta_file):
            section_header('Generating meta file for dataset')
            meta_data = {}
            for fold in xrange(1, self.evaluation_folds):
                # Read train files in
                train_filename = os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_train.txt')
                f = open(train_filename, 'rt')
                reader = csv.reader(f, delimiter='\t')
                for row in reader:
                    if row[0] not in meta_data:
                        meta_data[row[0]] = row[1]
                                    
                f.close()
                # Read evaluation files in
                eval_filename = os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_evaluate.txt')
                f = open(eval_filename, 'rt')
                reader = csv.reader(f, delimiter='\t')
                for row in reader:
                    if row[0] not in meta_data:
                        meta_data[row[0]] = row[1]
                f.close()

            f = open(self.meta_file, 'wt')
            try:
                writer = csv.writer(f, delimiter='\t')
                for file in meta_data:
                    raw_path, raw_filename = os.path.split(file)
                    relative_path = self.absolute_to_relative(raw_path)
                    label = meta_data[file]
                    writer.writerow((os.path.join(relative_path, raw_filename), label))
            finally:
                f.close()
            foot()


class TUTAcousticScenes_2016_EvaluationSet(Dataset):
    """TUT Acoustic scenes 2016 evaluation dataset

    This dataset is used in DCASE2016 - Task 1, Acoustic scene classification

    """

    def __init__(self, data_path='data'):
        Dataset.__init__(self, data_path=data_path, name='TUT-acoustic-scenes-2016-evaluation')

        self.authors = 'Annamaria Mesaros, Toni Heittola, and Tuomas Virtanen'
        self.name_remote = 'TUT Acoustic Scenes 2016, evaluation dataset'
        self.url = 'http://www.cs.tut.fi/sgn/arg/dcase2016/download/'
        self.audio_source = 'Field recording'
        self.audio_type = 'Natural'
        self.recording_device_model = 'Roland Edirol R-09'
        self.microphone_model = 'Soundman OKM II Klassik/studio A3 electret microphone'

        self.evaluation_folds = 1

        self.package_list = [
            {
                'remote_package': None,
                'local_package': None,
                'local_audio_path': os.path.join(self.local_path, 'audio'),
            },
        ]

    def on_after_extract(self):
        """After dataset packages are downloaded and extracted, meta-files are checked.

        Parameters
        ----------
        nothing

        Returns
        -------
        nothing

        """

        eval_filename = os.path.join(self.evaluation_setup_path, 'evaluate.txt')

        if not os.path.isfile(self.meta_file) and os.path.isfile(eval_filename):
            section_header('Generating meta file for dataset')
            meta_data = {}

            f = open(eval_filename, 'rt')
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if row[0] not in meta_data:
                    meta_data[row[0]] = row[1]

            f.close()

            f = open(self.meta_file, 'wt')
            try:
                writer = csv.writer(f, delimiter='\t')
                for file in meta_data:
                    raw_path, raw_filename = os.path.split(file)
                    relative_path = self.absolute_to_relative(raw_path)
                    label = meta_data[file]
                    writer.writerow((os.path.join(relative_path, raw_filename), label))
            finally:
                f.close()
            foot()

    def train(self, fold=0):
        raise IOError('Train setup not available.')


# TUT Sound events 2016 development and evaluation sets
class TUTSoundEvents_2016_DevelopmentSet(Dataset):
    """TUT Sound events 2016 development dataset

    This dataset is used in DCASE2016 - Task 3, Sound event detection in real life audio

    """
    def __init__(self, data_path='data'):
        Dataset.__init__(self, data_path=data_path, name='TUT-sound-events-2016-development')

        self.authors = 'Annamaria Mesaros, Toni Heittola, and Tuomas Virtanen'
        self.name_remote = 'TUT Sound Events 2016, development dataset'
        self.url = 'https://zenodo.org/record/45759'
        self.audio_source = 'Field recording'
        self.audio_type = 'Natural'
        self.recording_device_model = 'Roland Edirol R-09'
        self.microphone_model = 'Soundman OKM II Klassik/studio A3 electret microphone'

        self.evaluation_folds = 4

        self.package_list = [
            {
                'remote_package': None,
                'local_package': None,
                'local_audio_path': os.path.join(self.local_path, 'audio'),
            },
            {
                'remote_package': None,
                'local_package': None,
                'local_audio_path': os.path.join(self.local_path, 'audio', 'residential_area'),
            },
            {
                'remote_package': None,
                'local_package': None,
                'local_audio_path': os.path.join(self.local_path, 'audio', 'home'),
            },
            {
                'remote_package': 'https://zenodo.org/record/45759/files/TUT-sound-events-2016-development.doc.zip',
                'local_package': os.path.join(self.local_path, 'TUT-sound-events-2016-development.doc.zip'),
                'local_audio_path': os.path.join(self.local_path, 'audio'),
            },
            {
                'remote_package': 'https://zenodo.org/record/45759/files/TUT-sound-events-2016-development.meta.zip',
                'local_package': os.path.join(self.local_path, 'TUT-sound-events-2016-development.meta.zip'),
                'local_audio_path': os.path.join(self.local_path, 'audio'),
            },
            {
                'remote_package': 'https://zenodo.org/record/45759/files/TUT-sound-events-2016-development.audio.zip',
                'local_package': os.path.join(self.local_path, 'TUT-sound-events-2016-development.audio.zip'),
                'local_audio_path': os.path.join(self.local_path, 'audio'),
            },
        ]

    def event_label_count(self, scene_label=None):
        return len(self.event_labels(scene_label=scene_label))

    def event_labels(self, scene_label=None):
        labels = []
        for item in self.meta:
            if scene_label is None or item['scene_label'] == scene_label:
                if 'event_label' in item and item['event_label'].rstrip() not in labels:
                    labels.append(item['event_label'].rstrip())
        labels.sort()
        return labels

    def on_after_extract(self):
        """After dataset packages are downloaded and extracted, meta-files are checked.

        Parameters
        ----------
        nothing

        Returns
        -------
        nothing

        """

        if not os.path.isfile(self.meta_file):
            meta_file_handle = open(self.meta_file, 'wt')
            try:
                writer = csv.writer(meta_file_handle, delimiter='\t')
                for filename in self.audio_files:
                    raw_path, raw_filename = os.path.split(filename)
                    relative_path = self.absolute_to_relative(raw_path)
                    scene_label = relative_path.replace('audio', '')[1:]
                    base_filename, file_extension = os.path.splitext(raw_filename)

                    annotation_filename = os.path.join(self.local_path, relative_path.replace('audio', 'meta'), base_filename + '.ann')
                    if os.path.isfile(annotation_filename):
                        annotation_file_handle = open(annotation_filename, 'rt')
                        try:
                            annotation_file_reader = csv.reader(annotation_file_handle, delimiter='\t')
                            for annotation_file_row in annotation_file_reader:
                                writer.writerow((os.path.join(relative_path, raw_filename),
                                                 scene_label,
                                                 float(annotation_file_row[0].replace(',', '.')),
                                                 float(annotation_file_row[1].replace(',', '.')),
                                                 annotation_file_row[2], 'm'))
                        finally:
                            annotation_file_handle.close()
            finally:
                meta_file_handle.close()

    def train(self, fold=0, scene_label=None):
        if fold not in self.evaluation_data_train:
            self.evaluation_data_train[fold] = {}
            for scene_label_ in self.scene_labels:
                if scene_label_ not in self.evaluation_data_train[fold]:
                    self.evaluation_data_train[fold][scene_label_] = []

                if fold > 0:
                    with open(os.path.join(self.evaluation_setup_path, scene_label_+'_fold' + str(fold) + '_train.txt'), 'rt') as f:
                        for row in csv.reader(f, delimiter='\t'):
                            if len(row) == 5:
                                # Event meta
                                self.evaluation_data_train[fold][scene_label_].append({
                                    'file': self.relative_to_absolute_path(row[0]),
                                    'scene_label': row[1],
                                    'event_onset': float(row[2]),
                                    'event_offset': float(row[3]),
                                    'event_label': row[4]
                                })
                else:
                    data = []
                    for item in self.meta:
                        if item['scene_label'] == scene_label_:
                            if 'event_label' in item:
                                data.append({'file': self.relative_to_absolute_path(item['file']),
                                             'scene_label': item['scene_label'],
                                             'event_onset': item['event_onset'],
                                             'event_offset': item['event_offset'],
                                             'event_label': item['event_label'],
                                             })
                    self.evaluation_data_train[0][scene_label_] = data

        if scene_label:
            return self.evaluation_data_train[fold][scene_label]
        else:
            data = []
            for scene_label_ in self.scene_labels:
                for item in self.evaluation_data_train[fold][scene_label_]:
                    data.append(item)
            return data

    def test(self, fold=0, scene_label=None):
        if fold not in self.evaluation_data_test:
            self.evaluation_data_test[fold] = {}
            for scene_label_ in self.scene_labels:
                if scene_label_ not in self.evaluation_data_test[fold]:
                    self.evaluation_data_test[fold][scene_label_] = []
                if fold > 0:
                    with open(os.path.join(self.evaluation_setup_path, scene_label_+'_fold' + str(fold) + '_test.txt'), 'rt') as f:
                        for row in csv.reader(f, delimiter='\t'):
                            self.evaluation_data_test[fold][scene_label_].append({'file': self.relative_to_absolute_path(row[0])})
                else:
                    data = []
                    files = []
                    for item in self.meta:
                        if scene_label_ in item:
                            if self.relative_to_absolute_path(item['file']) not in files:
                                data.append({'file': self.relative_to_absolute_path(item['file'])})
                                files.append(self.relative_to_absolute_path(item['file']))

                    self.evaluation_data_test[0][scene_label_] = data

        if scene_label:
            return self.evaluation_data_test[fold][scene_label]
        else:
            data = []
            for scene_label_ in self.scene_labels:
                for item in self.evaluation_data_test[fold][scene_label_]:
                    data.append(item)
            return data


class TUTSoundEvents_2016_EvaluationSet(Dataset):
    """TUT Sound events 2016 evaluation dataset

    This dataset is used in DCASE2016 - Task 3, Sound event detection in real life audio

    """

    def __init__(self, data_path='data'):
        Dataset.__init__(self, data_path=data_path, name='TUT-sound-events-2016-evaluation')

        self.authors = 'Annamaria Mesaros, Toni Heittola, and Tuomas Virtanen'
        self.name_remote = 'TUT Sound Events 2016, evaluation dataset'
        self.url = 'http://www.cs.tut.fi/sgn/arg/dcase2016/download/'
        self.audio_source = 'Field recording'
        self.audio_type = 'Natural'
        self.recording_device_model = 'Roland Edirol R-09'
        self.microphone_model = 'Soundman OKM II Klassik/studio A3 electret microphone'

        self.evaluation_folds = 1

        self.package_list = [
            {
                'remote_package': None,
                'local_package': None,
                'local_audio_path': os.path.join(self.local_path, 'audio'),
            },
            {
                'remote_package': None,
                'local_package': None,
                'local_audio_path': os.path.join(self.local_path, 'audio', 'home'),
            },
            {
                'remote_package': None,
                'local_package': None,
                'local_audio_path': os.path.join(self.local_path, 'audio', 'residential_area'),
            },
        ]

    @property
    def scene_labels(self):
        labels = ['home', 'residential_area']
        labels.sort()
        return labels

    def event_label_count(self, scene_label=None):
        return len(self.event_labels(scene_label=scene_label))

    def event_labels(self, scene_label=None):
        labels = []
        for item in self.meta:
            if scene_label is None or item['scene_label'] == scene_label:
                if 'event_label' in item and item['event_label'] not in labels:
                    labels.append(item['event_label'])
        labels.sort()
        return labels

    def on_after_extract(self):
        """After dataset packages are downloaded and extracted, meta-files are checked.

        Parameters
        ----------
        nothing

        Returns
        -------
        nothing

        """

        if not os.path.isfile(self.meta_file) and os.path.isdir(os.path.join(self.local_path,'meta')):
            meta_file_handle = open(self.meta_file, 'wt')
            try:
                writer = csv.writer(meta_file_handle, delimiter='\t')
                for filename in self.audio_files:
                    raw_path, raw_filename = os.path.split(filename)
                    relative_path = self.absolute_to_relative(raw_path)
                    scene_label = relative_path.replace('audio', '')[1:]
                    base_filename, file_extension = os.path.splitext(raw_filename)

                    annotation_filename = os.path.join(self.local_path, relative_path.replace('audio', 'meta'), base_filename + '.ann')
                    if os.path.isfile(annotation_filename):
                        annotation_file_handle = open(annotation_filename, 'rt')
                        try:
                            annotation_file_reader = csv.reader(annotation_file_handle, delimiter='\t')
                            for annotation_file_row in annotation_file_reader:
                                writer.writerow((os.path.join(relative_path, raw_filename),
                                                 scene_label,
                                                 float(annotation_file_row[0].replace(',', '.')),
                                                 float(annotation_file_row[1].replace(',', '.')),
                                                 annotation_file_row[2], 'm'))
                        finally:
                            annotation_file_handle.close()
            finally:
                meta_file_handle.close()

    def train(self, fold=0, scene_label=None):
        raise IOError('Train setup not available.')

    def test(self, fold=0, scene_label=None):
        if fold not in self.evaluation_data_test:
            self.evaluation_data_test[fold] = {}
            for scene_label_ in self.scene_labels:
                if scene_label_ not in self.evaluation_data_test[fold]:
                    self.evaluation_data_test[fold][scene_label_] = []

                if fold > 0:
                    with open(os.path.join(self.evaluation_setup_path, scene_label + '_fold' + str(fold) + '_test.txt'), 'rt') as f:
                        for row in csv.reader(f, delimiter='\t'):
                            self.evaluation_data_test[fold][scene_label_].append({'file': self.relative_to_absolute_path(row[0])})
                else:
                    data = []
                    files = []
                    for item in self.audio_files:
                        if scene_label_ in item:
                            if self.relative_to_absolute_path(item) not in files:
                                data.append({'file': self.relative_to_absolute_path(item)})
                                files.append(self.relative_to_absolute_path(item))

                    self.evaluation_data_test[0][scene_label_] = data

        if scene_label:
            return self.evaluation_data_test[fold][scene_label]
        else:
            data = []
            for scene_label_ in self.scene_labels:
                for item in self.evaluation_data_test[fold][scene_label_]:
                    data.append(item)
            return data


# CHIME home
class CHiMEHome_DomesticAudioTag_DevelopmentSet(Dataset):
    def __init__(self, data_path=None):
        Dataset.__init__(self, data_path=data_path, name = 'CHiMeHome-audiotag-development')

        self.authors = 'Peter Foster, Siddharth Sigtia, Sacha Krstulovic, Jon Barker, and Mark Plumbley'
        self.name_remote = 'The CHiME-Home dataset is a collection of annotated domestic environment audio recordings.'
        self.url = ''
        self.audio_source = 'Field recording'
        self.audio_type = 'Natural'
        self.recording_device_model = 'Unknown'
        self.microphone_model = 'Unknown'

        self.evaluation_folds = 10

        self.package_list = [
            {
                'remote_package': 'https://archive.org/download/chime-home/chime_home.tar.gz',
                'local_package': os.path.join(self.local_path, 'chime_home.tar.gz'),
                'local_audio_path': os.path.join(self.local_path, 'chime_home', 'chunks'),
            },
        ]

    @property
    def audio_files(self):
        """Get all audio files in the dataset, use only file from CHime-Home-refined set.

        Parameters
        ----------
        nothing

        Returns
        -------
        files : list
            audio files

        """

        if self.files is None:
            refined_files = []
            with open(os.path.join(self.local_path, 'chime_home', 'chunks_refined.csv'), 'rt') as f:
                for row in csv.reader(f, delimiter=','):
                    refined_files.append(row[1])

            self.files = []
            for file in self.package_list:
                path = file['local_audio_path']
                if path:
                    l = os.listdir(path)
                    p = path.replace(self.local_path + os.path.sep, '')
                    for f in l:
                        fileName, fileExtension = os.path.splitext(f)
                        if fileExtension[1:] in self.audio_extensions and fileName in refined_files:
                            self.files.append(os.path.abspath(os.path.join(path, f)))

            self.files.sort()
        return self.files

    def read_chunk_meta(self, meta_filename):
        if os.path.isfile(meta_filename):
            meta_file_handle = open(meta_filename, 'rt')
            try:
                meta_file_reader = csv.reader(meta_file_handle, delimiter=',')
                data = {}
                for meta_file_row in meta_file_reader:
                    data[meta_file_row[0]] = meta_file_row[1]
            finally:
                meta_file_handle.close()
            return data

    def tagcode_to_taglabel(self, tag):
        map = {'c': 'child speech',
               'm': 'adult male speech',
               'f': 'adult female speech',
               'v': 'video game/tv',
               'p': 'percussive sound',
               'b': 'broadband noise',
               'o': 'other',
               'S': 'silence/background',
               'U': 'unidentifiable'
               }
        if tag in map:
            return map[tag]
        else:
            return None

    def on_after_extract(self):
        """After dataset packages are downloaded and extracted, meta-files are checked.

        Legacy dataset meta files are converted to be compatible with current scheme.

        Parameters
        ----------
        nothing

        Returns
        -------
        nothing

        """

        if not os.path.isfile(self.meta_file):
            section_header('Generating meta file for dataset')

            scene_label = 'home'
            f = open(self.meta_file, 'wt')
            try:
                writer = csv.writer(f, delimiter='\t')
                for file in self.audio_files:
                    raw_path, raw_filename = os.path.split(file)
                    relative_path = self.absolute_to_relative(raw_path)

                    base_filename, file_extension = os.path.splitext(raw_filename)
                    annotation_filename = os.path.join(raw_path, base_filename + '.csv')
                    meta_data = self.read_chunk_meta(annotation_filename)
                    tags = []

                    for i, tag in enumerate(meta_data['majorityvote']):
                        if tag is 'b':
                            print file

                        if tag is not 'S' and tag is not 'U':
                            tags.append(self.tagcode_to_taglabel(tag))
                    tags = ';'.join(tags)
                    writer.writerow(
                        (os.path.join(relative_path, raw_filename), scene_label, meta_data['majorityvote'], tags))
            finally:
                f.close()
            foot()

        all_folds_found = True
        for fold in xrange(1, self.evaluation_folds):
            for target_tag in self.audio_tags:
                if not os.path.isfile(os.path.join(self.evaluation_setup_path,
                                                   'fold' + str(fold) + '_' + target_tag.replace('/', '-').replace(' ',
                                                                                                                   '_') + '_train.txt')):
                    all_folds_found = False
                if not os.path.isfile(os.path.join(self.evaluation_setup_path,
                                                   'fold' + str(fold) + '_' + target_tag.replace('/', '-').replace(' ',
                                                                                                                   '_') + '_test.txt')):
                    all_folds_found = False

        if not all_folds_found:
            if not os.path.isdir(self.evaluation_setup_path):
                os.makedirs(self.evaluation_setup_path)

            numpy.random.seed(475686)
            kf = KFold(n=len(self.audio_files), n_folds=self.evaluation_folds, shuffle=True)

            refined_files = []
            with open(os.path.join(self.local_path, 'chime_home', 'chunks_refined.csv'), 'rt') as f:
                for row in csv.reader(f, delimiter=','):
                    refined_files.append(self.relative_to_absolute_path(os.path.join('chime_home','chunks',row[1]+'.wav')))

            fold = 1
            files = numpy.array(refined_files) 

            for train_index, test_index in kf:                

                train_files = files[train_index]
                test_files = files[test_index]

                with open(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_train.txt'), 'wt') as f:
                    writer = csv.writer(f, delimiter='\t')
                    for file in train_files:
                        raw_path, raw_filename = os.path.split(file)
                        relative_path = raw_path.replace(self.local_path + os.path.sep, '')
                        item = self.file_meta(file)[0]
                        writer.writerow([os.path.join(relative_path, raw_filename), item['scene_label'],item['tag_string'], ';'.join(item['tags'])])


                with open(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_test.txt'), 'wt') as f:
                    writer = csv.writer(f, delimiter='\t')
                    for file in test_files:
                        raw_path, raw_filename = os.path.split(file)
                        relative_path = raw_path.replace(self.local_path + os.path.sep, '')
                        writer.writerow([os.path.join(relative_path, raw_filename)])

                with open(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_evaluate.txt'), 'wt') as f:
                    writer = csv.writer(f, delimiter='\t')
                    for file in test_files:
                        raw_path, raw_filename = os.path.split(file)
                        relative_path = raw_path.replace(self.local_path + os.path.sep, '')
                        item = self.file_meta(file)[0]
                        writer.writerow([os.path.join(relative_path, raw_filename), item['scene_label'],item['tag_string'], ';'.join(item['tags'])])

                fold+= 1


# Legacy datasets
# =====================================================
# DCASE 2013
# =====================================================
class DCASE2013_Scene_DevelopmentSet(Dataset):
    """DCASE 2013 Acoustic scene classification, development dataset

    """

    def __init__(self, data_path='data'):
        Dataset.__init__(self, data_path=data_path, name='DCASE2013-scene-development')

        self.authors = 'Dimitrios Giannoulis, Emmanouil Benetos, Dan Stowell, and Mark Plumbley'
        self.name_remote = 'IEEE AASP 2013 CASA Challenge - Public Dataset for Scene Classification Task'
        self.url = 'http://www.elec.qmul.ac.uk/digitalmusic/sceneseventschallenge/'
        self.audio_source = 'Field recording'
        self.audio_type = 'Natural'
        self.recording_device_model = 'Unknown'
        self.microphone_model = 'Soundman OKM II Klassik/studio A3 electret microphone'

        self.evaluation_folds = 5

        self.package_list = [
            {
                'remote_package': 'http://c4dm.eecs.qmul.ac.uk/rdr/bitstream/handle/123456789/29/scenes_stereo.zip?sequence=1',
                'local_package': os.path.join(self.local_path, 'scenes_stereo.zip'),
                'local_audio_path': os.path.join(self.local_path, 'scenes_stereo'),
            }
        ]

    def on_after_extract(self):

        # Make legacy dataset compatible with DCASE2016 dataset scheme
        if not os.path.isfile(self.meta_file):
            section_header('Generating meta file for dataset')
            f = open(self.meta_file, 'wt')
            try:
                writer = csv.writer(f, delimiter='\t')
                for file in self.audio_files:
                    raw_path, raw_filename = os.path.split(file)
                    relative_path = self.absolute_to_relative(raw_path)
                    label = os.path.splitext(os.path.split(file)[1])[0][:-2]
                    writer.writerow((os.path.join(relative_path, raw_filename), label))
            finally:
                f.close()
            foot()

        all_folds_found = True
        for fold in xrange(1, self.evaluation_folds):
            if not os.path.isfile(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_train.txt')):
                all_folds_found = False
            if not os.path.isfile(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_test.txt')):
                all_folds_found = False

        if not all_folds_found:
            section_header('Generating evaluation setup files for dataset')
            if not os.path.isdir(self.evaluation_setup_path):
                os.makedirs(self.evaluation_setup_path)

            classes = []
            files = []
            for item in self.meta:
                classes.append(item['scene_label'])
                files.append(item['file'])
            files = numpy.array(files)

            sss = StratifiedShuffleSplit(y=classes, n_iter=self.evaluation_folds, test_size=0.3, random_state=0)
            fold = 1
            for train_index, test_index in sss:
                # print("TRAIN:", train_index, "TEST:", test_index)
                train_files = files[train_index]

                with open(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_train.txt'), 'wt') as f:
                    writer = csv.writer(f, delimiter='\t')
                    for file in train_files:
                        raw_path, raw_filename = os.path.split(file)
                        label = self.file_meta(file)[0]['scene_label']
                        writer.writerow([os.path.join(raw_path, raw_filename), label])

                test_files = files[test_index]
                with open(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_test.txt'), 'wt') as f:
                    writer = csv.writer(f, delimiter='\t')
                    for file in test_files:
                        raw_path, raw_filename = os.path.split(file)
                        writer.writerow([os.path.join(raw_path, raw_filename)])

                with open(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_evaluate.txt'), 'wt') as f:
                    writer = csv.writer(f, delimiter='\t')
                    for file in test_files:
                        raw_path, raw_filename = os.path.split(file)
                        label = self.file_meta(file)[0]['scene_label']
                        writer.writerow([os.path.join(raw_path, raw_filename), label])

                fold += 1
            foot()


class DCASE2013_Scene_EvaluationSet(DCASE2013_Scene_DevelopmentSet):
    """DCASE 2013 Acoustic scene classification, evaluation dataset

    """

    def __init__(self, data_path='data'):
        Dataset.__init__(self, data_path=data_path, name='DCASE2013-scene-challenge')

        self.authors = 'Dimitrios Giannoulis, Emmanouil Benetos, Dan Stowell, and Mark Plumbley'
        self.name_remote = 'IEEE AASP 2013 CASA Challenge - Private Dataset for Scene Classification Task'
        self.url = 'http://www.elec.qmul.ac.uk/digitalmusic/sceneseventschallenge/'
        self.audio_source = 'Field recording'
        self.audio_type = 'Natural'
        self.recording_device_model = 'Unknown'
        self.microphone_model = 'Soundman OKM II Klassik/studio A3 electret microphone'

        self.evaluation_folds = 5

        self.package_list = [
            {
                'remote_package': 'https://archive.org/download/dcase2013_scene_classification_testset/scenes_stereo_testset.zip',
                'local_package': os.path.join(self.local_path, 'scenes_stereo_testset.zip'),
                'local_audio_path': os.path.join(self.local_path, 'scenes_stereo_testset'),
            }
        ]

    def on_after_extract(self):
        # Make legacy dataset compatible with DCASE2016 dataset scheme
        if not os.path.isfile(self.meta_file) or 1:
            section_header('Generating meta file for dataset')
            f = open(self.meta_file, 'wt')
            try:
                writer = csv.writer(f, delimiter='\t')
                for file in self.audio_files:
                    raw_path, raw_filename = os.path.split(file)
                    relative_path = self.absolute_to_relative(raw_path)
                    label = os.path.splitext(os.path.split(file)[1])[0][:-2]
                    writer.writerow((os.path.join(relative_path, raw_filename), label))
            finally:
                f.close()
            foot()

        all_folds_found = True
        for fold in xrange(1, self.evaluation_folds):
            if not os.path.isfile(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_train.txt')):
                all_folds_found = False
            if not os.path.isfile(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_test.txt')):
                all_folds_found = False

        if not all_folds_found:
            section_header('Generating evaluation setup files for dataset')
            if not os.path.isdir(self.evaluation_setup_path):
                os.makedirs(self.evaluation_setup_path)

            classes = []
            files = []
            for item in self.meta:
                classes.append(item['scene_label'])
                files.append(item['file'])
            files = numpy.array(files)

            sss = StratifiedShuffleSplit(y=classes, n_iter=self.evaluation_folds, test_size=0.3, random_state=0)
            fold = 1
            for train_index, test_index in sss:

                train_files = files[train_index]

                with open(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_train.txt'), 'wt') as f:
                    writer = csv.writer(f, delimiter='\t')
                    for file in train_files:
                        raw_path, raw_filename = os.path.split(file)
                        label = self.file_meta(file)[0]['scene_label']
                        writer.writerow([os.path.join(raw_path, raw_filename), label])

                test_files = files[test_index]
                with open(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_test.txt'), 'wt') as f:
                    writer = csv.writer(f, delimiter='\t')
                    for file in test_files:
                        raw_path, raw_filename = os.path.split(file)
                        writer.writerow([os.path.join(raw_path, raw_filename)])

                with open(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_evaluate.txt'), 'wt') as f:
                    writer = csv.writer(f, delimiter='\t')
                    for file in test_files:
                        raw_path, raw_filename = os.path.split(file)
                        label = self.file_meta(file)[0]['scene_label']
                        writer.writerow([os.path.join(raw_path, raw_filename), label])

                fold += 1
            foot()


# Sound events
class DCASE2013_Event_DevelopmentSet(Dataset):
    """DCASE 2013 Sound event detection, development dataset

    """

    def __init__(self, data_path='data'):
        Dataset.__init__(self, data_path=data_path, name='DCASE2013-event-development')

        self.authors = 'Dimitrios Giannoulis, Emmanouil Benetos, Dan Stowell, and Mark Plumbley'
        self.name_remote = 'IEEE AASP CASA Challenge - Public Dataset for Event Detection Task'
        self.url = 'http://www.elec.qmul.ac.uk/digitalmusic/sceneseventschallenge/'
        self.audio_source = 'Field recording'
        self.audio_type = 'Natural'
        self.recording_device_model = 'Unknown'
        self.microphone_model = 'Soundman OKM II Klassik/studio A3 electret microphone'

        self.evaluation_folds = 5

        self.package_list = [
            {
                'remote_package': 'https://archive.org/download/dcase2013_event_detection_development_OS/events_OS_development_v2.zip',
                'local_package': os.path.join(self.local_path, 'events_OS_development_v2.zip'),
                'local_audio_path': os.path.join(self.local_path, 'events_OS_development_v2'),
            },
            # {
            #    'remote_package':'http://c4dm.eecs.qmul.ac.uk/rdr/bitstream/handle/123456789/28/singlesounds_annotation.zip?sequence=9',
            #    'local_package': os.path.join(self.local_path, 'singlesounds_annotation.zip'),
            #    'local_audio_path': None,
            # },
            # {
            #    'remote_package':'http://c4dm.eecs.qmul.ac.uk/rdr/bitstream/handle/123456789/28/singlesounds_stereo.zip?sequence=7',
            #    'local_package': os.path.join(self.local_path, 'singlesounds_stereo.zip'),
            #    'local_audio_path': os.path.join(self.local_path, 'singlesounds_stereo'),
            # },
        ]

    def on_after_extract(self):
        # Make legacy dataset compatible with DCASE2016 dataset scheme
        scene_label = 'office'
        if not os.path.isfile(self.meta_file):
            meta_file_handle = open(self.meta_file, 'wt')
            try:
                writer = csv.writer(meta_file_handle, delimiter='\t')
                for file in self.audio_files:
                    raw_path, raw_filename = os.path.split(file)
                    relative_path = self.absolute_to_relative(raw_path)

                    base_filename, file_extension = os.path.splitext(raw_filename)

                    if file.find('singlesounds_stereo') != -1:
                        annotation_filename = os.path.join(self.local_path, 'Annotation1', base_filename + '_bdm.txt')
                        label = base_filename[:-2]
                        if os.path.isfile(annotation_filename):
                            annotation_file_handle = open(annotation_filename, 'rt')
                            try:
                                annotation_file_reader = csv.reader(annotation_file_handle, delimiter='\t')
                                for annotation_file_row in annotation_file_reader:
                                    writer.writerow((os.path.join(relative_path, raw_filename), scene_label,
                                                     annotation_file_row[0], annotation_file_row[1], label, 'i'))
                            finally:
                                annotation_file_handle.close()

                    elif file.find('events_OS_development_v2') != -1:
                        annotation_filename = os.path.join(self.local_path, 'events_OS_development_v2',
                                                           base_filename + '_v2.txt')
                        if os.path.isfile(annotation_filename):
                            annotation_file_handle = open(annotation_filename, 'rt')
                            try:
                                annotation_file_reader = csv.reader(annotation_file_handle, delimiter='\t')
                                for annotation_file_row in annotation_file_reader:
                                    writer.writerow((os.path.join(relative_path, raw_filename), scene_label,
                                                     annotation_file_row[0], annotation_file_row[1],
                                                     annotation_file_row[2], 'm'))
                            finally:
                                annotation_file_handle.close()
            finally:
                meta_file_handle.close()

        all_folds_found = True
        for fold in xrange(1, self.evaluation_folds):
            if not os.path.isfile(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_train.txt')):
                all_folds_found = False
            if not os.path.isfile(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_test.txt')):
                all_folds_found = False

        if not all_folds_found:
            # Construct training and testing sets. Isolated sound are used for training and
            # polyphonic mixtures are used for testing.
            if not os.path.isdir(self.evaluation_setup_path):
                os.makedirs(self.evaluation_setup_path)

            files = []
            for item in self.meta:
                if item['file'] not in files:
                    files.append(item['file'])
            files = numpy.array(files)
            f = numpy.zeros(len(files))

            sss = StratifiedShuffleSplit(y=f, n_iter=5, test_size=0.3, random_state=0)
            fold = 1
            for train_index, test_index in sss:
                # print("TRAIN:", train_index, "TEST:", test_index)
                train_files = files[train_index]
                with open(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_train.txt'), 'wt') as f:
                    writer = csv.writer(f, delimiter='\t')
                    for file in train_files:
                        raw_path, raw_filename = os.path.split(file)
                        relative_path = raw_path.replace(self.local_path + os.path.sep, '')
                        for item in self.meta:
                            if item['file'] == file:
                                writer.writerow([os.path.join(relative_path, raw_filename), item['scene_label'],
                                                 item['event_onset'], item['event_offset'], item['event_label']])

                test_files = files[test_index]
                with open(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_test.txt'), 'wt') as f:
                    writer = csv.writer(f, delimiter='\t')
                    for file in test_files:
                        raw_path, raw_filename = os.path.split(file)
                        relative_path = raw_path.replace(self.local_path + os.path.sep, '')
                        writer.writerow([os.path.join(relative_path, raw_filename)])

                with open(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_evaluate.txt'), 'wt') as f:
                    writer = csv.writer(f, delimiter='\t')
                    for file in test_files:
                        raw_path, raw_filename = os.path.split(file)
                        relative_path = raw_path.replace(self.local_path + os.path.sep, '')
                        for item in self.meta:
                            if item['file'] == file:
                                writer.writerow([os.path.join(relative_path, raw_filename), item['scene_label'],
                                                 item['event_onset'], item['event_offset'], item['event_label']])

                fold += 1


class DCASE2013_Event_EvaluationSet(Dataset):
    """DCASE 2013 Sound event detection, evaluation dataset

    """

    def __init__(self, data_path='data'):
        Dataset.__init__(self, data_path=data_path, name='DCASE2013-event-challenge')

        self.authors = 'Dimitrios Giannoulis, Emmanouil Benetos, Dan Stowell, and Mark Plumbley'
        self.name_remote = 'IEEE AASP CASA Challenge - Private Dataset for Event Detection Task'
        self.url = 'http://www.elec.qmul.ac.uk/digitalmusic/sceneseventschallenge/'
        self.audio_source = 'Field recording'
        self.audio_type = 'Natural'
        self.recording_device_model = 'Unknown'
        self.microphone_model = 'Soundman OKM II Klassik/studio A3 electret microphone'

        self.evaluation_folds = 5

        self.package_list = [
            {
                'remote_package': 'https://archive.org/download/dcase2013_event_detection_testset_OS/dcase2013_event_detection_testset_OS.zip',
                'local_package': os.path.join(self.local_path, 'dcase2013_event_detection_testset_OS.zip'),
                'local_audio_path': os.path.join(self.local_path, 'dcase2013_event_detection_testset_OS'),
            }
        ]

    def on_after_extract(self):
        # Make legacy dataset compatible with DCASE2016 dataset scheme
        scene_label = 'office'

        if not os.path.isfile(self.meta_file):
            meta_file_handle = open(self.meta_file, 'wt')
            try:
                writer = csv.writer(meta_file_handle, delimiter='\t')
                for file in self.audio_files:
                    raw_path, raw_filename = os.path.split(file)
                    relative_path = self.absolute_to_relative(raw_path)

                    base_filename, file_extension = os.path.splitext(raw_filename)

                    if file.find('dcase2013_event_detection_testset_OS') != -1:
                        annotation_filename = os.path.join(self.local_path, 'dcase2013_event_detection_testset_OS',base_filename + '_v2.txt')
                        if os.path.isfile(annotation_filename):
                            annotation_file_handle = open(annotation_filename, 'rt')
                            try:
                                annotation_file_reader = csv.reader(annotation_file_handle, delimiter='\t')
                                for annotation_file_row in annotation_file_reader:
                                    writer.writerow((os.path.join(relative_path, raw_filename), scene_label,
                                                     annotation_file_row[0], annotation_file_row[1],
                                                     annotation_file_row[2], 'm'))
                            finally:
                                annotation_file_handle.close()
                        else:
                            annotation_filename = os.path.join(self.local_path, 'dcase2013_event_detection_testset_OS',base_filename + '.txt')
                            if os.path.isfile(annotation_filename):
                                annotation_file_handle = open(annotation_filename, 'rt')
                                try:
                                    annotation_file_reader = csv.reader(annotation_file_handle, delimiter='\t')
                                    for annotation_file_row in annotation_file_reader:
                                        writer.writerow((os.path.join(relative_path, raw_filename), scene_label,
                                                         annotation_file_row[0], annotation_file_row[1],
                                                         annotation_file_row[2], 'm'))
                                finally:
                                    annotation_file_handle.close()
            finally:
                meta_file_handle.close()

        all_folds_found = True
        for fold in xrange(1, self.evaluation_folds):
            if not os.path.isfile(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_train.txt')):
                all_folds_found = False
            if not os.path.isfile(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_test.txt')):
                all_folds_found = False

        if not all_folds_found:
            # Construct training and testing sets. Isolated sound are used for training and
            # polyphonic mixtures are used for testing.
            if not os.path.isdir(self.evaluation_setup_path):
                os.makedirs(self.evaluation_setup_path)

            files = []
            for item in self.meta:
                if item['file'] not in files:
                    files.append(item['file'])
            files = numpy.array(files)
            f = numpy.zeros(len(files))

            sss = StratifiedShuffleSplit(y=f, n_iter=5, test_size=0.3, random_state=0)
            fold = 1
            for train_index, test_index in sss:
                # print("TRAIN:", train_index, "TEST:", test_index)
                train_files = files[train_index]
                with open(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_train.txt'), 'wt') as f:
                    writer = csv.writer(f, delimiter='\t')
                    for file in train_files:
                        raw_path, raw_filename = os.path.split(file)
                        relative_path = raw_path.replace(self.local_path + os.path.sep, '')
                        for item in self.meta:
                            if item['file'] == file:
                                writer.writerow([os.path.join(relative_path, raw_filename), item['scene_label'],
                                                 item['event_onset'], item['event_offset'], item['event_label']])

                test_files = files[test_index]
                with open(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_test.txt'), 'wt') as f:
                    writer = csv.writer(f, delimiter='\t')
                    for file in test_files:
                        raw_path, raw_filename = os.path.split(file)
                        relative_path = raw_path.replace(self.local_path + os.path.sep, '')
                        writer.writerow([os.path.join(relative_path, raw_filename)])

                with open(os.path.join(self.evaluation_setup_path, 'fold' + str(fold) + '_evaluate.txt'), 'wt') as f:
                    writer = csv.writer(f, delimiter='\t')
                    for file in test_files:
                        raw_path, raw_filename = os.path.split(file)
                        relative_path = raw_path.replace(self.local_path + os.path.sep, '')
                        for item in self.meta:
                            if item['file'] == file:
                                writer.writerow([os.path.join(relative_path, raw_filename), item['scene_label'],
                                                 item['event_onset'], item['event_offset'], item['event_label']])

                fold += 1
