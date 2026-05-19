import os
from glob import glob

from setuptools import find_packages, setup

package_name = "tutorial_skill_executor"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/worlds", glob("worlds/*.*")),
        # Include launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Matteo MORELLI",
    maintainer_email="matteo.morelli@cea.fr",
    description="Example worlds for the CONVINCE overaching tutorial based on the work of Christian Henkel, christian.henkel2@de.bosch.com",
    license="Apache",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "run = tutorial_skill_executor.run:main",
        ],
    },
)
