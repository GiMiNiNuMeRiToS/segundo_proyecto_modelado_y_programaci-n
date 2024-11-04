import tkinter as tk
from tkinter import filedialog, messagebox,ttk
from script import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Steganografía en Imágenes")
        self.geometry("500x300")

        self.mostar_ventana_principal()
    def mostar_ventana_principal(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Seleccione una accion:").pack(pady=10)
        opciones = ["Ocultar Mensaje", "Extraer Mensaje", "Salir"]
        self.accion = tk.StringVar(self)
        self.accion.set(opciones[0])

        dropdown=tk.OptionMenu(self,self.accion,*opciones)
        dropdown.pack(pady=10)

        tk.Button(self, text="Confirmar", command=self.ejucutar_accion_seleccionada).pack(pady=20)

    def ejucutar_accion_seleccionada(self):
        opcion=self.accion.get()
        if opcion=="Ocultar Mensaje":
            self.mostrar_pantalla_ocultar()
        elif opcion=="Extraer Mensaje":
            self.mostrar_pantalla_extraer()
        elif opcion=="Salir":
            self.quit()

    def mostrar_pantalla_ocultar(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Escribe el nombre de la imagen con .png o .jpg :").pack(pady=10)
        self.ruta_imagen = tk.Entry(self,width=50)
        self.ruta_imagen.pack(pady=10)

        tk.Label(self, text="Escribe la ruta de tu archivo .txt").pack(pady=10)
        self.ruta_archivo = tk.Entry(self,width=50)
        self.ruta_archivo.pack(pady=10)

        tk.Label(self, text="Nombre de la imagen de salida").pack(pady=10)
        self.nombre_salida = tk.Entry(self,width=50)
        self.nombre_salida.pack(pady=10)

        tk.Button(self, text="Ocultar Mensaje", command=self.ocultar_mensaje).pack(pady=20)
        tk.Button(self, text="Volver", command=self.mostar_ventana_principal).pack(pady=20)

    def ocultar_mensaje(self):
        ruta_imagen=self.ruta_imagen.get()
        ruta_archivo=self.ruta_archivo.get()
        nombre_salida=self.nombre_salida.get()
        if ruta_imagen and ruta_archivo and nombre_salida:
            try:
                mensaje=extraer_mensaje_archivo(ruta_archivo)
                ocultar_mensaje(ruta_imagen,mensaje,nombre_salida)
                messagebox.showinfo("Mensaje Ocultado", f"Mensaje ocultado en {nombre_salida}.png")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrio un error: {e}")
        else:
            messagebox.showwarning("Error", "Complete todos los campos")

    def mostrar_pantalla_extraer(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Escribe el nombre de la imagen con .png o .jpg :").pack(pady=10)
        self.ruta_imagen = tk.Entry(self,width=50)
        self.ruta_imagen.pack(pady=10)

        tk.Label(self, text="Nombre del archivo de salida").pack(pady=10)
        self.nombre_salida = tk.Entry(self,width=50)
        self.nombre_salida.pack(pady=10)

        tk.Button(self, text="Extraer Mensaje", command=self.extraer_mensaje).pack(pady=20)
        tk.Button(self, text="Volver", command=self.mostar_ventana_principal).pack(pady=20)
        
    def extraer_mensaje(self):
        ruta_imagen=self.ruta_imagen.get()
        nombre_salida=self.nombre_salida.get()
        if ruta_imagen and nombre_salida:
            try:
                salida=extraer_mensaje(ruta_imagen,nombre_salida)
                longitud_mensaje = extraer_longitud_mensaje(ruta_imagen)
                messagebox.showinfo("Mensaje Extraido", f"Mensaje: {salida}")
                messagebox.showinfo("Mensaje Extraido", f"Longitud del mensaje: {longitud_mensaje}")
                messagebox.showinfo("Mensaje Guardado", f"Mensaje ocultado en {nombre_salida}.txt")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrio un error: {e}")
        else:
            messagebox.showwarning("Error", "Complete todos los campos")
if __name__ == "__main__":
    app=App()
    app.mainloop()