import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, INITIAL_SCORE, INITIAL_LIVES, INITIAL_LEVEL, ENEMY_SPEED, WHITE
from player import Player
from enemy import Enemy
from bullet import Bullet
from helpers import draw_text, load_scaled_image, show_start_screen, show_instruction_screen, show_level_screen, show_game_over_screen, wait_for_key, create_enemies

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Vertical Space Shooter")
    
    show_start_screen(screen)
    show_instruction_screen(screen)
    
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)  # Provide initial x and y positions
    level = INITIAL_LEVEL
    enemies = create_enemies(level)
    bullets = []
    
    score = INITIAL_SCORE
    lives = INITIAL_LIVES
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
                enemies = create_enemies(level)  # Restart the level
                if lives <= 0:
                    show_game_over_screen(screen, level, score)
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

        # Check if all enemies are shot down
        if not enemies:
            level += 1
            score += 500  # Bonus points for leveling up
            show_level_screen(screen, level)
            enemies = create_enemies(level)
        
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