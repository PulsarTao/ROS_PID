from setuptools import setup

package_name = 'process'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='zhijiatao',
    maintainer_email='zhijiatao@outlook.com',
    description='Example package for processing ROS2 messages',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'process_node = process.process_node:main'
        ],
    },
)