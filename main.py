import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, INITIAL_SCORE, INITIAL_LIVES, INITIAL_LEVEL, WHITE, BLACK, ENEMY_SPEED
from player import Player
from enemy import Enemy
from bullet import Bullet

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

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Vertical Space Shooter")
    
    show_start_screen(screen)
    
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)  # Provide initial x and y positions
    enemies = [Enemy(x, 50) for x in range(100, SCREEN_WIDTH - 100, 100)]  # Create a list of enemies with initial positions
    bullets = []
    
    score = INITIAL_SCORE
    lives = INITIAL_LIVES
    level = INITIAL_LEVEL
    enemy_timer = 0
    enemy_interval = 1000  # Time in milliseconds between enemy spawns
    fast_enemy = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.append(bullet)

        player.handle_movement()
        
        for bullet in bullets:
            bullet.update()
            if bullet.off_screen(SCREEN_HEIGHT):
                bullets.remove(bullet)

        # Update enemies
        current_time = pygame.time.get_ticks()
        if current_time - enemy_timer > enemy_interval:
            enemy_timer = current_time
            # Reset the speed of the previously selected fast enemy
            if fast_enemy:
                fast_enemy.speed = ENEMY_SPEED
            # Select a new random enemy to move faster if there are any enemies left
            if enemies:
                fast_enemy = random.choice(enemies)
                fast_enemy.speed = ENEMY_SPEED * 2  # Double the speed for the selected enemy

        for enemy in enemies:
            enemy.move()
            # Check for collision with player
            if enemy.rect.colliderect(player.rect):
                lives -= 1
                enemies.remove(enemy)
                if lives <= 0:
                    running = False
            # Reset enemy position if it moves off the screen
            if enemy.rect.top > SCREEN_HEIGHT:
                enemy.rect.y = 0
                enemy.rect.x = random.randint(0, SCREEN_WIDTH - enemy.rect.width)

        # Check for collisions between bullets and enemies
        for bullet in bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    score += 100
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break
        
        screen.fill((0, 0, 0))  # Clear the screen
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        
        # Draw score
        draw_text(screen, f"Score: {score:06}", 18, SCREEN_WIDTH // 2, 10, WHITE)
        
        # Draw lives
        for i in range(lives):
            screen.blit(player.image, (10 + i * 40, 10))
        
        # Draw level
        draw_text(screen, f"Level: {level}", 18, SCREEN_WIDTH - 100, 10, WHITE)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()