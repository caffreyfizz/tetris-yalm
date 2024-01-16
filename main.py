import pygame

from settings_window import SettingsWindow
from main_window import MainWindow
from game_window import GameWindow
from levels_window import LevelsWindow


from assets import WINDOW_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, FPS


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    mode = 1
    level = "test3"

    window = MainWindow(WINDOW_WIDTH, WINDOW_HEIGHT)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            result = window.events_processing(event)
            if result:
                if result[0] == 1:
                    window = MainWindow(WINDOW_WIDTH, WINDOW_HEIGHT)
                elif result[0] == 2:
                    window = GameWindow(WINDOW_WIDTH, WINDOW_HEIGHT, mode, screen, level)
                elif result[0] == 3:
                    window = SettingsWindow(WINDOW_WIDTH, WINDOW_HEIGHT, mode)
                elif result[0] == 4:
                    window = LevelsWindow(WINDOW_WIDTH, WINDOW_HEIGHT)

                if result[1]:
                    mode = result[1]

        window.render(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
