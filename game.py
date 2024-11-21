from board import Board
from player import HumanPlayer
from ai import AIPlayer1, AIPlayer2


class Game:
    def __init__(self, mode, difficulty_ia1=None, difficulty_ia2=None):
        self.board = Board()
        self.players = self.create_players(mode, difficulty_ia1, difficulty_ia2)
        self.current_turn = 'white'  # El caballo blanco inicia
        self.scores = {'white': 0, 'black': 0}
        self.game_over = False

    def create_players(self, mode, difficulty_ia1, difficulty_ia2):
        if mode == 'Humano vs Humano':
            return {'white': HumanPlayer('white'), 'black': HumanPlayer('black')}
        elif mode == 'Humano vs IA':
            return {'white': AIPlayer1('white', difficulty_ia1), 'black': HumanPlayer('black')}
        elif mode == 'IA 1 vs IA 2':
            return {'white': AIPlayer1('white', difficulty_ia1), 'black': AIPlayer2('black', difficulty_ia2)}
        else:
            return None

    def play_turn(self):
        player = self.players[self.current_turn]
        horse = self.board.get_horse(self.current_turn)
        move = player.get_move(self.board, horse)
        self.update_state(horse, move)
        self.switch_turn()

    def update_state(self, horse, new_position):
        """
        Actualiza el tablero y aplica los puntos si corresponde.
        """
        current_cell = self.board.get_grid(new_position)
        # Actualizar puntuación si recoge puntos
        if 'point' in str(current_cell):
            point_value = int(current_cell.split('_')[0])
            if horse.has_x2:
                point_value *= 2
                horse.has_x2 = 0  # Consumimos el x2
            self.scores[horse.color] += point_value
            self.board.set_grid(new_position, None)
        elif current_cell == 'x2' and not horse.has_x2:
            horse.has_x2 = 1
            self.board.set_grid(new_position, None)
        # Actualizar posición del caballo
        self.board.set_grid(horse.position, None)
        horse.move_to(new_position)
        self.board.set_grid(new_position, f'{horse.color}_horse')

    def switch_turn(self):
        """
        Cambia el turno entre los jugadores.
        """
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def is_game_over(self):
        """
        Verifica si el juego ha terminado.
        """
        return self.board.is_game_over()

    def get_scores(self):
        return self.scores

    def declare_winner(self):
        """
        Devuelve el ganador basado en la puntuación.
        """
        white_score = self.scores['white']
        black_score = self.scores['black']
        if white_score > black_score:
            return f"El ganador es el caballo blanco con {white_score} puntos."
        elif black_score > white_score:
            return f"El ganador es el caballo negro con {black_score} puntos."
        else:
            return "Es un empate."