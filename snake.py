import pygame
import random
import sys

pygame.init()

# made with art.text2art lol
snake_logo = pygame.image.load('snake.png')

dis_wh = 600
dis = pygame.display.set_mode((dis_wh, dis_wh))
pygame.display.set_caption("Snake")

c_yellow = (255, 255, 0)
c_green = (0, 120, 0)
c_red = (255, 0, 0)
c_white = (255, 255, 255)

clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 32)

grid_size = 20
grid_count = int(dis_wh / grid_size)

score = 0


class Snake(object):
    def __init__(self):
        self.headx, self.heady = random.randint(2, grid_count - 1), random.randint(0, grid_count - 1)
        self.body = [pygame.math.Vector2(self.headx, self.heady), pygame.math.Vector2(self.headx - 1, self.heady),
                     pygame.math.Vector2(self.headx - 2, self.heady)]
        self.width = grid_size
        self.dead = False
        self.color = c_yellow
        self.length = len(self.body)
        self.direction = 'right'
        self.grow = False

    def draw_snake(self):
        for block in self.body:
            pygame.draw.rect(dis, self.color, (block.x * grid_size, block.y * grid_size, self.width, self.width))

    def move_snake(self):
        if self.grow:
            body_copy = self.body
        else:
            body_copy = self.body[:-1]

        if self.direction == 'right':
            body_copy.insert(0, body_copy[0] + pygame.math.Vector2(1, 0))
        elif self.direction == 'left':
            body_copy.insert(0, body_copy[0] + pygame.math.Vector2(-1, 0))
        elif self.direction == 'up':
            body_copy.insert(0, body_copy[0] + pygame.math.Vector2(0, -1))
        elif self.direction == 'down':
            body_copy.insert(0, body_copy[0] + pygame.math.Vector2(0, 1))

        self.grow = False
        self.body = body_copy

    def collide_walls(self):
        for block in self.body:
            if 0 > block.x or block.x > grid_count - 1 or 0 > block.y or block.y > grid_count - 1:
                snake.dead = True

    def collide_body(self):
        if snake.body[0] in snake.body[1:]:  # index from 1 to the end
            snake.dead = True


class Fruit(object):
    def __init__(self):
        self.radius = 10
        self.pos = [pygame.math.Vector2(random.randint(0, grid_count - 1), random.randint(0, grid_count - 1))]
        self.color = c_red

    def draw_fruit(self):
        for block in self.pos:
            pygame.draw.circle(dis, self.color, radius=self.radius,
                               center=(block.x * grid_size + self.radius, block.y * grid_size + self.radius))

    def eat_fruit(self):
        global score
        if self.pos[0] == snake.body[0]:
            self.pos = [pygame.math.Vector2(random.randint(0, grid_count - 1), random.randint(0, grid_count - 1))]
            snake.grow = True
            score += 1
            print(f"Ate fruit, score: {score}")


snake = Snake()
apple = Fruit()

start_game = False
running = True

while running:

    game_over = font.render("Game over", True, c_white)
    retry = pygame.font.Font("freesansbold.ttf", 20).render("Press [SPACE] to retry", True, c_white)

    dis.fill(c_green)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            start_game = True
            if event.key == pygame.K_RIGHT:
                if snake.direction != 'left':
                    snake.direction = 'right'
            elif event.key == pygame.K_LEFT:
                if snake.direction != 'right':
                    snake.direction = 'left'
            elif event.key == pygame.K_UP:
                if snake.direction != 'down':
                    snake.direction = 'up'
            elif event.key == pygame.K_DOWN:
                if snake.direction != 'up':
                    snake.direction = 'down'

            elif event.key == pygame.K_SPACE:
                if snake.dead:
                    score = 0
                    snake = Snake()
                    start_game = True
                    snake.dead = False

    if snake.dead:
        dis.blit(game_over, (220, 275))
        dis.blit(retry, (200, 325))

    if not snake.dead:
        apple.draw_fruit()
        apple.eat_fruit()

        snake.draw_snake()
        snake.collide_walls()
        snake.collide_body()

        if start_game:
            snake.move_snake()

    if not start_game:
        dis.fill(c_green)
        dis.blit(pygame.font.Font("freesansbold.ttf", 32).render("Press [SPACE] to start", True, c_white), (135, 325))
        dis.blit(snake_logo, (180, 200))

    dis.blit(pygame.font.Font("freesansbold.ttf", 32).render(f"Score: {score}", True, c_white), (10, 10))

    clock.tick(10)
    pygame.display.update()
