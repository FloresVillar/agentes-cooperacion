from setuptools import setup
from glob import glob

package_name = 'agente_pkg'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Esau',
    maintainer_email='efloresv@uni.pe',
    description='Paquete ROS2 agente',
    license='Apache-2.0',

    entry_points={
        'console_scripts': [
            'mover_agente = agente_pkg.mover_agente:main',
        ],
    },

    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),

        ('share/' + package_name, ['package.xml']),

        ('share/' + package_name + '/launch',
            glob('launch/*.launch.py')),

        ('share/' + package_name + '/urdf',
            glob('urdf/*.xacro')),
    ],
)