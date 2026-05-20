import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'monitors_anchoring_interface'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include launch files
        ('share/'+ package_name + '/launch/cfg/', ['launch/cfg/params.yaml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Matteo MORELLI',
    maintainer_email='matteo.morelli@cea.fr',
    description='Component that triggers the anchoring''s knowledge update process when a property violation is detected by monitors',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "run = monitors_anchoring_interface.run:main",
        ],
    },
)
