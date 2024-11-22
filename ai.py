import math
import copy
from player import Player

class AIPlayer(Player):
    def __init__(self, color, difficulty):
        super().__init__(color)
        self.depth = self.get_depth_from_difficulty(difficulty)
        self.visited_positions = set()  # Para evitar ciclos

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
                if move in self.visited_positions:  # Evitar ciclos
                    continue
                board_copy = copy.deepcopy(board)
                horse_copy = copy.deepcopy(horse)
                board_copy.move_horse(horse_copy, move)
                self.visited_positions.add(move)  # Agregar al historial de movimientos
                eval, _ = self.minimax(board_copy, horse_copy, depth - 1, False, alpha, beta)
                self.visited_positions.remove(move)  # Eliminar después de la recursión
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
                if move in self.visited_positions:  # Evitar ciclos
                    continue
                board_copy = copy.deepcopy(board)
                horse_copy = copy.deepcopy(opponent_horse)
                board_copy.move_horse(horse_copy, move)
                self.visited_positions.add(move)  # Agregar al historial de movimientos
                eval, _ = self.minimax(board_copy, horse_copy, depth - 1, True, alpha, beta)
                self.visited_positions.remove(move)  # Eliminar después de la recursión
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

        # Factor 1: Priorizar `x2` siempre que sea posible (si aún no lo ha recogido)
        if cell_content == 'x2' and not horse.has_x2:
            score += 100  # Priorizar `x2` con un valor alto
            horse.has_x2 = 1  # Marcar que el caballo ha recogido el `x2`

        # Factor 2: Acumulación de puntos
        elif cell_content and 'point' in cell_content:
            point_value = int(cell_content.split('_')[0])
            score += point_value * 10  # Ponderar mucho más los puntos

        # Factor 3: Evaluar las posiciones de los puntos en el tablero
        points_positions = self.get_points_positions(board)
        min_distance = math.inf

        # Primero, evaluar los puntos cercanos alcanzables
        closest_point_found = False
        for point in points_positions:
            if point in horse.get_valid_moves(board):  # Solo considerar puntos alcanzables
                distance = self.calculate_distance(horse.position, point)
                if distance < min_distance:
                    min_distance = distance
                    score += 5 / min_distance  # Priorizar las casillas con puntos cercanos
                    closest_point_found = True  # Hemos encontrado un punto cercano alcanzable

        # Si no se encontró un punto cercano alcanzable, evaluamos los puntos lejanos
        if not closest_point_found:
            for point in points_positions:
                # Evaluar puntos lejanos aunque no sean alcanzables en este turno
                distance = self.calculate_distance(horse.position, point)
                if distance < min_distance:
                    min_distance = distance
                    # Si el punto es alcanzable a futuro, asigna una penalización pequeña
                    score += 3 / distance  # Priorizar los puntos lejanos si no se encuentran puntos cercanos

        # Factor 4: Buscar las casillas de puntos o `x2` más cercanas pero fuera del alcance inmediato
        # Si la casilla está dentro del tablero pero no es alcanzable directamente, nos movemos hacia ella
        for point in points_positions:
            if point not in horse.get_valid_moves(board):  # Solo considerar puntos no alcanzables directamente
                distance = self.calculate_distance(horse.position, point)
                # Evaluar puntos lejanos de una forma más flexible, ya que están dentro del tablero
                score += 3 / distance  # Penaliza los puntos lejanos, pero los evalúa con menor peso

        # Factor 5: Posición relativa al caballo oponente
        opponent_horse = board.get_opponent_horse(horse.color)
        distance_to_opponent = abs(horse.position[0] - opponent_horse.position[0]) + abs(horse.position[1] - opponent_horse.position[1])
        score -= distance_to_opponent / 20  # Penalización por estar demasiado cerca

        return score

    def get_points_positions(self, board):
        """
        Obtiene las posiciones de todas las casillas con puntos.
        """
        points_positions = []
        for x in range(board.size):
            for y in range(board.size):
                cell = board.get_grid((x, y))
                if 'point' in str(cell):
                    points_positions.append((x, y))
        return points_positions

    def calculate_distance(self, start_pos, end_pos):
        """
        Calcula la distancia Manhattan entre dos posiciones.
        """
        return abs(start_pos[0] - end_pos[0]) + abs(start_pos[1] - end_pos[1])


class AIPlayer1(AIPlayer):
    def evaluate_horse(self, board, horse):
        score = 0
        cell_content = board.get_grid(horse.position)

        # Factor 1: Ponderación de puntos
        if cell_content and 'point' in cell_content:
            point_value = int(cell_content.split('_')[0])
            score += point_value * 10  # Ponderar mucho más los puntos

        # Factor 2: Considerar la casilla `x2`
        elif cell_content == 'x2' and not horse.has_x2:
            score += 100  # Priorizar el bono `x2`

        # Factor 3: Evaluar las posiciones de los puntos en el tablero
        points_positions = self.get_points_positions(board)
        min_distance = math.inf
        for point in points_positions:
            distance = self.calculate_distance(horse.position, point)
            if distance < min_distance:
                min_distance = distance
                score += 5 / min_distance  # Priorizar las casillas más cercanas con puntos

        # Factor 4: Posición relativa al caballo oponente
        opponent_horse = board.get_opponent_horse(horse.color)
        distance_to_opponent = abs(horse.position[0] - opponent_horse.position[0]) + abs(horse.position[1] - opponent_horse.position[1])
        score -= distance_to_opponent / 10  # Penalizar estar demasiado cerca

        return score

class AIPlayer2(AIPlayer):
    def evaluate_horse(self, board, horse):
        score = 0
        cell_content = board.get_grid(horse.position)

        # Factor 1: Ponderación de puntos
        if cell_content and 'point' in cell_content:
            point_value = int(cell_content.split('_')[0])
            score += point_value * 10  # Ponderar mucho más los puntos

        # Factor 2: Considerar la casilla `x2`
        elif cell_content == 'x2' and not horse.has_x2:
            score += 100  # Priorizar el bono `x2`

        # Factor 3: Evaluar las posiciones de los puntos en el tablero
        points_positions = self.get_points_positions(board)
        min_distance = math.inf
        for point in points_positions:
            distance = self.calculate_distance(horse.position, point)
            if distance < min_distance:
                min_distance = distance
                score += 5 / min_distance  # Mayor ponderación para las casillas cercanas

        # Factor 4: Posición relativa al caballo oponente
        opponent_horse = board.get_opponent_horse(horse.color)
        distance_to_opponent = abs(horse.position[0] - opponent_horse.position[0]) + abs(horse.position[1] - opponent_horse.position[1])
        score -= distance_to_opponent / 15  # Penalización moderada

        return score
