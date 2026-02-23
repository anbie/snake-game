"""
Snake Game Module
=================

A classic Snake game implementation using Pygame with two game modes:
Classic mode (game ends on wall collision) and Fun mode (snake wraps around walls).

The game features:
    - Two game modes (Classic and Fun)
    - Configurable number of food items on the board
    - High score tracking
    - Colorful graphics
    - Menu system for mode selection
    - Pause functionality

Constants:
    WINDOW_WIDTH (int): Width of the game window in pixels
    WINDOW_HEIGHT (int): Height of the game window in pixels
    BLOCK_SIZE (int): Size of each game block in pixels
    SPEED (int): Game speed (frames per second)
    DEFAULT_NUM_FOOD_ITEMS (int): Default number of food items on the board
    HIGHSCORE_FILE (str): Filename for storing high scores

.. moduleauthor:: Snake Game Developer
"""

import pygame
import random
import json
import os
import logging
from enum import Enum
from collections import namedtuple
from typing import List, Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Initialize pygame once at module level
pygame.init()

# Game constants
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BLOCK_SIZE = 20
SPEED = 10
DEFAULT_NUM_FOOD_ITEMS = 4  # Default number of food items on the board
MIN_FOOD_ITEMS = 1
MAX_FOOD_ITEMS = 50
HIGHSCORE_FILE = os.environ.get('SNAKE_HIGHSCORE_FILE', 'highscores.json')

# Visual constants
SNAKE_INNER_OFFSET = 4
SNAKE_INNER_SIZE = 12
MAX_FOOD_PLACEMENT_ATTEMPTS = 100

# Validate constants
assert WINDOW_WIDTH % BLOCK_SIZE == 0, "WINDOW_WIDTH must be divisible by BLOCK_SIZE"
assert WINDOW_HEIGHT % BLOCK_SIZE == 0, "WINDOW_HEIGHT must be divisible by BLOCK_SIZE"

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


def load_highscores() -> dict:
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
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to load highscores: {e}")
            return {'classic': 0, 'fun': 0}
    return {'classic': 0, 'fun': 0}


