import pygame
import random
from settings import ENEMY_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.load_sprite()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.speed = ENEMY_SPEED
        self.direction = random.choice([-1, 1])  # Random initial direction for x-axis movement

    def load_sprite(self):
        self.image = pygame.image.load('assets/enemy.png').convert_alpha()

    def move(self):
        self.rect.y += self.speed
        self.rect.x += self.direction * random.randint(1, 3)  # Random x-axis movement
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = 0  # Reset to the top of the screen
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)  # Random x position
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction *= -1  # Change direction if hitting screen boundaries

    def draw(self, screen):
        screen.blit(self.image, self.rect)