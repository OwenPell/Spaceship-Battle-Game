import pygame
import random

class PowerUps:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.width = 30
        self.height = 30
        self.color = (0, 255, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_window(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def apply_player(self, player):
        if self.type == 'speed':
            player.speed += 1
        elif self.type == 'health':
            player.health += 10 - player.health

    def apply_bullet(self, bullets):
        if self.type == 'extra':
            bullets.len += 1
        elif self.type == 'homing':
            bullets.homing