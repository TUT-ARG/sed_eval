``sed_eval`` - Evaluation toolbox for Sound Event Detection
===========================================================

- Toni Heittola (toni.heittola@tut.fi, `GitHub <https://github.com/toni-heittola>`_, `Home <http://www.cs.tut.fi/~heittolt/>`_)
- Annamaria Mesaros (annamaria.mesaros@tut.fi, `Home <http://www.cs.tut.fi/~mesaros/>`_)

.. figure:: _static/evaluation_overview.png
    :target: _static/evaluation_overview.png
    :align: center
    :width: 100%


``sed_eval`` is an open source Python toolbox which provides a standardized, and transparent way to evaluate
sound event detection systems (see :ref:`sound_event`). In addition to this, it provides tools for evaluating acoustic
scene classification systems, as the fields are closely related (see :ref:`scene`).

The toolbox can be used in any of the following ways:

* By using the included evaluator scripts directly (see :ref:`install` and :ref:`evaluators`). This is suitable if the system to be evaluated is implemented using some other platform than Python.
* By importing it and calling it from your own Python code (see :ref:`install` and :ref:`sed_eval_quickstart`)

Citing
------

If you use ``sed_eval`` in a research project, please cite the following paper:

Annamaria Mesaros, Toni Heittola, and Tuomas Virtanen, "Metrics for polyphonic sound event detection", Applied Sciences, 6(6):162, 2016 [`HTML <http://www.mdpi.com/2076-3417/6/6/162>`_][`PDF <http://www.mdpi.com/2076-3417/6/6/162/pdf>`_]

.. _installation:

Getting started
---------------
.. toctree::
    :maxdepth: 1

    install
    tutorial

API documentation
-----------------

.. toctree::
    :maxdepth: 1

    sound_event
    scene
    metric
    util
    io

Reference
---------

.. toctree::
    :maxdepth: 1

    glossary
    changelog

* :ref:`genindex`


