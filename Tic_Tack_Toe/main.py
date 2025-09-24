# import moduleas
from typing import Final
import sys
import pygame as pg
import functions

# initialize pygame
pg.init()
# clock = pg.time.Clock()
pg.display.set_caption("Tic Tac Toe")
running: bool = True

# create screen
SCREEN_X: Final[int] = 600
SCREEN_Y: Final[int] = 600
screen: pg.Surface = pg.display.set_mode((SCREEN_X, SCREEN_Y))

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# variables
# Player 1 = x, Player 2 = o
current_player: int = 1
pitch: list[list[int]] = [[0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]]

# draw pitch
screen.fill(white)
pg.draw.line(screen, black, (0, 200), (600, 200), 5)
pg.draw.line(screen, black, (0, 400), (600, 400), 5)
pg.draw.line(screen, black, (200, 0), (200, 600), 5)
pg.draw.line(screen, black, (400, 0), (400, 600), 5)

# game loop
running = True

while running:
    # event loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        elif event.type == pg.MOUSEBUTTONDOWN:
            if current_player == 1:
                if pitch[(event.pos[1] // 200)][(event.pos[0] // 200)] == 0:
                    pitch[(event.pos[1] // 200)][(event.pos[0] // 200)] = 1
                    functions.draw_x((event.pos[0] // 200) * 200,
                                     (event.pos[1] // 200) * 200,
                                     screen, black)
                    current_player = 2
            elif current_player == 2:
                if pitch[(event.pos[1] // 200)][(event.pos[0] // 200)] == 0:
                    pitch[(event.pos[1] // 200)][(event.pos[0] // 200)] = 2
                    functions.draw_o((event.pos[0] // 200) * 200,
                                     (event.pos[1] // 200) * 200,
                                     screen, black)
                    current_player = 1

            # check if there is a winner or tie
            if functions.check_winner(pitch):
                print(f"Player {functions.check_winner(pitch)[1]} won!")
                running = False
            elif functions.check_tie(pitch):
                print("Tie")
                running = False

    # update screen
    pg.display.update()

# end game
pg.quit()
