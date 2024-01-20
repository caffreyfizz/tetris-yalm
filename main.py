import pygame

from settings_window import SettingsWindow
from main_window import MainWindow
from game_window import GameWindow
from levels_window import LevelsWindow


from assets import WINDOW_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, FPS, COUNT_OF_LEVELS


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    mode = 50

    window = MainWindow(WINDOW_WIDTH, WINDOW_HEIGHT)

    pygame.mixer.music.load('data/sounds/soundtrack.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

    clock = pygame.time.Clock()
    running = True
    while running:
        with open(f"data/results.txt") as file:
            level = int(file.read()) + 1
        if level > COUNT_OF_LEVELS:
            level = COUNT_OF_LEVELS
        print("main", level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            result = window.events_processing(event)
            if result:
                if result[1]:
                    if result[1] == 1:
                        if result[2]:
                            mode = result[2]
                    elif result[1] == 2:
                        level = f"{result[2]}"
                        print("KJHGKJHGKJHJKKKKKKKKKKK", level)

                if result[0] == 1:
                    window = MainWindow(WINDOW_WIDTH, WINDOW_HEIGHT)
                elif result[0] == 2:
                    print("\nchange", level, "lllllllllllllllllllllllllllllllllllllllllllllllllll\n")
                    window = GameWindow(WINDOW_WIDTH, WINDOW_HEIGHT, mode, screen, level)
                elif result[0] == 3:
                    window = SettingsWindow(WINDOW_WIDTH, WINDOW_HEIGHT, mode)
                elif result[0] == 4:
                    window = LevelsWindow(WINDOW_WIDTH, WINDOW_HEIGHT)

        window.render(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
