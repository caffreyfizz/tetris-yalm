import pygame

from main_window import MainWindow


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    window = MainWindow(WINDOW_WIDTH, WINDOW_HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                window.check_buttons(event.pos)

        window.render(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()