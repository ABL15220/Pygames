import pygame
import math
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker (Turn-Based)")

# Game settings
BALL_RADIUS = 5
BLOCK_SIZE = 40
BALL_SPEED = 5
FPS = 60
FONT = pygame.font.SysFont("Arial", 18)
BIG_FONT = pygame.font.SysFont("Arial", 36)

class Ball:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.dx = math.cos(angle) * BALL_SPEED
        self.dy = math.sin(angle) * BALL_SPEED
        self.active = True

    def move(self):
        if not self.active:
            return
        self.x += self.dx
        self.y += self.dy

        # Bounce on walls
        if self.x <= 0 or self.x >= WIDTH:
            self.dx *= -1
        if self.y <= 0:
            self.dy *= -1

        if self.y >= HEIGHT:
            self.active = False

    def draw(self, win):
        pygame.draw.circle(win, (255, 255, 255), (int(self.x), int(self.y)), BALL_RADIUS)

class Block:
    def __init__(self, x, y, health):
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.health = health

    def draw(self, win):
        color = (255, 100, 100)
        pygame.draw.rect(win, color, self.rect)
        text = FONT.render(str(self.health), True, (255, 255, 255))
        win.blit(text, (self.rect.x + 10, self.rect.y + 10))

    def hit(self):
        self.health -= 1
        return self.health <= 0

def generate_blocks(row_health):
    blocks = []
    for i in range(WIDTH // BLOCK_SIZE):
        if random.random() < 0.7:
            blocks.append(Block(i * BLOCK_SIZE, 0, row_health))
    return blocks

def show_game_over(win, score):
    while True:
        win.fill((30, 30, 30))
        text = BIG_FONT.render("Game Over", True, (255, 50, 50))
        score_text = FONT.render(f"Final Score: {score}", True, (255, 255, 255))
        play_again_text = FONT.render("Play Again", True, (0, 0, 0))
        button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 40, 120, 40)

        win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 60))
        win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 10))
        pygame.draw.rect(win, (200, 200, 200), button_rect)
        win.blit(play_again_text, (button_rect.x + 15, button_rect.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Exit game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True  # Restart game

def main_game():
    clock = pygame.time.Clock()
    balls = []
    blocks = []
    base_x = WIDTH // 2
    throw_ready = True
    row_health = 1
    ball_count = 1
    base_point = (base_x, HEIGHT - 10)
    score = 0

    launching = False
    launch_index = 0
    launch_delay = 5
    launch_timer = 0
    launch_angle = 0

    running = True
    while running:
        clock.tick(FPS)
        WIN.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if throw_ready and event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                launch_angle = math.atan2(my - base_point[1], mx - base_point[0])
                launching = True
                throw_ready = False
                launch_index = 0
                launch_timer = 0
                balls = []

        if launching:
            launch_timer += 1
            if launch_timer >= launch_delay:
                balls.append(Ball(*base_point, launch_angle))
                launch_index += 1
                launch_timer = 0
                if launch_index >= ball_count:
                    launching = False

        all_inactive = True
        for ball in balls:
            ball.move()
            ball.draw(WIN)
            if ball.active:
                all_inactive = False
                for block in blocks:
                    if block.rect.collidepoint(ball.x, ball.y):
                        score += 1
                        ball.dy *= -1
                        if block.hit():
                            blocks.remove(block)
                        break

        if throw_ready is False and launching is False and all_inactive:
            throw_ready = True
            row_health += 2
            ball_count += 1
            blocks.extend(generate_blocks(row_health))
            for block in blocks:
                block.rect.y += BLOCK_SIZE
                if block.rect.y + BLOCK_SIZE >= HEIGHT:
                    return show_game_over(WIN, score)
            base_x = int(balls[-1].x) if balls else WIDTH // 2
            base_point = (base_x, HEIGHT - 10)

        for block in blocks:
            block.draw(WIN)

        pygame.draw.circle(WIN, (0, 255, 0), base_point, BALL_RADIUS)

        if throw_ready:
            mx, my = pygame.mouse.get_pos()
            pygame.draw.line(WIN, (100, 255, 100), base_point, (mx, my), 2)

        score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
        WIN.blit(score_text, (10, 10))

        pygame.display.flip()

def main():
    while True:
        play = main_game()
        if not play:
            break
    pygame.quit()

if __name__ == "__main__":
    main()
