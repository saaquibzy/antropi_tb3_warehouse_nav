from glob import glob
import os
from setuptools import setup

package_name = 'tb3_nav_demo'
data_files = [
    ('share/ament_index/resource_index/packages', ['resource/tb3_nav_demo']),
    (os.path.join('share', package_name), ['package.xml']),
]
for directory in ('launch', 'config', 'maps', 'rviz', 'scripts'):
    files = glob(os.path.join(directory, '*'))
    if files:
        data_files.append((os.path.join('share', package_name, directory), files))

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
)
