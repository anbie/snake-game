"""Snake AI vs Player Mode - Competitive gameplay between human and AI."""

import pygame
import sys
import random
from typing import Optional, Tuple
from snake_game import (
    SnakeGame, GameMode, Direction, Point, WINDOW_WIDTH, WINDOW_HEIGHT,
    BLOCK_SIZE, SPEED, WHITE, BLACK, GRAY, LIGHT_GRAY, GREEN, BLUE, RED,
    YELLOW, ORANGE, load_highscores, save_highscores
)
from snake_ai import AIGameState
from snake_ai_difficulties import create_ai, AIDifficulty


class AIVsPlayerGame:
    """
    AI vs Player competitive mode.
    
    Features:
    - Player (green) vs AI (blue)
    - Shared food pool
    - Collision with other snake = death
    - First to target score wins OR last snake standing
    - Separate score tracking
    """
    
    def __init__(self, ai_difficulty: AIDifficulty = AIDifficulty.MEDIUM,
                 game_mode: GameMode = GameMode.CLASSIC,
                 num_food_items: int = 6,
                 target_score: int = 50):
        """
        Initialize AI vs Player mode.
        
        Args:
            ai_difficulty: AI opponent difficulty
            game_mode: Game mode (Classic or Fun)
            num_food_items: Number of food items
            target_score: Score needed to win (0 = play until death)
        """
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake - AI vs Player')
        self.clock = pygame.time.Clock()
        
        self.ai_difficulty = ai_difficulty
        self.game_mode = game_mode
        self.num_food_items = num_food_items
        self.target_score = target_score
        
        # Fonts
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.title_font = pygame.font.Font(None, 32)
        
        # Game state
        self.paused = False
        self.game_over = False
        self.winner = None  # 'player' or 'ai'
        
        # Initialize game
        self.reset()
    
    def reset(self):
        """Reset game to initial state."""
        # Player snake (green) - starts on left
        self.player_snake = [
            Point(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2),
            Point(WINDOW_WIDTH // 4 - BLOCK_SIZE, WINDOW_HEIGHT // 2),
            Point(WINDOW_WIDTH // 4 - 2 * BLOCK_SIZE, WINDOW_HEIGHT // 2)
        ]
        self.player_direction = Direction.RIGHT
        self.player_score = 0
        self.player_alive = True
        
        # AI snake (blue) - starts on right
        self.ai_snake = [
            Point(3 * WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2),
            Point(3 * WINDOW_WIDTH // 4 + BLOCK_SIZE, WINDOW_HEIGHT // 2),
            Point(3 * WINDOW_WIDTH // 4 + 2 * BLOCK_SIZE, WINDOW_HEIGHT // 2)
        ]
        self.ai_direction = Direction.LEFT
        self.ai_score = 0
        self.ai_alive = True
        
        # Food items
        self.food_items = []
        self._place_food()
        
        # Create AI instance
        self.ai = self._create_ai_instance()
        
        # Reset game state
        self.game_over = False
        self.winner = None
        self.paused = False
    
    def _create_ai_instance(self):
        """Create AI instance with current game state."""
        game_state = AIGameState(
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            block_size=BLOCK_SIZE,
            ai_snake=self.ai_snake.copy(),
            ai_direction=self.ai_direction,
            ai_score=self.ai_score,
            food_items=self.food_items.copy(),
            player_snake=self.player_snake.copy(),
            player_direction=self.player_direction,
            wraps_walls=(self.game_mode == GameMode.FUN)
        )
        return create_ai(self.ai_difficulty, game_state)
    
    def _place_food(self):
        """Place food items avoiding both snakes."""
        self.food_items = []
        all_snake_positions = set(self.player_snake + self.ai_snake)
        
        for _ in range(self.num_food_items):
            for attempt in range(100):
                x = random.randint(0, (WINDOW_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
                y = random.randint(0, (WINDOW_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
                new_food = Point(x, y)
                
                if new_food not in all_snake_positions and new_food not in self.food_items:
                    self.food_items.append(new_food)
                    break
    
    def _update_ai_game_state(self):
        """Update AI's game state with current information."""
        self.ai.game_state.ai_snake = self.ai_snake.copy()
        self.ai.game_state.ai_direction = self.ai_direction
        self.ai.game_state.ai_score = self.ai_score
        self.ai.game_state.food_items = self.food_items.copy()
        self.ai.game_state.player_snake = self.player_snake.copy()
        self.ai.game_state.player_direction = self.player_direction
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = self._handle_keypress(event.key)
            
            # Update game if not paused and not game over
            if not self.paused and not self.game_over:
                self._update_game()
            
            # Render
            self._render()
            
            # Control speed
            self.clock.tick(SPEED)
        
        pygame.quit()
        sys.exit()
    
    def _handle_keypress(self, key: int) -> bool:
        """Handle keyboard input."""
        if key == pygame.K_ESCAPE or key == pygame.K_q:
            return False
        elif key == pygame.K_p or key == pygame.K_SPACE:
            if not self.game_over:
                self.paused = not self.paused
        elif key == pygame.K_r:
            self.reset()
        elif not self.paused and not self.game_over and self.player_alive:
            # Player controls
            if key == pygame.K_LEFT and self.player_direction != Direction.RIGHT:
                self.player_direction = Direction.LEFT
            elif key == pygame.K_RIGHT and self.player_direction != Direction.LEFT:
                self.player_direction = Direction.RIGHT
            elif key == pygame.K_UP and self.player_direction != Direction.DOWN:
                self.player_direction = Direction.UP
            elif key == pygame.K_DOWN and self.player_direction != Direction.UP:
                self.player_direction = Direction.DOWN
        
        return True
    
    def _update_game(self):
        """Update game state for both player and AI."""
        # Update AI decision
        if self.ai_alive:
            self._update_ai_game_state()
            self.ai_direction = self.ai.update(self.ai.game_state)
        
        # Move both snakes
        if self.player_alive:
            self._move_snake(self.player_snake, self.player_direction, 'player')
        
        if self.ai_alive:
            self._move_snake(self.ai_snake, self.ai_direction, 'ai')
        
        # Check for food consumption
        self._check_food_consumption()
        
        # Check collisions
        self._check_collisions()
        
        # Check win condition
        self._check_win_condition()
    
    def _move_snake(self, snake: list, direction: Direction, owner: str):
        """Move a snake in the given direction."""
        head = snake[0]
        
        # Calculate new head position
        if direction == Direction.RIGHT:
            new_head = Point(head.x + BLOCK_SIZE, head.y)
        elif direction == Direction.LEFT:
            new_head = Point(head.x - BLOCK_SIZE, head.y)
        elif direction == Direction.DOWN:
            new_head = Point(head.x, head.y + BLOCK_SIZE)
        else:  # UP
            new_head = Point(head.x, head.y - BLOCK_SIZE)
        
        # Wrap around in Fun mode
        if self.game_mode == GameMode.FUN:
            new_head = Point(new_head.x % WINDOW_WIDTH, new_head.y % WINDOW_HEIGHT)
        
        # Insert new head
        snake.insert(0, new_head)
    
    def _check_food_consumption(self):
        """Check if either snake ate food."""
        # Check player
        if self.player_alive and self.player_snake[0] in self.food_items:
            self.food_items.remove(self.player_snake[0])
            self.player_score += 1
            self._add_single_food()
        else:
            if self.player_alive:
                self.player_snake.pop()
        
        # Check AI
        if self.ai_alive and self.ai_snake[0] in self.food_items:
            self.food_items.remove(self.ai_snake[0])
            self.ai_score += 1
            self.ai.statistics.food_eaten += 1
            self._add_single_food()
        else:
            if self.ai_alive:
                self.ai_snake.pop()
    
    def _add_single_food(self):
        """Add a single food item to maintain count."""
        all_snake_positions = set(self.player_snake + self.ai_snake)
        
        for _ in range(100):
            x = random.randint(0, (WINDOW_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (WINDOW_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            new_food = Point(x, y)
            
            if new_food not in all_snake_positions and new_food not in self.food_items:
                self.food_items.append(new_food)
                break
    
    def _check_collisions(self):
        """Check for collisions (walls, self, other snake)."""
        # Check player collisions
        if self.player_alive:
            player_head = self.player_snake[0]
            
            # Wall collision (Classic mode)
            if self.game_mode == GameMode.CLASSIC:
                if (player_head.x < 0 or player_head.x >= WINDOW_WIDTH or
                    player_head.y < 0 or player_head.y >= WINDOW_HEIGHT):
                    self.player_alive = False
            
            # Self collision
            if player_head in self.player_snake[1:]:
                self.player_alive = False
            
            # Collision with AI snake
            if player_head in self.ai_snake:
                self.player_alive = False
        
        # Check AI collisions
        if self.ai_alive:
            ai_head = self.ai_snake[0]
            
            # Wall collision (Classic mode)
            if self.game_mode == GameMode.CLASSIC:
                if (ai_head.x < 0 or ai_head.x >= WINDOW_WIDTH or
                    ai_head.y < 0 or ai_head.y >= WINDOW_HEIGHT):
                    self.ai_alive = False
            
            # Self collision
            if ai_head in self.ai_snake[1:]:
                self.ai_alive = False
            
            # Collision with player snake
            if ai_head in self.player_snake:
                self.ai_alive = False
    
    def _check_win_condition(self):
        """Check if game is over and determine winner."""
        # Check if both died (draw)
        if not self.player_alive and not self.ai_alive:
            self.game_over = True
            self.winner = 'draw'
            return
        
        # Check if one died
        if not self.player_alive:
            self.game_over = True
            self.winner = 'ai'
            return
        
        if not self.ai_alive:
            self.game_over = True
            self.winner = 'player'
            return
        
        # Check target score
        if self.target_score > 0:
            if self.player_score >= self.target_score:
                self.game_over = True
                self.winner = 'player'
            elif self.ai_score >= self.target_score:
                self.game_over = True
                self.winner = 'ai'
    
    def _render(self):
        """Render the game."""
        self.display.fill(BLACK)
        
        # Draw food
        for food in self.food_items:
            pygame.draw.rect(self.display, RED,
                           pygame.Rect(food.x, food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw player snake (green)
        if self.player_alive:
            for i, segment in enumerate(self.player_snake):
                color = GREEN if i == 0 else (0, 150, 0)
                pygame.draw.rect(self.display, color,
                               pygame.Rect(segment.x, segment.y, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw AI snake (blue)
        if self.ai_alive:
            for i, segment in enumerate(self.ai_snake):
                color = BLUE if i == 0 else (0, 0, 150)
                pygame.draw.rect(self.display, color,
                               pygame.Rect(segment.x, segment.y, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw UI
        self._draw_ui()
        
        # Draw overlays
        if self.paused:
            self._draw_pause_overlay()
        elif self.game_over:
            self._draw_game_over_overlay()
        
        pygame.display.flip()
    
    def _draw_ui(self):
        """Draw UI elements."""
        # Title
        mode_name = "CLASSIC" if self.game_mode == GameMode.CLASSIC else "FUN"
        title = f"PLAYER vs AI ({self.ai_difficulty.name}) - {mode_name}"
        title_surface = self.font.render(title, True, WHITE)
        self.display.blit(title_surface, (10, 5))
        
        # Scores
        player_text = f"PLAYER: {self.player_score}"
        player_surface = self.font.render(player_text, True, GREEN)
        self.display.blit(player_surface, (10, 35))
        
        ai_text = f"AI: {self.ai_score}"
        ai_surface = self.font.render(ai_text, True, BLUE)
        self.display.blit(ai_surface, (WINDOW_WIDTH - 120, 35))
        
        # Target score
        if self.target_score > 0:
            target_text = f"First to {self.target_score} wins!"
            target_surface = self.small_font.render(target_text, True, LIGHT_GRAY)
            self.display.blit(target_surface, (WINDOW_WIDTH // 2 - 80, 10))
        
        # Controls
        controls = "Arrow Keys: Move | P: Pause | R: Restart | Q: Quit"
        controls_surface = self.small_font.render(controls, True, LIGHT_GRAY)
        self.display.blit(controls_surface, (10, WINDOW_HEIGHT - 20))
    
    def _draw_pause_overlay(self):
        """Draw pause overlay."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.display.blit(overlay, (0, 0))
        
        pause_text = "PAUSED"
        pause_surface = self.title_font.render(pause_text, True, WHITE)
        text_rect = pause_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.display.blit(pause_surface, text_rect)
    
    def _draw_game_over_overlay(self):
        """Draw game over overlay."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.display.blit(overlay, (0, 0))
        
        # Winner announcement
        if self.winner == 'draw':
            text = "DRAW!"
            color = YELLOW
        elif self.winner == 'player':
            text = "PLAYER WINS!"
            color = GREEN
        else:
            text = "AI WINS!"
            color = BLUE
        
        winner_surface = self.title_font.render(text, True, color)
        text_rect = winner_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        self.display.blit(winner_surface, text_rect)
        
        # Final scores
        score_text = f"Player: {self.player_score}  |  AI: {self.ai_score}"
        score_surface = self.font.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.display.blit(score_surface, score_rect)
        
        # Restart hint
        hint_text = "Press R to restart or Q to quit"
        hint_surface = self.font.render(hint_text, True, LIGHT_GRAY)
        hint_rect = hint_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
        self.display.blit(hint_surface, hint_rect)


def validate_positive_int(value):
    """Validate positive integer argument."""
    import argparse
    try:
        ivalue = int(value)
        if ivalue < 0:
            raise argparse.ArgumentTypeError(f"Value must be non-negative: {value}")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid integer value: {value}")


def validate_food_count(value):
    """Validate food count is within acceptable range (1-99)."""
    import argparse
    try:
        ivalue = int(value)
        if ivalue < 1 or ivalue > 99:
            raise argparse.ArgumentTypeError(f"Food count must be between 1 and 99: {value}")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid integer value: {value}")


def main():
    """Main entry point for AI vs Player mode."""
    import argparse
    import random
    
    parser = argparse.ArgumentParser(description='Snake AI vs Player Mode')
    parser.add_argument('--difficulty', type=str, default='medium',
                       choices=['easy', 'medium', 'hard'],
                       help='AI difficulty level')
    parser.add_argument('--mode', type=str, default='classic',
                       choices=['classic', 'fun'],
                       help='Game mode')
    parser.add_argument('--food', type=validate_food_count, default=6,
                       help='Number of food items (1-99)')
    parser.add_argument('--target', type=validate_positive_int, default=0,
                       help='Target score to win (0 = play until death)')
    
    args = parser.parse_args()
    
    # Convert arguments
    difficulty_map = {
        'easy': AIDifficulty.EASY,
        'medium': AIDifficulty.MEDIUM,
        'hard': AIDifficulty.HARD
    }
    
    mode_map = {
        'classic': GameMode.CLASSIC,
        'fun': GameMode.FUN
    }
    
    difficulty = difficulty_map[args.difficulty]
    game_mode = mode_map[args.mode]
    num_food = max(1, min(args.food, 99))
    target_score = max(0, args.target)
    
    # Run vs mode
    game = AIVsPlayerGame(difficulty, game_mode, num_food, target_score)
    game.run()


if __name__ == '__main__':
    main()
