import pygame
from settings import *
from level import *

class Overlay:
    def __init__(self, player):

        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # imports
        overlay_path = '/Users/twixturtle/Desktop/PycharmProjects/gametime/Sprout_Lands/Objects/overlay/'
        self.tools_surf = { tool: pygame.transform.scale(
        pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha(),
        (50, 50))
        for tool in player.tools
        }
        self.seeds_surf = {seed: pygame.transform.scale(
            pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha(),
            (50,50))
            for seed in player.seeds
        }

    def display(self):

        # tool
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surf, tool_rect)

        # seeds
        seed_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom = OVERLAY_POSITIONS['seed'])
        self.display_surface.blit(seed_surf, seed_rect)