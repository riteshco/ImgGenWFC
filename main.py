import pygame
import sys

pygame.init()

screen_width, screen_height = 9 * 64, 9 * 64

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('My Pygame Window')

clock = pygame.time.Clock()

image = pygame.image.load("./samples/City.png")
ROWS , COLS = 9 , 9
DIM = 9

def split_image(img , rows , cols):
    sub_images = []
    img_width , img_height = img.get_size()

    tile_width = img_width // cols
    tile_height = img_height // rows
    for y in range(rows):
        row_images = []
        for x in range(cols):
            rect = pygame.Rect(x * tile_width , y * tile_height , tile_width , tile_height)
            sub_image = img.subsurface(rect).copy()
            row_images.append(sub_image)
        sub_images.append(row_images)
    return sub_images

def transform_tiles(tiles , block_size , rows , cols):
    new_tiles = []

    for y in range(0, rows):
        new_row = []
        for x in range(0, cols):
            block = []
            for dy in range(block_size):
                block_row = []
                for dx in range(block_size):
                    if y + dy < rows and x + dx < cols:
                        block_row.append(tiles[y + dy][x + dx])
                block.append(block_row)
            new_row.append(block)
        new_tiles.append(new_row)
    return new_tiles

def overlapping_right(source_tile, comparison_tile, overlap_size=2):
    rows = len(source_tile)
    cols = len(source_tile[0])
    
    for i in range(rows):
        for j in range(overlap_size):
            if source_tile[i][cols - overlap_size + j] != comparison_tile[i][j]:
                return False
    return True

def overlapping_left(source, comp, overlap_size=2):
    rows = len(source)
    for i in range(rows):
        for j in range(overlap_size):
            if source[i][j] != comp[i][-overlap_size + j]:
                return False
    return True

def overlapping_down(source, comp, overlap_size=2):
    cols = len(source[0])
    for i in range(overlap_size):
        if source[-overlap_size + i] != comp[i]:
            return False
    return True

def overlapping_up(source , comp , overlap_size=2):
    cols = len(source[0])
    for i in range(overlap_size):
        if source[i] != comp[-overlap_size + i]:
            return False
    return True


tiles = split_image(image , ROWS , COLS)
tile_width = screen_width // DIM
tile_height = screen_height // DIM

transformed_tiles = transform_tiles(tiles , 3 , ROWS , COLS)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
    
    screen.fill((0, 0, 0))    
    for row in range(ROWS):
        for col in range(COLS):
            scaled_tile = pygame.transform.scale(tiles[row][col] , (tile_width , tile_height))
            x = col * tile_width
            y = row * tile_height
            screen.blit(scaled_tile , (x , y))

            pygame.draw.rect(screen , (50,50,50) , (x , y , tile_width , tile_height) , 1)


    
    # Update the display to show the changes
    pygame.display.flip()
    clock.tick(60)


pygame.quit()