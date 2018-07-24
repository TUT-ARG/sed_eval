Contributing
============

How to contribute
-----------------

The preferred way to contribute to `sed_eval` is to fork the 
[main repository](https://github.com/TUT-ARG/sed_eval) on
GitHub:

1. Fork the [project repository](https://github.com/TUT-ARG/sed_eval):
   click on the 'Fork' button near the top of the page. This creates
   a copy of the code under your account on the GitHub server.

2. Clone this copy to your local disk:

        git clone git@github.com:[YOUR_LOGIN]/sed_eval.git
        cd sed_eval 

3. Create a branch to hold your changes:

        git checkout -b my-new-feature

   and start making changes. You should never work in the ``master`` branch directly. 

4. Work on this copy on your computer using Git to do the version
   control. When you're done editing, do:

        git add [MODIFIED FILES]
        git commit

   to record your changes in Git, then push them to GitHub with:

        git push -u origin my-new-feature

Finally, go to the web page of the your fork of the sed_eval repo,
and click 'Pull request' to send your changes to the maintainers for
review. This will send an email to the committers.

More information about this kind of process can be found in 
[Git documentation](http://git-scm.com/documentation).

You should check that your contribution complies with the
following rules before submitting a pull request:

- All public methods should have informative docstrings
- Code should be sufficiently commented
- For major new features there should be also an unittest  

You should check for common programming errors with the following
tools:

-  Check unittests:

        pip install nose coverage
        cd tests/
        nosetests -v --with-coverage --cover-erase --cover-html --cover-package=sed_eval --nocapture

-  There should be no major pyflakes warnings, check with:

        pip install pyflakes
        pyflakes path/to/module.py

-  There should be no major PEP8 warnings, check with:

        pip install pep8
        pep8 path/to/module.py

Creating an issue
-----------------

We use Github issues to track all bugs and feature requests; feel free to
open an issue if you have found a bug or wish to see a new feature implemented.

It is recommended to check that your issue complies with the
following rules before submitting:

-  Verify that your issue is not being currently addressed by other
   [issues](https://github.com/TUT-ARG/sed_eval/issues?q=)
   or [pull requests](https://github.com/TUT-ARG/sed_eval/pulls?q=).

-  Please ensure all code snippets and error messages are formatted in
   appropriate code blocks.
   See [Creating and highlighting code blocks](https://help.github.com/articles/creating-and-highlighting-code-blocks).

-  Please include your operating system type and version number, as well
   as your Python, numpy, and dcase_util versions. You can get this
   information with following code:

    import platform; print(platform.platform())
    import sys; print("Python", sys.version)
    import numpy; print("NumPy", numpy.__version__)
    

Documentation
-------------

You can edit the documentation using any text editor and then generate
the HTML output by typing ``make html`` from the docs/ directory.
The resulting HTML files will be placed in docs/ and are viewable 
in a web browser. See the README file in the documentation/ directory for more information.

Note
----
This document is based on contribution instructions for [LibROSA](https://github.com/librosa/librosa).
