import pygame
pygame.init()

# Variables
FPS = 60
WIDTH, HEIGHT = 720, 640
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_RADIUS = 10
FONT = pygame.font.SysFont("comicsans", 50)
SCORE_LIMIT = 5

class Paddle:
    COLOR = (255, 255, 255)
    VEL = 7

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL
    
    def reset(self, x, y):
        self.x = x
        self.y = y

class Ball:
    COLOR = WHITE
    MAX_VEL = 5
    
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
    
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)
    left_score_text = FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))
    
    ball.draw(win)
    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1.01
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1.01
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

def home_screen():
    title_font = pygame.font.SysFont("comicsans", 70)
    instruction_font = pygame.font.SysFont("comicsans", 40)
    run = True
    while run:
        SCREEN.fill(BLACK)
        title_label = title_font.render("Pong Game", 1, WHITE)
        instruction_label = instruction_font.render("Press any key to start", 1, WHITE)

        SCREEN.blit(title_label, (WIDTH//2 - title_label.get_width()//2, HEIGHT//3))
        SCREEN.blit(instruction_label, (WIDTH//2 - instruction_label.get_width()//2, HEIGHT//2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                run = False

def display_winner(winner):
    winner_font = pygame.font.SysFont("comicsans", 70)
    instruction_font = pygame.font.SysFont("comicsans", 40)
    run = True
    while run:
        SCREEN.fill(BLACK)
        winner_label = winner_font.render(f"{winner} Wins!", 1, WHITE)
        instruction_label = instruction_font.render("Press any key to exit", 1, WHITE)

        SCREEN.blit(winner_label, (WIDTH//2 - winner_label.get_width()//2, HEIGHT//3))
        SCREEN.blit(instruction_label, (WIDTH//2 - instruction_label.get_width()//2, HEIGHT//2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                run = False

def main():
    home_screen()
    status = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    left_score = 0
    right_score = 0

    while status:
        clock.tick(FPS)
        draw(SCREEN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
            left_paddle.reset(10, HEIGHT//2 - PADDLE_HEIGHT//2)
            right_paddle.reset(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)
        elif ball.x > WIDTH:
            left_score += 1
            left_paddle.reset(10, HEIGHT//2 - PADDLE_HEIGHT//2)
            right_paddle.reset(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)
            ball.reset()

        if left_score >= SCORE_LIMIT:
            display_winner("Left Player")
            status = False
        elif right_score >= SCORE_LIMIT:
            display_winner("Right Player")
            status = False

    pygame.quit()

if __name__ == '__main__':
    main()
