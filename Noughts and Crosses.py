__author__ = 'Alastair'
import random, pygame, sys, time
from pygame.locals import *
WINDOWSIZE = 600
BOARDSIZE = 3
BOXSIZE = int(WINDOWSIZE / BOARDSIZE)
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BGCOLOUR = WHITE
BLANK = 'blank'
NOUGHT = 'nought'
CROSS = 'cross'


def main():
    global FPSCLOCK, DISPLAYSURF
    GAMEWON = 'blank'
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWSIZE, WINDOWSIZE))
    mousex = 0
    mousey = 0
    TURN = 0
    pygame.display.set_caption('Noughts and Crosses')
    mainBoard = generateboard()
    myfont = pygame.font.SysFont("impact", 50)

    while True:
        GAMEWON = checkWin(mainBoard)
        DISPLAYSURF.fill(BGCOLOUR)
        drawboard()
        for x in range(BOARDSIZE):
            for y in range(BOARDSIZE):
                if mainBoard[x][y] == CROSS:
                    drawCross(x, y)
                if mainBoard[x][y] == NOUGHT:
                    drawNought(x, y)
        if GAMEWON == 'nought' or GAMEWON == 'cross':
            label = myfont.render("The winner is the " + str(GAMEWON), 1, BLACK)
            DISPLAYSURF.blit(label, (50, 150))
        elif TURN == 9:
            label = myfont.render("The game is a draw", 1, BLACK)
            DISPLAYSURF.blit(label, (105, 150))
        elif TURN % 2 == 1:
            AIboxx, AIboxy = AIMove(mainBoard)
            mainBoard[AIboxx][AIboxy] = NOUGHT
            TURN += 1
        GAMEWON = checkWin(mainBoard)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
                boxx, boxy = getBoxAtPixel(mousex, mousey)
                if mainBoard[boxx][boxy] == BLANK:
                    mainBoard[boxx][boxy] = CROSS
                    TURN += 1

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateboard():
    board = []
    for x in range(BOARDSIZE):
        column = []
        for y in range(BOARDSIZE):
            column.append(BLANK)
        board.append(column)

    return board


def drawboard():
    for linex in range(BOXSIZE, WINDOWSIZE, BOXSIZE):
        pygame.draw.line(DISPLAYSURF, BLACK, (linex, 0), (linex, WINDOWSIZE), 5)
    for liney in range(BOXSIZE, WINDOWSIZE, BOXSIZE):
        pygame.draw.line(DISPLAYSURF, BLACK, (0, liney), (WINDOWSIZE, liney), 5)


def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * BOXSIZE
    top = boxy * BOXSIZE
    return left, top


def getBoxAtPixel(x, y):
    for boxx in range(BOARDSIZE):
        for boxy in range(BOARDSIZE):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return boxx, boxy
    return None, None


def drawCross(x, y):
    boxx, boxy = leftTopCoordsOfBox(x, y)
    pygame.draw.line(DISPLAYSURF, RED, (boxx + (BOXSIZE/10), boxy + (BOXSIZE/10)), (boxx + BOXSIZE - (BOXSIZE/10), boxy + BOXSIZE - (BOXSIZE/10)), 5)
    pygame.draw.line(DISPLAYSURF, RED, (boxx + BOXSIZE - (BOXSIZE/10), boxy + (BOXSIZE/10)), (boxx + (BOXSIZE/10), boxy + BOXSIZE - (BOXSIZE/10)), 5)

def drawNought(x, y):
    boxx, boxy = leftTopCoordsOfBox(x, y)
    pygame.draw.circle(DISPLAYSURF, BLUE, (int(boxx + (BOXSIZE/2)), int(boxy + (BOXSIZE/2))), int((BOXSIZE/2) - (BOXSIZE/10)), 5)


def AIMove(mainBoard):
    spaces = []
    for x in range(3):
        for y in range(3):
            if mainBoard[x][y] == BLANK:
                spaces.append([x, y])
    return spaces[random.randint(0, len(spaces) - 1)]

def checkWin(mainBoard):
    # check vertical
    for x in range(3):
        combo = []
        for y in range(3):
            combo.append(mainBoard[x][y])
        if combo[0] != BLANK:
            if combo[0] == combo[1] and combo[1] == combo[2]:
                return combo[0]
    # check horizontal
    for x in range(3):
        combo = []
        for y in range(3):
            combo.append(mainBoard[y][x])
        if combo[0] != BLANK:
            if combo[0] == combo[1] and combo[1] == combo[2]:
                return combo[0]
    # check diagonal
    if mainBoard[0][0] == mainBoard[1][1] and mainBoard[1][1] == mainBoard[2][2]:
        if mainBoard[1][1] != BLANK:
            return mainBoard[1][1]
    elif mainBoard[2][0] == mainBoard[1][1] and mainBoard[1][1] == mainBoard[0][2]:
        if mainBoard[1][1] != BLANK:
            return mainBoard[1][1]
    return 'blank'



main()