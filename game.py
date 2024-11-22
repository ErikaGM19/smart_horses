# game.py
from board import Board
from player import HumanPlayer
from ai import AIPlayer1, AIPlayer2

class Game:
    def __init__(self, mode, difficulty_ia1=None, difficulty_ia2=None):
        self.board = Board()
        self.players = {}

        if mode == "Humano vs Humano":
            self.current_turn = 'white'  # El blanco inicia
            self.players['white'] = HumanPlayer('white')
            self.players['black'] = HumanPlayer('black')
        elif mode == "Humano vs IA":
            self.current_turn = 'white'  # La IA inicia
            self.players['white'] = AIPlayer1('white', difficulty_ia1)
            self.players['black'] = HumanPlayer('black')
        elif mode == "IA 1 vs IA 2":
            self.current_turn = 'white'  # La IA 1 inicia
            self.players['white'] = AIPlayer1('white', difficulty_ia1)
            self.players['black'] = AIPlayer2('black', difficulty_ia2)
        else:
            raise ValueError("Modo de juego no soportado")

    def switch_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def update_state(self, horse, new_position):
        self.board.move_horse(horse, new_position)

    def is_game_over(self):
        return self.board.is_game_over()

    def declare_winner(self):
        scores = self.get_scores()
        if scores['white'] > scores['black']:
            return "¡Caballo Blanco gana!"
        elif scores['white'] < scores['black']:
            return "¡Caballo Negro gana!"
        else:
            return "¡Empate!"

    def is_game_over(self):
        return self.board.is_game_over()

    def get_scores(self):
        return {
            'white': self.board.get_horse('white').points,
            'black': self.board.get_horse('black').points
        }
