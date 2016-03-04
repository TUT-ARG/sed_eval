#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import hashlib
import json


def check_path(path):
    """Check if path exists, if not creates one

    Parameters
    ----------
    path : str
        Path to be checked.

    Returns
    -------
    Nothing

    """

    if not os.path.isdir(path):
        os.makedirs(path)


def get_parameter_hash(params):
    """Get unique hash string (md5) for given parameter dict

    Parameters
    ----------
    params : dict
        Input parameters

    Returns
    -------
    md5_hash : str
        Unique hash for parameter dict

    """

    md5 = hashlib.md5()
    md5.update(str(json.dumps(params, sort_keys=True)))
    return md5.hexdigest()

