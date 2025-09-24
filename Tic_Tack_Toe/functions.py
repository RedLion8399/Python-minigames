# import moduleas
import pygame as pg


# draw x
def draw_x(x: int, y: int, screen: pg.Surface, color: tuple[int, int, int]
           ) -> None:
    pg.draw.line(screen, color, (x, y), (x + 200, y + 200), 5)
    pg.draw.line(screen, color, (x + 200, y), (x, y + 200), 5)


# draw o
def draw_o(x: int, y: int, screen: pg.Surface, color: tuple[int, int, int]
           ) -> None:
    pg.draw.circle(screen, color, (x + 100, y + 100), 100, 5)


# check if there is a winner
def check_winner(pitch: list[list[int]]) -> tuple[bool, int] | None:
    for i in range(3):
        if len(set(pitch[i])) == 1 and pitch[i][0] != 0:
            return True, pitch[i][0]
        elif len(set([pitch[0][i], pitch[1][i], pitch[2][i]])) == 1 and pitch[0][i] != 0:
            return True, pitch[0][i]
    if len(set([pitch[0][0], pitch[1][1], pitch[2][2]])) == 1 and pitch[0][0] != 0:
        return True, pitch[0][0]
    elif len(set([pitch[0][2], pitch[1][1], pitch[2][0]])) == 1 and pitch[0][2] != 0:
        return True, pitch[0][2]


# check if there is a tie
def check_tie(pitch: list[list[int]]) -> bool | None:
    if 0 not in pitch[0] and 0 not in pitch[1] and 0 not in pitch[2]:
        return True
