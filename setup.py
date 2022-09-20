from gettext import install
from setuptools import setup,find_packages
from typing import List

#Declaring the varibales to setup the function

PROJECT_NAME='housing-price-predictor'
VERSION="0.0.1"
AUTHOR="Sagar Kanade"
DESCRIPTION="This is first End to End Machine Learning Project"
PACKAGES=['housing']
REQUIREMENT_FILE_NAME='requirements.txt'

def get_requirements_list() -> List[str]:
    """
    Description: This function is going to return the list of requirement mentioned in requirements.txt file

    return - This fucntion is going to return a list which contain name 
    of libraries mentioned in requirements.txt file
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        return requirement_file.readlines().remove("-e .") #-e  . is removed because, below find_packages() is going to do the same what '-e .' is going to do

setup(

name=PROJECT_NAME,
version=VERSION,
author=AUTHOR,
description=DESCRIPTION,
packages=find_packages(),
install_requires=get_requirements_list()
)