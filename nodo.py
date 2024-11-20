import copy

class Nodo:
    def __init__(self, estado, utilidad, minmax, tablero, estadoContrincante, nodo_padre=None, profundidad=0):
        self.estado = estado
        self.nodo_padre = nodo_padre
        self.hijos = []
        self.profundidad = profundidad
        self.utilidad = utilidad
        self.minmax = minmax
        self.tablero = copy.deepcopy(tablero)  # Aseguramos una copia profunda
        self.estadoContrincante = estadoContrincante
        self.puntos_acumulados_ia = nodo_padre.puntos_acumulados_ia if nodo_padre else 0
        self.puntos_acumulados_oponente = nodo_padre.puntos_acumulados_oponente if nodo_padre else 0


    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def obtener_hijos(self):
        return self.hijos

    def agregar_posicion_tablero(self):
        # Copiar el tablero del nodo padre si existe
        if self.nodo_padre:
            self.tablero = copy.deepcopy(self.nodo_padre.tablero)
        else:
            self.tablero = copy.deepcopy(self.tablero)

        # Determinar quién es el jugador actual
        if self.minmax == "MAX":
            jugador = "c1"  # Caballo de la IA
            fila_anterior, col_anterior = self.nodo_padre.estado if self.nodo_padre else self.estado
            self.tablero[fila_anterior][col_anterior] = 0  # Limpiar posición anterior
            valor_casilla = self.tablero[self.estado[0]][self.estado[1]]
            self.tablero[self.estado[0]][self.estado[1]] = jugador
            # Actualizar puntos
            self.puntos_acumulados_ia = Nodo.calcular_puntos(self.estado, self.tablero, self.puntos_acumulados_ia)
        else:
            jugador = "c2"  # Caballo del oponente
            fila_anterior, col_anterior = self.nodo_padre.estadoContrincante if self.nodo_padre else self.estadoContrincante
            self.tablero[fila_anterior][col_anterior] = 0  # Limpiar posición anterior
            valor_casilla = self.tablero[self.estadoContrincante[0]][self.estadoContrincante[1]]
            self.tablero[self.estadoContrincante[0]][self.estadoContrincante[1]] = jugador
            # Actualizar puntos
            self.puntos_acumulados_oponente = Nodo.calcular_puntos(self.estadoContrincante, self.tablero, self.puntos_acumulados_oponente)


    @staticmethod
    def calcular_puntos(posicion, tablero, puntos_acumulados):
        fila, col = posicion
        valor_casilla = tablero[fila][col]

        if isinstance(valor_casilla, int):
            puntos_acumulados += valor_casilla
        elif valor_casilla == 'x2':
            puntos_acumulados *= 2

        return puntos_acumulados

    
    
    def expandir_arbol(self, depth=0):
        if depth == 0:
            return

        movimientos_validos = self.obtener_movimientos_validos()
        for move in movimientos_validos:
            if self.minmax == "MAX":
                nuevo_nodo = Nodo(
                    estado=move,
                    utilidad=None,
                    minmax="MIN",
                    tablero=self.tablero,
                    estadoContrincante=self.estadoContrincante,
                    nodo_padre=self,
                    profundidad=self.profundidad + 1,
                )
                nuevo_nodo.puntos_acumulados_ia = Nodo.calcular_puntos(move, self.tablero, self.puntos_acumulados_ia)
            else:
                nuevo_nodo = Nodo(
                    estado=self.estado,
                    utilidad=None,
                    minmax="MAX",
                    tablero=self.tablero,
                    estadoContrincante=move,
                    nodo_padre=self,
                    profundidad=self.profundidad + 1,
                )
                nuevo_nodo.puntos_acumulados_oponente = Nodo.calcular_puntos(
                    move, self.tablero, self.puntos_acumulados_oponente
                )

            nuevo_nodo.agregar_posicion_tablero()
            self.agregar_hijo(nuevo_nodo)
            nuevo_nodo.expandir_arbol(depth - 1)


    def obtener_movimientos_validos(self):
        movimientos = []
        fila, col = self.estado if self.minmax == "MAX" else self.estadoContrincante
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)
        ]

        for df, dc in knight_moves:
            nueva_fila = fila + df
            nueva_col = col + dc
            if (
                0 <= nueva_fila < 8
                and 0 <= nueva_col < 8
                and self.tablero[nueva_fila][nueva_col] != "c1"
                and self.tablero[nueva_fila][nueva_col] != "c2"
            ):
                movimientos.append((nueva_fila, nueva_col))
        return movimientos

    @staticmethod
    def calcular_utilidad(nodo):
        if not nodo.hijos:  # Nodo hoja
            utilidad_ia = nodo.puntos_acumulados_ia
            utilidad_oponente = nodo.puntos_acumulados_oponente
            nodo.utilidad = utilidad_ia - utilidad_oponente
            return nodo.utilidad

        utilidades_hijos = [Nodo.calcular_utilidad(hijo) for hijo in nodo.hijos]
        if nodo.minmax == "MAX":
            nodo.utilidad = max(utilidades_hijos)
        else:
            nodo.utilidad = min(utilidades_hijos)

        return nodo.utilidad
