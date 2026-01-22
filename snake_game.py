import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()

# Game constants
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BLOCK_SIZE = 20
SPEED = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Food colors for variety
FOOD_COLORS = [RED, ORANGE, YELLOW]

# Direction enum
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# Game mode enum
class GameMode(Enum):
    CLASSIC = 1  # Game ends when hitting wall
    FUN = 2      # Snake wraps around when hitting wall

Point = namedtuple('Point', 'x, y')

class SnakeGame:
    def __init__(self, mode=GameMode.CLASSIC):
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.mode = mode
        self.reset()
        
    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)
        ]
        self.score = 0
        self.food_items = []
        self._place_food()
        
    def set_mode(self, mode):
        """Set the game mode"""
        self.mode = mode
        self.reset()
        
    def _place_food(self):
        """Place 3 food items on the board"""
        self.food_items = []
        attempts = 0
        max_attempts = 100
        
        while len(self.food_items) < 3 and attempts < max_attempts:
            x = random.randint(0, (WINDOW_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (WINDOW_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            new_food = Point(x, y)
            
            # Check if position is valid (not on snake or other food)
            if new_food not in self.snake and new_food not in self.food_items:
                self.food_items.append(new_food)
            attempts += 1
            
    def play_step(self):
        # 1. Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_SPACE:
                    self.reset()
        
        # 2. Move snake
        self._move(self.direction)
        self.snake.insert(0, self.head)
        
        # 3. Check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. Check if food eaten and place new food or just move
        food_eaten = False
        for food in self.food_items:
            if self.head == food:
                self.score += 1
                food_eaten = True
                self.food_items.remove(food)
                # Add a new food item to maintain 3 food items
                self._add_single_food()
                break
        
        if not food_eaten:
            self.snake.pop()
        
        # 5. Update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)
        
        return game_over, self.score
    
    def _add_single_food(self):
        """Add a single food item to the board"""
        attempts = 0
        max_attempts = 100
        
        while attempts < max_attempts:
            x = random.randint(0, (WINDOW_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (WINDOW_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            new_food = Point(x, y)
            
            # Check if position is valid (not on snake or other food)
            if new_food not in self.snake and new_food not in self.food_items:
                self.food_items.append(new_food)
                break
            attempts += 1
    
    def _is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        
        # Check wall collision based on game mode
        if self.mode == GameMode.CLASSIC:
            # Classic mode: hitting wall ends game
            if pt.x > WINDOW_WIDTH - BLOCK_SIZE or pt.x < 0 or pt.y > WINDOW_HEIGHT - BLOCK_SIZE or pt.y < 0:
                return True
        # Fun mode: no wall collision (wrapping handled in _move)
        
        # Hit itself
        if pt in self.snake[1:]:
            return True
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        # Draw mode indicator
        font_small = pygame.font.Font(None, 24)
        mode_text = f"Mode: {self.mode.name}"
        mode_surface = font_small.render(mode_text, True, GRAY)
        self.display.blit(mode_surface, [WINDOW_WIDTH - 150, 10])
        
        # Draw snake
        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
            
        # Draw all food items with different colors
        for i, food in enumerate(self.food_items):
            color = FOOD_COLORS[i % len(FOOD_COLORS)]
            pygame.draw.rect(self.display, color, pygame.Rect(food.x, food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(text, [10, 10])
        
        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        
        # Fun mode: wrap around walls
        if self.mode == GameMode.FUN:
            if x >= WINDOW_WIDTH:
                x = 0
            elif x < 0:
                x = WINDOW_WIDTH - BLOCK_SIZE
            if y >= WINDOW_HEIGHT:
                y = 0
            elif y < 0:
                y = WINDOW_HEIGHT - BLOCK_SIZE
            
        self.head = Point(x, y)

def show_menu(display):
    """Display the game mode selection menu"""
    clock = pygame.time.Clock()
    selected = 0  # 0 for Classic, 1 for Fun
    
    # Menu options
    options = [
        ("CLASSIC MODE", "Game ends when hitting walls"),
        ("FUN MODE", "Snake wraps around walls")
    ]
    
    while True:
        display.fill(BLACK)
        
        # Title
        font_title = pygame.font.Font(None, 64)
        title = font_title.render("SNAKE GAME", True, GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 80))
        display.blit(title, title_rect)
        
        # Instructions
        font_small = pygame.font.Font(None, 24)
        instruction = font_small.render("Use UP/DOWN arrows to select, ENTER to start", True, WHITE)
        instruction_rect = instruction.get_rect(center=(WINDOW_WIDTH // 2, 140))
        display.blit(instruction, instruction_rect)
        
        # Menu options
        font_option = pygame.font.Font(None, 36)
        font_desc = pygame.font.Font(None, 20)
        
        for i, (option, description) in enumerate(options):
            y_pos = 220 + i * 100
            
            # Highlight selected option
            if i == selected:
                color = YELLOW
                # Draw selection box
                pygame.draw.rect(display, GRAY, 
                               (WINDOW_WIDTH // 2 - 180, y_pos - 10, 360, 70), 2)
            else:
                color = WHITE
            
            # Option text
            option_text = font_option.render(option, True, color)
            option_rect = option_text.get_rect(center=(WINDOW_WIDTH // 2, y_pos + 10))
            display.blit(option_text, option_rect)
            
            # Description text
            desc_text = font_desc.render(description, True, LIGHT_GRAY)
            desc_rect = desc_text.get_rect(center=(WINDOW_WIDTH // 2, y_pos + 40))
            display.blit(desc_text, desc_rect)
        
        pygame.display.flip()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % 2
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 2
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return GameMode.CLASSIC if selected == 0 else GameMode.FUN
        
        clock.tick(30)

def main():
    display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Snake Game')
    
    # Show menu and get selected mode
    mode = show_menu(display)
    
    # Create game with selected mode
    game = SnakeGame(mode)
    
    # Game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over:
            # Display game over message
            font = pygame.font.Font(None, 48)
            text = font.render('Game Over!', True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            game.display.blit(text, text_rect)
            
            # Display final score
            score_text = font.render(f'Score: {score}', True, YELLOW)
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            game.display.blit(score_text, score_rect)
            
            font_small = pygame.font.Font(None, 24)
            restart_text = font_small.render('Press SPACE to restart or ESC for menu', True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            game.display.blit(restart_text, restart_rect)
            
            pygame.display.flip()
            
            # Wait for restart or quit
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            game.reset()
                            waiting = False
                        elif event.key == pygame.K_ESCAPE:
                            # Return to menu
                            mode = show_menu(display)
                            game.set_mode(mode)
                            waiting = False

if __name__ == '__main__':
    main()

# Made with Bob
