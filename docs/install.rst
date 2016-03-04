.. _install:

Installation instructions
=========================

Using pip
---------

The latest stable release is available on PyPI, and you can install with pip:

```
pip install sed_eval
```

Alternatively you can download or clone toolbox and use ``pip`` to handle dependencies:

```
unzip sed_eval.zip
pip install -e sed_eval
```
or
```
git clone https://github.com/TUT-ARG/sed_eval.git
pip install -e sed_eval
```

Using ``setyp.py``
------------------

You can install ``sed_eval`` from source by first installing the dependencies

``pip install -r requirements.txt``

and then running

```
python setup.py install
```

To uninstall the toolbox if it was installed with ``setyp.py``:

``python setup.py install --record files.txt`` to get files associated with toolbox
``cat files.txt | xargs rm -rf`` to remove the files recorded by the previous step.

You can also install the toolbox in *develop* mode:

```
python setup.py develop
```

Toolbox can be uninstalled:

```
python setup.py develop --uninstall
```


Requirements
------------

Following libraries are required:

    - numpy >= 1.7.0
