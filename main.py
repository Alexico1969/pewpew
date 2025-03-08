import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from player import Player
from enemy import Enemy
from bullet import Bullet

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Vertical Space Shooter")
    
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)  # Provide initial x and y positions
    enemies = [Enemy(x, 50) for x in range(100, SCREEN_WIDTH - 100, 100)]  # Create a list of enemies with initial positions
    bullets = []
    
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
        
        screen.fill((0, 0, 0))  # Clear the screen
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()