from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [
    'numpy',
    'pandas',
    'nltk',
    'bs4',
    'spacy',
    'tqdm'
]

setup(
    name='text_prep_utils',
    version='1.0.0',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    author="ytchen175",
    description='Text preprocessing utils.'
)
