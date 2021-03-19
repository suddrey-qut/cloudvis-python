#!/usr/bin/env python3
"""
.. codeauthor:: Gavin Suddreys
"""
import os
from typing import List
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

req = [
    'numpy',
    'pyzmq',
    'opencv-python',
    'pyyaml'
]

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# list all data folders here, to ensure they get packaged

data_folders = [
]


def package_files(directory: List[str]) -> List[str]:
    """[summary]
    :param directory: [description]
    :type directory: [type]
    :return: [description]
    :rtype: [type]
    """
    paths: List[str] = []
    for (pathhere, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', pathhere, filename))
    return paths


extra_files = []
for data_folder in data_folders:
    extra_files += package_files(data_folder)

setup(
    name='cloudvis',

    version='1.0.0',

    description='Cloudvis API for Python',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://github.com/suddrey-qut/manipulation_driver/cloudvis-python',

    author='Gavin Suddrey',

    license='MIT',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    python_requires='>=2.7',

    project_urls={
        # 'Documentation': 'https://petercorke.github.io/roboticstoolbox-python',
        'Source': 'https://github.com/suddrey-qut/cloudvis-python',
        'Tracker': 'https://github.com/suddrey-qut/cloudvis-python/issues'#,
        # 'Coverage': 'https://codecov.io/gh/petercorke/roboticstoolbox-python'
    },

    keywords='python computer-vision robotics',

    packages=find_packages(exclude=['tests']),
    package_data={'cloudvis': extra_files},

    include_package_data=True,

    install_requires=req,
)
