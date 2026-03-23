from glob import glob

from setuptools import find_packages, setup

package_name = "tutorial_sim"

setup(
    name=package_name,
    version="1.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/worlds", glob("worlds/*.*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Christian Henkel",
    maintainer_email="christian.henkel2@de.bosch.com",
    description="Example worlds for the CONVINCE overaching tutorial",
    license="Apache",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "run = tutorial_sim.run:main",
        ],
    },
)
