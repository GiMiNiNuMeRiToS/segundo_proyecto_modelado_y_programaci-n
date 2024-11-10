# segundo_proyecto_modelado_y_programaci-n
Programa que codifica texto en una imagen
# Como ejecutar el script

Este script usa las siguientes librerias:
- PIL: Que se puede instalar con:
```bash
pip install pillow
```

Para poder ejecutar este script, debe hacerse desde terminal, teniendo las siguientes opciones para ejecutar:

- Para ocultar:
```bash
python script.py -h archivo_mensaje ruta_imagen nombre_archivo_salida
```
Esta opción te permitira insertar la ruta de un archivo que contenga el mensaje a ocultar, una ruta de una imagen con extensión .png y un nombre para ponerle a la imagen de salida, generando una imagen nueva pero con el mensaje oculto, esta imagen nueva, se guardara en el directorio donde se encuentre el archivo script.py con el nombre proporcionado.

- Para revelar:
```bash
python script.py -u ruta_imagen.png nombre_archivo_salida
```
Esta opción mostrara el mensaje encontrado en la imagen, ademas te dira la longitud del mensaje.
Se le debe pasar la imagen png con el mensaje oculto y el nombre del archivo de salida, generandote un archivo .txt con el nombre proporcionado, este archivo generado se guardara en el directorio donde se encuentre el archivo script.py 
