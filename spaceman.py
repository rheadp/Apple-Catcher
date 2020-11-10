import pygame
import random
import math
import os

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Collector")

# Load Images
ITEM_STAR = pygame.image.load(os.path.join('items', 'star.png'))
ITEM_PLANET = pygame.image.load(os.path.join('items', 'planet.png'))
ITEM_MOON = pygame.image.load(os.path.join('items', 'moon.png'))
ITEM_ROCK = pygame.image.load(os.path.join('items', 'rock.png'))
ITEM_SHIP = pygame.image.load(os.path.join('items', 'spaceship.png'))


# Background Image
BG = pygame.transform.scale(pygame.image.load(os.path.join('items', 'background.png')), (WIDTH, HEIGHT))

class Ship:
    
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = ITEM_SHIP
        self.mask = pygame.mask.from_surface(self.ship_img)

    def draw(self, window):
        super().draw(window)

class Point(Ship):
    ITEM_MAP = {
        "moon": (ITEM_MOON),
        "star": (ITEM_STAR),
        "planet": (ITEM_PLANET)
    }

    def __init__(self, x, y, item, health=100):
        super().__init__(x, y, health)
        self.ship_img = self.ITEM_MAP[item]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

class Enemy(Ship):
    def __init__ (self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = ITEM_ROCK
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def move(self, vel):
        self.y += vel

# Main Loop
def main():
    run = True
    FPS = 60    
    points = []
    num_points = 10
    points_vel = 2
    player_vel = 5
    enemies = []
    num_enemies = 5
    enemies_vel = 4
    player = Player(300, 630)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0))
        
        for enemy in enemies:
            enemy.draw(WIN)

        for point in points:
            point.draw(WIN)

        player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        
        if len(points) == 0:
            num_points += 10
            for i in range(num_points):
                point = Point(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["moon", "star", "planet"]))
                points.append(point)

        if len(enemies) == 0:
            num_enemies += 4
            for i in range(num_enemies):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT:
            player.y += player_vel

        for point in points[:]:
            point.move(points_vel)

        for enemy in enemies[:]:
            enemy.move(enemies_vel)
        
main()
