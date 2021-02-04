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
    license='LICENSE.txt',
    description='OpenSourceBrain Model Validation',
    long_description=open('README.md').read(),
    install_requires=[
        'PyYAML',
        'numpy',
        'pyrx',
        'pathlib',
        'docopt'],
)
