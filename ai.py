import copy
from player import Player
from nodo import Nodo
import math

class AIPlayer(Player):
    def __init__(self, color, difficulty):
        super().__init__(color)
        self.depth = self.get_depth_from_difficulty(difficulty)
    
    def get_depth_from_difficulty(self, difficulty):
        mapping = {'Principiante': 2, 'Amateur': 4, 'Experto': 6}
        return mapping.get(difficulty, 2)
    
    def get_move(self, board, horse):
        valid_moves = horse.get_valid_moves(board)
        if not valid_moves:
            return None
        best_score = -math.inf
        best_move = None
        for move in valid_moves:
            board_copy = copy.deepcopy(board)
            horse_copy = copy.deepcopy(horse)
            board_copy.move_horse(horse_copy, move)
            score = self.evaluate(board_copy)
            if score > best_score:
                best_score = score
                best_move = move
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
        score = 0
        horse = board.get_horse(self.color)
        opponent_horse = board.get_opponent_horse(self.color)

        # Evaluación para el caballo propio
        score += self.evaluate_horse(board, horse)

        # Evaluación para el caballo oponente
        score -= self.evaluate_horse(board, opponent_horse)

        return score
        
    def evaluate_horse(self, board, horse):
        score = 0
        cell_content = board.get_grid(horse.position)

        # Factor 1: Puntos acumulados
        score += horse.points * 100  # Alto peso a los puntos acumulados

        # Factor 2: Distancia al punto más cercano
        points_positions = self.get_points_positions(board)
        if points_positions:
            distances = [self.calculate_distance(horse.position, point) for point in points_positions]
            min_distance = min(distances)
            score -= min_distance * 20  # Penalizar fuertemente la distancia al punto más cercano
        else:
            # No hay más puntos en el tablero
            pass

        # Factor 3: Número de movimientos válidos
        num_valid_moves = len(horse.get_valid_moves(board))
        score += num_valid_moves * 5  # Favorecer tener más opciones de movimiento

        # Factor 4: Proximidad al oponente
        opponent_horse = board.get_opponent_horse(horse.color)
        distance_to_opponent = self.calculate_distance(horse.position, opponent_horse.position)
        if distance_to_opponent < 3:
            score -= (3 - distance_to_opponent) * 10  # Penalizar estar demasiado cerca del oponente

        return score

    def get_points_positions(self, board):
        points_positions = []
        for x in range(board.size):
            for y in range(board.size):
                cell = board.get_grid((x, y))
                if cell and ('point' in cell or cell == 'x2'):
                    points_positions.append((x, y))
        return points_positions

    def calculate_distance(self, start_pos, end_pos):
        return abs(start_pos[0] - end_pos[0]) + abs(start_pos[1] - end_pos[1])


class AIPlayer1(AIPlayer):
    pass

class AIPlayer2(AIPlayer):
    pass