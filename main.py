import pygame
import sys
import utils
import random

pygame.init()

DIM = 50
TILE_SIZE = 18
SCREEN_SIZE = DIM * TILE_SIZE
N = 3 

screen_width, screen_height = SCREEN_SIZE , SCREEN_SIZE

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('My Pygame Window')
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 12, bold=True)
small_font = pygame.font.SysFont("Arial", 18)

image = pygame.image.load("./samples/Cats.png")
ROWS , COLS = image.get_height() , image.get_width()

tiles = utils.split_image(image , ROWS , COLS)

transformed_tiles = utils.transform_tiles(tiles , 3 , ROWS , COLS)
# print(transformed_tiles)
Hashes_of_tranformed_tile = []
for p_surface in transformed_tiles:
    hash_pattern = tuple(tuple(utils.hash_tile(tile) for tile in row) for row in p_surface)
    Hashes_of_tranformed_tile.append(hash_pattern) 

unique_hashes = list(set(Hashes_of_tranformed_tile))
weights = [Hashes_of_tranformed_tile.count(h) for h in unique_hashes]

hash_to_transformed_tiles = {
    h: transformed_tiles[Hashes_of_tranformed_tile.index(h)] for h in unique_hashes
}

adjacency_rules = {}
num_unique_patterns = len(unique_hashes)

for i, p1_hash in enumerate(unique_hashes):
    adjacency_rules[i] = {'up': [], 'right': [], 'down': [], 'left': []}
    for j, p2_hash in enumerate(unique_hashes):
        if utils.overlapping_right(p1_hash, p2_hash):
            adjacency_rules[i]['right'].append(j)
        if utils.overlapping_left(p1_hash, p2_hash):
            adjacency_rules[i]['left'].append(j)
        if utils.overlapping_down(p1_hash, p2_hash):
            adjacency_rules[i]['down'].append(j)
        if utils.overlapping_up(p1_hash, p2_hash):
            adjacency_rules[i]['up'].append(j)
print("Adjacency rules generated.")

# Wave Function Collapse logic
wave = []
is_generating = False

def initialize_wave():
    global wave
    wave = []
    all_possibilities = list(range(num_unique_patterns))
    for y in range(DIM):
        row = [all_possibilities[:] for _ in range(DIM)]
        wave.append(row)

def find_lowest_entropy_cell():
    min_entropy = num_unique_patterns + 1
    lowest_entropy_cells = []
    for y in range(DIM):
        for x in range(DIM):
            num_possibilities = len(wave[y][x])
            if 1 < num_possibilities < min_entropy:
                min_entropy = num_possibilities
                lowest_entropy_cells = [(x, y)]
            elif num_possibilities == min_entropy:
                lowest_entropy_cells.append((x, y))
    return random.choice(lowest_entropy_cells) if lowest_entropy_cells else None

def collapse_at(x, y):
    possible_indices = wave[y][x]
    possible_weights = [weights[i] for i in possible_indices]
    chosen_index = random.choices(possible_indices, weights=possible_weights, k=1)[0]
    wave[y][x] = [chosen_index]
    return True

def propagate(start_x, start_y):
    stack = [(start_x, start_y)]
    while stack:
        cx, cy = stack.pop()
        current_patterns = wave[cy][cx]
        dirs = [(0, -1, 'up'), (1, 0, 'right'), (0, 1, 'down'), (-1, 0, 'left')]
        
        for dx, dy, direction in dirs:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < DIM and 0 <= ny < DIM:
                neighbor_possibilities = wave[ny][nx]
                original_neighbor_count = len(neighbor_possibilities)
                
                valid_neighbor_indices = set()
                for pattern_index in current_patterns:
                    valid_neighbor_indices.update(adjacency_rules[pattern_index][direction])
                
                new_possibilities = [p for p in neighbor_possibilities if p in valid_neighbor_indices]
                
                if not new_possibilities: return False
                
                if len(new_possibilities) != original_neighbor_count:
                    wave[ny][nx] = new_possibilities
                    if (nx, ny) not in stack:
                        stack.append((nx, ny))
    return True

def start_wfc():
    global is_generating
    initialize_wave()
    is_generating = True

def step_wfc():
    global is_generating
    cell_to_collapse = find_lowest_entropy_cell()
    
    if cell_to_collapse is None:
        print("Generation complete!")
        is_generating = False
        return

    x, y = cell_to_collapse
    collapse_at(x, y)
    if not propagate(x, y):
        print("Contradiction found. Restarting...")
        start_wfc()

def draw_wfc_state():
    for y in range(DIM):
        for x in range(DIM):
            possibilities = wave[y][x]
            num_possibilities = len(possibilities)
            
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            if num_possibilities == 1:
                # Cell is collapsed, draw the tile
                pattern_index = possibilities[0]
                hash_pattern = unique_hashes[pattern_index]
                surface_pattern = hash_to_transformed_tiles[hash_pattern]
                center_tile = surface_pattern[N // 2][N // 2]
                scaled_tile = pygame.transform.scale(center_tile, (TILE_SIZE, TILE_SIZE))
                screen.blit(scaled_tile, rect.topleft)
            else:
                # Cell not collapsed, show number of possibilities
                pygame.draw.rect(screen, (60, 20, 80), rect) # Dark purple background
                text = font.render(str(num_possibilities), True, (255, 255, 255))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

# Main game loop
start_wfc()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                print("\nRegenerating...")
                start_wfc()   
    
    if is_generating:
        step_wfc()

    screen.fill((0, 0, 0))
    draw_wfc_state()

    # text = small_font.render("Press [R] to Regenerate", True, (255, 255, 255))
    # screen.blit(text, (10, SCREEN_SIZE - 30))


    # for row in range(ROWS):
    #     for col in range(COLS):
    #         scaled_tile = pygame.transform.scale(tiles[row][col] , (TILE_SIZE , TILE_SIZE))
    #         x = col * TILE_SIZE
    #         y = row * TILE_SIZE
    #         screen.blit(scaled_tile , (x , y))

    #         pygame.draw.rect(screen , (50,50,50) , (x , y , TILE_SIZE , TILE_SIZE) , 1)
    

    # Update the display to show the changes
    pygame.display.flip()
    clock.tick(60)


pygame.quit()