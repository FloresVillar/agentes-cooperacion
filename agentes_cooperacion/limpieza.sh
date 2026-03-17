#!/bin/bash
rm -rf install/
rm -rf log/
rm -rf build/
if ! command -v flake8 &> /dev/null; then # si no instalar
    sudo apt install -y python3-flake8 #sudo apt update && sudo apt install -y python3-flake8
fi
flake8 src/agente_pkg/ --select=E9,F63,F7,F82
if [ $? -eq 0 ];then
    echo "todo correcto"
else
    echo "errores"
fi