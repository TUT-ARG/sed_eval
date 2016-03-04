sed_eval - Evaluation toolbox for Sound Event Detection
=======================================================

.. image:: https://travis-ci.org/TUT-ARG/sed_eval.svg?branch=master
    :target: https://travis-ci.org/TUT-ARG/sed_eval

.. image:: https://coveralls.io/repos/github/TUT-ARG/sed_eval/badge.svg?branch=master 
    :target: https://coveralls.io/github/TUT-ARG/sed_eval?branch=master

sed_eval is an open source Python toolbox which provides a standardized, 
and transparent way to evaluate sound event detection systems. 

Documentation and usage information: http://tut-arg.github.io/sed_eval

Installation instructions
=========================

You can install ``sed_eval``, run:

``python setup.py install``

from the source directory.

To uninstall the toolbox:

``python setup.py install --record files.txt`` to get files associated with toolbox

``cat files.txt | xargs rm -rf`` to remove the files recorded by the previous step.

You can also install the toolbox in develop mode:

``python setup.py develop``

Toolbox can be uninstalled:

``python setup.py develop --uninstall``

Dependencies
------------

The toolbox is tested with Python 2.7.10. 

- numpy >= 1.7.0

License
=======

Code released under `the MIT license <https://github.com/TUT-ARG/sed_eval/tree/master/LICENSE.txt>`_.
