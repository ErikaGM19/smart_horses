import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import random
import time

class Main():
    def __init__(self):
        self.tablero = self.generar_tablero()
        self.turno_actual = "c1"  # Comienza el caballo blanco


    def generar_tablero(self):
        elementos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'x2', 'x2', 'x2', 'x2', 'c1', 'c2']
        total_casillas = 8 * 8
        ceros_necesarios = total_casillas - len(elementos)
        elementos.extend([0] * ceros_necesarios)
        random.shuffle(elementos)
        matriz = [elementos[i * 8:(i + 1) * 8] for i in range(8)]
        return matriz

class InterfazTableroGUI:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Smart Horses")
        self.ventana.geometry('900x650')
        self.ventana.configure(bg='#82dad3')
        self.crear_frames()
        self.crear_cuadricula()
        self.crear_widgets()
        self.imagenes = {}
        self.juego = None
        self.casillas_resaltadas = []  # Para almacenar las casillas disponibles
        self.posicion_seleccionada = None  # Para almacenar la posición del caballo seleccionado
        self.ventana.mainloop()
        
    def cargar_imagenes(self):
        # Cargar imágenes y guardarlas en un diccionario
        self.imagenes["0"] = ImageTk.PhotoImage(Image.open("images/blanco.png").resize((self.tam_celda, self.tam_celda)))
        for i in range(1, 11):
            self.imagenes[str(i)] = ImageTk.PhotoImage(Image.open(f"images/{i}.png").resize((self.tam_celda, self.tam_celda)))
        self.imagenes["x2"] = ImageTk.PhotoImage(Image.open("images/x2.png").resize((self.tam_celda, self.tam_celda)))
        self.imagenes["c1"] = ImageTk.PhotoImage(Image.open("images/c1.png").resize((self.tam_celda, self.tam_celda)))
        self.imagenes["c2"] = ImageTk.PhotoImage(Image.open("images/c2.png").resize((self.tam_celda, self.tam_celda)))

    def crear_frames(self):
        self.content_frame = tk.Frame(self.ventana, bg='#82dad3')
        self.content_frame.pack(fill='both', expand=True) 
        self.frame_cuadricula = tk.Frame(self.content_frame, bg='#82dad3')
        self.frame_cuadricula.pack(pady=10)
        self.frame_botones = tk.Frame(self.content_frame, bg='#6f96b4')
        self.frame_botones.pack(side=tk.BOTTOM, fill='x')
        self.frame_botones.configure(height=100)

    def crear_cuadricula(self):
        self.tam_celda = 50
        self.ancho_tablero = self.tam_celda * 8  
        self.alto_tablero = self.tam_celda * 8  
        self.canvas = tk.Canvas(
            self.frame_cuadricula, width=self.ancho_tablero, height=self.alto_tablero, bg='white'
        )
        self.canvas.pack()

    def crear_widgets(self):
        tipo_fuente = ('Arial Black', 12)
        frame_menus = tk.Frame(self.frame_botones, bg='#6f96b4')
        frame_menus.pack(side=tk.LEFT, padx=20, pady=20)
        frame_modo_juego = tk.Frame(frame_menus, bg='#6f96b4')
        frame_modo_juego.pack(side=tk.LEFT, padx=20)

        self.label_modo_juego = tk.Label(
            frame_modo_juego,
            text="Seleccione modo de juego:",
            bg='#6f96b4',
            font=tipo_fuente
        )
        self.label_modo_juego.pack()

        self.modo_juego_seleccionado = tk.StringVar(value="Seleccione")
        self.modo_juego = ttk.Combobox(
            frame_modo_juego,
            textvariable=self.modo_juego_seleccionado,
            values=["Humano vs Humano", "Humano vs IA", "IA 1 vs IA 2"],
            state="readonly"
        )
        self.modo_juego.pack()
        self.modo_juego.bind("<<ComboboxSelected>>", self.modo_juego_seleccionado_callback)

        # ComboBox para la dificultad de IA1
        self.label_dificultad_ia1 = tk.Label(
            frame_modo_juego,
            text="Dificultad IA 1:",
            bg='#6f96b4',
            font=tipo_fuente
        )
        self.label_dificultad_ia1.pack()
        self.dificultad_ia1 = ttk.Combobox(
            frame_modo_juego,
            values=["Pricipiante", "Amateur", "Experto"],
            state="disabled"
        )
        self.dificultad_ia1.pack()

        # ComboBox para la dificultad de IA2
        self.label_dificultad_ia2 = tk.Label(
            frame_modo_juego,
            text="Dificultad IA 2:",
            bg='#6f96b4',
            font=tipo_fuente
        )
        self.label_dificultad_ia2.pack()
        self.dificultad_ia2 = ttk.Combobox(
            frame_modo_juego,
            values=["Pricipiante", "Amateur", "Experto"],
            state="disabled"
        )
        self.dificultad_ia2.pack()
        
        frame_iniciar = tk.Frame(self.frame_botones, bg='#6f96b4')
        frame_iniciar.pack(side=tk.RIGHT, padx=20, pady=20)
        
        self.boton_limpiar = tk.Button(
            frame_iniciar,
            text="Limpiar",
            font=tipo_fuente,
            bg='#008CBA',
            fg='white',
            activebackground='#007bb5',
            width=15,
            command=self.limpiar_tablero,
            state=tk.DISABLED 
        )
        self.boton_limpiar.pack(side=tk.LEFT, padx=5)

        self.boton_iniciar = tk.Button(
            frame_iniciar,
            text="Iniciar Juego",
            font=tipo_fuente,
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            width=15,
            command=self.iniciar_juego,
            state="disabled"
        )
        self.boton_iniciar.pack(side=tk.LEFT, padx=5)

        self.mensaje_estado = tk.Label(
            self.content_frame,
            text="",
            font=tipo_fuente,
            bg='#82dad3'
        )
        self.mensaje_estado.pack(side=tk.BOTTOM, fill='x')

        self.label_puntos_caballo_blanco = tk.Label(
            self.content_frame,
            text="Puntos Caballo Blanco: ",
            bg='#82dad3',
            font=tipo_fuente
        )

        self.label_puntos_caballo_blanco.place(x=10, y=10)
        self.puntos_caballo_blanco = tk.Label(
            self.content_frame,
            text="0",
            font=tipo_fuente,
            bg='#6f96b4'
        )

        self.puntos_caballo_blanco.place(x=110, y=40)  
        
        self.label_puntos_caballo_negro = tk.Label(
            self.content_frame,
            text="Puntos Caballo Negro: ",
            bg='#82dad3',
            font=tipo_fuente
        )

        self.label_puntos_caballo_negro.place(x=10, y=110)
        self.puntos_caballo_negro = tk.Label(
            self.content_frame,
            text="0",
            font=tipo_fuente,
            bg='#6f96b4'
        )

        self.puntos_caballo_negro.place(x=110, y=150)  

    def modo_juego_seleccionado_callback(self, event):
        modo = self.modo_juego.get()
        # Habilitar o deshabilitar campos de dificultad según el modo de juego seleccionado
        if modo == "Humano vs Humano":
            self.boton_limpiar.config(state=tk.DISABLED)
            self.modo_juego.config(state="disabled")
            self.dificultad_ia1.config(state="disabled")
            self.dificultad_ia2.config(state="disabled")
            self.boton_iniciar.config(state=tk.NORMAL)
        elif modo == "Humano vs IA":
            self.boton_limpiar.config(state=tk.DISABLED)
            self.modo_juego.config(state="disabled")
            self.dificultad_ia1.config(state="readonly")
            self.dificultad_ia2.config(state="disabled")
            self.dificultad_ia1.bind("<<ComboboxSelected>>", self.verificar_seleccion)
            self.boton_iniciar.config(state=tk.DISABLED)
        elif modo == "IA 1 vs IA 2":
            self.boton_limpiar.config(state=tk.DISABLED)
            self.modo_juego.config(state="disabled")
            self.dificultad_ia1.config(state="readonly")
            self.dificultad_ia2.config(state="readonly")
            self.dificultad_ia1.bind("<<ComboboxSelected>>", self.verificar_seleccion)
            self.dificultad_ia2.bind("<<ComboboxSelected>>", self.verificar_seleccion)
            self.boton_iniciar.config(state=tk.DISABLED)

    def verificar_seleccion(self, event):
        # Verifica que se hayan seleccionado las dificultades necesarias antes de habilitar el botón Iniciar
        modo = self.modo_juego.get()
        if modo == "Humano vs IA" and self.dificultad_ia1.get():
            self.boton_iniciar.config(state=tk.NORMAL)
        elif modo == "IA 1 vs IA 2" and self.dificultad_ia1.get() and self.dificultad_ia2.get():
            self.boton_iniciar.config(state=tk.NORMAL)

    def limpiar_tablero(self):
        self.canvas.delete("all")  
        self.juego = Main() 
        self.modo_juego_seleccionado.set("Seleccione")
        self.modo_juego.config(state=tk.NORMAL)
        self.boton_iniciar.config(state=tk.DISABLED)
        self.boton_limpiar.config(state=tk.DISABLED)
        self.dificultad_ia1.set("")
        self.dificultad_ia1.config(state="disabled")
        self.dificultad_ia2.set("")
        self.dificultad_ia2.config(state="disabled")
        self.mensaje_estado.config(text="")
        self.puntos_caballo_blanco.config(text="0")
        self.puntos_caballo_negro.config(text="0")
    
  
    def iniciar_juego(self):
        self.cargar_imagenes()
        self.juego = Main()  
        self.dibujar_tablero()
        self.boton_limpiar.config(state=tk.NORMAL)
        self.mensaje_estado.config(text="Tablero generado correctamente.")
        self.dificultad_ia1.config(state="disabled")
        self.dificultad_ia2.config(state="disabled")

    def obtener_movimientos_posibles(self, fila, columna):
        movimientos = []
        # Todos los posibles movimientos del caballo
        patrones = [
            (-2, -1), (-2, 1),  # Arriba
            (-1, -2), (-1, 2),  # Izquierda/Derecha arriba
            (1, -2), (1, 2),    # Izquierda/Derecha abajo
            (2, -1), (2, 1)     # Abajo
        ]
        
        for df, dc in patrones:
            nueva_fila = fila + df
            nueva_col = columna + dc
            if 0 <= nueva_fila < 8 and 0 <= nueva_col < 8:
                # Verifica que la casilla destino no tenga otro caballo
                if self.juego.tablero[nueva_fila][nueva_col] != "c1" and \
                   self.juego.tablero[nueva_fila][nueva_col] != "c2":
                    movimientos.append((nueva_fila, nueva_col))
        return movimientos

    def resaltar_movimientos_posibles(self, movimientos):
        # Limpia resaltados anteriores
        for casilla in self.casillas_resaltadas:
            self.canvas.delete(casilla)
        self.casillas_resaltadas.clear()

        # Resalta las nuevas casillas disponibles
        for fila, col in movimientos:
            x1 = col * self.tam_celda
            y1 = fila * self.tam_celda
            x2 = x1 + self.tam_celda
            y2 = y1 + self.tam_celda
            # Crear un rectángulo semitransparente verde
            resaltado = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill='#00FF00',
                stipple='gray50',
                tags='resaltado'
            )
            self.casillas_resaltadas.append(resaltado)

    def seleccionar_casilla(self, event):
        col = event.x // self.tam_celda
        fila = event.y // self.tam_celda
        
        # Si no hay una pieza seleccionada
        if self.posicion_seleccionada is None:
            # Verifica si la casilla contiene un caballo y si es su turno
            if self.juego.tablero[fila][col] == self.juego.turno_actual:
                self.posicion_seleccionada = (fila, col)
                movimientos = self.obtener_movimientos_posibles(fila, col)
                self.resaltar_movimientos_posibles(movimientos)
                self.mensaje_estado.config(text=f"Caballo seleccionado. Seleccione destino.")
        else:
            # Verifica si la casilla destino es un movimiento válido
            movimientos = self.obtener_movimientos_posibles(self.posicion_seleccionada[0], 
                                                          self.posicion_seleccionada[1])
            if (fila, col) in movimientos:
                # Realiza el movimiento
                fila_origen, col_origen = self.posicion_seleccionada
                pieza = self.juego.tablero[fila_origen][col_origen]
                self.juego.tablero[fila_origen][col_origen] = 0
                self.juego.tablero[fila][col] = pieza
                
                # Cambiar turno
                self.juego.turno_actual = "c2" if self.juego.turno_actual == "c1" else "c1"
                
                # Actualiza el tablero
                self.dibujar_tablero()
                self.mensaje_estado.config(text=f"Turno del {'caballo negro' if self.juego.turno_actual == 'c2' else 'caballo blanco'}")
            else:
                self.mensaje_estado.config(text="Movimiento inválido. Intente nuevamente.")
            
            # Limpia la selección y los resaltados
            self.posicion_seleccionada = None
            self.resaltar_movimientos_posibles([])


    def dibujar_tablero(self):
        self.canvas.delete("all")
        for i, fila in enumerate(self.juego.tablero):
            for j, valor in enumerate(fila):
                x1, y1 = j * self.tam_celda, i * self.tam_celda
                x2, y2 = x1 + self.tam_celda, y1 + self.tam_celda

                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=1)

                if valor == 0:
                    imagen = self.imagenes["0"]
                elif valor in range(1, 11):
                    imagen = self.imagenes[str(valor)]
                elif valor == "x2":
                    imagen = self.imagenes["x2"]
                elif valor == "c1":
                    imagen = self.imagenes["c1"]
                elif valor == "c2":
                    imagen = self.imagenes["c2"]

                self.canvas.create_image(x1, y1, image=imagen, anchor="nw")
        
        # Vincular el evento de clic
        self.canvas.bind("<Button-1>", self.seleccionar_casilla)

# Ejecutar la interfaz
InterfazTableroGUI()
