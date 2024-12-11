import pygame
import os
import sys

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

pygame.init()

APP_WIDTH = 800
APP_HEIGHT = 600
FPS = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
pygame.display.set_caption("Pong")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

field_division_path = os.path.join(base_path, "assets/field_division.png")
field_division = pygame.image.load(field_division_path).convert_alpha()
font_path = os.path.join(base_path, "assets/Montserrat-Light.ttf")
label = pygame.font.Font(font_path, 64)

class Rect:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 8
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.score = 0

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def up(self):
        if self.y > 0:
            self.y -= self.speed
            self.update_rect()

    def down(self):
        if self.y < APP_HEIGHT - self.height:
            self.y += self.speed
            self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def add_score(self):
        self.score += 1

player_1 = Rect(18, 264, 8, 72, WHITE)
player_2 = Rect(774, 264, 8, 72, WHITE)

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = 6
        self.speed_y = 6
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def reset_position(self, direction):
        self.x = 400
        self.y = 300
        if direction:
            self.speed_x = 6
            self.speed_y = 6
        else:
            self.speed_x = -6
            self.speed_y = -6

    def increase_speed(self, factor):
        self.speed_x *= factor
        self.speed_y *= factor

    def check_collision(self, app_width, app_height):

        if self.y - self.radius <= 0 or self.y + self.radius >= app_height:
            self.speed_y *= -1

        elif self.x <= 0:
            player_2.add_score()
            self.reset_position(False)

        elif self.x + self.radius >= app_width:
            player_1.add_score()
            self.reset_position(True)

ball = Ball(400, 300, 8, WHITE)

def game_field_draw(): # (scores)
    screen.fill(BLACK)
    screen.blit(field_division, (398, 0))
    player_1_score = label.render(str(player_1.score), True, (217, 217, 217, 40))
    screen.blit(player_1_score, (182, 48))
    player_2_score = label.render(str(player_2.score), True, (217, 217, 217, 40))
    screen.blit(player_2_score, (581, 48))

running = True
while running:

    game_field_draw()
    player_1.draw()
    player_2.draw()
    ball.draw()
    ball.move()
    ball.check_collision(APP_WIDTH, APP_HEIGHT)

    keys = pygame.key.get_pressed()

    if player_1.rect.colliderect(ball.rect):
        relative_intersect_y = (ball.y - player_1.y) / player_1.height
        angle = relative_intersect_y - 0.5
        ball.speed_x = abs(ball.speed_x)
        ball.speed_y += angle * 10

    if player_2.rect.colliderect(ball.rect):
        relative_intersect_y = (ball.y - player_2.y) / player_2.height
        angle = relative_intersect_y - 0.5
        ball.speed_x = -abs(ball.speed_x)
        ball.speed_y += angle * 10

    ''' Automatic
    if ball.speed_x > 0:
        if ball.y > player_2.y + player_2.height // 2:
            player_2.down()
        else:
            player_2.up()

        if player_1.y + player_1.height // 2 > APP_HEIGHT // 2:
            player_1.up()
        else:
            player_1.down()

    else:
        if player_2.y + player_2.height // 2 > APP_HEIGHT // 2:
            player_2.up()
        else:
            player_2.down()

        if ball.y > player_1.y + player_1.height // 2:
            player_1.down()
        else:
            player_1.up()
    '''

    if keys[pygame.K_w]:
        player_1.up()

    if keys[pygame.K_s]:
        player_1.down()

    if keys[pygame.K_UP]:
        player_2.up()

    if keys[pygame.K_DOWN]:
        player_2.down()

    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()