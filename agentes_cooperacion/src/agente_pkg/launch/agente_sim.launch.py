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

    ld = LaunchDescription()

    for i in [1, 2, 3]:
        ns = f'carro{i}'
        prefijo = f'{ns}/'
        offset_y = str(float(i - 2) * 1.5)

        # 1. PROCESAR XACRO PASANDO EL ARGUMENTO
        robot_desc_config = xacro.process_file(urdf_file, mappings={'prefix': prefijo}).toxml()

        ld.add_action(Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            namespace=ns,
            parameters=[{'robot_description': robot_desc_config}] # Quitamos frame_prefix, ya va en el XML
        ))

        # 2. El clavo estático se mantiene igual
        ld.add_action(Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', offset_y, '0', '0', '0', '0', 'map', f'{prefijo}base_link']
        ))

        # 3. Tu script de movimiento
        ld.add_action(Node(
            package='agente_pkg',
            executable='mover_agente',
            namespace=ns,
            output='screen'
        ))

    # 4. RViz
    ld.add_action(Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_file]
    ))

    return ld