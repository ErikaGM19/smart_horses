class Horse:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.points_x2 = 0

    def get_moves(self, board):
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
                cell_content = board.get_cell((mx, my))
                # Revisa que la casilla no esté ocupada por otro caballo
                if cell_content not in ['white_horse', 'black_horse']:
                    valid_moves.append((mx, my))
        return valid_moves

    def move_to(self, position):
        self.position = position