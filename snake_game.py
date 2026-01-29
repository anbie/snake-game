"""
Snake Game Module
=================

A classic Snake game implementation using Pygame with two game modes:
Classic mode (game ends on wall collision) and Fun mode (snake wraps around walls).

The game features:
    - Two game modes (Classic and Fun)
    - Multiple food items on the board
    - High score tracking
    - Colorful graphics
    - Menu system for mode selection

Constants:
    WINDOW_WIDTH (int): Width of the game window in pixels
    WINDOW_HEIGHT (int): Height of the game window in pixels
    BLOCK_SIZE (int): Size of each game block in pixels
    SPEED (int): Game speed (frames per second)
    NUM_FOOD_ITEMS (int): Number of food items on the board
    HIGHSCORE_FILE (str): Filename for storing high scores

.. moduleauthor:: Snake Game Developer
"""

import pygame
import random
import json
import os
from enum import Enum
from collections import namedtuple

pygame.init()

# Game constants
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BLOCK_SIZE = 20
SPEED = 10
NUM_FOOD_ITEMS = 8  # Number of food items on the board
HIGHSCORE_FILE = 'highscores.json'

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
FOOD_COLORS = [RED, ORANGE, YELLOW, BLUE]


class Direction(Enum):
    """
    Enumeration for snake movement directions.
    
    Attributes:
        RIGHT (int): Move right direction
        LEFT (int): Move left direction
        UP (int): Move up direction
        DOWN (int): Move down direction
    """
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class GameMode(Enum):
    """
    Enumeration for game modes.
    
    Attributes:
        CLASSIC (int): Classic mode where game ends when hitting walls
        FUN (int): Fun mode where snake wraps around when hitting walls
    """
    CLASSIC = 1  # Game ends when hitting wall
    FUN = 2      # Snake wraps around when hitting wall


Point = namedtuple('Point', 'x, y')
"""
A named tuple representing a 2D point.

Attributes:
    x (int): X coordinate
    y (int): Y coordinate
"""


def load_highscores():
    """
    Load high scores from the JSON file.
    
    Reads the high scores from the HIGHSCORE_FILE. If the file doesn't exist
    or contains invalid JSON, returns default scores of 0 for both modes.
    
    :return: Dictionary containing high scores for 'classic' and 'fun' modes
    :rtype: dict
    
    Example:
        >>> scores = load_highscores()
        >>> print(scores)
        {'classic': 10, 'fun': 15}
    """
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {'classic': 0, 'fun': 0}
    return {'classic': 0, 'fun': 0}


def save_highscores(highscores):
    """
    Save high scores to the JSON file.
    
    Writes the high scores dictionary to HIGHSCORE_FILE. Silently fails
    if the file cannot be written.
    
    :param highscores: Dictionary containing high scores for both game modes
    :type highscores: dict
    
    Example:
        >>> save_highscores({'classic': 10, 'fun': 15})
    """
    try:
        with open(HIGHSCORE_FILE, 'w') as f:
            json.dump(highscores, f)
    except IOError:
        pass  # Silently fail if can't save


