# from typing import List
# from setuptools import find_packages, setup


# def get_requirements(file_path: str) -> List[str]:
#     rq = []
#     with open(file_path) as file_obj:
#         rq = file_obj.readline()
#         rq = [req.replace('\n', '') for req in rq]

#     return rq


# setup(
#     name='Sensor_Fault',
#     version='0.0.0.1',
#     author='Shivansh',
#     author_email='xyz@gmail.com',
#     install_requires=get_requirements('requirements.txt'),
#     packages=find_packages()
# )



from typing import List
from setuptools import find_packages, setup

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    """
    This function will return the list of requirements.
    """
    requirements = []
    with open(file_path) as file_obj:
        # readlines() reads all lines from the file into a list
        requirements = file_obj.readlines()
        # This list comprehension removes the newline character '\n' from each requirement
        requirements = [req.replace('\n', '') for req in requirements]

        # The '-e .' in requirements.txt tells setup.py to also look for packages
        # in the current directory. We handle this by using find_packages() instead,
        # so we can safely remove it from the install_requires list.
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    return requirements


setup(
    name='Sensor_Fault',
    version='0.0.0.1',
    author='Shivansh',
    author_email='xyz@gmail.com', # Remember to update this with a real email
    install_requires=get_requirements('requirements.txt'),
    packages=find_packages()
)