from pygame.math import Vector2

# screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 45


# overlay positions
OVERLAY_POSITIONS = {
    'tool' : (40, SCREEN_HEIGHT - 15),
    'seed' : (90, SCREEN_HEIGHT - 10)
}

PLAYER_TOOL_OFFSET = {
    'Left' : Vector2(-50,40),
    'Right' : Vector2(50,40),
    'Up' : Vector2(0,-10),
    'Down' : Vector2(0,50)
}

LAYERS = {
    'Water' : 0,
    'Farmable': 0,
    'Collision' : 1,
    'Grass': 2,
    'Soil': 3,
    'Bridge/Path': 3,
    'House' : 4,
    'House Back Wall' : 5,
    'Hills' : 6,
    'Fence': 7,
    'Hill Extras' : 8,
    'House Inside' : 9,
    'Player': 10,
    'Bed' : 11,
    'main' : 12,
    'House Walls': 13,
    'Hill Trees': 14,
    'Trees': 15,
    'Tree Objects': 16,
    'Hill Flowers': 17,
    'Flowers': 18,
    'Water Extras': 19,
    'Fruit': 20

}

APPLE_POS = {
    'smallie' : [(18,17), (30,37), (12,50), (30,54), (20,30), (30,10)],
    'biggie' : [(30,24), (60,65), (50,50), (16,40), (45,50), (42,70)]
}

GROW_SPEED = {
    'corn' : 1,
    'tomato' : 0.7
}

SALE_PRICES = {
    'wood' : 4,
    'apple' : 2,
    'corn' : 10,
    'tomato' : 20
}

PURCHASE_PRICES = {
    'corn' : 4,
    'tomato' : 5
}