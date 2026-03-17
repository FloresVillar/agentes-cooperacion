#!/bin/bash

CARRO_NUM=$1
VEL_LINEAL=$2
GRADOS=$3

# Operacion matematica en caliente
PI=3.14159
RAD=$(bc <<< "scale=4; $GRADOS * $PI / 180")
# ejemplo de ejecucion:   bash ordenes.sh 3 0.0 0
echo "Comando: Carro $CARRO_NUM a $VEL_LINEAL m/s con timon en $GRADOS grados ($RAD rad)"

# Inyeccion al topico usando el numero de carro para construir el namespace
ros2 topic pub --once /carro$CARRO_NUM/cmd_vel geometry_msgs/msg/Twist "{
    linear: {x: $VEL_LINEAL, y: 0.0, z: 0.0}, 
    angular: {x: 0.0, y: 0.0, z: $RAD}
}"