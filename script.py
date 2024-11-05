from PIL import Image
import sys

# Funcion que consigue el mensaje a ocultar dentro de un archivo.
def extraer_mensaje_archivo(ruta):
    with open(ruta, "r") as archivo:
        mensaje = archivo.read()
    return f'"{mensaje}"'

def calcularCifrado(ancho, alto, longitudtex):
    numeropixel=ancho*alto
    espaciodisponiblebits=numeropixel*4
    espaciobytes=espaciodisponiblebits//8
    if longitudtex>espaciobytes:    
        return False
    else:
        return True

def ocultar_mensaje(imagen,mensaje,nombre_archivo_salida):
    
    try:
        imag = Image.open(imagen, formats=["PNG", "JPEG"])
    except TypeError as e:
        print(e)
        print("Formato no valido")

    # Convertimos el mensaje en binario y añadimos la longitud del mensaje
    mensaje_binario = ''.join([format(ord(i), '08b') for i in mensaje])
    longitud_mensaje = len(mensaje_binario) // 8  # Convertimos a bytes
    ancho, alto = imag.width, imag.height

    if calcularCifrado(ancho, alto, longitud_mensaje):
        if imag.format == "PNG":
            ocultar_mensaje_png(imagen, mensaje, nombre_archivo_salida)
        elif imag.format == "JPG":
            ocultar_mensaje_jpg(imagen, mensaje, nombre_archivo_salida)
    else:
        print("Tamaño de imagen no valido")

# Función para ocultar un mensaje usando LSB.
def ocultar_mensaje_png(imagen, mensaje, nombre_archivo_salida):

    img = Image.open(imagen, formats=["PNG"])
    
    # Convertimos el mensaje en binario y añadimos la longitud del mensaje
    mensaje_binario = ''.join([format(ord(i), '08b') for i in mensaje])
    longitud_mensaje = len(mensaje_binario) // 8  # Convertimos a bytes
    # Agregamos los primeros dos bytes que contienen la longitud del mensaje
    longitud_binario = format(longitud_mensaje, '016b')
    # Añadimos el byte terminador 'x00' (00000000 en binario)
    mensaje_completo = longitud_binario + mensaje_binario + '00000000'
    
    # Convertir la imagen a modo RGB si tiene transparencia  
    
    img = img.convert("RGBA")
    
    imagen_nueva = img.copy()  # Copiar la imagen para modificarla
    indice = 0
    ancho, alto = img.width, img.height

    # Ocultar el mensaje
    for x in range(ancho):
        for y in range(alto):
            pix = list(imagen_nueva.getpixel((x, y)))  # Obtener el valor RGB de cada píxel
            for canal in range(3):  # Modificar solo los 3 primeros canales (R, G, B)
                if indice < len(mensaje_completo):
                    valor_actual = pix[canal]
                    valor_mascarado = (valor_actual >> 1) << 1  # Poner a 0 el bit menos significativo
                    bit_mensaje = int(mensaje_completo[indice])  # Obtener el bit del mensaje
                    nuevo_valor = valor_mascarado | bit_mensaje  # Insertar el bit
                    pix[canal] = nuevo_valor  # Actualizar el valor del canal
                    indice += 1
            imagen_nueva.putpixel((x, y), tuple(pix))  # Actualizar el píxel con los nuevos valores
            if indice >= len(mensaje_completo):  # Terminar cuando el mensaje esté completamente oculto
                break
        if indice >= len(mensaje_completo):
            break
    imagen_nueva.save(f"{nombre_archivo_salida}.png", "PNG")  # Guardar la imagen con el mensaje oculto

