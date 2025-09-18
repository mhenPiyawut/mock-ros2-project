from setuptools import setup

package_name = 'mock_ros2_project'

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
    maintainer='user',
    maintainer_email='user@example.com',
    description='Mock ROS2 project with example code',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publisher_node = mock_ros2_project.publisher_node:main',
            'subscriber_node = mock_ros2_project.subscriber_node:main',
            'service_server = mock_ros2_project.service_server:main',
            'service_client = mock_ros2_project.service_client:main',
            'action_server = mock_ros2_project.action_server:main',
            'action_client = mock_ros2_project.action_client:main',
            'parameter_node = mock_ros2_project.parameter_node:main',
            'timer_node = mock_ros2_project.timer_node:main',
        ],
    },
)
