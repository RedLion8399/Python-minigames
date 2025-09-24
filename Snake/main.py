from typing import Final
import random as rd
import time
import pygame as pg

# Bildschirmgröße festlegen
WINDOW_X: Final[int] = 720
WINDOW_Y: Final[int] = 480

# Farbe erstellen
RED: Final[pg.Color] = pg.Color(255, 0, 0)
GREEN: Final[pg.Color] = pg.Color(0, 255, 0)
BLUE: Final[pg.Color] = pg.Color(0, 0, 255)
YELLOW: Final[pg.Color] = pg.Color(255, 255, 0)
BLACK: Final[pg.Color] = pg.Color(0, 0, 0)
WHITE: Final[pg.Color] = pg.Color(255, 255, 255)

# Geschwindigkeit der Schlange
SNAKE_SPEED: Final[int] = 15

# Pygame initialisieren
pg.init()

# Fenster erstellen
pg.display.set_caption('Snake')
window = pg.display.set_mode((WINDOW_X, WINDOW_Y))

# FPS Kontrolle
fps = pg.time.Clock()

# Position der Schlange
snake_position = [100, 50]


# Teile der Schlange erstellen
snake_body = [
    [100, 50],
    [90, 50],
    [80, 50],
    [70, 50]
]

# Frucht Position festlegen
fruit_position: list[int] = [rd.randrange(1, (WINDOW_X // 10)) * 10,
                             rd.randrange(1, (WINDOW_Y // 10)) * 10]

fruit_spawn: bool = True

direction: str = "RIGHT"
change_to_direction: str = direction

# Startscpre festlegen
score: int = 0


# Scoreposition erstellen
def showscore(color: pg.Color, font: str, size: int) -> None:
    # Font des Scores erstellen
    score_font = pg.font.SysFont(font, size)
    # Objekt auf dem Bildschirm erstellen
    score_surface = score_font.render(f"score: {score}", True, color)
    # Rechteck für den Text erstellen
    score_ract = score_surface.get_rect()
    # Text zeichnen
    window.blit(score_surface, score_ract)


def game_over():
    # Font für Game Over erstellen
    my_font = pg.font.SysFont('times new roman', 50)
    # Getract auf dem Bildschirm erstellen
    game_over_surface = my_font.render(f"Your final score is: {score}", True, RED)
    # Rechteck für den Text erstellen
    game_over_ract = game_over_surface.get_rect()
    # Position des Textes festlege
    game_over_ract.midtop = (WINDOW_X // 2, WINDOW_Y // 4)
    # Text zeichnen
    window.blit(game_over_surface, game_over_ract)
    pg.display.flip()
    # 2 Sekunden warten
    time.sleep(2)
    # Pygame beenden
    pg.quit()
    # Programm beenden
    quit()


while True:
    # Keyeingaben festlegen
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                change_to_direction = "UP"
            if event.key == pg.K_DOWN:
                change_to_direction = "DOWN"
            if event.key == pg.K_LEFT:
                change_to_direction = "LEFT"
            if event.key == pg.K_RIGHT:
                change_to_direction = "RIGHT"

    # Schlange soll sich nicht in engegengesetzte Bewegungsrichtung drehen
    if change_to_direction == "UP" and direction != "DOWN":
        direction = "UP"
    if change_to_direction == "DOWN" and direction != "UP":
        direction = "DOWN"
    if change_to_direction == "LEFT" and direction != "RIGHT":
        direction = "LEFT"
    if change_to_direction == "RIGHT" and direction != "LEFT":
        direction = "RIGHT"

    # Schlange bewegen
    if direction == "UP":
        snake_position[1] -= 10
    if direction == "DOWN":
        snake_position[1] += 10
    if direction == "LEFT":
        snake_position[0] -= 10
    if direction == "RIGHT":
        snake_position[0] += 10

    # Schlange verlängern, wenn die Schlange auf die Frucht trifft
    snake_body.insert(0, list(snake_position))
    if (
        snake_position[0] == fruit_position[0]
        and snake_position[1] == fruit_position[1]
    ):
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [rd.randrange(1, (WINDOW_X//10))*10,
                          rd.randrange(1, (WINDOW_Y//10))*10]

    fruit_spawn = True
    window.fill(BLACK)

    for pos in snake_body:
        pg.draw.rect(window, YELLOW, pg.Rect(pos[0], pos[1], 10, 10))
    pg.draw.rect(window, RED, pg.Rect(fruit_position[0], fruit_position[1], 10, 10))

    if snake_position[0] < 0 or snake_position[0] > WINDOW_X - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > WINDOW_Y - 10:
        game_over()

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    showscore(1, GREEN, 'times new roman', 20)

    pg.display.update()

    fps.tick(SNAKE_SPEED)
