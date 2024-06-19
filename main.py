"""
Tic-Tac-Toe Game

Authors: Merismbatyan and Karolinasurmenelyan
License: MIT License (see LICENSE file for details)
"""


import random
import pygame
import time
import copy
import math

from collections import deque


class TicTacToe:
    def __init__(self):
        self.state = [['', '', ''],
                      ['', '', ''],
                      ['', '', '']]
        self.move = 'X'
        self.algorithm = None
        self.end_game = False
        self.target_depth = 8
        self.transposition_table = {}  # For storing evaluated states

        self.width = 300
        self.height = 300
        self.line_width = 10
        self.rows = len(self.state)
        self.cols = len(self.state[0])
        self.square_size = self.width // self.cols
        self.winner = None



    def check_winner(self, state):
        if state is None:
            return
        n = len(state)
        for i in range(n):
            if state[i][0] == state[i][1] == state[i][2] != '':
                return state[i][0]

            if state[0][i] == state[1][i] == state[2][i] != '':
                return state[0][i]

        if state[0][0] == state[1][1] == state[2][2] != '':
            return state[0][0]

        if state[0][2] == state[1][1] == state[2][0] != '':
            return state[0][2]
        return None


    def check_end(self, state):
        if state is None:
            return
        for r in state:
            if '' in r:
                return False
        return True


    def board_state(self):
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)

        WINDOW = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tic Tac Toe")

        WINDOW.fill(BLACK)
        for row in range(self.rows):
            for col in range(self.cols):
                pygame.draw.rect(WINDOW, WHITE, (col * self.square_size, row *
                                                 self.square_size, self.square_size, self.square_size), self.line_width)
                if self.state[row][col] == 'X':
                    pygame.draw.line(WINDOW, RED, (col * self.square_size + 20, row * self.square_size + 20),
                                     ((col + 1) * self.square_size - 20, (row + 1) * self.square_size - 20),
                                     self.line_width - 5)
                    pygame.draw.line(WINDOW, RED, ((col + 1) * self.square_size - 20, row * self.square_size + 20),
                                     (col * self.square_size + 20, (row + 1) * self.square_size - 20),
                                     self.line_width - 5)
                elif self.state[row][col] == 'O':
                    pygame.draw.circle(WINDOW, RED, (
                        col * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2),
                        self.square_size // 2 - 20, self.line_width - 5)


    def get_row_col_from_mouse(self, pos):
        x, y = pos
        row = y // self.square_size
        col = x // self.square_size
        return row, col


    def state_evaluation(self, state):
        winner = self.check_winner(state)
        if winner == 'X':
            return -1
        elif winner == 'O':
            return 1
        return 0


    def find_best_move(self):
        best_move = None
        best_value = float('-inf')

        if self.algorithm == 'bfs':
            best_move = self.bfs()
            self.state = best_move
        else:
            for neighbour in self.get_possible_moves(self.state, 'O'):
                if self.check_winner(neighbour) == 'O':
                    return neighbour

                if self.algorithm == 'minimax':
                    move_value = self.minimax('X', neighbour, self.target_depth)
                elif self.algorithm == 'alphabetapruning':
                    move_value = self.alpha_beta_pruning('X', neighbour, self.target_depth, -math.inf, math.inf)

                if move_value > best_value:
                    best_value = move_value
                    best_move = neighbour
        return best_move


    def get_possible_moves(self, state, move):
        neighbours = []
        for r in range(self.rows):
            for c in range(self.cols):
                if state[r][c] == '':
                    new_state = copy.deepcopy(state)
                    new_state[r][c] = move
                    neighbours.append(new_state)
        return neighbours


    def minimax(self, move, state, depth):
        if self.check_end(state) or self.check_winner(state):
            return self.state_evaluation(state)
        if move == 'O':
            max_eval = -math.inf
            state_neighbours = self.get_possible_moves(state, move)
            for neighbour in state_neighbours:
                eval = self.minimax('X', neighbour, depth - 1)
                max_eval = max(max_eval, eval)
            return max_eval
        elif move == 'X':
            min_eval = math.inf
            state_neighbours = self.get_possible_moves(state, move)
            for neighbour in state_neighbours:
                eval = self.minimax('O', neighbour, depth - 1)
                min_eval = min(min_eval, eval)
            return min_eval


    def alpha_beta_pruning(self, move, state, depth, alpha, beta):
        state_key = tuple(map(tuple, state))
        if state_key in self.transposition_table:
            return self.transposition_table[state_key]

        if depth == 0:
            evaluation = self.state_evaluation(state)
            self.transposition_table[state_key] = evaluation
            return evaluation

        if self.check_end(state) or self.check_winner(state):
            evaluation = self.state_evaluation(state)
            self.transposition_table[state_key] = evaluation
            return evaluation

        if move == 'O':
            max_eval = -math.inf
            state_neighbours = self.get_possible_moves(state, move)
            for neighbour in state_neighbours:
                eval = self.alpha_beta_pruning('X', neighbour, depth - 1, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[state_key] = max_eval
            return max_eval
        elif move == 'X':
            min_eval = math.inf
            state_neighbours = self.get_possible_moves(state, move)
            for neighbour in state_neighbours:
                eval = self.alpha_beta_pruning('O', neighbour, depth - 1, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table[state_key] = min_eval
            return min_eval


    def bfs(self):
        best_move = None
        queue = deque([self.state]) 

        while queue:
            current_state = queue.popleft()
            state_neighbours = self.get_possible_moves(current_state, 'O')
            for neighbour in state_neighbours:
                queue.append(neighbour)
                if not best_move or random.random() < 0.5:
                    best_move = neighbour
                    return best_move


    def print_info_end_game(self, state):
        winner = self.check_winner(state)
        if winner:
            self.end_game = True
            print("WINNER", winner)
            return winner

        if self.check_end(state):
            self.end_game = True
            print("DRAW!")
            return None


    def make_move(self, row, col, algorithm):
        self.algorithm = algorithm

        if self.state[row][col] == '' and not self.end_game:
            # Player's move
            self.state[row][col] = 'X'
            self.board_state()
            end = self.check_end(self.state)
            self.end_game = end

            pygame.display.update()
            winner = self.print_info_end_game(self.state)
            if winner is not None:
                time.sleep(3)
                return

            # Algorithm's move
            self.state = self.find_best_move()
            if self.state is None:
                self.print_info_end_game(self.state)
                time.sleep(3)
                return

            self.board_state()
            pygame.display.update()
            winner = self.print_info_end_game(self.state)
            if winner is not None:
                time.sleep(3)
                return
            


def main():
    pygame.init()
    agent = TicTacToe()
    agent.board_state()
    while not agent.end_game:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, col = agent.get_row_col_from_mouse(mouse_pos)
                # you need to choose algorithm you want
                # agent.make_move(row, col, 'bfs')
                agent.make_move(row, col, 'minimax')
                # agent.make_move(row, col, 'alphabetapruning')


if __name__ == "__main__":
    main()
