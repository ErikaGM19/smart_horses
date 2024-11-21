class Horse:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.has_x2 = 0
        self.previous_position = None

    def get_valid_moves(self, board):
        x, y = self.position
        moves = [
            (x + 2, y + 1), (x + 2, y - 1),
            (x - 2, y + 1), (x - 2, y - 1),
            (x + 1, y + 2), (x + 1, y - 2),
            (x - 1, y + 2), (x - 1, y - 2),
        ]
        valid_moves = []
        for mx, my in moves:
            if 0 <= mx < board.size and 0 <= my < board.size:
                cell_content = board.get_grid((mx, my))
                # Revisa que la casilla no esté ocupada por otro caballo
                if cell_content not in ['white_horse', 'black_horse']:
                    #Evita los ciclos
                    if (mx, my) != self.previous_position:
                        valid_moves.append((mx, my))
        return valid_moves

    def move_to(self, position):
        self.previous_position = self.position
        self.position = position