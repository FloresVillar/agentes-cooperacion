#!/bin/bash
chmod +x src/agente_pkg/agente_pkg/mover_agente.py
source /opt/ros/kilted/setup.bash
colcon build 
source install/setup.bash
colcon test
colcon test-result --all
ros2 launch agente_pkg agente_sim.launch.py