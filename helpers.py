import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, INITIAL_LEVEL
from enemy import Enemy

def draw_text(screen, text, size, x, y, color):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def load_scaled_image(image_path, scale_factor):
    image = pygame.image.load(image_path).convert_alpha()
    width, height = image.get_size()
    scaled_image = pygame.transform.scale(image, (int(width * scale_factor), int(height * scale_factor)))
    return scaled_image

def show_start_screen(screen):
    screen.fill(BLACK)
    draw_text(screen, "Pew Pew", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, WHITE)
    draw_text(screen, "By Alex van Winkel", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, WHITE)
    draw_text(screen, "Press any key to start", 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4, WHITE)
    draw_text(screen, f"Level: {INITIAL_LEVEL}", 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4 + 30, WHITE)
    
    # Load and display the scaled player's ship image
    player_ship_image = load_scaled_image('assets/player.png', 2)  # Scale factor of 2 for a larger image
    player_ship_rect = player_ship_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + player_ship_image.get_height() + 20))
    screen.blit(player_ship_image, player_ship_rect)
    
    pygame.display.flip()
    wait_for_key()

def show_instruction_screen(screen):
    screen.fill(BLACK)
    draw_text(screen, "Instructions", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, WHITE)
    draw_text(screen, "Use the arrow keys to move the spaceship", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, WHITE)
    draw_text(screen, "Press the space bar to shoot", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40, WHITE)
    
    # Load and display the player's ship and enemy sprites
    player_ship_image = load_scaled_image('assets/player.png', 1.5)  # Scale factor of 1.5 for a larger image
    player_ship_rect = player_ship_image.get_rect(center=(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 140))
    screen.blit(player_ship_image, player_ship_rect)
    
    enemy_image = load_scaled_image('assets/enemy.png', 1.5)  # Scale factor of 1.5 for a larger image
    enemy_rect = enemy_image.get_rect(center=(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 + 140))
    screen.blit(enemy_image, enemy_rect)
    
    pygame.display.flip()
    wait_for_key()

def show_level_screen(screen, level):
    screen.fill(BLACK)
    draw_text(screen, f"Level {level}", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, WHITE)
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds

def show_game_over_screen(screen, level, score):
    screen.fill(BLACK)
    draw_text(screen, "Game Over", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, WHITE)
    draw_text(screen, f"Level: {level}", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, WHITE)
    draw_text(screen, f"Score: {score:06}", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40, WHITE)
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False

def create_enemies(level):
    enemies = []
    for row in range(level):
        for x in range(100, SCREEN_WIDTH - 100, 100):
            enemies.append(Enemy(x, 50 + row * 50))
    return enemies