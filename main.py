import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, INITIAL_SCORE, INITIAL_LIVES, WHITE
from player import Player
from enemy import Enemy
from bullet import Bullet

def draw_text(screen, text, size, x, y, color):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Vertical Space Shooter")
    
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)  # Provide initial x and y positions
    enemies = [Enemy(x, 50) for x in range(100, SCREEN_WIDTH - 100, 100)]  # Create a list of enemies with initial positions
    bullets = []
    
    score = INITIAL_SCORE
    lives = INITIAL_LIVES
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

        for enemy in enemies:
            enemy.move()
            # Check for collision with player
            if enemy.rect.colliderect(player.rect):
                lives -= 1
                enemies.remove(enemy)
                if lives <= 0:
                    running = False

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

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()