def ocultar_mensaje_jpg(imagen, mensaje, nombre_archivo_salida):
    
    img = Image.open(imagen, formats=["JPEG"])

    # Convertimos el mensaje en binario y añadimos la longitud del mensaje
    mensaje_binario = ''.join([format(ord(i), '08b') for i in mensaje])
    longitud_mensaje = len(mensaje_binario) // 8  # Convertimos a bytes
    # Agregamos los primeros dos bytes que contienen la longitud del mensaje
    longitud_binario = format(longitud_mensaje, '016b')
    # Añadimos el byte terminador 'x00' (00000000 en binario)
    mensaje_completo = longitud_binario + mensaje_binario + '00000000'
    
    # Convertir la imagen a modo RGB si tiene transparencia  
    
    img=img.convert("RGB")
    
    imagen_nueva = img.copy()  # Copiar la imagen para modificarla
    indice = 0
    ancho, alto = img.width, img.height

    # Ocultar el mensaje
    for x in range(ancho):
        for y in range(alto):
            pix = list(imagen_nueva.getpixel((x, y)))  # Obtener el valor RGB de cada píxel
            for canal in range(3):  # Modificar solo los 3 primeros canales (R, G, B)
                if indice < len(mensaje_completo):
                    valor_actual = pix[canal]
                    valor_mascarado = (valor_actual >> 1) << 1  # Poner a 0 el bit menos significativo
                    bit_mensaje = int(mensaje_completo[indice])  # Obtener el bit del mensaje
                    nuevo_valor = valor_mascarado | bit_mensaje  # Insertar el bit
                    pix[canal] = nuevo_valor  # Actualizar el valor del canal
                    indice += 1
            imagen_nueva.putpixel((x, y), tuple(pix))  # Actualizar el píxel con los nuevos valores
            if indice >= len(mensaje_completo):  # Terminar cuando el mensaje esté completamente oculto
                break
        if indice >= len(mensaje_completo):
            break
    imagen_nueva.save(f"{nombre_archivo_salida}.jpg", "JPG")  # Guardar la imagen con el mensaje oculto

# Función para extraer la longitud del mensaje de los primeros 16 bits
def extraer_longitud_mensaje(imagen):
    img = Image.open(imagen)
    
    # Convertir la imagen a modo RGB si tiene transparencia
    img=img.convert("RGBA")
    
    longitud_binario = ""
    contador = 0

    # Extraer los primeros 16 bits para obtener la longitud del mensaje
    for x in range(img.width):
        for y in range(img.height):
            pix = img.getpixel((x, y))
            for canal in range(3):  # Solo revisar los canales R, G, B
                longitud_binario += str(pix[canal] & 1)  # Extraer el bit menos significativo
                contador += 1
                if contador == 16:  # Detenerse cuando se tienen los 16 bits de longitud
                    return int(longitud_binario, 2)


# Función para extraer el mensaje oculto hasta encontrar 'x00'
def extraer_mensaje(ruta_imagen, nombre_archivo_salida):
    img = Image.open(ruta_imagen, formats=["PNG"])
    
    # Convertir la imagen a modo RGB si tiene transparencia
    img=img.convert("RGBA")
    
    mensaje_binario = ""
    longitud_mensaje = extraer_longitud_mensaje(ruta_imagen)
    contador = 0

    # Extraer el mensaje de los bits menos significativos de cada píxel
    for x in range(img.width):
        for y in range(img.height):
            pix = img.getpixel((x, y))
            for canal in range(3):
                mensaje_binario += str(pix[canal] & 1)  # Extraer el bit menos significativo
                contador += 1
                if contador == (longitud_mensaje * 8) + 16:  # 16 bits para la longitud + el mensaje
                    mensaje_binario = mensaje_binario[16:16 + longitud_mensaje * 8]  # Saltar los bits de longitud
                    #return ''.join([chr(int(mensaje_binario[i:i + 8], 2)) for i in range(0, len(mensaje_binario), 8)])  # Convertir a texto
                    mensaje = ''.join([chr(int(mensaje_binario[i:i + 8], 2)) for i in range(0, len(mensaje_binario), 8)])  # Convertir a texto
                    with open(f"{nombre_archivo_salida}.txt", "w") as archivo:
                        archivo.write(mensaje)
                    return mensaje

if __name__ == "__main__":

    # Ocultar mensaje: python script.py -h archivo_mensaje ruta_imagen nombre_archivo_salida
    if sys.argv[1] == "-h":
        mensaje = extraer_mensaje_archivo(sys.argv[2])
        ocultar_mensaje(sys.argv[3], mensaje, sys.argv[4])
        print(f"Mensaje ocultado en {sys.argv[4]}.png")

    # Extraer mensaje: python script.py -u ruta_imagen nombre_archivo_salida
    elif sys.argv[1] == "-u":
        salida = extraer_mensaje(sys.argv[2], sys.argv[3])
        longitud = extraer_longitud_mensaje(sys.argv[2])
        print(f"Longitud del mensaje: {longitud}")
        print(f"Mensaje extraido: {salida}")
        
    
    else:
        print("Argumentos incorrectos.")
        print("Ejemplos de uso:")
        print("Ocultar mensaje: python script.py -h archivo_mensaje ruta_imagen nombre_archivo_salida")
        print("Extraer mensaje: python script.py -u ruta_imagen.png nombre_archivo_salida")
        sys.exit(1)

