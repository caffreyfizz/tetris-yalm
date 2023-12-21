import pygame

from settings_window import SettingsWindow


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    window = SettingsWindow(WINDOW_WIDTH, WINDOW_HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            window.events_processing(event)

        window.render(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()