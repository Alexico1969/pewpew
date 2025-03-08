import pygame
from settings import ENEMY_SPEED

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.load_sprite()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.speed = ENEMY_SPEED

    def load_sprite(self):
        self.image = pygame.image.load('assets/enemy.png').convert_alpha()

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)