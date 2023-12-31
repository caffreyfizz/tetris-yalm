import pygame

from settings_window import SettingsWindow
from main_window import MainWindow
from game_window import GameWindow


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    mode = 1

    window = MainWindow(WINDOW_WIDTH, WINDOW_HEIGHT)

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
                    window = GameWindow(WINDOW_WIDTH, WINDOW_HEIGHT, mode)
                elif result[0] == 3:
                    window = SettingsWindow(WINDOW_WIDTH, WINDOW_HEIGHT, mode)
                elif result[0] == 4:
                    print("open_levels")

                if result[1]:
                    mode = result[1]

        window.render(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()