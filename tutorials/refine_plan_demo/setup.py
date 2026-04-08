from setuptools import find_packages, setup
from glob import glob
import os

package_name = "refine_plan_demo"


def package_files(directory_list):
    """Glob wasn't working how I intended, so I took this nice function from:
    https://answers.ros.org/question/397319/how-to-copy-folders-with-subfolders-to-package-installation-path/
    """
    paths_dict = {}
    data_files = []
    for directory in directory_list:
        for path, _, filenames in os.walk(directory):

            for filename in filenames:
                file_path = os.path.join(path, filename)
                install_path = os.path.join("share", package_name, path)
                if install_path in paths_dict.keys():
                    paths_dict[install_path].append(file_path)
                else:
                    paths_dict[install_path] = [file_path]

    for key in paths_dict.keys():
        data_files.append((key, paths_dict[key]))
    return data_files


setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=package_files(["params/"])  # Params needed to send over the policy
    + [
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (
            os.path.join("share", package_name, "launch"),
            glob(os.path.join("launch", "*launch.[pxy][yma]*")),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="charlie",
    maintainer_email="me@charliestreet.net",
    description="A REFINE-PLAN demo in Pyrobosim for the CONVINCE project.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": ["policy_executor = refine_plan_demo.policy_executor:main"],
    },
)
