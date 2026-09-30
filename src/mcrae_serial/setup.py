from setuptools import find_packages, setup

package_name = 'mcrae_serial'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='watergold12',
    maintainer_email='techieman7@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'serial_bridge = mcrae_serial.serial_bridge:main',
            'command_sender = mcrae_serial.command_sender:main',
            'command_receiver = mcrae_serial.command_receiver:main',
        ],
    },
)
