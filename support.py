import os
import pygame


def import_folder(path):
    surface_list = []

    for root, dirs, files in os.walk(path):
        for file in files:
            # Check if the file is a PNG image
            if file.lower().endswith('.png'):
                full_path = os.path.join(root, file)  # Construct the full path to the file

                try:
                    # Load the image
                    image_surface = pygame.image.load(full_path).convert_alpha()
                    image_surface = pygame.transform.scale(image_surface,(150,150))
                    surface_list.append(image_surface)  # Append the loaded image
                except pygame.error as e:
                    print(f"Failed to load {file}: {e}")

    return surface_list