class SnakeGame:
    """
    Main Snake Game class.
    
    This class manages the game state, rendering, and game logic for the Snake game.
    It supports two game modes: Classic (walls are deadly) and Fun (walls wrap around).
    
    :param mode: The game mode to use, defaults to GameMode.CLASSIC
    :type mode: GameMode, optional
    
    Attributes:
        display (pygame.Surface): The game display surface
        clock (pygame.time.Clock): Clock for controlling game speed
        mode (GameMode): Current game mode
        highscores (dict): Dictionary of high scores for both modes
        direction (Direction): Current movement direction of the snake
        head (Point): Current position of the snake's head
        snake (list): List of Points representing the snake's body
        score (int): Current game score
        food_items (list): List of Points representing food positions
    
    Example:
        >>> game = SnakeGame(GameMode.CLASSIC)
        >>> game_over, score = game.play_step()
    """
    
    def __init__(self, mode=GameMode.CLASSIC):
        """
        Initialize the Snake Game.
        
        :param mode: The game mode to use, defaults to GameMode.CLASSIC
        :type mode: GameMode, optional
        """
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.mode = mode
        self.highscores = load_highscores()
        self.reset()
        
    def reset(self):
        """
        Reset the game to initial state.
        
        Resets the snake position, direction, score, and places new food items.
        Called at game start and when restarting after game over.
        """
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
        """
        Set the game mode and reset the game.
        
        :param mode: The new game mode to use
        :type mode: GameMode
        """
        self.mode = mode
        self.reset()
        
    def _place_food(self):
        """
        Place multiple food items on the board.
        
        Attempts to place NUM_FOOD_ITEMS food items in valid positions
        (not on the snake or other food). Makes up to 100 attempts per food item.
        """
        self.food_items = []
        attempts = 0
        max_attempts = 100
        
        while len(self.food_items) < NUM_FOOD_ITEMS and attempts < max_attempts:
            x = random.randint(0, (WINDOW_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (WINDOW_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            new_food = Point(x, y)
            
            # Check if position is valid (not on snake or other food)
            if new_food not in self.snake and new_food not in self.food_items:
                self.food_items.append(new_food)
            attempts += 1
            
    def play_step(self):
        """
        Execute one step of the game loop.
        
        Handles user input, moves the snake, checks for collisions and food consumption,
        updates the UI, and controls the game speed.
        
        :return: Tuple of (game_over, score) where game_over is True if the game ended
        :rtype: tuple(bool, int)
        
        Example:
            >>> game = SnakeGame()
            >>> game_over, score = game.play_step()
            >>> if game_over:
            ...     print(f"Game Over! Final score: {score}")
        """
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
            self._update_highscore()
            return game_over, self.score
            
        # 4. Check if food eaten and place new food or just move
        food_eaten = False
        for food in self.food_items:
            if self.head == food:
                self.score += 1
                food_eaten = True
                self.food_items.remove(food)
                # Add a new food item to maintain NUM_FOOD_ITEMS
                self._add_single_food()
                break
        
        if not food_eaten:
            self.snake.pop()
        
        # 5. Update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)
        
        return game_over, self.score
    
    def _add_single_food(self):
        """
        Add a single food item to the board.
        
        Attempts to place one food item in a valid position (not on the snake
        or other food). Makes up to 100 attempts.
        """
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
    
    def _update_highscore(self):
        """
        Update the high score if the current score is higher.
        
        Compares the current score with the saved high score for the current
        game mode and updates it if necessary. Saves the updated scores to file.
        """
        mode_key = 'classic' if self.mode == GameMode.CLASSIC else 'fun'
        if self.score > self.highscores[mode_key]:
            self.highscores[mode_key] = self.score
            save_highscores(self.highscores)
    
    def get_highscore(self):
        """
        Get the high score for the current game mode.
        
        :return: The high score for the current mode
        :rtype: int
        """
        mode_key = 'classic' if self.mode == GameMode.CLASSIC else 'fun'
        return self.highscores[mode_key]
    
    def _is_collision(self, pt=None):
        """
        Check if there is a collision at the given point.
        
        Checks for wall collision (in Classic mode) and self-collision.
        In Fun mode, wall collision is not checked as the snake wraps around.
        
        :param pt: The point to check for collision, defaults to snake's head
        :type pt: Point, optional
        :return: True if there is a collision, False otherwise
        :rtype: bool
        """
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
        """
        Update the game display.
        
        Renders the snake, food items, score, high score, and game mode indicator
        on the display surface.
        """
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
        
        # Draw high score
        highscore = self.get_highscore()
        highscore_text = font_small.render(f"High Score: {highscore}", True, YELLOW)
        self.display.blit(highscore_text, [10, 45])
        
        pygame.display.flip()
        
    def _move(self, direction):
        """
        Move the snake's head in the specified direction.
        
        Updates the head position based on the direction. In Fun mode,
        wraps the snake around when it reaches the screen boundaries.
        
        :param direction: The direction to move the snake
        :type direction: Direction
        """
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
    """
    Display the game mode selection menu.
    
    Shows a menu where the player can select between Classic and Fun game modes
    using arrow keys and Enter. The menu includes descriptions of each mode.
    
    :param display: The pygame display surface to render the menu on
    :type display: pygame.Surface
    :return: The selected game mode
    :rtype: GameMode
    
    Example:
        >>> display = pygame.display.set_mode((640, 480))
        >>> mode = show_menu(display)
        >>> print(f"Selected mode: {mode.name}")
    """
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
    """
    Main entry point for the Snake Game.
    
    Initializes the game, displays the menu for mode selection, and runs
    the main game loop. Handles game over state and allows restarting or
    returning to the menu.
    
    The game loop continues until the user quits the application.
    """
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