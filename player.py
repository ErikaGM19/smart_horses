class Player:
    def __init__(self,color):
        self.color = color

    def get_move(self, board, horse):
        raise NotImplementedError

class HumanPlayer(Player):
    def get_move(self, board, horse):
        # La interacción con el usuario se maneja en la interfaz
        pass
