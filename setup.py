from setuptools import setup, find_packages

long_description = open('README.rst').read()

setup(
    name='sed_eval',
    version='0.1.9',
    description='Evaluation toolbox for Sound Event Detection',
    author='Toni Heittola',
    author_email='toni.heittola@gmail.com',
    url='https://github.com/TUT-ARG/sed_eval',
    packages=find_packages(),
    long_description=long_description,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Programming Language :: Python :: 2.7",
    ],
    keywords=['audio analysis', 'sound event detection', 'dsp'],
    license='MIT',
    install_requires=[
        'numpy >= 1.7.0',
    ],
)
