import pygame
from settings import *
from pytmx.util_pygame import load_pygame

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['Soil']

class SoilLayer:
    def __init__(self, all_sprites):

        # sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        # graphics
        self.soil_surf = pygame.image.load('/Users/twixturtle/Desktop/PycharmProjects/gametime/Sprout_Lands/soil.png')
        # ADD THE O FILE THAT HE IS TALKNNIG ABOUT

        self.create_soil_grid()
        self.create_hit_rects()

        # requirements
        # if the area is farmable
        # if the soil has been watered
        # if the soil has a plant

    def create_soil_grid(self):
        ground = pygame.image.load('/Users/twixturtle/Desktop/PycharmProjects/gametime/Sprout_Lands/Please.png')
        h_tiles = ground.get_width() // TILE_SIZE
        v_tiles = ground.get_height() // TILE_SIZE

        # Initialize the grid
        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]

        # Load the Farmable layer from the tilemap
        farmable_layer = load_pygame(
            '/Users/twixturtle/Desktop/PycharmProjects/gametime/Sprout_Lands/Tilesets/Background.tmx').get_layer_by_name(
            'Farmable')
        for x, y, _ in farmable_layer.tiles():
            # Ensure the coordinates are within grid bounds
            if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
                self.grid[y][x].append('F')  # Mark the position as farmable

        # Debugging: Print the grid to verify alignment with the Farmable layer
        print("Farmable grid:")
        for row in self.grid:
            print(row)

    def create_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x,y,TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE
                if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
                    if 'F' in self.grid[y][x]:
                        print('farmable')
                        self.grid[y][x].append('X')
                        self.create_soil_tiles()

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:
                    SoilTile(
                        pos = (index_row * TILE_SIZE, index_col * TILE_SIZE),
                        surf = self.soil_surf,
                        groups = [self.all_sprites, self.soil_sprites])
                    print(f"Creating tile at position: ({index_row * TILE_SIZE}, {index_col * TILE_SIZE})")
                    