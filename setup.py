#! /usr/bin/env python

# Copyright (c) 2020 Gabriel Potter
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
Setuptools config
"""

try:
    from setuptools import setup, find_packages
except:
    raise ImportError("setuptools is required to install force-graph !")
import io
import os


def get_long_description():
    """Extract description from README.md, for PyPI's usage"""
    def process_ignore_tags(buffer):
        return "\n".join(
            x for x in buffer.split("\n") if "<!-- ignore_ppi -->" not in x
        )
    try:
        fpath = os.path.join(os.path.dirname(__file__), "README.md")
        with io.open(fpath, encoding="utf-8") as f:
            readme = f.read()
            desc = readme.partition("<!-- start_ppi_description -->")[2]
            desc = desc.partition("<!-- stop_ppi_description -->")[0]
            return process_ignore_tags(desc.strip())
    except IOError:
        return None


# https://packaging.python.org/guides/distributing-packages-using-setuptools/
setup(
    name='hamiltonian',
    version='0.0.1',
    packages=find_packages(),
    python_requires='>=3.5, <4',
    install_requires=['matplotlib', 'numpy'],
    zip_safe=True,
    # Metadata
    author='gpotter2',
    description='Hamiltonian: dynamic hamiltonian graphs with matplotlib',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    license='MIT',
    project_urls={
        'Source Code': 'https://github.com/gpotter2/hamiltonian/',
    },
    download_url='https://github.com/gpotter2/hamiltonian/tarball/master',
    keywords=["network"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Multimedia :: Graphics",
    ]
)