def save_highscores(highscores: dict) -> None:
    """
    Save high scores to the JSON file.
    
    Writes the high scores dictionary to HIGHSCORE_FILE. Logs warning
    if the file cannot be written.
    
    :param highscores: Dictionary containing high scores for both game modes
    :type highscores: dict
    
    Example:
        >>> save_highscores({'classic': 10, 'fun': 15})
    """
    try:
        with open(HIGHSCORE_FILE, 'w') as f:
            json.dump(highscores, f)
    except IOError as e:
        logger.warning(f"Failed to save highscores: {e}")


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
    
    def __init__(self, mode: GameMode = GameMode.CLASSIC, num_food_items: int = DEFAULT_NUM_FOOD_ITEMS):
        """
        Initialize the Snake Game.
        
        :param mode: The game mode to use, defaults to GameMode.CLASSIC
        :type mode: GameMode, optional
        :param num_food_items: Number of food items on the board, defaults to DEFAULT_NUM_FOOD_ITEMS
        :type num_food_items: int, optional
        """
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.mode = mode
        self.num_food_items = max(MIN_FOOD_ITEMS, min(num_food_items, MAX_FOOD_ITEMS))
        self.highscores = load_highscores()
        self.quit_prompt = False
        self.paused = False
        self.reset()
        
    def reset(self) -> None:
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
        self.quit_prompt = False
        self.paused = False
        self.food_items = []
        self._place_food()
        
    def set_mode(self, mode: GameMode) -> None:
        """
        Set the game mode and reset the game.
        
        :param mode: The new game mode to use
        :type mode: GameMode
        """
        self.mode = mode
        self.reset()
    
    def _generate_valid_food_position(self) -> Point:
        """
        Generate a valid food position not on snake or existing food.
        
        :return: A valid Point for food placement
        :rtype: Point
        """
        for _ in range(MAX_FOOD_PLACEMENT_ATTEMPTS):
            x = random.randint(0, (WINDOW_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (WINDOW_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            new_food = Point(x, y)
            
            # Check if position is valid (not on snake or other food)
            if new_food not in self.snake and new_food not in self.food_items:
                return new_food
        
        # Fallback: return a position even if not ideal
        x = random.randint(0, (WINDOW_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (WINDOW_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        return Point(x, y)
        
    def _place_food(self) -> None:
        """
        Place multiple food items on the board.
        
        Places self.num_food_items food items in valid positions
        (not on the snake or other food).
        """
        self.food_items = []
        for _ in range(self.num_food_items):
            self.food_items.append(self._generate_valid_food_position())
            
    def play_step(self) -> Tuple[bool, int]:
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
                # Handle quit prompt
                if self._handle_quit_prompt(event):
                    pygame.quit()
                    quit()
                
                # Handle pause
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    continue
                
                # Handle direction changes (only if not paused)
                if not self.paused:
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
        
        # If paused, just update UI and return
        if self.paused:
            self._update_ui()
            self.clock.tick(SPEED)
            return False, self.score
        
        # 2. Move snake
        self._move(self.direction)
        self.snake.insert(0, self.head)
        
        # 3. Check if food eaten and place new food or just move
        food_eaten = False
        for food in self.food_items:
            if self.head == food:
                self.score += 1
                food_eaten = True
                self.food_items.remove(food)
                # Add a new food item to maintain num_food_items
                self._add_single_food()
                break

        # 4. Check if game over (avoid false collision with tail if it will move)
        if self.mode == GameMode.CLASSIC:
            if (self.head.x > WINDOW_WIDTH - BLOCK_SIZE or self.head.x < 0 or
                    self.head.y > WINDOW_HEIGHT - BLOCK_SIZE or self.head.y < 0):
                self._update_highscore()
                return True, self.score

        body_to_check = self.snake[1:] if food_eaten else self.snake[1:-1]
        if self.head in body_to_check:
            self._update_highscore()
            return True, self.score

        if not food_eaten:
            self.snake.pop()
        
        # 5. Update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)
        
        return False, self.score
    
    def _handle_quit_prompt(self, event: pygame.event.Event) -> bool:
        """
        Handle quit prompt logic.
        
        :param event: The pygame event to process
        :type event: pygame.event.Event
        :return: True if should quit, False otherwise
        :rtype: bool
        """
        if event.key == pygame.K_ESCAPE:
            if self.quit_prompt:
                return True
            self.quit_prompt = True
            return False
        elif self.quit_prompt:
            self.quit_prompt = False
        return False
    
    def _add_single_food(self) -> None:
        """
        Add a single food item to the board.
        
        Uses the refactored _generate_valid_food_position method.
        """
        self.food_items.append(self._generate_valid_food_position())
    
    def _update_highscore(self) -> None:
        """
        Update the high score if the current score is higher.
        
        Compares the current score with the saved high score for the current
        game mode and updates it if necessary. Saves the updated scores to file.
        """
        mode_key = 'classic' if self.mode == GameMode.CLASSIC else 'fun'
        if self.score > self.highscores[mode_key]:
            self.highscores[mode_key] = self.score
            save_highscores(self.highscores)
    
    def get_highscore(self) -> int:
        """
        Get the high score for the current game mode.
        
        :return: The high score for the current mode
        :rtype: int
        """
        mode_key = 'classic' if self.mode == GameMode.CLASSIC else 'fun'
        return self.highscores[mode_key]
    
    def _is_collision(self, pt: Optional[Point] = None) -> bool:
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
        
    def _update_ui(self) -> None:
        """
        Update the game display.
        
        Renders the snake, food items, score, high score, game mode indicator,
        and pause/quit prompts on the display surface.
        """
        self.display.fill(BLACK)
        
        # Draw mode indicator
        font_small = pygame.font.Font(None, 24)
        mode_text = f"Mode: {self.mode.name}"
        mode_surface = font_small.render(mode_text, True, GRAY)
        self.display.blit(mode_surface, [WINDOW_WIDTH - 150, 10])
        
        # Draw snake with inner detail
        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN,
                           pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE,
                           pygame.Rect(pt.x + SNAKE_INNER_OFFSET,
                                     pt.y + SNAKE_INNER_OFFSET,
                                     SNAKE_INNER_SIZE, SNAKE_INNER_SIZE))
            
        # Draw all food items with different colors
        for i, food in enumerate(self.food_items):
            color = FOOD_COLORS[i % len(FOOD_COLORS)]
            pygame.draw.rect(self.display, color,
                           pygame.Rect(food.x, food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(text, [10, 10])
        
        # Draw high score
        highscore = self.get_highscore()
        highscore_text = font_small.render(f"High Score: {highscore}", True, YELLOW)
        self.display.blit(highscore_text, [10, 45])
        
        # Draw pause indicator
        if self.paused:
            pause_text = font.render("PAUSED", True, YELLOW)
            pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.display.blit(pause_text, pause_rect)
            
            resume_text = font_small.render("Press P to resume", True, WHITE)
            resume_rect = resume_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
            self.display.blit(resume_text, resume_rect)

        # Draw quit prompt
        if self.quit_prompt:
            prompt_text = font_small.render(
                "Press ESC again to quit, any other key to continue",
                True, LIGHT_GRAY
            )
            prompt_rect = prompt_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))
            self.display.blit(prompt_text, prompt_rect)
        
        pygame.display.flip()
        
    def _move(self, direction: Direction) -> None:
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


def show_menu(display: pygame.Surface) -> Tuple[GameMode, int]:
    """
    Display the game mode and settings selection menu with enhanced visual design.
    
    Shows a menu where the player can select between Classic and Fun game modes,
    and configure the number of food items using arrow keys and Enter.
    
    :param display: The pygame display surface to render the menu on
    :type display: pygame.Surface
    :return: Tuple of (selected game mode, number of food items)
    :rtype: Tuple[GameMode, int]
    
    Example:
        >>> display = pygame.display.set_mode((640, 480))
        >>> mode, num_food = show_menu(display)
        >>> print(f"Selected mode: {mode.name}, Food items: {num_food}")
    """
    clock = pygame.time.Clock()
    selected = 0  # 0 for Classic, 1 for Fun
    num_food_items = DEFAULT_NUM_FOOD_ITEMS
    highscores = load_highscores()
    
    # Menu options with icons
    options = [
        ("🏛️ CLASSIC MODE", "Game ends when hitting walls", "⚡ Challenge yourself!"),
        ("🎪 FUN MODE", "Snake wraps around walls", "🌀 Endless gameplay!")
    ]
    
    while True:
        # Gradient-like background effect
        display.fill(BLACK)
        for i in range(0, WINDOW_HEIGHT, 20):
            alpha = int(20 * (1 - i / WINDOW_HEIGHT))
            pygame.draw.rect(display, (0, alpha, 0), (0, i, WINDOW_WIDTH, 20))
        
        # Decorative border
        pygame.draw.rect(display, GREEN, (10, 10, WINDOW_WIDTH - 20, WINDOW_HEIGHT - 20), 3)
        pygame.draw.rect(display, (0, 100, 0), (15, 15, WINDOW_WIDTH - 30, WINDOW_HEIGHT - 30), 1)
        
        # Title with shadow effect
        font_title = pygame.font.Font(None, 72)
        title_shadow = font_title.render("🐍 SNAKE GAME 🐍", True, (0, 50, 0))
        title_shadow_rect = title_shadow.get_rect(center=(WINDOW_WIDTH // 2 + 3, 48))
        display.blit(title_shadow, title_shadow_rect)
        
        title = font_title.render("🐍 SNAKE GAME 🐍", True, GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 45))
        display.blit(title, title_rect)
        
        # Subtitle
        font_subtitle = pygame.font.Font(None, 20)
        subtitle = font_subtitle.render("Classic Arcade Action", True, LIGHT_GRAY)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 85))
        display.blit(subtitle, subtitle_rect)
        
        # Divider line
        pygame.draw.line(display, GREEN, (WINDOW_WIDTH // 2 - 150, 100),
                        (WINDOW_WIDTH // 2 + 150, 100), 2)
        
        # High Scores Section with box
        scores_box_y = 115
        scores_box_height = 70
        pygame.draw.rect(display, (20, 20, 20),
                        (WINDOW_WIDTH // 2 - 160, scores_box_y, 320, scores_box_height))
        pygame.draw.rect(display, YELLOW,
                        (WINDOW_WIDTH // 2 - 160, scores_box_y, 320, scores_box_height), 2)
        
        font_scores_title = pygame.font.Font(None, 28)
        scores_title = font_scores_title.render("🏆 HIGH SCORES 🏆", True, YELLOW)
        scores_title_rect = scores_title.get_rect(center=(WINDOW_WIDTH // 2, scores_box_y + 15))
        display.blit(scores_title, scores_title_rect)
        
        font_scores = pygame.font.Font(None, 22)
        classic_score = highscores.get('classic', 0)
        fun_score = highscores.get('fun', 0)
        
        # Centered high scores
        classic_text = font_scores.render(f"Classic: {classic_score:>3}", True, WHITE)
        fun_text = font_scores.render(f"Fun: {fun_score:>3}", True, WHITE)
        classic_rect = classic_text.get_rect(center=(WINDOW_WIDTH // 2 - 60, scores_box_y + 45))
        fun_rect = fun_text.get_rect(center=(WINDOW_WIDTH // 2 + 60, scores_box_y + 45))
        display.blit(classic_text, classic_rect)
        display.blit(fun_text, fun_rect)
        
        # Settings Section
        settings_y = 200
        font_settings = pygame.font.Font(None, 24)
        settings_title = font_settings.render("⚙️  SETTINGS", True, ORANGE)
        settings_title_rect = settings_title.get_rect(center=(WINDOW_WIDTH // 2, settings_y))
        display.blit(settings_title, settings_title_rect)
        
        # Food items with better visual
        food_y = settings_y + 30
        pygame.draw.rect(display, (30, 30, 30),
                        (WINDOW_WIDTH // 2 - 120, food_y - 5, 240, 30))
        pygame.draw.rect(display, ORANGE,
                        (WINDOW_WIDTH // 2 - 120, food_y - 5, 240, 30), 2)
        
        food_label = font_settings.render("Food Items:", True, ORANGE)
        food_value = font_settings.render(f"◀  {num_food_items:>2}  ▶", True, YELLOW)
        food_label_rect = food_label.get_rect(center=(WINDOW_WIDTH // 2 - 60, food_y + 10))
        food_value_rect = food_value.get_rect(center=(WINDOW_WIDTH // 2 + 50, food_y + 10))
        display.blit(food_label, food_label_rect)
        display.blit(food_value, food_value_rect)
        
        # Game Mode Selection
        font_mode_title = pygame.font.Font(None, 26)
        mode_title = font_mode_title.render("SELECT GAME MODE", True, WHITE)
        mode_title_rect = mode_title.get_rect(center=(WINDOW_WIDTH // 2, 270))
        display.blit(mode_title, mode_title_rect)
        
        # Menu options with enhanced styling
        font_option = pygame.font.Font(None, 32)
        font_desc = pygame.font.Font(None, 18)
        font_extra = pygame.font.Font(None, 16)
        
        menu_start_y = 305
        menu_gap = 75
        
        for i, (option, description, extra) in enumerate(options):
            y_pos = menu_start_y + i * menu_gap
            
            # Draw option box
            box_width = 380
            box_height = 65
            box_x = WINDOW_WIDTH // 2 - box_width // 2
            box_y = y_pos - 8
            
            if i == selected:
                # Selected option - highlighted
                pygame.draw.rect(display, (50, 50, 0), (box_x, box_y, box_width, box_height))
                pygame.draw.rect(display, YELLOW, (box_x, box_y, box_width, box_height), 3)
                # Glow effect
                pygame.draw.rect(display, (100, 100, 0), (box_x - 2, box_y - 2, box_width + 4, box_height + 4), 1)
                color = YELLOW
                desc_color = WHITE
            else:
                # Unselected option
                pygame.draw.rect(display, (20, 20, 20), (box_x, box_y, box_width, box_height))
                pygame.draw.rect(display, GRAY, (box_x, box_y, box_width, box_height), 2)
                color = WHITE
                desc_color = LIGHT_GRAY
            
            # Option text
            option_text = font_option.render(option, True, color)
            option_rect = option_text.get_rect(center=(WINDOW_WIDTH // 2, y_pos + 8))
            display.blit(option_text, option_rect)
            
            # Description text
            desc_text = font_desc.render(description, True, desc_color)
            desc_rect = desc_text.get_rect(center=(WINDOW_WIDTH // 2, y_pos + 32))
            display.blit(desc_text, desc_rect)
            
            # Extra info
            extra_text = font_extra.render(extra, True, desc_color)
            extra_rect = extra_text.get_rect(center=(WINDOW_WIDTH // 2, y_pos + 48))
            display.blit(extra_text, extra_rect)
        
        # Instructions at bottom
        font_instructions = pygame.font.Font(None, 18)
        instructions = [
            "↑↓ Select Mode  •  ←→ Adjust Food  •  ENTER Start  •  ESC Quit"
        ]
        inst_y = WINDOW_HEIGHT - 25
        for instruction in instructions:
            inst_text = font_instructions.render(instruction, True, LIGHT_GRAY)
            inst_rect = inst_text.get_rect(center=(WINDOW_WIDTH // 2, inst_y))
            display.blit(inst_text, inst_rect)
        
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
                elif event.key == pygame.K_LEFT:
                    num_food_items = max(MIN_FOOD_ITEMS, num_food_items - 1)
                elif event.key == pygame.K_RIGHT:
                    num_food_items = min(MAX_FOOD_ITEMS, num_food_items + 1)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    mode = GameMode.CLASSIC if selected == 0 else GameMode.FUN
                    return mode, num_food_items
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
        
        clock.tick(30)


def main() -> None:
    """
    Main entry point for the Snake Game.
    
    Initializes the game, displays the menu for mode and settings selection,
    and runs the main game loop. Handles game over state and allows restarting
    or returning to the menu.
    
    The game loop continues until the user quits the application.
    """
    display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Snake Game')
    
    # Show menu and get selected mode and food items
    mode, num_food_items = show_menu(display)
    
    # Create game with selected mode and food items
    game = SnakeGame(mode, num_food_items)
    
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
                            mode, num_food_items = show_menu(display)
                            game.mode = mode
                            game.num_food_items = num_food_items
                            game.reset()
                            waiting = False


if __name__ == '__main__':
    main()

# Made with Bob
