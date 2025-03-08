import pygame

class Bullet:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/bullet.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def off_screen(self, height):
        return self.rect.bottom < 0