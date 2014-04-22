from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages
setup(
    name='OSBModelValidation',
    version='0.1.0',
    author='Boris Marin',
    author_email='borismarin@gmail.com',
    packages=find_packages(),
    entry_points = {'console_scripts':
                    ['validate_mep = omv.validation.validate_mep:main']},
    package_data = {'omv':['schemata/mep.yaml',
                           'schemata/types/*.yaml',
                           'schemata/types/base/*.yaml']},
    url='http://opensourcebrain.org/OSBModelValidation',
    license='LICENSE.txt',
    description='OpenSourceBrain Model Validation',
    long_description=open('README.md').read(),
    install_requires=['PyYAML', 'numpy', 'pyrx', 'pathlib'],
)










