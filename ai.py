# ai.py
class AIPlayer(Player):
    def get_move(self, board, horse):
        best_move = self.minimax(board, horse, self.depth, True)
        return best_move

    def minimax(self, board, horse, depth, maximizing_player):
        # Implementar el algoritmo minimax 
        pass

    def heuristic(self, board, horse):
        # Implementar la función heurística
        pass
