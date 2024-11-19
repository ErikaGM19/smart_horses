import copy

class Nodo:
    def __init__(self, estado, utilidad, minmax, tablero, estadoContrincante, nodo_padre=None, profundidad = 0):
        self.estado = estado
        self.nodo_padre = nodo_padre
        self.hijos = []
        self.profundidad= profundidad
        self.utilidad = utilidad
        self.minmax = minmax
        self.tablero = copy.deepcopy(tablero) 
        self.estadoContrincante = estadoContrincante

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)
    def obtener_hijos(self):
        return self.hijos
    def agregarPosicionTablero(self):
        # Copy the parent's board if it exists
        if self.nodo_padre:
            self.tablero = copy.deepcopy(self.nodo_padre.tablero)
        else:
            self.tablero = copy.deepcopy(self.tablero)

        # Determine the moving player's symbol
        jugador = self.nodo_padre.tablero[self.nodo_padre.estado[0]][self.nodo_padre.estado[1]] if self.minmax == "MAX" else self.nodo_padre.tablero[self.nodo_padre.estadoContrincante[0]][self.nodo_padre.estadoContrincante[1]]

        # Remove the horse from the previous position
        if self.minmax == "MAX":
            prev_pos = self.nodo_padre.estado if self.nodo_padre else self.estado
            self.tablero[prev_pos[0]][prev_pos[1]] = '0'
            # Move the horse to the new position
            self.tablero[self.estado[0]][self.estado[1]] = jugador
        else:
            prev_pos = self.nodo_padre.estadoContrincante if self.nodo_padre else self.estadoContrincante
            self.tablero[prev_pos[0]][prev_pos[1]] = '0'
            # Move the horse to the new position
            self.tablero[self.estado[0]][self.estado[1]] = jugador
