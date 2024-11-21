import random
from horse import Horse

class Board:
    def __init__(self):
        self.size = 8
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.horses = {}
        self.place_elements()

    def place_elements(self):
        """
        Coloca los caballos, los puntos y los multiplicadores (x2) en posiciones aleatorias
        sobre el tablero.
        """
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
        
        # Colocamos los puntos x2
        for _ in range(4):
            pos = positions.pop()
            self.set_grid(pos, 'x2')

    def set_grid(self, pos, value):
        x, y = pos
        self.grid[x][y] = value

    def get_grid(self, pos):
        x, y = pos
        return self.grid[x][y]

    def move_horse(self, horse, new_position):
        """
        Mueve un caballo a una nueva posición y actualiza el tablero y los puntos si corresponde.
        """
        current_pos = horse.position
        # Remover el caballo de la posición anterior
        self.set_grid(current_pos, None)

        # Obtener el contenido de la nueva posición
        cell_content = self.get_grid(new_position)

        # Manejar la recolección de puntos o x2
        if cell_content and ('point' in cell_content or cell_content == 'x2'):
            self.set_grid(new_position, None)

        # Colocar el caballo en la nueva posición
        self.set_grid(new_position, f'{horse.color}_horse')
        horse.move_to(new_position)

    def get_horse(self, color):
        return self.horses[color]

    def get_opponent_horse(self, color):
        opponent_color = 'black' if color == 'white' else 'white'
        return self.horses[opponent_color]

    def is_game_over(self):
        """
        Verifica si el juego ha terminado:
        - Si no hay más puntos en el tablero (solo puntos, no x2).
        """
        # Verificar si ya no hay puntos en el tablero (solo puntos, no x2)
        print("Comprobando si no hay más puntos en el tablero...")
        for x in range(self.size):
            for y in range(self.size):
                cell = self.get_grid((x, y))
                if 'point' in str(cell):  # Solo puntos, no x2
                    print(f"Punto encontrado en ({x}, {y})")
                    return False  # Aún hay puntos en el tablero

        print("No quedan puntos en el tablero.")

        # Si llegamos aquí, es porque no quedan puntos en el tablero
        return True  # No hay más puntos, el juego termina
