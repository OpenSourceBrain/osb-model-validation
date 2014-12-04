from setuptools import setup, find_packages
setup(
    name='OSBModelValidation',
    version='0.1.0',
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
        'watchdog',
        'docopt'],
)
