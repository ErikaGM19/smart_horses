class Horse:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.has_x2 = 0
        self.previous_position = None  # Para evitar ciclos

    def get_valid_moves(self, board):
        """
        Genera los movimientos válidos para el caballo, respetando el movimiento en "L"
        y evitando los ciclos.
        """
        x, y = self.position
        moves = [
            (x + 2, y + 1), (x + 2, y - 1),
            (x - 2, y + 1), (x - 2, y - 1),
            (x + 1, y + 2), (x + 1, y - 2),
            (x - 1, y + 2), (x - 1, y - 2),
        ]
        valid_moves = []
        for mx, my in moves:
            # Verifica que el movimiento esté dentro del tablero
            if 0 <= mx < board.size and 0 <= my < board.size:
                cell_content = board.get_grid((mx, my))
                # Verifica que no esté ocupada por otro caballo
                if cell_content not in ['white_horse', 'black_horse']:
                    # Evita los ciclos (no regresar a la posición anterior)
                    if (mx, my) != self.previous_position:
                        valid_moves.append((mx, my))
        return valid_moves

    def move_to(self, position):
        # Actualiza la posición y guarda la anterior para evitar ciclos
        self.previous_position = self.position
        self.position = position