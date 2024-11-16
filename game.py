from board import Board
from player import HumanPlayer, IAplayer


class Game:
    def __init__(self, mode, difficulty_ia1=None, difficulty_ia2=None):
        self.board = Board()
        self.players = self.create_playres(mode, difficulty_ia1, difficulty_ia2)
        self.current_turn = 'white' # El caballo blanco inicia
        self.scores = {'white': 0, 'black': 0}
        self.game_over = False
    def create_players(self, mode, difficulty_ia1, difficulty_ia2):
        if mode == 'Humano vs Humano':
            return {'white': HumanPlayer('white'), 
                    'black': HumanPlayer('black')}
        elif mode == 'Humano vs IA':
            return {'white': IAplayer('white', difficulty_ia1), 
                    'black': HumanPlayer('black')}
        elif mode == 'IA1 vs IA2':
            return {'white': IAplayer('white', difficulty_ia1), 
                    'black': IAplayer('black', difficulty_ia2)}

    def play_turn(self):
        player = self.players[self.current_turn]
        horse = self.board.get_horse(self.current_turn)
        move = player.get_move(self.board, horse)
        self.update_state(horse, move)
        self.switch_turn()

    def update_state(self, horse, new_position):
        # Actualiza el tablero y aplica los puntos si corresponde
        pass

    def switch_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def is_over(self):
        #Si se acaba el juego
        pass

    def get_scores(self):
        return self.scores

    def get_winner(self):
        #Devuelve el ganador
        pass