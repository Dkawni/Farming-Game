import pygame, sys
from settings import *
from level import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('DeemaDew')
        self.all_sprites = pygame.sprite.Group()
        self.level = Level()

    def run(self):

        while True: #check if close the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.all_sprites.update()
            #update game
            dt = self.clock.tick() / 1000
            self.level.run(dt)
            self.all_sprites.draw(self.screen)

            pygame.display.update()



if __name__ == '__main__': #checking if in the main file
    game = Game() #creates an object then runs it
    game.run()
