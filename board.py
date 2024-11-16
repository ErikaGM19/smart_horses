import random
from horse import Horse

class Board:
    def __init__(self):
        self.size = 8
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.horses = {}
        self.place_elements()

    def place_elements(self):
        positions = [(x, y) for x in range(self.size) for y in range(self.size)]
        random.shuffle(positions)

        #Se ccolocan los caballos
        white_pos = positions.pop
        black_pos = positions.pop
        self.horses['white'] = Horse('white', white_pos)
        self.horses['black'] = Horse('black', black_pos)
        self.set_grid(white_pos, 'white_horse')
        self.set_grid(black_pos, 'black_horse')

        #Se dan los puntos
        for value in range (1, 11):
            pos = positions.pop()
            self.set_grid(pos, f'{value}_point')
        
        #Punto x2
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
        #Se actualiza la posición del caballo y se asignan los puntos si corresponde
        pass

    def get_horse(self, color):
        return self.horses[color]