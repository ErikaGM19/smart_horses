# main.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from game import Game
from ai import AIPlayer1, AIPlayer2
from player import HumanPlayer
from horse import Horse
import random
import time

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
        self.game = None
        self.casillas_resaltadas = []  # Para almacenar las casillas disponibles
        self.posicion_seleccionada = None  # Para almacenar la posición del caballo seleccionado
        self.ventana.mainloop()

    def cargar_imagenes(self):
        # Cargar imágenes y guardarlas en un diccionario
        self.imagenes["0"] = ImageTk.PhotoImage(Image.open("images/blanco.png").resize((self.tam_celda, self.tam_celda)))
        for i in range(1, 11):
            self.imagenes[f"{i}_point"] = ImageTk.PhotoImage(Image.open(f"images/{i}.png").resize((self.tam_celda, self.tam_celda)))
        self.imagenes["x2"] = ImageTk.PhotoImage(Image.open("images/x2.png").resize((self.tam_celda, self.tam_celda)))
        self.imagenes["white_horse"] = ImageTk.PhotoImage(Image.open("images/c1.png").resize((self.tam_celda, self.tam_celda)))
        self.imagenes["black_horse"] = ImageTk.PhotoImage(Image.open("images/c2.png").resize((self.tam_celda, self.tam_celda)))

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
            values=["Principiante", "Amateur", "Experto"],
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
            values=["Principiante", "Amateur", "Experto"],
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
            self.dificultad_ia1.config(state="disabled")
            self.dificultad_ia2.config(state="disabled")
            self.boton_iniciar.config(state=tk.NORMAL)
        elif modo == "Humano vs IA":
            self.boton_limpiar.config(state=tk.DISABLED)
            self.dificultad_ia1.config(state="readonly")
            self.dificultad_ia2.config(state="disabled")
            self.dificultad_ia1.bind("<<ComboboxSelected>>", self.verificar_seleccion)
            self.boton_iniciar.config(state=tk.DISABLED)
        elif modo == "IA 1 vs IA 2":
            self.boton_limpiar.config(state=tk.DISABLED)
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
        self.game = None
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
        # Obtener el modo y las dificultades
        modo = self.modo_juego.get()
        dificultad_ia1 = self.dificultad_ia1.get()
        dificultad_ia2 = self.dificultad_ia2.get()

        if modo != "Seleccione":
            self.game = Game(modo, dificultad_ia1, dificultad_ia2)
        else:
            messagebox.showerror("Error", "Debe seleccionar un modo de juego válido.")
            return

        if not self.game:
            messagebox.showerror("Error", "No se pudo crear el juego.")
            return

        # Cargar imágenes
        if not self.imagenes:
            self.cargar_imagenes()

        # Dibujar el tablero inicial
        self.dibujar_tablero()
        self.boton_limpiar.config(state=tk.NORMAL)
        self.mensaje_estado.config(text="Tablero generado correctamente.")
        # Deshabilitar opciones mientras el juego está en curso
        self.dificultad_ia1.config(state="disabled")
        self.dificultad_ia2.config(state="disabled")
        self.modo_juego.config(state="disabled")
        self.boton_iniciar.config(state="disabled")

        # Si es el turno de la IA, iniciar su movimiento
        if isinstance(self.game.players[self.game.current_turn], (AIPlayer1, AIPlayer2)):
            self.ventana.after(500, self.realizar_movimiento_ia)
        else:
            self.mensaje_estado.config(text=f"Turno del jugador {self.game.current_turn}")

    def realizar_movimiento_ia(self):
        if not self.game:
            return

        try:
            current_player = self.game.players[self.game.current_turn]
            horse = self.game.board.get_horse(self.game.current_turn)
        
            if isinstance(current_player, (AIPlayer1, AIPlayer2)):
                print(f"AI ({horse.color}) está buscando un movimiento...")
                move = current_player.get_move(self.game.board, horse)
                print(f"AI ({horse.color}) ha elegido mover a: {move}")
                if move:
                    self.game.update_state(horse, move)
                    self.actualizar_puntuaciones()
                    self.dibujar_tablero()
                else:
                    self.mensaje_estado.config(text=f"La IA {self.game.current_turn} no tiene movimientos válidos.")
                
                if self.game.is_game_over():
                    self.finalizar_juego()
                    return

                
                self.game.switch_turn()
                self.dibujar_tablero()  # Actualizar la interfaz y re-vincular el evento de clic
                
                if isinstance(self.game.players[self.game.current_turn], (AIPlayer1, AIPlayer2)):
                     self.ventana.after(500, self.realizar_movimiento_ia)
                else:
                    self.mensaje_estado.config(text=f"Turno del jugador {self.game.current_turn}")
            else:
                self.mensaje_estado.config(text=f"Turno del jugador {self.game.current_turn}")
        except Exception as e:
            print(f"Error durante el movimiento de la IA: {e}")
            self.mensaje_estado.config(text=f"Error durante el movimiento de la IA: {e}")

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
        if not self.game:
            return

        col = event.x // self.tam_celda
        fila = event.y // self.tam_celda

        if self.posicion_seleccionada is None:
            # Primera selección: seleccionar el caballo
            horse = self.game.board.get_horse(self.game.current_turn)
            if (fila, col) == horse.position:
                self.posicion_seleccionada = (fila, col)
                valid_moves = horse.get_valid_moves(self.game.board)
                self.resaltar_movimientos_posibles(valid_moves)
                self.mensaje_estado.config(text="Seleccione el destino.")
            else:
                self.mensaje_estado.config(text="Seleccione su caballo para mover.")
        else:
            # Segunda selección: seleccionar el destino
            horse = self.game.board.get_horse(self.game.current_turn)
            valid_moves = horse.get_valid_moves(self.game.board)
            if (fila, col) in valid_moves:
                self.game.update_state(horse, (fila, col))
                self.actualizar_puntuaciones()
                self.resaltar_movimientos_posibles([])  # Limpiar resaltados
                self.posicion_seleccionada = None
                if self.game.is_game_over():
                    self.dibujar_tablero()
                    self.finalizar_juego()
                else:
                    self.game.switch_turn()
                    self.dibujar_tablero()
                    if isinstance(self.game.players[self.game.current_turn], (AIPlayer1, AIPlayer2)):
                        self.ventana.after(500, self.realizar_movimiento_ia)
                    else:
                        self.mensaje_estado.config(text=f"Turno del jugador {self.game.current_turn}")
            else:
                self.mensaje_estado.config(text="Movimiento inválido. Seleccione un destino válido.")
                # Mantener las casillas resaltadas

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


    def finalizar_juego(self):
        winner_message = self.game.declare_winner()
        print(f"Finalizando juego: {winner_message}")
        self.mensaje_estado.config(text=winner_message)
        self.ventana.update_idletasks()
        self.canvas.unbind("<Button-1>")
        self.boton_iniciar.config(state=tk.NORMAL)
        self.modo_juego.config(state="readonly")
        messagebox.showinfo("Juego Terminado", winner_message)

    def actualizar_puntuaciones(self):
        # Actualizar las etiquetas de puntuaciones
        scores = self.game.get_scores()
        self.puntos_caballo_blanco.config(text=str(scores['white']))
        self.puntos_caballo_negro.config(text=str(scores['black']))
    
    def dibujar_tablero(self):
        if not self.game or not self.game.players:
            return

        # Limpiar resaltados anteriores
        for casilla in self.casillas_resaltadas:
            self.canvas.delete(casilla)
        self.casillas_resaltadas.clear()

        self.canvas.delete("all")
        for x in range(self.game.board.size):
            for y in range(self.game.board.size):
                x1, y1 = y * self.tam_celda, x * self.tam_celda
                x2, y2 = x1 + self.tam_celda, y1 + self.tam_celda

                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=1)

                cell_content = self.game.board.get_grid((x, y))

                if cell_content is None:
                    imagen = self.imagenes["0"]
                elif 'point' in str(cell_content):
                    imagen = self.imagenes[cell_content]
                elif cell_content == 'x2':
                    imagen = self.imagenes["x2"]
                elif cell_content == 'white_horse':
                    imagen = self.imagenes["white_horse"]
                elif cell_content == 'black_horse':
                    imagen = self.imagenes["black_horse"]
                else:
                    imagen = self.imagenes["0"]

                self.canvas.create_image(x1, y1, image=imagen, anchor="nw")
        
        # Vincular el evento de clic para el jugador actual si es humano
        self.canvas.unbind("<Button-1>")
        if isinstance(self.game.players[self.game.current_turn], HumanPlayer):
            self.canvas.bind("<Button-1>", self.seleccionar_casilla)
# Ejecutar la interfaz
InterfazTableroGUI()
