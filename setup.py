from setuptools import setup, find_packages
setup(
    name='OSBModelValidation',
    version='0.1.0',
    author='Boris Marin',
    author_email='borismarin@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'omv_validate_mep = omv.validation.validate_mep:main',
            'omv_alltests = omv.test_finder:test_all',
            'omv_autogen = omv.autogen:autogen',
            'omv_test = omv.test_finder:test_one']},
    package_data={
        'omv': [
            'schemata/mep.yaml',
            'schemata/types/*.yaml',
            'schemata/types/base/*.yaml']},
    url='http://opensourcebrain.org/OSBModelValidation',
    license='LICENSE.txt',
    description='OpenSourceBrain Model Validation',
    long_description=open('README.md').read(),
    install_requires=[
        'PyYAML',
        'numpy',
        'pyrx',
        'pathlib',
        'pyinotify'],
)
