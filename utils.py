import pygame

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
        for x in range(0, cols):
            block = []
            for dy in range(block_size):
                block_row = []
                for dx in range(block_size):
                    wrapped_y = (y + dy) % rows
                    wrapped_x = (x + dx) % cols
                    block_row.append(tiles[wrapped_y][wrapped_x])
                block.append(block_row)
            new_tiles.append(block)
    return new_tiles

def hash_tile(tile_surface):
    return hash(pygame.image.tostring(tile_surface, 'RGB'))

def overlapping_right(source_tile, comparison_tile, overlap_size=2):

    tile_left_side = [row[:-1] for row in comparison_tile]
    tile_right_side = [row[1:] for row in source_tile]
    return tile_right_side == tile_left_side

def overlapping_left(source, comp, overlap_size=2):
    return overlapping_right(comp , source)

def overlapping_down(source, comp, overlap_size=2):

    tile_top_side = comp[:-1]
    tile_bottom_side = source[1:]
    return tile_bottom_side == tile_top_side

def overlapping_up(source , comp , overlap_size=2):
    return overlapping_down(comp , source)