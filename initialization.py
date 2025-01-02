import pygame


def init():
    pygame.init()
    pygame.display.set_caption('Верю-не-верю')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    running = True

    fps = 100
    clock = pygame.time.Clock()

    while running:
        screen.fill(pygame.Color(0, 128, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()