import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprite import *
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import *

class Level:
    def __init__(self):

        #get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()
        self.soil_layer = SoilLayer(self.all_sprites)


        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)

    def setup(self):
        tmx_data = load_pygame('/Users/twixturtle/Desktop/PycharmProjects/gametime/Sprout_Lands/Tilesets/Background.tmx')

        # house
        house_offset_x = -40  # Move 10 pixels to the left
        house_offset_y = -60

        # house
        for layer_name in ['House', 'House Inside']:
            for x,y, surf in tmx_data.get_layer_by_name(layer_name).tiles():
                Generic(((x * TILE_SIZE + house_offset_x) , (y * TILE_SIZE + house_offset_y)), surf, self.all_sprites, LAYERS[layer_name], (45,45))

        for layer_name in ['House Walls', 'Bed', 'House Back Wall']:
            for x,y, surf in tmx_data.get_layer_by_name(layer_name).tiles():
                Generic(((x * TILE_SIZE + house_offset_x) , (y * TILE_SIZE + house_offset_y)), surf, self.all_sprites, LAYERS[layer_name], (45,45))

        # fence
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic(
                pos=((x * TILE_SIZE + house_offset_x), (y * TILE_SIZE + house_offset_y)),
                surf=surf,
                groups=[self.all_sprites, self.collision_sprites],
                z=LAYERS['Fence'],
                scale = (50,50)
            )

        # water
        water_frames = import_folder(
            '/Users/twixturtle/Desktop/PycharmProjects/gametime/Sprout_Lands/Tilesets/Water Animation')

        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():

            Water(
                pos=(x * TILE_SIZE + house_offset_x, y * TILE_SIZE + house_offset_y),
                frames=water_frames,
                groups=self.all_sprites,
                z=LAYERS['Water'],
                scale = (50,50)
            )

        # wildflowers
        for x, y, surf in tmx_data.get_layer_by_name('Flowers').tiles():
            WildFlower(
                pos=((x * TILE_SIZE + house_offset_x), (y * TILE_SIZE + house_offset_y)),
                surf=surf,
                groups=[self.all_sprites, self.collision_sprites],
                scale = (50,50)
            )

        for x, y, surf in tmx_data.get_layer_by_name('Hill Flowers').tiles():
            WildFlower(
                pos=((x * TILE_SIZE + house_offset_x), (y * TILE_SIZE + house_offset_y)),
                surf=surf,
                groups=[self.all_sprites, self.collision_sprites],
                scale = (50,50)
            )

        for x, y, surf in tmx_data.get_layer_by_name('Hill Extras').tiles():
            Generic(
                pos=((x * TILE_SIZE + house_offset_x), (y * TILE_SIZE + house_offset_y)),
                surf=surf,
                groups=self.all_sprites,
                z=LAYERS['Hill Extras'],
                scale = (50,50)
            )

        # trees
        max_x = max(obj.x for obj in tmx_data.get_layer_by_name('Tree Objects') if obj.image)
        min_x = min(obj.x for obj in tmx_data.get_layer_by_name('Tree Objects') if obj.image)
        min_y = min(obj.y for obj in tmx_data.get_layer_by_name('Tree Objects') if obj.image)
        max_y = max(obj.y for obj in tmx_data.get_layer_by_name('Tree Objects') if obj.image)

        # Step 2: Calculate the scaling factors
        original_width = max_x - min_x
        original_height = max_y - min_y

        # Define the new dimensions for the expanded rectangle
        new_width = 2600
        new_height = 1700

        # Calculate scale factors
        scale_x = new_width / original_width
        scale_y = new_height / original_height

        # Step 3: Adjust the tree positions
        for obj in tmx_data.get_layer_by_name('Tree Objects'):
            if obj.image:
                # Scale the positions
                new_x = (obj.x - min_x) * scale_x + 700  # Apply offset
                new_y = (obj.y - min_y) * scale_y + 160  # Apply offset

                # Create the tree at the new position
                Tree(
                    pos = (new_x, new_y),
                    surf = obj.image,
                    groups = [self.all_sprites, self.collision_sprites, self.tree_sprites],
                    name = obj.name,
                    player_add = self.player_add,
                    scale=(70, 95),
                )


        for x, y, surf in tmx_data.get_layer_by_name('Trees').tiles():
            Generic(
                pos=((x * TILE_SIZE + house_offset_x), (y * TILE_SIZE + house_offset_y)),
                surf=surf,
                groups=[self.all_sprites, self.collision_sprites],
                scale=(50, 50)
            )

        for x, y, surf in tmx_data.get_layer_by_name('Hill Trees').tiles():
            Generic(
                pos=((x * TILE_SIZE + house_offset_x), (y * TILE_SIZE + house_offset_y)),
                surf=surf,
                groups=[self.all_sprites, self.collision_sprites],
                scale = (50,50)
            )


        # Bridge
        for x, y, surf in tmx_data.get_layer_by_name('Bridge/Path').tiles():
            Generic(
                pos=((x * TILE_SIZE + house_offset_x), (y * TILE_SIZE + house_offset_y)),
                surf=surf,
                groups=self.all_sprites,
                z=LAYERS['Bridge/Path'],
                scale = (50,50)
            )

        # Water Extras
        for x, y, surf in tmx_data.get_layer_by_name('Water Extras').tiles():
            Generic(
                pos=((x * TILE_SIZE + house_offset_x), (y * TILE_SIZE + house_offset_y)),
                surf=surf,
                groups=self.all_sprites,
                z=LAYERS['Water Extras'],
                scale = (50,50)
            )

        # collision tiles
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            Generic(
                pos=((x * TILE_SIZE + house_offset_x), (y * TILE_SIZE + house_offset_y)),
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE)),
                groups=self.collision_sprites,
                z=LAYERS['Water Extras'],
                scale=(50, 50)
            )

        self.player = Player((1080,585), self.all_sprites, self.collision_sprites, self.tree_sprites, self.interaction_sprites, self.soil_layer)

        ground_surf = pygame.image.load(
            '/Users/twixturtle/Desktop/PycharmProjects/gametime/Sprout_Lands/Please.png').convert_alpha()

        # Add the transformed background as a sprite
        Generic(
            pos=(-20, -40),
            surf=ground_surf,
            groups=self.all_sprites,
            z=LAYERS['Grass'],
            scale=(3550, 2000)
        )

        # Player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    pos = (obj.x, obj.y),
                    group = self.all_sprites,
                    collision_sprites = self.collision_sprites,
                    tree_sprites = self.tree_sprites,
                    interaction = self.interaction_sprites,
                    soil_layer = self.soil_layer
                )
            if obj.name == 'Carpet':
                carpet = Interaction((obj.x, obj.y), (50,50), [self.all_sprites, self.interaction_sprites], "Carpet")
                carpet.z = LAYERS['Player']
                self.all_sprites.add(carpet)

    def player_add(self, item):

        self.player.item_inventory[item] += 1

    def reset(self):

        # apples on the trees
        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            tree.create_fruit()

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()

        if self.player.sleep:
            self.transition.play()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in sorted(LAYERS.values()):  # Ensure layers are drawn in order
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

