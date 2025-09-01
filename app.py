import pygame
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)       # Frog color
DARK_GREEN = (0, 100, 0)  # Safe zone color
GRAY = (100, 100, 100)    # Road color
YELLOW = (255, 235, 59)   # Lane marker color

# Game Object Sizes
PLAYER_SIZE = 30
LANE_HEIGHT = 50
SAFE_ZONE_HEIGHT = 60

# --- Game Classes ---

class Player(pygame.sprite.Sprite):
    """Represents the frog the player controls."""
    def __init__(self):
        super().__init__()
        # Create a square surface for the player
        self.image = pygame.Surface([PLAYER_SIZE, PLAYER_SIZE])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        
        # Store starting position for resetting
        self.start_x = (SCREEN_WIDTH - PLAYER_SIZE) / 2
        self.start_y = SCREEN_HEIGHT - SAFE_ZONE_HEIGHT + (SAFE_ZONE_HEIGHT - PLAYER_SIZE) / 2
        self.reset()

    def reset(self):
        """Move the player back to the starting position."""
        self.rect.x = self.start_x
        self.rect.y = self.start_y

    def move_up(self):
        # Move one "lane" up, but don't go off screen
        self.rect.y -= LANE_HEIGHT
        if self.rect.y < 0:
            self.rect.y = 0

    def move_down(self):
        # Move one "lane" down, but not into the starting safe zone
        self.rect.y += LANE_HEIGHT
        if self.rect.y > self.start_y:
            self.rect.y = self.start_y

    def move_left(self):
        self.rect.x -= PLAYER_SIZE
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self):
        self.rect.x += PLAYER_SIZE
        if self.rect.x > SCREEN_WIDTH - PLAYER_SIZE:
            self.rect.x = SCREEN_WIDTH - PLAYER_SIZE

class Obstacle(pygame.sprite.Sprite):
    """Represents a car on the road."""
    def __init__(self, x, y, speed, width, color):
        super().__init__()
        self.image = pygame.Surface([width, PLAYER_SIZE])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        """Move the obstacle and wrap around the screen."""
        self.rect.x += self.speed
        # If moving right and off-screen
        if self.speed > 0 and self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        # If moving left and off-screen
        if self.speed < 0 and self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

# --- Game Setup ---

def draw_background(screen):
    """Draws the static background elements (road, safe zones, lane markers)."""
    # Fill background
    screen.fill(GRAY)
    
    # Draw safe zones
    pygame.draw.rect(screen, DARK_GREEN, [0, 0, SCREEN_WIDTH, SAFE_ZONE_HEIGHT])
    pygame.draw.rect(screen, DARK_GREEN, [0, SCREEN_HEIGHT - SAFE_ZONE_HEIGHT, SCREEN_WIDTH, SAFE_ZONE_HEIGHT])

    # Draw lane markers
    num_lanes = 8
    for i in range(1, num_lanes):
        y_pos = SAFE_ZONE_HEIGHT + i * LANE_HEIGHT
        # Draw dashed lines
        for x in range(0, SCREEN_WIDTH, 40): # 40 = dash length + gap
            pygame.draw.line(screen, YELLOW, (x, y_pos), (x + 20, y_pos), 4)

def show_message(screen, text, size, color, y_position):
    """Helper function to display text on the screen."""
    font = pygame.font.SysFont("Arial", size, bold=True)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (SCREEN_WIDTH / 2, y_position)
    screen.blit(text_surface, text_rect)

# --- Main Game Function ---

def main():
    """Main game loop."""
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Frogger Clone")
    clock = pygame.time.Clock()

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    obstacle_group = pygame.sprite.Group()

    # Create player
    player = Player()
    all_sprites.add(player)

    # Game state variables
    game_over = False
    game_win = False
    score = 0
    
    # --- Create Obstacles (Cars) ---
    lane_y_start = SAFE_ZONE_HEIGHT + (LANE_HEIGHT - PLAYER_SIZE) / 2
    car_colors = [(211, 0, 211), (100, 0, 200), (123, 200, 0), (150, 0, 150), (221, 165, 0)]
    
    # Define lanes: y_position, speed, number_of_cars, car_width
    lanes_config = [
        (lane_y_start, 3, 2, 80),
        (lane_y_start + LANE_HEIGHT, -2, 3, 50),
        (lane_y_start + 2 * LANE_HEIGHT, 4, 2, 70),
        (lane_y_start + 3 * LANE_HEIGHT, -3, 3, 60),
        (lane_y_start + 4 * LANE_HEIGHT, 2, 2, 90),
        (lane_y_start + 5 * LANE_HEIGHT, -4, 2, 50),
        (lane_y_start + 6 * LANE_HEIGHT, 3, 3, 60),
        (lane_y_start + 7 * LANE_HEIGHT, -2, 2, 80),
    ]

    for y, speed, num_cars, width in lanes_config:
        for i in range(num_cars):
            # Space cars out evenly across the screen
            x = (SCREEN_WIDTH / num_cars) * i + random.randint(-50, 50)
            color = random.choice(car_colors)
            obstacle = Obstacle(x, y, speed, width, color)
            all_sprites.add(obstacle)
            obstacle_group.add(obstacle)

    # --- Game Loop ---
    running = True
    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not game_over and not game_win:
                    if event.key == pygame.K_UP:
                        player.move_up()
                    elif event.key == pygame.K_DOWN:
                        player.move_down()
                    elif event.key == pygame.K_LEFT:
                        player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        player.move_right()
                
                # Restart game
                if (game_over or game_win) and event.key == pygame.K_r:
                    # Reset game state
                    game_over = False
                    game_win = False
                    score = 0
                    player.reset()


        # --- Game Logic ---
        if not game_over and not game_win:
            # Update all sprites
            all_sprites.update()

            # Check for collision with cars
            if pygame.sprite.spritecollide(player, obstacle_group, False):
                game_over = True
                
            # Check for win condition (reaching the top)
            if player.rect.y < SAFE_ZONE_HEIGHT:
                game_win = True
                score += 1

        # --- Drawing ---
        draw_background(screen)
        all_sprites.draw(screen)

        # Draw Score
        show_message(screen, f"SCORE: {score}", 30, WHITE, 25)

        # Display game over or win message
        if game_over:
            show_message(screen, "GAME OVER", 70, (255, 50, 50), SCREEN_HEIGHT / 2 - 40)
            show_message(screen, "Press 'R' to Restart", 30, WHITE, SCREEN_HEIGHT / 2 + 20)

        if game_win:
            show_message(screen, "YOU MADE IT!", 70, (50, 255, 50), SCREEN_HEIGHT / 2 - 40)
            show_message(screen, "Press 'R' to Play Again", 30, WHITE, SCREEN_HEIGHT / 2 + 20)
            player.reset() # Reset player for the next round
            game_win = False # Continue playing after a brief pause effect


        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()