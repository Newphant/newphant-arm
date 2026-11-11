from setuptools import find_packages, setup

package_name = 'newphant_arm_isaac'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='newphant',
    maintainer_email='3584046379@qq.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "test_node = newphant_arm_isaac.test_node:main",
            "dummy_control_node = newphant_arm_isaac.dummy_control_node:main",
            "slider_node = newphant_arm_isaac.slider_node:main",
            "control_node = newphant_arm_isaac.control_node:main",
            
            
        ],
    },
)
