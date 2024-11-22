import random
from horse import Horse

class Board:
    def __init__(self):
        self.size = 8
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.horses = {}
        self.place_elements()
        self.total_points = self.calculate_total_points()

    def place_elements(self):
        positions = [(x, y) for x in range(self.size) for y in range(self.size)]
        random.shuffle(positions)

        # Colocamos los caballos
        white_pos = positions.pop()
        black_pos = positions.pop()
        self.horses['white'] = Horse('white', white_pos)
        self.horses['black'] = Horse('black', black_pos)
        self.set_grid(white_pos, 'white_horse')
        self.set_grid(black_pos, 'black_horse')


      # Colocamos los puntos (1 a 10)
        for value in range(1, 11):
            pos = positions.pop()
            self.set_grid(pos, f'{value}_point')

        # Colocamos los multiplicadores x2
        for _ in range(4):
            pos = positions.pop()
            self.set_grid(pos, 'x2')

    def calculate_total_points(self):
        total = 0
        for row in self.grid:
            for cell in row:
                if cell and 'point' in cell:
                    total += int(cell.split('_')[0])
        return total

    def set_grid(self, pos, value):
        x, y = pos
        self.grid[x][y] = value

    def get_grid(self, pos):
        x, y = pos
        return self.grid[x][y]

    def move_horse(self, horse, new_position):
        current_pos = horse.position
        # Remover el caballo de la posición anterior
        self.set_grid(current_pos, None)

        # Obtener el contenido de la nueva posición
        cell_content = self.get_grid(new_position)

        # Manejar la recolección de puntos o x2
        if cell_content and ('point' in cell_content or cell_content == 'x2'):
            horse.collect_item(cell_content)
            self.set_grid(new_position, None)
            print(f"{horse.color.capitalize()} ha recogido {cell_content} en {new_position}")

        # Colocar el caballo en la nueva posición
        self.set_grid(new_position, f'{horse.color}_horse')
        horse.move_to(new_position)

    def get_horse(self, color):
        return self.horses[color]

    def get_opponent_horse(self, color):
        opponent_color = 'black' if color == 'white' else 'white'
        return self.horses[opponent_color]

    def is_game_over(self):
        # Verificar si ya no hay puntos en el tablero
        points_left = any(cell and 'point' in cell for row in self.grid for cell in row)
        print(f"is_game_over: points_left={points_left}")  # Depuración
        if not points_left:
            return True  # Fin del juego porque ya no hay puntos

        # Verificar si ambos caballos no tienen movimientos válidos
        if not any(horse.get_valid_moves(self) for horse in self.horses.values()):
            print("is_game_over: Ningún caballo puede moverse.")
            return True  # Fin del juego porque ninguna IA puede moverse

        # El juego continúa
        return False
