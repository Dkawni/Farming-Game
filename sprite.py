import pygame
from settings import *
from random import randint, choice
from timer import Timer

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main'], scale = None):
        super().__init__(groups)

        # Apply scaling only if a scale is specified
        if scale:
            surf = pygame.transform.scale(surf, scale)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.9)

class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surf = pygame.image.load('/Users/twixturtle/Desktop/PycharmProjects/gametime/Sprout_Lands/Objects/Carpet.png')
        surf = pygame.transform.scale(surf, (90,40))
        pos = (1310,1300)
        super().__init__(pos, surf, groups)
        self.name = name


class Water(Generic):
    def __init__(self, pos, frames, groups, z, scale = None):

        # animation setup
        self.frames = frames
        self.frame_index = 0

        if scale:
            self.frames = [
                pygame.transform.scale(frame, scale) for frame in self.frames
            ]
        # sprite setup
        super().__init__(pos = pos,
                         surf = self.frames[0],
                         groups = groups,
                         z = z, scale=None)
        self.rect = self.image.get_rect(topleft=pos)


    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)

class WildFlower(Generic):
    def __init__(self, pos, surf, groups, scale = None):
        super().__init__(pos, surf, groups)
        if scale:
            surf = pygame.transform.scale(surf, scale)
        self.image = surf  # Assign the scaled surface to self.image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy().inflate(-20,-self.rect.height * 0.9)

class Particle(Generic):
    def __init__(self, pos, surf, groups, z, scale = None, duration = 200):
        super().__init__(pos,surf,groups, z)

        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        # white surface
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0,0,0))
        self.image = new_surf

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()

class Tree(Generic):
    def __init__(self, pos, surf, groups, name, player_add, scale = None,):
        if scale:
            surf = pygame.transform.scale(surf, scale)

        super().__init__(pos, surf, groups)


        # tree attributes
        self.health = 3
        self.alive = True
        self.stump_surf = pygame.image.load(f'/Users/twixturtle/Desktop/PycharmProjects/gametime/Sprout_Lands/Objects/Stumps/{"smallie" if name == "Small" else "biggie"}.png')
        self.stump_surf = pygame.transform.scale(self.stump_surf, (40,40))
        self.invul_timer = Timer(200)

        # apple
        self.apple_surf =pygame.image.load('/Users/twixturtle/Desktop/PycharmProjects/gametime/Sprout_Lands/Objects/apple.png')
        self.apple_surf = pygame.transform.scale(self.apple_surf, (50,50))
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

        self.player_add = player_add

    def damage(self):
        # damaging the tree
        self.health -= 1

        # remove an apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            Particle(
                pos = random_apple.rect.topleft,
                surf = random_apple.image,
                groups = self.groups()[0],
                z = LAYERS['Fruit']
            )
            self.player_add('apple')
            random_apple.kill()

    def check_death(self):
        if self.health <= 0:
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            Particle(self.rect.topleft, self.image, self.groups()[0], LAYERS['Fruit'], 300)
            self.alive = False
            self.player_add('wood')


    def update(self, dt):
        if self.alive:
            self.check_death()

    def create_fruit(self):
        for pos in self.apple_pos:
            if randint(0,3) < 4:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic(
                    pos = (x,y),
                    surf = self.apple_surf,
                    groups = [self.apple_sprites, self.groups()[0]],
                    z = LAYERS['Fruit']
                ) # calls self.all_sprites
