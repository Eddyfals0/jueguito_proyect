#!/bin/bash

# Imprimir información de depuración
echo "Configurando entorno de Render"
echo "Directorio actual: $(pwd)"
echo "Contenido del directorio:"
ls -la

# Verificar si existen las imágenes en la carpeta assets
if [ -d "assets" ]; then
  echo "Copiando archivos de la carpeta assets a la raíz"
  cp assets/* .
fi

# Listar el contenido de la carpeta después de la configuración
echo "Contenido del directorio después de la configuración:"
ls -la

echo "Configuración completada" 