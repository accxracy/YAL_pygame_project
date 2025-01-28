import pygame

size = width, height = 300, 300

if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption('Перетаскивание')
    screen = pygame.display.set_mode(size)

    running = True
    drawing = False
    pos_rect = 0, 0
    pos_dx, pos_dy = 0, 0
    screen.fill(pygame.Color('black'))

    pygame.draw.rect(screen, (0, 255, 0), (pos_rect, (100, 100)))

    while running:
        # screen.fill(pygame.Color('black'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = event.pos
                x0, y0 = pos_rect
                if x0 <= x1 <= x0 + 100 and y0 <= y1 <= y0 + 100:
                    drawing = True
                    pos_dx = x1 - x0
                    pos_dy = y1 - y0
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    screen.fill(pygame.Color('black'))
                    x1, y1 = event.pos
                    pos_rect = x1 - pos_dx, y1 - pos_dy
                    pygame.draw.rect(screen,
                                     (0, 255, 0),
                                     (pos_rect, (100, 100)))

        pygame.display.flip()
    pygame.quit()