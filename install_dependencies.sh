#!/bin/bash

# Verificar si el archivo requirements.txt existe
if [ ! -f requirements.txt ]; then
    echo "El archivo requirements.txt no existe."
    exit 1
fi

# Instalar las dependencias
echo "Instalando dependencias desde requirements.txt..."
pip install -r requirements.txt

# Verificar si la instalación fue exitosa
if [ $? -eq 0 ]; then
    echo "Dependencias instaladas correctamente."
else
    echo "Hubo un error instalando las dependencias."
    exit 1
fi
