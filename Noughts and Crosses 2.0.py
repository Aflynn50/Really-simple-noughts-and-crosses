import random
import sys
import pygame
from pygame.locals import *
import copy

author__ = 'Alastair'


class Game:

    def __init__(self):
        pygame.init()
        self.WINDOWSIZE = 600
        self.BOARDSIZE = 3
        self.BOXSIZE = int(self.WINDOWSIZE / self.BOARDSIZE)
        self.FPS = 30
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.LIGHTRED = (255, 153, 153)
        self.BLUE = (0, 0, 255)
        self.LIGHTBLUE = (153, 153, 255)
        self.BGCOLOUR = (255, 255, 255)
        self.DRAW = 'draw'
        self.BLANK = 'blank'
        self.NOUGHT = 'nought'
        self.CROSS = 'cross'
        self.mouse_box = list([0, 0])
        self.mouse = list([0, 0])
        self.turn = True  # True is crosses False is noughts
        self.board = self.generate_board()
        self.DISPLAYSURF = pygame.display.set_mode((self.WINDOWSIZE, self.WINDOWSIZE))
        self.FPSCLOCK = 0
        pygame.display.set_caption('Noughts and Crosses')

    @staticmethod
    def terminate():  # Shuts down the pygame module and the sys module and
        pygame.quit()
        sys.exit()

    def check_for_quit(self):
        for event in pygame.event.get(QUIT):  # get all the QUIT events
            if event.type == QUIT:
                self.terminate()  # terminate if any QUIT events are present
        for event in pygame.event.get(KEYUP):  # Check what keys have been released
            if event.key == K_ESCAPE:
                self.terminate()  # Calls the function to shut down the program
            pygame.event.post(event)  # put the other KEYUP event objects back

    def main(self):
        self.FPSCLOCK = pygame.time.Clock()
        while True:
            self.check_for_quit()
            self.update_board()
            self.draw_board()
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)

    def generate_board(self):
        board = list()
        for x in range(self.BOARDSIZE):
            board.append([])
            for y in range(self.BOARDSIZE):
                board[x].append(self.BLANK)
        return board

    def draw_board(self):
        self.DISPLAYSURF.fill(self.BGCOLOUR)

        for linex in range(self.BOXSIZE, self.WINDOWSIZE, self.BOXSIZE):
            pygame.draw.line(self.DISPLAYSURF, self.BLACK, (linex, 0), (linex, self.WINDOWSIZE), 5)
        for liney in range(self.BOXSIZE, self.WINDOWSIZE, self.BOXSIZE):
            pygame.draw.line(self.DISPLAYSURF, self.BLACK, (0, liney), (self.WINDOWSIZE, liney), 5)

        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y] == self.CROSS:
                    self.draw_cross(x, y, self.RED)
                elif self.board[x][y] == self.NOUGHT:
                    self.draw_nought(x, y, self.BLUE)

        if self.board[self.mouse_box[0]][self.mouse_box[1]] == self.BLANK:
            if self.turn:
                self.draw_cross(self.mouse_box[0], self.mouse_box[1], self.LIGHTRED)
            else:
                self.draw_nought(self.mouse_box[0], self.mouse_box[1], self.LIGHTBLUE)

    def draw_cross(self, x, y, colour):
        boxx, boxy = self.top_left_coords(x, y)
        pygame.draw.line(self.DISPLAYSURF, colour, (boxx + (self.BOXSIZE / 10), boxy + (self.BOXSIZE / 10)),
                         (boxx + self.BOXSIZE - (self.BOXSIZE / 10), boxy + self.BOXSIZE - (self.BOXSIZE / 10)), 5)
        pygame.draw.line(self.DISPLAYSURF, colour, (boxx + self.BOXSIZE - (self.BOXSIZE / 10), boxy + (self.BOXSIZE / 10)),
                         (boxx + (self.BOXSIZE / 10), boxy + self.BOXSIZE - (self.BOXSIZE / 10)), 5)

    def draw_nought(self, x, y, colour):
        boxx, boxy = self.top_left_coords(x, y)
        pygame.draw.circle(self.DISPLAYSURF, colour, (int(boxx + (self.BOXSIZE / 2)), int(boxy + (self.BOXSIZE / 2))),
                           int((self.BOXSIZE / 2) - (self.BOXSIZE / 10)), 5)

    def top_left_coords(self, x, y):
        return x * self.BOXSIZE, y * self.BOXSIZE

    def get_box_at_pixel(self, x, y):
        boxx = -1
        boxy = -1
        while x > 0:
            x -= self.BOXSIZE
            boxx += 1
        while y > 0:
            y -= self.BOXSIZE
            boxy += 1
        return boxx, boxy

    def update_board(self):
        if not self.turn:
            pos = self.find_move()
            self.board[pos[0]][pos[1]] = self.NOUGHT
            self.win(self.check_win(self.board))
            self.turn = not self.turn
            print(self.board)
        else:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    boxx, boxy = self.get_box_at_pixel(event.pos[0], event.pos[1])
                    if self.board[boxx][boxy] == self.BLANK and self.turn:
                        self.board[boxx][boxy] = self.CROSS
                    elif self.board[boxx][boxy] == self.BLANK and not self.turn:
                        self.board[boxx][boxy] = self.NOUGHT
                    self.turn = not self.turn
                    self.win(self.check_win(self.board))

                elif event.type == MOUSEMOTION:
                    self.mouse_box[0], self.mouse_box[1] = self.get_box_at_pixel(event.pos[0], event.pos[1])

    def check_win(self, board):
        draw_flag = True
        for x in range(3):
            if 'blank' in board[x]:
                draw_flag = False
        if draw_flag:
            return self.DRAW

        if board[0][0] == board[0][1] and board[0][1] == board[0][2]:
            return board[0][0]
        elif board[1][0] == board[1][1] and board[1][1] == board[1][2]:
            return board[1][0]
        elif board[2][0] == board[2][1] and board[2][1] == board[2][2]:
            return board[2][0]
        elif board[0][0] == board[1][0] and board[1][0] == board[2][0]:
            return board[0][0]
        elif board[0][1] == board[1][1] and board[1][1] == board[2][1]:
            return board[0][1]
        elif board[0][2] == board[1][2] and board[1][2] == board[2][2]:
            return board[0][2]
        elif board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            return board[0][0]
        elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            return board[0][2]
        else:
            return self.BLANK

    def win(self, winner):
        if winner == self.NOUGHT:
            msg = "Noughts win!"
        elif winner == self.CROSS:
            msg = "Crosses win!"
        elif winner == self.DRAW:
            msg = "Nobody wins!"
        else:
            return
        font = pygame.font.SysFont("consolas", 90)
        message = font.render(msg, 1, (100, 100, 100))

        while True:
            self.check_for_quit()
            self.draw_board()
            self.DISPLAYSURF.blit(message, (20, (self.WINDOWSIZE / 3)))
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)

    def find_move(self):
        boxx = 0
        boxy = 0
        value = -10000000000
        temp_board = copy.deepcopy(self.board)
        if self.turn:
            piece = self.CROSS
        else:
            piece = self.NOUGHT
        for x in range(3):
            for y in range(3):
                if temp_board[x][y] == self.BLANK:
                    new_board = temp_board
                    new_board[x][y] = piece
                    current_value = self.min_max(copy.deepcopy(new_board), (not self.turn))
                    if current_value >= value:
                        boxx = x
                        boxy = y
                        value = current_value
                temp_board = copy.deepcopy(self.board)
        return boxx, boxy

    def min_max(self, board, turn):
        if turn:
            piece = self.CROSS
        else:
            piece = self.NOUGHT

        winner = self.check_win(board)
        if winner == self.NOUGHT:
            return 10
        elif winner == self.CROSS:
            return -10
        elif winner == self.DRAW:
            return 0
        else:
            scores = []
            for x in range(3):
                for y in range(3):
                    if board[x][y] == self.BLANK:
                        new_board = copy.deepcopy(board)
                        new_board[x][y] = piece
                        scores.append(self.min_max(copy.deepcopy(new_board), (not turn)))

            if turn:
                return min(scores)
            else:
                return max(scores)








game1 = Game()
game1.main()