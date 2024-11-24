# ai.py
import copy
from player import Player
import math
import random


class AIPlayer(Player):
    def __init__(self, color, difficulty):
        super().__init__(color)
        self.max_depth = self.get_depth_from_difficulty(difficulty)
        self.difficulty = difficulty  # Guardar la dificultad para uso en la evaluación

    def get_depth_from_difficulty(self, difficulty):
        mapping = {'Principiante': 2, 'Amateur': 4, 'Experto': 6}
        return mapping.get(difficulty, 2)

    def get_move(self, board, horse):
        print(f"AI ({horse.color}) buscando movimiento con profundidad {self.max_depth}")
        best_score, best_move = self.minimax(board, horse, self.max_depth, True, -math.inf, math.inf)
        print(f"AI ({horse.color}) seleccionó movimiento: {best_move} con puntuación: {best_score}")
        return best_move

    def minimax(self, board, horse, depth, maximizing_player, alpha, beta):
        if depth == 0 or board.is_game_over():
            eval_score = self.evaluate(board, horse, depth)
            print(f"Minimax: Profundidad 0 o juego terminado. Evaluación: {eval_score}")
            return eval_score, None

        valid_moves = horse.get_valid_moves(board)

        points_to_block = [
            move for move in valid_moves
            if 'point' in str(board.get_grid(move)) and int(board.get_grid(move).split('_')[0]) >= 8
        ]
        if points_to_block:
            return 1000, points_to_block[0]

        if not valid_moves:
            eval_score = self.evaluate(board, horse, depth)
            print(f"Minimax: No hay movimientos válidos. Evaluación: {eval_score}")
            return eval_score, None

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
                    print("Minimax: Poda alfa-beta en maximizer")
                    break
            print(f"Minimax: Maximizador retorna {max_eval} para movimiento {best_move}")
            return max_eval, best_move
        else:
            min_eval = math.inf
            opponent_horse = board.get_opponent_horse(self.color)
            opponent_moves = opponent_horse.get_valid_moves(board)
            for move in opponent_moves:
                board_copy = copy.deepcopy(board)
                opponent_horse_copy = copy.deepcopy(opponent_horse)
                board_copy.move_horse(opponent_horse_copy, move)
                eval, _ = self.minimax(board_copy, opponent_horse_copy, depth - 1, True, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    print("Minimax: Poda alfa-beta en minimizer")
                    break
            print(f"Minimax: Minimizador retorna {min_eval} para movimiento {best_move}")
            return min_eval, best_move

    def evaluate(self, board, horse, current_depth):
        if self.difficulty == 'Principiante':
            return self.evaluate_simple(board, horse)
        elif self.difficulty == 'Amateur':
            return self.evaluate_balanced(board, horse)
        elif self.difficulty == 'Experto':
            return self.evaluate_complex(board, horse, current_depth)
        else:
            return self.evaluate_balanced(board, horse)  # Por defecto

    def evaluate_simple(self, board, horse):
        # Heurística básica para puntos inmediatos
        score = horse.points * 50

        # Posibilidad de ignorar puntos (50% de las veces)
        if random.random() > 0.5:
            reachable_points = []
        else:
            reachable_multipliers = [
            move for move in horse.get_valid_moves(board)
            if board.get_grid(move) == 'x2'
        ]
            score += len(reachable_multipliers) * 80

        points_positions = self.get_points_positions(board)
        if points_positions:
            distances = [self.calculate_euclidean_distance(horse.position, point) for point in points_positions]
            score -= min(distances) * 10  # Penalización más baja.

        return score

    def evaluate_balanced(self, board, horse):
        # Heurística mixta: puntos acumulados, distancia a puntos, y movilidad
        score = horse.points * 100

        points_positions = self.get_points_positions(board)
        if points_positions:
            distances = [self.calculate_euclidean_distance(horse.position, point) for point in points_positions]
            score -= min(distances) * 20

        # Incentivar recoger puntos
        reachable_points = [
            move for move in horse.get_valid_moves(board)
            if 'point' in str(board.get_grid(move))
        ]
        score += len(reachable_points) * 50

        # Considerar multiplicadores
        reachable_multipliers = [
            move for move in horse.get_valid_moves(board)
            if board.get_grid(move) == 'x2'
        ]
        score += len(reachable_multipliers) * 40

        # Penalización leve por ignorar puntos cercanos al oponente
        opponent_horse = board.get_opponent_horse(horse.color)
        distances_to_opponent = [
            self.calculate_euclidean_distance(opponent_horse.position, point) for point in points_positions
        ]
        if distances_to_opponent:
            score -= min(distances_to_opponent) * 10  # Penalizar puntos que el oponente podría tomar.

        return score

    def evaluate_complex(self, board, horse, current_depth):
        # Heurística avanzada: incluye aspectos estratégicos a largo plazo
        score = horse.points * (100 + 10 * current_depth)

        # Distancia al punto más cercano
        points_positions = self.get_points_positions(board)
        if points_positions:
            distances = [self.calculate_euclidean_distance(horse.position, point) for point in points_positions]
            min_distance = min(distances)
            score -= min_distance * (20 - 2 * current_depth)

        # Incentivar recoger puntos altos
        reachable_points = [
            move for move in horse.get_valid_moves(board)
            if 'point' in str(board.get_grid(move))
        ]
        reachable_points_values = [
            int(board.get_grid(move).split('_')[0]) for move in reachable_points
        ]
        if reachable_points_values:
            score += max(reachable_points_values) * 60

        visited_moves = [
            move for move in horse.get_valid_moves(board)
            if move in horse.visited_positions
        ]
        score -= len(visited_moves) * 30

        # Considerar movimientos del oponente
        opponent_horse = board.get_opponent_horse(horse.color)
        opponent_moves = opponent_horse.get_valid_moves(board)

        # Considerar x2 estratégicamente
        reachable_multipliers = [
            move for move in horse.get_valid_moves(board)
            if board.get_grid(move) == 'x2'
        ]
        if reachable_multipliers:
            score += len(reachable_multipliers) * 50

        # Penalizar puntos que el oponente pueda tomar
        opponent_horse = board.get_opponent_horse(horse.color)
        distances_to_opponent = [
            self.calculate_euclidean_distance(opponent_horse.position, point) for point in points_positions
        ]

        nearest_opponent_point = float('inf')

        if distances_to_opponent:
            nearest_opponent_point = min(distances_to_opponent)
            score -= nearest_opponent_point * 30  # Penalización fuerte.

        # Incentivar bloquear puntos clave del oponente
        if nearest_opponent_point < 2:
            score += 50  # Recompensar el bloqueo de puntos.

        return score

    def get_points_positions(self, board):
        points_positions = []
        for x in range(board.size):
            for y in range(board.size):
                cell = board.get_grid((x, y))
                if cell and 'point' in cell:
                    points_positions.append((x, y))
        return points_positions

    def calculate_euclidean_distance(self, start_pos, end_pos):
        return math.sqrt((start_pos[0] - end_pos[0]) ** 2 + (start_pos[1] - end_pos[1]) ** 2)


class AIPlayer1(AIPlayer):
    pass

class AIPlayer2(AIPlayer):
    pass
