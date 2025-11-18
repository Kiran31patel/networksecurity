'''
the setup.py
'''
from setuptools import setup, find_packages 
from typing import List


def get_requirements() -> List[str]:
    """ 
    This function will return the list of requirements 
    mentioned in the requirements.txt file 
    """
    try:
        with open('requirements.txt') as req_file:
            requirements = req_file.readlines()
            requirements = [req.strip() for req in requirements if req.strip()]
        return requirements
    except FileNotFoundError:
        return []