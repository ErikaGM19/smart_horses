import copy

class Nodo:
    def __init__(self, estado, utilidad, minmax, tablero, estadoContrincante, nodo_padre=None, profundidad=0, puntos_acumulados_ia=0, puntos_acumulados_oponente=0, visitados_ia=None, visitados_oponente=None):
        self.estado = estado
        self.nodo_padre = nodo_padre
        self.hijos = []
        self.profundidad = profundidad
        self.utilidad = utilidad
        self.minmax = minmax
        self.tablero = copy.deepcopy(tablero)  # Copia profunda del tablero
        self.estadoContrincante = estadoContrincante
        self.puntos_acumulados_ia = puntos_acumulados_ia
        self.puntos_acumulados_oponente = puntos_acumulados_oponente
        # Inicializar conjuntos de posiciones visitadas
        self.visitados_ia = visitados_ia.copy() if visitados_ia else set()
        self.visitados_oponente = visitados_oponente.copy() if visitados_oponente else set()

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def obtener_hijos(self):
        return self.hijos


    def agregar_posicion_tablero(self):
        # Copiar el tablero y las posiciones visitadas del nodo padre
        if self.nodo_padre:
            self.tablero = copy.deepcopy(self.nodo_padre.tablero)
            self.visitados_ia = self.nodo_padre.visitados_ia.copy()
            self.visitados_oponente = self.nodo_padre.visitados_oponente.copy()
            self.puntos_acumulados_ia = self.nodo_padre.puntos_acumulados_ia
            self.puntos_acumulados_oponente = self.nodo_padre.puntos_acumulados_oponente

        # Determinar quién es el jugador actual
        if self.minmax == "MAX":
            jugador = "white_horse"
            fila_anterior, col_anterior = self.nodo_padre.estado if self.nodo_padre else self.estado
            self.tablero[fila_anterior][col_anterior] = None  # Limpiar posición anterior
            valor_casilla = self.tablero[self.estado[0]][self.estado[1]]
            self.tablero[self.estado[0]][self.estado[1]] = jugador
            # Actualizar puntos
            self.puntos_acumulados_ia = Nodo.calcular_puntos(self.estado, self.tablero, self.puntos_acumulados_ia)
            # Actualizar posiciones visitadas
            self.visitados_ia.add(self.estado)
        else:
            jugador = "black_horse"
            fila_anterior, col_anterior = self.nodo_padre.estadoContrincante if self.nodo_padre else self.estadoContrincante
            self.tablero[fila_anterior][col_anterior] = None  # Limpiar posición anterior
            valor_casilla = self.tablero[self.estadoContrincante[0]][self.estadoContrincante[1]]
            self.tablero[self.estadoContrincante[0]][self.estadoContrincante[1]] = jugador
            # Actualizar puntos
            self.puntos_acumulados_oponente = Nodo.calcular_puntos(self.estadoContrincante, self.tablero, self.puntos_acumulados_oponente)
            # Actualizar posiciones visitadas
            self.visitados_oponente.add(self.estadoContrincante)

    @staticmethod
    def calcular_puntos(posicion, tablero, puntos_acumulados):
        fila, col = posicion
        valor_casilla = tablero[fila][col]

        if valor_casilla and 'point' in valor_casilla:
            point_value = int(valor_casilla.split('_')[0])
            puntos_acumulados += point_value
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
                    puntos_acumulados_ia=self.puntos_acumulados_ia,
                    puntos_acumulados_oponente=self.puntos_acumulados_oponente,
                    visitados_ia=self.visitados_ia,
                    visitados_oponente=self.visitados_oponente
                )
            else:
                nuevo_nodo = Nodo(
                    estado=self.estado,
                    utilidad=None,
                    minmax="MAX",
                    tablero=self.tablero,
                    estadoContrincante=move,
                    nodo_padre=self,
                    profundidad=self.profundidad + 1,
                    puntos_acumulados_ia=self.puntos_acumulados_ia,
                    puntos_acumulados_oponente=self.puntos_acumulados_oponente,
                    visitados_ia=self.visitados_ia,
                    visitados_oponente=self.visitados_oponente
                )

            nuevo_nodo.agregar_posicion_tablero()
            self.agregar_hijo(nuevo_nodo)
            nuevo_nodo.expandir_arbol(depth - 1)

    def obtener_movimientos_validos(self):
        movimientos = []
        fila, col = self.estado if self.minmax == "MAX" else self.estadoContrincante
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]

        for df, dc in knight_moves:
            nueva_fila = fila + df
            nueva_col = col + dc
            if (
                0 <= nueva_fila < 8
                and 0 <= nueva_col < 8
                and self.tablero[nueva_fila][nueva_col] != "white_horse"
                and self.tablero[nueva_fila][nueva_col] != "black_horse"
            ):
                nueva_posicion = (nueva_fila, nueva_col)
                # Verificar si la posición ya ha sido visitada
                if self.minmax == "MAX":
                    if nueva_posicion not in self.visitados_ia:
                        movimientos.append(nueva_posicion)
                else:
                    if nueva_posicion not in self.visitados_oponente:
                        movimientos.append(nueva_posicion)
        return movimientos


    def calcular_utilidad(self):
        if not self.hijos:  # Nodo hoja
            utilidad_ia = self.puntos_acumulados_ia
            utilidad_oponente = self.puntos_acumulados_oponente
            self.utilidad = utilidad_ia - utilidad_oponente
            return self.utilidad

        utilidades_hijos = [hijo.calcular_utilidad() for hijo in self.hijos]
        if self.minmax == "MAX":
            self.utilidad = max(utilidades_hijos)
        else:
            self.utilidad = min(utilidades_hijos)

        return self.utilidad
    

    def calcular_mejor_movimiento(self, depth):
        def minimax(nodo, profundidad, maximizador, alpha, beta):
            if profundidad == 0 or not nodo.hijos:
                utilidad = nodo.calcular_utilidad()
                return utilidad, nodo.estado

            if maximizador:
                max_eval = -float('inf')
                mejor_movimiento = None
                for hijo in nodo.hijos:
                    eval, _ = minimax(hijo, profundidad - 1, False, alpha, beta)
                    if eval > max_eval:
                        max_eval = eval
                        mejor_movimiento = hijo.estado
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                return max_eval, mejor_movimiento
            else:
                min_eval = float('inf')
                mejor_movimiento = None
                for hijo in nodo.hijos:
                    eval, _ = minimax(hijo, profundidad - 1, True, alpha, beta)
                    if eval < min_eval:
                        min_eval = eval
                        mejor_movimiento = hijo.estadoContrincante
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                return min_eval, mejor_movimiento

        # Expandir el árbol antes de calcular Minimax
        self.expandir_arbol(depth)
        _, mejor_movimiento = minimax(self, depth, True, -float('inf'), float('inf'))
        return mejor_movimiento