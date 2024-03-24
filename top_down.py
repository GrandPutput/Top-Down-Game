import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survive for as long as possible!")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player properties
player_size = 40
player_speed = 5

# Enemy properties
enemy_size = 30
enemies = []
enemy_speed = 3
enemy_spawn_rate = 50
enemy_spawn_counter = enemy_spawn_rate

# Item properties
item_size = 20
item_count = 10
items = [(random.randint(0, WIDTH - item_size), random.randint(0, HEIGHT - item_size)) for _ in range(item_count)]

# High score
high_score = 0

# Starting menu
def start_menu():
    global high_score
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    score = main_game()
                    if score > high_score:
                        high_score = score
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        window.fill(WHITE)
        font = pygame.font.Font(None, 36)
        title_text = font.render("Survive for as long as possible", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score} seconds", True, BLACK)
        start_text = font.render("Press SPACE to start", True, BLACK)
        quit_text = font.render("Press Q to quit", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
        high_score_rect = high_score_text.get_rect(center=(WIDTH/2, HEIGHT/2))
        start_rect = start_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
        quit_rect = quit_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 100))
        window.blit(title_text, title_rect)
        window.blit(high_score_text, high_score_rect)
        window.blit(start_text, start_rect)
        window.blit(quit_text, quit_rect)
        pygame.display.flip()

# Main game loop
def main_game():
    global player_x, player_y, enemies, items

    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT // 2 - player_size // 2

    running = True
    frame_count = 0
    while running:
        frame_count += 1

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get keys pressed
        keys = pygame.key.get_pressed()

        # Move player
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

        # Clamp player position to stay within the window boundaries
        player_x = max(0, min(player_x, WIDTH - player_size))
        player_y = max(0, min(player_y, HEIGHT - player_size))

        # Spawn enemies
        spawn_enemies()

        # Move enemies towards the player
        move_enemies()

        # Collision detection between player and enemies
        if not check_collision_with_enemies():
            return frame_count // 30  # Convert frames to seconds

        # Collision detection between player and items
        check_collision_with_items()

        # Clear the screen
        window.fill(WHITE)

        # Draw the player
        pygame.draw.rect(window, BLACK, (player_x, player_y, player_size, player_size))

        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(window, RED, (enemy[0], enemy[1], enemy_size, enemy_size))

        # Draw items
        for item in items:
            pygame.draw.rect(window, BLACK, (item[0], item[1], item_size, item_size))

        # Update the display
        pygame.display.flip()

        # Limit frames per second
        pygame.time.Clock().tick(30)

def spawn_enemies():
    global enemy_spawn_counter
    enemy_spawn_counter -= 1
    if enemy_spawn_counter <= 0:
        enemies.append((random.randint(0, WIDTH - enemy_size), random.randint(0, HEIGHT - enemy_size)))
        enemy_spawn_counter = enemy_spawn_rate

def move_enemies():
    global enemies, player_x, player_y
    for i, enemy in enumerate(enemies):
        enemy_x, enemy_y = enemy
        if enemy_x < player_x:
            enemy_x += enemy_speed
        elif enemy_x > player_x:
            enemy_x -= enemy_speed
        if enemy_y < player_y:
            enemy_y += enemy_speed
        elif enemy_y > player_y:
            enemy_y -= enemy_speed
        enemies[i] = (enemy_x, enemy_y)

def check_collision_with_enemies():
    global player_x, player_y, player_size, enemies
    for enemy in enemies:
        if (player_x < enemy[0] + enemy_size and
            player_x + player_size > enemy[0] and
            player_y < enemy[1] + enemy_size and
            player_y + player_size > enemy[1]):
            # Game over if player collides with enemy
            print("Game Over!")
            return False
    return True

def check_collision_with_items():
    global player_x, player_y, player_size, items
    for item in items[:]:
        if (player_x < item[0] + item_size and
            player_x + player_size > item[0] and
            player_y < item[1] + item_size and
            player_y + player_size > item[1]):
            # Remove collected items
            items.remove(item)

start_menu()
