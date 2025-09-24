from typing import Final
import random
import time

import numpy as np
import pygame

# Bildschirmgröße festlegen
WINDOW_X: Final[int] = 720
WINDOW_Y: Final[int] = 480

# Farben erstellen
RED: Final[pygame.Color] = pygame.Color(255, 0, 0)
YELLOW: Final[pygame.Color] = pygame.Color(255, 255, 0)
GREEN: Final[pygame.Color] = pygame.Color(0, 255, 0)
BLUE: Final[pygame.Color] = pygame.Color(0, 0, 255)
BLACK: Final[pygame.Color] = pygame.Color(0, 0, 0)
WHITE: Final[pygame.Color] = pygame.Color(255, 255, 255)

# pygame initialisieren
pygame.init()

# Fenster erstellen
pygame.display.set_caption("Tetris")
window: pygame.Surface = pygame.display.set_mode((WINDOW_X, WINDOW_Y))


# Klasse Blöcke erstellen
class Block(pygame.sprite.Sprite):

    @staticmethod
    def collide(block: pygame.sprite.Sprite, group: pygame.sprite.Group
                ) -> bool:
        """
        Check if the specified block collides with some other block
        in the group.
        """
        for other_block in group:
            # Ignore the current block which will always collide with itself.
            if block == other_block:
                continue
            if pygame.sprite.collide_mask(block, other_block) is not None:
                return True
        return False

    def __init__(self):
        super().__init__()
        # Get a random color.
        self.color = random.choice(
            (
                (200, 200, 200),
                (215, 133, 133),
                (30, 145, 255),
                (0, 170, 0),
                (180, 0, 140),
                (200, 200, 0),
            )
        )
        self.current: bool = True
        self.struct: np.ndarray = np.array(self.struct)

        # Initial random rotation and flip.
        if random.randint(0, 1):
            self.struct = np.rot90(self.struct)
        if random.randint(0, 1):
            # Flip in the X axis.
            self.struct = np.flip(self.struct, 0)
        self._draw()

    def _draw(self, x: int = 4, y: int = 0):
        width: int = len(self.struct[0]) * TILE_SIZE
        height: int = len(self.struct) * TILE_SIZE
        self.image = pygame.surface.Surface([width, height])
        self.image.set_colorkey((0, 0, 0))

        # Position and size
        self.rect: pygame.Rect = Rect(0, 0, width, height)
        self.x = x
        self.y = y

        for y, row in enumerate(self.struct):
            for x, col in enumerate(row):
                if col:
                    pygame.draw.rect(
                        self.image,
                        self.color,
                        Rect(
                            x * TILE_SIZE + 1,
                            y * TILE_SIZE + 1,
                            TILE_SIZE - 2,
                            TILE_SIZE - 2,
                        ),
                    )
        self._create_mask()

    def redraw(self) -> None:
        self._draw(self.x, self.y)

    def _create_mask(self) -> None:
        """
        Create the mask attribute from the main surface.
        The mask is required to check collisions. This should be called
        after the surface is created or update.
        """
        self.mask: pygame.Mask = pygame.mask.from_surface(self.image)

    def initial_draw(self) -> None:
        raise NotImplementedError

    @property
    def group(self) -> pygame.sprite.Group:
        return self.groups()[0]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.rect.left = value * TILE_SIZE

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.rect.top = value * TILE_SIZE

    def move_left(self, group):
        self.x -= 1
        # Check if we reached the left margin.
        if self.x < 0 or Block.collide(self, group):
            self.x += 1

    def move_right(self, group):
        self.x += 1
        # Check if we reached the right margin or collided with another block.
        if self.rect.right > GRID_WIDTH or Block.collide(self, group):
            # Rollback.
            self.x -= 1

    def move_down(self, group):
        self.y += 1
        # Check if the block reached the bottom or collided with another one.
        if self.rect.bottom > GRID_HEIGHT or Block.collide(self, group):
            # Rollback to the previous position.
            self.y -= 1
            self.current = False
            raise BottomReached

    def rotate(self, group):
        self.image = pygame.transform.rotate(self.image, 90)
        # Once rotated we need to update the size and position.
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        self._create_mask()

        # Check the new position doesn't exceed the limits or collide
        # with other blocks and adjust it if necessary.
        while self.rect.right > GRID_WIDTH:
            self.x -= 1
        while self.rect.left < 0:
            self.x += 1
        while self.rect.bottom > GRID_HEIGHT:
            self.y -= 1
        while True:
            if not Block.collide(self, group):
                break
            self.y -= 1
        self.struct = np.rot90(self.struct)

    def update(self):
        if self.current:
            self.move_down()


# Definieren der Blöcke (noch nicht komplett)
class BoxBlock(Block):
    struct = (
        (1, 1),
        (1, 1),
    )


class TBlock(Block):
    struct = (
        (1, 1, 1),
        (0, 1, 0),
    )


while True:
    # Keyeingaben festlegen
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                change_to = "DOWN"
            if event.key == pygame.K_LEFT:
                change_to = "LEFT"
            if event.key == pygame.K_RIGHT:
                change_to = "RIGHT"
            if event.key == pygame.K_m:
                if musik_playing:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play(-1, 0.0)
                musik_playing = not musik_playing
