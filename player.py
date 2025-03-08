import pygame
from settings import PLAYER_SPEED, SCREEN_WIDTH

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.load_sprite()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = PLAYER_SPEED

    def load_sprite(self):
        self.image = pygame.image.load('assets/player.png').convert_alpha()

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)