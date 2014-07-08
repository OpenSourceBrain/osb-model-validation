from setuptools import setup, find_packages
setup(
    name='OSBModelValidation',
    version='0.1.0',
    author='Boris Marin',
    author_email='borismarin@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'omv = omv.omv_util:main',
            'omv_alltests = omv.find_tests:test_all',
            'omv_autogen = omv.autogen:autogen']},
    package_data={
        'omv': [
            'schemata/mep.yaml',
            'schemata/types/*.yaml',
            'schemata/types/base/*.yaml',
            'backends/utils/genesis_utils.g']},
    url='http://opensourcebrain.org/OSBModelValidation',
    license='LICENSE.txt',
    description='OpenSourceBrain Model Validation',
    long_description=open('README.md').read(),
    install_requires=[
        'PyYAML',
        'numpy',
        'pyrx',
        'pathlib',
        'watchdog',
        'docopt'],
)
