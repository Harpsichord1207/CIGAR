import sys
import pygame


if __name__ == '__main__':

    pygame.init()
    size = width, height = 800, 600

    screen = pygame.display.set_mode(size)
    hero_img = pygame.image.load(r'D:\Projects\Py\CIGAR\resources\game_outman.png').convert()
    hero_img = pygame.transform.scale(hero_img, (80, 120))

    monster_img = pygame.image.load(r'D:\Projects\Py\CIGAR\resources\game_monster.jpg').convert()
    monster_img = pygame.transform.scale(monster_img, (80, 120))

    cnt = 1
    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if cnt % 1000 <= 300:
            # cnt = 1
            screen.blit(hero_img, (10, 240))
            screen.blit(monster_img, (660, 240))
            pygame.draw.rect(screen, (17, 238, 238), (36, 270, 700, 20), 10)
        else:
            screen.fill(color=(0, 0, 0))
            screen.blit(hero_img, (10, 240))
            screen.blit(monster_img, (660, 240))

        pygame.display.update()
        pygame.display.flip()
        cnt += 1
