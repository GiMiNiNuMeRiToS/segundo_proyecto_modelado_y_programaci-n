import os
import pytest
from PIL import Image
from script import ocultar_mensaje, extraer_mensaje, calcularCifrado

def setup_module(module):
    # Se ejecuta al inicio de la ejecución del módulo
    imagen=Image.new("RGBA", (100, 100), "white")
    imagen.save("imagenprueba.png")

def teardown_module(module):
    # Se ejecuta al final de la ejecución del módulo
    os.remove("imagenprueba.png")
    for archivo in ["imagen_ocultada.png","imagen_oculta.png","imagen_larga.png"]:
        if os.path.exists(archivo):
            os.remove(archivo)

def test_creacion_archivo_salida():
    """Prueba que el archivo de salida se cree correctamente."""
    ocultar_mensaje("imagen_prueba.png", "Hola", "imagen_ocultada")
    assert os.path.exists("imagen_ocultada.png"), "El archivo de salida no se creó."

def test_recuperacion_mensaje():
    """Prueba que el mensaje oculto se pueda recuperar correctamente."""
    mensaje_original = "Hola mundo"
    ocultar_mensaje("imagen_prueba.png", mensaje_original, "imagen_oculta")
    extraer_mensaje("imagen_oculta.png", "mensaje_revelado")
    with open("mensaje_revelado.txt", "r") as archivo:
        mensaje_revelado = archivo.read()
    assert mensaje_revelado == mensaje_original, "El mensaje revelado no coincide con el original."

def test_largo_mensaje():
    """Prueba que el mensaje oculto se pueda recuperar correctamente."""
    mensaje_largo = "A"*10000
    resultado=ocultar_mensaje("imagen_prueba.png", mensaje_largo, "imagen_larga")
    extraer_mensaje("imagen_oculta.png", "mensaje_largo")
    assert resultado =="El mensaje es muy largo para ser ocultado en la imagen", "No se detectó que el mensaje era muy largo."