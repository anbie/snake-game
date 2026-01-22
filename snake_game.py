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

# Food colors for variety
FOOD_COLORS = [RED, ORANGE, YELLOW]

# Direction enum
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

class SnakeGame:
    def __init__(self):
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
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
        
    def _place_food(self):
        """Place 3 food items on the board"""
        self.food_items = []
        attempts = 0
        max_attempts = 100
        
        while len(self.food_items) < 3 and attempts < max_attempts:
            x = random.randint(0, (WINDOW_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (WINDOW_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            new_food = Point(x+10, y)
            
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
        # Hit boundary
        if pt.x > WINDOW_WIDTH - BLOCK_SIZE or pt.x < 0 or pt.y > WINDOW_HEIGHT - BLOCK_SIZE or pt.y < 0:
            return True
        # Hit itself
        if pt in self.snake[1:]:
            return True
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
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
            
        self.head = Point(x, y)

def main():
    game = SnakeGame()
    
    # Game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over:
            # Display game over message
            font = pygame.font.Font(None, 48)
            text = font.render('Game Over!', True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
            game.display.blit(text, text_rect)
            
            font_small = pygame.font.Font(None, 24)
            restart_text = font_small.render('Press SPACE to restart', True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
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

if __name__ == '__main__':
    main()

# Made with Bob
