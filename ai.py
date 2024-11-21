import math
import copy
from player import Player

class AIPlayer(Player):
    def __init__(self, color, difficulty):
        super().__init__(color)
        self.depth = self.get_depth_from_difficulty(difficulty)

    def get_depth_from_difficulty(self, difficulty):
        mapping = {'Principiante': 2, 'Amateur': 4, 'Experto': 6}
        return mapping.get(difficulty, 2)

    def get_move(self, board, horse):
        best_score, best_move = self.minimax(board, horse, self.depth, True, -math.inf, math.inf)
        return best_move

    def minimax(self, board, horse, depth, maximizing_player, alpha, beta):
        if depth == 0 or board.is_game_over():
            return self.evaluate(board), None

        valid_moves = horse.get_valid_moves(board)
        if not valid_moves:
            return self.evaluate(board), None

        best_move = None

        if maximizing_player:
            max_eval = -math.inf
            for move in valid_moves:
                board_copy = copy.deepcopy(board)
                horse_copy = copy.deepcopy(horse)
                board_copy.move_horse(horse_copy, move)
                eval, _ = self.minimax(board_copy, horse_copy, depth - 1, False, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            opponent_horse = board.get_opponent_horse(self.color)
            opponent_moves = opponent_horse.get_valid_moves(board)
            for move in opponent_moves:
                board_copy = copy.deepcopy(board)
                horse_copy = copy.deepcopy(opponent_horse)
                board_copy.move_horse(horse_copy, move)
                eval, _ = self.minimax(board_copy, horse_copy, depth - 1, True, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate(self, board):
        # Implementar la función heurística basada en distancia Manhattan
        score = 0
        horse = board.get_horse(self.color)
        opponent_horse = board.get_opponent_horse(self.color)
        # Heurística para el caballo propio
        score += self.evaluate_horse(board, horse)
        # Heurística para el caballo oponente
        score -= self.evaluate_horse(board, opponent_horse)
        return score

    def evaluate_horse(self, board, horse):
        # Este método será sobrescrito por las subclases AIPlayer1 y AIPlayer2
        raise NotImplementedError

class AIPlayer1(AIPlayer):
    def evaluate_horse(self, board, horse):
        score = 0
        # Factor 1: Acumulación de puntos en la posición actual
        cell_content = board.get_grid(horse.position)
        if cell_content and 'point' in cell_content:
            point_value = int(cell_content.split('_')[0])
            score += point_value
        elif cell_content == 'x2':
            score += 0  # x2 se maneja en otro lugar

        # Factor 2: Preferir casillas con puntos cercanos
        min_distance = math.inf
        for x in range(board.size):
            for y in range(board.size):
                cell = board.get_grid((x, y))
                if cell and ('point' in cell or cell == 'x2'):
                    distance = abs(horse.position[0] - x) + abs(horse.position[1] - y)
                    if distance < min_distance:
                        min_distance = distance
        if min_distance != math.inf:
            score += 1 / min_distance  # Priorizar casillas más cercanas

        # Factor 3: Posición relativa al caballo oponente
        opponent_horse = board.get_opponent_horse(horse.color)
        distance_to_opponent = abs(horse.position[0] - opponent_horse.position[0]) + abs(horse.position[1] - opponent_horse.position[1])
        score -= distance_to_opponent / 10  # Penalizar estar demasiado cerca

        return score

class AIPlayer2(AIPlayer):
    def evaluate_horse(self, board, horse):
        # Función de utilidad específica para AIPlayer2
        score = 0
        cell_content = board.get_grid(horse.position)
        if cell_content and 'point' in cell_content:
            point_value = int(cell_content.split('_')[0])
            score += point_value * 1.5  # Diferencia en ponderación
        elif cell_content == 'x2':
            score += 0

        # Preferir casillas con puntos aún más cercanos
        min_distance = math.inf
        for x in range(board.size):
            for y in range(board.size):
                cell = board.get_grid((x, y))
                if cell and ('point' in cell or cell == 'x2'):
                    distance = abs(horse.position[0] - x) + abs(horse.position[1] - y)
                    if distance < min_distance:
                        min_distance = distance
        if min_distance != math.inf:
            score += 2 / min_distance  # Mayor ponderación

        # Posición relativa al oponente
        opponent_horse = board.get_opponent_horse(horse.color)
        distance_to_opponent = abs(horse.position[0] - opponent_horse.position[0]) + abs(horse.position[1] - opponent_horse.position[1])
        score -= distance_to_opponent / 5  # Mayor penalización

        return score
