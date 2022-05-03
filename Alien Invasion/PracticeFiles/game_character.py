import pygame
import sys

class GameCharacter:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1500, 1000))
        pygame.display.set_caption("Game Character")
        self.image = pygame.image.load(
            'Python/Python_Crash_Course_2nd_edition/Alien Invasion/images/guy.jpg')
        self.image = pygame.transform.scale(self.image, (100, 100))
        pygame.Surface.set_colorkey(self.image, [255, 255, 255])



    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill((50, 156, 59))
            self.screen.blit(self.image, (650,400))
            pygame.display.flip()

gc = GameCharacter()
gc.run()