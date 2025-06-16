import pygame
import sys
import math
import random
import os


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Slingshot Shooting Simulator')
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

PROJ_FOLDER = os.path.dirname(os.path.abspath(__file__))

window_sprite = pygame.image.load(rf"{PROJ_FOLDER}\window.png")
projectile_sprite = pygame.image.load(rf"{PROJ_FOLDER}\projectile.png")
slingshot_sprite = pygame.image.load(rf"{PROJ_FOLDER}\slingshot.png")

SLING_X, SLING_Y = 100, HEIGHT - 100

TARGET_WIDTH, TARGET_HEIGHT = 80, 120
TARGET_X = 650
TARGET_RECT = pygame.Rect(TARGET_X, HEIGHT - 250, TARGET_WIDTH, TARGET_HEIGHT)


GRAVITY = 0.5

angle = 45

projectile = None
hit = False
font = pygame.font.SysFont(None, 48)

current_power = 0
MAX_POWER = 30

points = 0
projectiles_left = 5
shop_button = pygame.Rect(WIDTH - 100, 20, 80, 40)


def update_power():
    global current_power
    current_power = (current_power + 1) % (MAX_POWER + 1)


def spawn_target():
    y = random.randint(100, HEIGHT - TARGET_HEIGHT)
    return pygame.Rect(TARGET_X, y, TARGET_WIDTH, TARGET_HEIGHT)


def draw_slingshot(angle):
    screen.blit(slingshot_sprite, (SLING_X - 20, SLING_Y - 20))

    rad = math.radians(angle)
    hint_length = 100
    hint_x = SLING_X + math.cos(rad) * hint_length
    hint_y = SLING_Y - math.sin(rad) * hint_length
    pygame.draw.line(screen, RED, (SLING_X, SLING_Y), (hint_x, hint_y), 2)


def draw_target():
    screen.blit(window_sprite, TARGET_RECT)


def draw_projectile():
    if projectile:
        x, y, _, _ = projectile
        screen.blit(projectile_sprite, (x - 10, y - 10))


def reset_projectile():
    global projectile, hit, projectiles_left
    if projectiles_left > 0:
        rad = math.radians(angle)
        vx = math.cos(rad) * current_power
        vy = -math.sin(rad) * current_power
        projectile = [SLING_X, SLING_Y, vx, vy]
        hit = False
        projectiles_left -= 1
    


def update_projectile():
    global projectile, hit, TARGET_RECT, points
    if projectile:
        x, y, vx, vy = projectile
        vy += GRAVITY
        x += vx
        y += vy
        projectile = [x, y, vx, vy]
        if TARGET_RECT.collidepoint(x, y):
            hit = True
            projectile = None
            TARGET_RECT = spawn_target()
            points += 1
        elif x > WIDTH or y > HEIGHT or x < 0 or y < 0:
            projectile = None


def draw_text(text, color, y):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(WIDTH // 2, y))
    screen.blit(img, rect)


def draw_shop_button():
    pygame.draw.rect(screen, GREEN, shop_button)
    shop_text = font.render("Shop", True, BLACK)
    screen.blit(shop_text, (shop_button.x + 10, shop_button.y + 5))


def buy_projectiles():
    global projectiles_left, points
    if points >= 1:
        projectiles_left += 1
        points -= 1


def draw_power_bar():
    bar_width = 200
    bar_height = 20
    bar_x = WIDTH // 2 - bar_width // 2
    bar_y = HEIGHT - 60
    progress = current_power / MAX_POWER
    color = (int(255 * (1 - progress)), int(255 * progress), 0)  # Green to Red
    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, color, (bar_x, bar_y, int(bar_width * progress), bar_height))


running = True
while running:
    screen.fill(WHITE)
    update_power()
    draw_slingshot(angle)
    draw_target()
    draw_projectile()
    draw_shop_button()
    draw_power_bar()
    if hit:
        draw_text('Hit!', RED, 100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                angle = min(angle + 2, 80)
            elif event.key == pygame.K_DOWN:
                angle = max(angle - 2, 10)
            elif event.key == pygame.K_SPACE and projectile is None:
                reset_projectile()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if shop_button.collidepoint(event.pos):
                buy_projectiles()

    update_projectile()

    draw_text(f'Angle: {angle}°  Points: {points}  Projectiles: {projectiles_left}', BLACK, HEIGHT - 30)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit() 
