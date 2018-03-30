from setuptools import setup, find_packages
import numpy as np
import imp

version = imp.load_source('grbpy.version', 'version.py')

setup(
    name='jetpy',
    version=version.version,
    description='Tools for the JET code',
    packages=['jetpy'],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy"],
    install_requires=['numpy>=1.10', 'scipy>=0.14', 'h5py>=2.0',
                        'matplotlib>=1.3'],
    extras_require={
        'docs': ['numpydoc']
        }
    )
