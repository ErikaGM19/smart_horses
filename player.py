class Player:
    def __initi__(self,color):
        self.color = color

    def get_move(self, board, horse):
        raise NotImplementedError

class HumanPlayer(Player):
    def get_move(self, board, horse):
        # La interacción con el usuario se maneja en la interfaz
        pass

class IAPlayer(Player):
    def __init__(self, color, difficulty):
        super().__init__(color)
        self.depth = self.get_depth_from_difficulty(difficulty)
        # se define la heurística específica de la IA

    def get_depth_from_difficulty(self, difficulty):
        mapping = {'Principiante': 2, 'Amateur': 4, 'Experto': 6}
        return mapping.get(difficulty, 2)

    def get_move(self, board, horse):
        # Implementar el algoritmo minimax con la profundidad correspondiente
        pass