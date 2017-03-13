sed_eval - Evaluation toolbox for Sound Event Detection
=======================================================

.. image:: https://travis-ci.org/TUT-ARG/sed_eval.svg?branch=master
    :target: https://travis-ci.org/TUT-ARG/sed_eval

.. image:: https://coveralls.io/repos/github/TUT-ARG/sed_eval/badge.svg?branch=master 
    :target: https://coveralls.io/github/TUT-ARG/sed_eval?branch=master

sed_eval is an open source Python toolbox which provides a standardized, 
and transparent way to evaluate sound event detection systems. 

Authors

- Toni Heittola (toni.heittola@tut.fi, `GitHub <https://github.com/toni-heittola>`_, `<http://www.cs.tut.fi/~heittolt/>`_)
- Annamaria Mesaros (annamaria.mesaros@tut.fi, `<http://www.cs.tut.fi/~mesaros/>`_)

Documentation
=============

See http://tut-arg.github.io/sed_eval for manual and tutorials.

Installation instructions
=========================

The latest stable release is available on PyPI, and you can install with pip::

    pip install sed_eval

Alternatively you can download or clone toolbox and use ``pip`` to handle dependencies::

    unzip sed_eval.zip
    pip install -e sed_eval


or::

    git clone https://github.com/TUT-ARG/sed_eval.git
    pip install -e sed_eval


Dependencies
------------

The toolbox is tested to work with Python 2.7 and Python 3.6.

- numpy >= 1.7.0

Citing
======

If you use sed_eval in a research project, please cite the following paper:

Annamaria Mesaros, Toni Heittola, and Tuomas Virtanen, "Metrics for polyphonic sound event detection", Applied Sciences, 6(6):162, 2016 [`HTML <http://www.mdpi.com/2076-3417/6/6/162>`_][`PDF <http://www.mdpi.com/2076-3417/6/6/162/pdf>`_]

License
=======

Code released under `the MIT license <https://github.com/TUT-ARG/sed_eval/tree/master/LICENSE.txt>`_.
