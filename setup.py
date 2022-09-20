from setuptools import setup
from typing import List

#Declaring the varibales to setup the 

def get_requirements_list() -> List[str]:
    pass

setup(

name='housing-price-predictor',
version="0.0.1",
author="Sagar Kanade",
description="This is first End to End Machine Learning Project",
packages=['housing']
install_requires=get_requirements_list()
)