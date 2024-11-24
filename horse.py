# horse.py
class Horse:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.points = 0
        self.has_x2 = False
        self.visited_positions = set([position])
        self.previous_position = None

    def move_to(self, new_position):
        self.previous_position = self.position
        self.position = new_position
        self.visited_positions.add(new_position)

    def collect_item(self, item):
        if 'point' in item:
            point_value = int(item.split('_')[0])
            multiplier = 2 if self.has_x2 else 1
            self.points += point_value * multiplier
            self.has_x2 = False
        elif item == 'x2':
            self.has_x2 = True

    def get_valid_moves(self, board):
        moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        valid_moves = []
        x, y = self.position
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                cell = board.get_grid((nx, ny))
                if cell in ['white_horse', 'black_horse']:
                    continue  # Evitar posiciones ocupadas por cualquier caballo
                if (nx, ny) in self.visited_positions:
                    continue  # Evitar posiciones ya visitadas
                valid_moves.append((nx, ny))

        if valid_moves:
            return valid_moves
        else:
            # Si no hay movimientos no visitados, permitir movimientos a posiciones visitadas excepto la anterior
            revisited_moves = []
            for dx, dy in moves:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    cell = board.get_grid((nx, ny))
                    if cell in ['white_horse', 'black_horse']:
                        continue
                    if (nx, ny) == self.previous_position:
                        continue  # Evitar regresar inmediatamente a la posición anterior para evitar ciclos
                    revisited_moves.append((nx, ny))
            if revisited_moves:
                return revisited_moves
            else:
                # Si aún así no hay movimientos, permitir regresar a la posición anterior como último recurso
                last_resort_moves = []
                for dx, dy in moves:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < board.size and 0 <= ny < board.size:
                        cell = board.get_grid((nx, ny))
                        if cell in ['white_horse', 'black_horse']:
                            continue
                        last_resort_moves.append((nx, ny))
                return last_resort_moves
