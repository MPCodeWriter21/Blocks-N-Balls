"""Block N Balls"""

import sys
import time
import random
from typing import Union, Iterable, Optional
from threading import Thread

import log21
import pygame

# Colors (R, G, B)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
LIGHT_GRAY = pygame.Color(200, 200, 200)


class BlocksNBalls:
    current_difficulty: float

    def __init__(
        self,
        frame_size_x: int = 720,
        frame_size_y: int = 480,
        font: Union[str, bytes, Iterable[Union[str, bytes]]] = 'consolas',
        fps: int = 60
    ) -> None:
        """Blacks N Balls class.

        Args:
            frame_size_x (int, optional): Frame size x. Defaults to 720.
            frame_size_y (int, optional): Frame size y. Defaults to 480.
            font (Union[str, bytes, Iterable[Union[str, bytes]]], optional): Font.
                Defaults to 'consolas'.
            fps (int): Frames per Second
        """
        self.__frame_size_x = (frame_size_x // 10) * 10
        self.__frame_size_y = (frame_size_y // 10) * 10
        self.wall_size = min(self.__frame_size_x, self.__frame_size_y)
        self.font = font
        self.fps = fps

        # Checks for errors encountered
        check_errors = pygame.init()
        # pygame.init() example output -> (6, 0)
        # second number in tuple gives number of errors
        if check_errors[1] > 0:
            log21.error(
                f'Had {check_errors[1]} errors when initialising game, exiting...'
            )
            sys.exit(-1)
        else:
            log21.info('Game successfully initialised')

        # Initialise game window
        pygame.display.set_caption('Blocks N Balls')
        self.game_window = pygame.display.set_mode(
            (frame_size_x, frame_size_y), pygame.RESIZABLE
        )

        # Game variables
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0

        self.__running = False

    def game_over(self):
        """Game Over function."""
        self.__running = False
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render('YOU DIED', True, RED)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.frame_size_x // 2, self.frame_size_y // 4)
        self.game_window.fill(BLACK)
        self.game_window.blit(game_over_surface, game_over_rect)
        self.show_score(color=RED, font='times', size=20)
        pygame.display.flip()
        time.sleep(3)

    def show_score(
        self,
        *,
        color: pygame.Color = WHITE,
        font: Optional[Union[str, bytes, Iterable[Union[str, bytes]]]] = None,
        size: int = 16,
        draw: bool = True
    ):
        """Show score function."""
        font = font or self.font
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        score_rect.topleft = (self.frame_size_x // 25, self.frame_size_y // 25)
        if draw:
            self.game_window.blit(score_surface, score_rect)

    def show_pause(
        self,
        *,
        color: pygame.Color = RED,
        size: int = 30,
        font: Optional[Union[str, bytes, Iterable[Union[str, bytes]]]] = None,
    ):
        """Show pause function."""
        font = font or self.font
        pause_font = pygame.font.SysFont(font, size)
        pause_surface = pause_font.render('Paused', True, color)
        pause_rect = pause_surface.get_rect()
        pause_rect.midtop = (
            self.frame_size_x // 2, self.frame_size_y // 2 - pause_rect[3] // 2
        )
        self.game_window.blit(pause_surface, pause_rect)

    def do_drawings(self):
        """Draw the things that need to be drawn."""
        self.game_window.fill(BLACK)

        # Show score
        self.show_score(color=WHITE)

        # Show the walls
        if self.wall_size == self.frame_size_x:
            # Draw horizontal lines
            line_1_y = (self.frame_size_y - self.frame_size_x) // 2
            pygame.draw.line(
                self.game_window, WHITE, (0, line_1_y), (self.frame_size_x, line_1_y), 5
            )
            line_2_y = line_1_y + self.frame_size_x
            pygame.draw.line(
                self.game_window, WHITE, (0, line_2_y), (self.frame_size_x, line_2_y), 5
            )
        elif self.wall_size == self.frame_size_y:
            # Draw vertical lines
            line_1_x = (self.frame_size_x - self.frame_size_y) // 2
            pygame.draw.line(
                self.game_window, WHITE, (line_1_x, 0), (line_1_x, self.frame_size_y), 5
            )
            line_2_x = line_1_x + self.frame_size_y
            pygame.draw.line(
                self.game_window, WHITE, (line_2_x, 0), (line_2_x, self.frame_size_y), 5
            )

    def main_loop(self):
        """Main loop function."""
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                    return

                # Change the frame size when the window is resized
                elif event.type == pygame.VIDEORESIZE:
                    self.frame_size_x, self.frame_size_y = event.size

                # Whenever a key is pressed down
                elif event.type == pygame.KEYDOWN:
                    # W -> Up; S -> Down; A -> Left; D -> Right
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.change_to = 'UP'
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.change_to = 'RIGHT'
                    if event.key == pygame.K_PAUSE or event.key == ord('p'):
                        self.change_to = 'PAUSE'
                        self.show_pause(font='consolas')
                        pygame.display.update()
                    # Esc -> Create event to quit the game
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

            self.do_drawings()

            if self.change_to == 'PAUSE':
                time.sleep(self.tick)
                continue
            if self.change_to == 'UP' and self.direction != 'DOWN':
                self.direction = 'UP'
            if self.change_to == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'
            if self.change_to == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            if self.change_to == 'RIGHT' and self.direction != 'LEFT':
                self.direction = 'RIGHT'

            # Refresh game screen
            pygame.display.update()
            # Refresh rate
            time.sleep(self.tick)

    def __run(self):
        while self.__running:
            if self.change_to == 'PAUSE':
                time.sleep(self.tick)
                continue

            # Show score
            self.show_score(draw=False)

    def run(self):
        """Run the game."""
        threads = []
        self.__running = True
        threads.append(Thread(target=self.__run, daemon=True))
        threads[-1].start()

        self.main_loop()
        self.__running = False
        for thread in threads:
            thread.join()

    @property
    def frame_size_x(self) -> int:
        """Get the width of the game frame."""
        return self.__frame_size_x

    @frame_size_x.setter
    def frame_size_x(self, value: int):
        self.__frame_size_x = (value // 10) * 10
        if self.game_window.get_width() != value:
            self.game_window = pygame.display.set_mode(
                (self.frame_size_x, self.frame_size_y), pygame.RESIZABLE
            )
        self.wall_size = min(self.__frame_size_x, self.__frame_size_y)

    @property
    def frame_size_y(self) -> int:
        """Get the height of the game frame."""
        return self.__frame_size_y

    @frame_size_y.setter
    def frame_size_y(self, value: int):
        self.__frame_size_y = (value // 10) * 10
        if self.game_window.get_height() != value:
            self.game_window = pygame.display.set_mode(
                (self.frame_size_x, self.frame_size_y), pygame.RESIZABLE
            )
        self.wall_size = min(self.__frame_size_x, self.__frame_size_y)

    @property
    def fps(self) -> int:
        """Get the number of frames per second."""
        return self.__fps

    @fps.setter
    def fps(self, value: int):
        self.__fps = value
        self.__tick = 1 / value

    @property
    def tick(self) -> float:
        """Get the time between each frame."""
        return self.__tick

    def __del__(self):
        pygame.quit()


def main(
    frame_size_x: int = 720,
    frame_size_y: int = 480,
):
    """Run the game.

    Args:
        frame_size_x (int): The width of the game frame. (default: 720)
        frame_size_y (int): The height of the game frame. (default: 480)
    """

    game = BlocksNBalls(
        frame_size_x=frame_size_x,
        frame_size_y=frame_size_y,
    )
    game.run()


if __name__ == '__main__':
    log21.argumentify(main)
