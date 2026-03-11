from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import xacro


def generate_launch_description():
    pkg_share = get_package_share_directory('agente_pkg')

    urdf_file = os.path.join(pkg_share, 'urdf', 'agente.xacro')
    robot_desc = xacro.process_file(urdf_file).toxml()
    rviz_config_file = os.path.join(pkg_share, 'rviz', 'agente.rviz')

    return LaunchDescription([
        # Publica el URDF y TF
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_desc}]
        ),
        # Publica estados de joints (sliders para mover)
        Node(
            package='agente_pkg',
            executable='mover_agente',
            name='mover_agente',
            output='screen'
        ),
        # Abre RViz
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_file]
        )
    ])
