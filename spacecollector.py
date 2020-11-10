import pygame
import random
import time
import os
pygame.font.init()

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
        self.max_health = health

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

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

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

# Main Loop
def main():
    run = True
    FPS = 60
    score = 0    
    points = []
    num_points = 10
    points_vel = 4
    player_vel = 5
    enemies = []
    num_enemies = 10
    enemies_vel = 4
    player = Player(300, 630)
    main_font = pygame.font.SysFont("comicsans", 50)
    game_over_font = pygame.font.SysFont("comicsans", 60)
    

    clock = pygame.time.Clock()

    game_over = False
    game_over_count = 0 # to make sure game pauses when over

    def redraw_window():
        WIN.blit(BG, (0, 0))
        score_label = main_font.render(f"Score: {score}", 1, (255, 255, 255))

        WIN.blit(score_label, (10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        for point in points:
            point.draw(WIN)

        player.draw(WIN)

        if game_over:
            game_over_label = game_over_font.render("GAME OVER!", 1, (255, 255, 255))
            WIN.blit(game_over_label, (WIDTH/2 - game_over_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        
        if player.health <= 0:
            game_over = True
            game_over_count += 1 # to make sure game pauses when over
        
        if game_over:
            if game_over_count > FPS * 3: # to make sure game pauses when over
                run = False
            else:
                continue

        if len(points) < 10:
            num_points += 1
            for i in range(num_points):
                point = Point(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["moon", "star", "planet"]))
                points.append(point)

        if len(enemies) < 10:
            num_enemies += 1
            for i in range(num_enemies):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Player Movement:
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

            if collide(point, player): #collision detection
                score += 10
                points.remove(point)
            
            elif point.y + point.get_height() > HEIGHT:
                points.remove(point)

        for enemy in enemies[:]:
            enemy.move(enemies_vel)

            if collide(enemy, player):
                player.health -= 20
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                enemies.remove(enemy)

# Start Menu

def main_menu(): 
    instructions_font = pygame.font.SysFont("comicsans", 30)
    start_font = pygame.font.SysFont("comicsans", 45)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        instructions_label = instructions_font.render("A blackhole has opened! Save all that you can while avoiding asteroids!", 1, (255, 255, 255))
        WIN.blit(instructions_label, (WIDTH/2 - instructions_label.get_width()/2, 250))
        start_label = start_font.render("Click mouse button to begin", 1, (255, 255, 255))
        WIN.blit(start_label, (WIDTH/2 - start_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()
    
main_menu()
