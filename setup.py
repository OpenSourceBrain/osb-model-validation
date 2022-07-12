from setuptools import setup, find_packages

import omv
version = omv.__version__

setup(
    name='OSBModelValidation',
    version=version,
    author='Boris Marin',
    author_email='borismarin@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['omv = omv.omv_util:main']},
    package_data={
        'omv': [
            'schemata/mep.yaml',
            'schemata/types/*.yaml',
            'schemata/types/base/*.yaml',
            'engines/utils/genesis_utils.g']},
    url='https://github.com/OpenSourceBrain/osb-model-validation',
    license='LICENSE.lesser',
    description='OpenSourceBrain Model Validation',
    long_description=open('README.md').read(),
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=[
        'PyYAML',
        'numpy',
        'pyrx',
        'pathlib',
        'docopt'],
)
