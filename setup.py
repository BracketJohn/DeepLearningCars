"""Make package installable via pip."""
from setuptools import find_packages, setup

setup(
    name='DeepLearningCars',
    version='0.0.2',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'deepcars = deepcars.__main__:start_sim'
        ]
    },
    python_requires=">=3.0")
