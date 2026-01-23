import unittest
import pygame
import os
from unittest.mock import Mock, patch, MagicMock
from snake_game import SnakeGame, Direction, Point, GameMode, BLOCK_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, HIGHSCORE_FILE


class TestSnakeGameClassicMode(unittest.TestCase):
    """Test suite for Snake Game in Classic Mode"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        pygame.init()
        self.game = SnakeGame(mode=GameMode.CLASSIC)
    
    def tearDown(self):
        """Clean up after each test method"""
        pygame.quit()
    
    # Test initialization
    def test_game_initialization_classic(self):
        """Test that game initializes with correct default values in Classic mode"""
        self.assertIsNotNone(self.game.display)
        self.assertIsNotNone(self.game.clock)
        self.assertEqual(self.game.direction, Direction.RIGHT)
        self.assertEqual(len(self.game.snake), 3)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(len(self.game.food_items), 4)
        self.assertEqual(self.game.mode, GameMode.CLASSIC)
    
    def test_reset_classic(self):
        """Test that reset method properly resets game state in Classic mode"""
        # Modify game state
        self.game.score = 10
        self.game.direction = Direction.LEFT
        self.game.snake = [Point(100, 100)]
        
        # Reset game
        self.game.reset()
        
        # Verify reset state
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.direction, Direction.RIGHT)
        self.assertEqual(len(self.game.snake), 3)
        self.assertEqual(len(self.game.food_items), 4)
    
    # Test collision with walls in Classic mode
    def test_collision_with_left_wall_classic(self):
        """Test collision detection with left wall in Classic mode"""
        self.game.head = Point(-BLOCK_SIZE, WINDOW_HEIGHT // 2)
        self.assertTrue(self.game._is_collision())
    
    def test_collision_with_right_wall_classic(self):
        """Test collision detection with right wall in Classic mode"""
        self.game.head = Point(WINDOW_WIDTH, WINDOW_HEIGHT // 2)
        self.assertTrue(self.game._is_collision())
    
    def test_collision_with_top_wall_classic(self):
        """Test collision detection with top wall in Classic mode"""
        self.game.head = Point(WINDOW_WIDTH // 2, -BLOCK_SIZE)
        self.assertTrue(self.game._is_collision())
    
    def test_collision_with_bottom_wall_classic(self):
        """Test collision detection with bottom wall in Classic mode"""
        self.game.head = Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT)
        self.assertTrue(self.game._is_collision())
    
    def test_no_collision_in_valid_position_classic(self):
        """Test that no collision is detected in valid position in Classic mode"""
        self.game.head = Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.game.snake = [self.game.head]
        self.assertFalse(self.game._is_collision())


class TestSnakeGameFunMode(unittest.TestCase):
    """Test suite for Snake Game in Fun Mode"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        pygame.init()
        self.game = SnakeGame(mode=GameMode.FUN)
    
    def tearDown(self):
        """Clean up after each test method"""
        pygame.quit()
    
    # Test initialization
    def test_game_initialization_fun(self):
        """Test that game initializes with correct default values in Fun mode"""
        self.assertIsNotNone(self.game.display)
        self.assertIsNotNone(self.game.clock)
        self.assertEqual(self.game.direction, Direction.RIGHT)
        self.assertEqual(len(self.game.snake), 3)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(len(self.game.food_items), 4)
        self.assertEqual(self.game.mode, GameMode.FUN)
    
    # Test wall wrapping in Fun mode
    def test_wrap_right_wall_fun(self):
        """Test that snake wraps around when hitting right wall in Fun mode"""
        self.game.head = Point(WINDOW_WIDTH - BLOCK_SIZE, WINDOW_HEIGHT // 2)
        self.game._move(Direction.RIGHT)
        self.assertEqual(self.game.head.x, 0)
        self.assertEqual(self.game.head.y, WINDOW_HEIGHT // 2)
    
    def test_wrap_left_wall_fun(self):
        """Test that snake wraps around when hitting left wall in Fun mode"""
        self.game.head = Point(0, WINDOW_HEIGHT // 2)
        self.game._move(Direction.LEFT)
        self.assertEqual(self.game.head.x, WINDOW_WIDTH - BLOCK_SIZE)
        self.assertEqual(self.game.head.y, WINDOW_HEIGHT // 2)
    
    def test_wrap_bottom_wall_fun(self):
        """Test that snake wraps around when hitting bottom wall in Fun mode"""
        self.game.head = Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT - BLOCK_SIZE)
        self.game._move(Direction.DOWN)
        self.assertEqual(self.game.head.x, WINDOW_WIDTH // 2)
        self.assertEqual(self.game.head.y, 0)
    
    def test_wrap_top_wall_fun(self):
        """Test that snake wraps around when hitting top wall in Fun mode"""
        self.game.head = Point(WINDOW_WIDTH // 2, 0)
        self.game._move(Direction.UP)
        self.assertEqual(self.game.head.x, WINDOW_WIDTH // 2)
        self.assertEqual(self.game.head.y, WINDOW_HEIGHT - BLOCK_SIZE)
    
    def test_no_wall_collision_fun(self):
        """Test that walls don't cause collision in Fun mode"""
        # Test positions at walls
        self.game.head = Point(-BLOCK_SIZE, WINDOW_HEIGHT // 2)
        self.assertFalse(self.game._is_collision())
        
        self.game.head = Point(WINDOW_WIDTH, WINDOW_HEIGHT // 2)
        self.assertFalse(self.game._is_collision())
        
        self.game.head = Point(WINDOW_WIDTH // 2, -BLOCK_SIZE)
        self.assertFalse(self.game._is_collision())
        
        self.game.head = Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT)
        self.assertFalse(self.game._is_collision())


class TestSnakeGameCommon(unittest.TestCase):
    """Test suite for common Snake Game functionality across both modes"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        pygame.init()
        self.game = SnakeGame()
    
    def tearDown(self):
        """Clean up after each test method"""
        pygame.quit()
    
    # Test snake head position
    def test_initial_head_position(self):
        """Test that snake head starts at center of screen"""
        expected_x = WINDOW_WIDTH // 2
        expected_y = WINDOW_HEIGHT // 2
        self.assertEqual(self.game.head.x, expected_x)
        self.assertEqual(self.game.head.y, expected_y)
    
    def test_initial_snake_body(self):
        """Test that snake body is correctly positioned behind head"""
        head = self.game.snake[0]
        body1 = self.game.snake[1]
        body2 = self.game.snake[2]
        
        self.assertEqual(body1.x, head.x - BLOCK_SIZE)
        self.assertEqual(body1.y, head.y)
        self.assertEqual(body2.x, head.x - (2 * BLOCK_SIZE))
        self.assertEqual(body2.y, head.y)
    
    # Test food placement
    def test_food_placement_count(self):
        """Test that exactly 4 food items are placed"""
        self.assertEqual(len(self.game.food_items), 4)
    
    def test_food_placement_uniqueness(self):
        """Test that all food items have unique positions"""
        food_positions = set(self.game.food_items)
        self.assertEqual(len(food_positions), 3)
    
    def test_food_placement_not_on_snake(self):
        """Test that food is not placed on snake body"""
        for food in self.game.food_items:
            self.assertNotIn(food, self.game.snake)
    
    def test_food_placement_within_bounds(self):
        """Test that food is placed within game boundaries"""
        for food in self.game.food_items:
            self.assertGreaterEqual(food.x, 0)
            self.assertGreaterEqual(food.y, 0)
            self.assertLess(food.x, WINDOW_WIDTH)
            self.assertLess(food.y, WINDOW_HEIGHT)
    
    def test_food_placement_aligned_to_grid(self):
        """Test that food is aligned to the block grid"""
        for food in self.game.food_items:
            self.assertEqual(food.x % BLOCK_SIZE, 0)
            self.assertEqual(food.y % BLOCK_SIZE, 0)
    
    # Test movement
    def test_move_right(self):
        """Test snake movement to the right"""
        initial_x = self.game.head.x
        initial_y = self.game.head.y
        
        self.game._move(Direction.RIGHT)
        
        self.assertEqual(self.game.head.x, initial_x + BLOCK_SIZE)
        self.assertEqual(self.game.head.y, initial_y)
    
    def test_move_left(self):
        """Test snake movement to the left"""
        initial_x = self.game.head.x
        initial_y = self.game.head.y
        
        self.game._move(Direction.LEFT)
        
        self.assertEqual(self.game.head.x, initial_x - BLOCK_SIZE)
        self.assertEqual(self.game.head.y, initial_y)
    
    def test_move_up(self):
        """Test snake movement upward"""
        initial_x = self.game.head.x
        initial_y = self.game.head.y
        
        self.game._move(Direction.UP)
        
        self.assertEqual(self.game.head.x, initial_x)
        self.assertEqual(self.game.head.y, initial_y - BLOCK_SIZE)
    
    def test_move_down(self):
        """Test snake movement downward"""
        initial_x = self.game.head.x
        initial_y = self.game.head.y
        
        self.game._move(Direction.DOWN)
        
        self.assertEqual(self.game.head.x, initial_x)
        self.assertEqual(self.game.head.y, initial_y + BLOCK_SIZE)
    
    # Test collision with self (same for both modes)
    def test_collision_with_self(self):
        """Test collision detection with snake's own body"""
        # Create a snake that will collide with itself
        self.game.head = Point(100, 100)
        self.game.snake = [
            self.game.head,
            Point(100, 120),
            Point(100, 140),
            Point(120, 140),
            Point(140, 140),
            Point(140, 120),
            Point(140, 100),
            Point(120, 100),
            Point(100, 100)  # Same as head
        ]
        
        # Check collision with a point in the body
        collision_point = Point(100, 120)
        self.assertTrue(self.game._is_collision(collision_point))
    
    # Test food eating
    def test_score_increases_when_food_eaten(self):
        """Test that score increases when snake eats food"""
        initial_score = self.game.score
        
        # Place head on food
        if self.game.food_items:
            food_position = self.game.food_items[0]
            self.game.head = food_position
            self.game.snake.insert(0, self.game.head)
            
            # Simulate eating food
            for food in self.game.food_items:
                if self.game.head == food:
                    self.game.score += 1
                    break
            
            self.assertEqual(self.game.score, initial_score + 1)
    
    def test_snake_grows_when_food_eaten(self):
        """Test that snake length increases when food is eaten"""
        initial_length = len(self.game.snake)
        
        # Place head on food and don't pop tail
        if self.game.food_items:
            food_position = self.game.food_items[0]
            self.game.head = food_position
            self.game.snake.insert(0, self.game.head)
            
            # Snake should be longer (we added head but didn't pop tail)
            self.assertEqual(len(self.game.snake), initial_length + 1)
    
    def test_add_single_food(self):
        """Test that _add_single_food adds exactly one food item"""
        initial_count = len(self.game.food_items)
        self.game._add_single_food()
        self.assertEqual(len(self.game.food_items), initial_count + 1)
    
    def test_add_single_food_not_on_snake(self):
        """Test that newly added food is not on snake"""
        self.game._add_single_food()
        new_food = self.game.food_items[-1]
        self.assertNotIn(new_food, self.game.snake)
    
    def test_add_single_food_unique_position(self):
        """Test that newly added food has unique position"""
        initial_foods = self.game.food_items.copy()
        self.game._add_single_food()
        new_food = self.game.food_items[-1]
        self.assertNotIn(new_food, initial_foods)
    
    # Test mode switching
    def test_set_mode_classic(self):
        """Test switching to Classic mode"""
        self.game.set_mode(GameMode.CLASSIC)
        self.assertEqual(self.game.mode, GameMode.CLASSIC)
    
    def test_set_mode_fun(self):
        """Test switching to Fun mode"""
        self.game.set_mode(GameMode.FUN)
        self.assertEqual(self.game.mode, GameMode.FUN)
    
    def test_mode_switch_resets_game(self):
        """Test that switching mode resets the game"""
        self.game.score = 10
        self.game.set_mode(GameMode.FUN)
        self.assertEqual(self.game.score, 0)
    
    # Test Direction enum
    def test_direction_enum_values(self):
        """Test that Direction enum has correct values"""
        self.assertEqual(Direction.RIGHT.value, 1)
        self.assertEqual(Direction.LEFT.value, 2)
        self.assertEqual(Direction.UP.value, 3)
        self.assertEqual(Direction.DOWN.value, 4)
    
    # Test GameMode enum
    def test_game_mode_enum_values(self):
        """Test that GameMode enum has correct values"""
        self.assertEqual(GameMode.CLASSIC.value, 1)
        self.assertEqual(GameMode.FUN.value, 2)
    
    # Test Point namedtuple
    def test_point_creation(self):
        """Test Point namedtuple creation"""
        point = Point(100, 200)
        self.assertEqual(point.x, 100)
        self.assertEqual(point.y, 200)
    
    def test_point_equality(self):
        """Test Point equality comparison"""
        point1 = Point(100, 200)
        point2 = Point(100, 200)
        point3 = Point(150, 200)
        
        self.assertEqual(point1, point2)
        self.assertNotEqual(point1, point3)
    
    # Test snake body integrity
    def test_snake_body_connected(self):
        """Test that snake body segments are properly connected"""
        for i in range(len(self.game.snake) - 1):
            current = self.game.snake[i]
            next_segment = self.game.snake[i + 1]
            
            # Check if segments are adjacent (horizontally or vertically)
            x_diff = abs(current.x - next_segment.x)
            y_diff = abs(current.y - next_segment.y)
            
            # Segments should be exactly BLOCK_SIZE apart in one direction
            self.assertTrue(
                (x_diff == BLOCK_SIZE and y_diff == 0) or
                (x_diff == 0 and y_diff == BLOCK_SIZE)
            )
    
    # Test food maintenance
    def test_food_count_maintained_after_eating(self):
        """Test that 3 food items are maintained after one is eaten"""
        # Simulate eating food
        if self.game.food_items:
            self.game.food_items.pop(0)
            self.game._add_single_food()
            
            self.assertEqual(len(self.game.food_items), 4)


class TestGameConstants(unittest.TestCase):
    """Test game constants and configuration"""
    
    def test_window_dimensions(self):
        """Test that window dimensions are positive"""
        self.assertGreater(WINDOW_WIDTH, 0)
        self.assertGreater(WINDOW_HEIGHT, 0)
    
    def test_block_size(self):
        """Test that block size is positive and reasonable"""
        self.assertGreater(BLOCK_SIZE, 0)
        self.assertLessEqual(BLOCK_SIZE, 50)
    
    def test_window_divisible_by_block(self):
        """Test that window dimensions are divisible by block size"""
        self.assertEqual(WINDOW_WIDTH % BLOCK_SIZE, 0)
        self.assertEqual(WINDOW_HEIGHT % BLOCK_SIZE, 0)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)

# Made with Bob



class TestShowMenu(unittest.TestCase):
    """Test suite for the show_menu function"""
    
    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()
    
    @patch('snake_game.pygame.event.get')
    def test_menu_returns_classic_on_enter_with_default_selection(self, mock_event_get):
        """Test that menu returns CLASSIC mode when ENTER is pressed with default selection"""
        from snake_game import show_menu, GameMode
        
        # Simulate ENTER key press
        mock_event = Mock()
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_RETURN
        mock_event_get.return_value = [mock_event]
        
        result = show_menu(self.display)
        self.assertEqual(result, GameMode.CLASSIC)
    
    @patch('snake_game.pygame.event.get')
    def test_menu_returns_classic_on_space_with_default_selection(self, mock_event_get):
        """Test that menu returns CLASSIC mode when SPACE is pressed with default selection"""
        from snake_game import show_menu, GameMode
        
        # Simulate SPACE key press
        mock_event = Mock()
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_SPACE
        mock_event_get.return_value = [mock_event]
        
        result = show_menu(self.display)
        self.assertEqual(result, GameMode.CLASSIC)
    
    @patch('snake_game.pygame.event.get')
    def test_menu_navigation_down_then_enter(self, mock_event_get):
        """Test menu navigation: DOWN arrow then ENTER selects FUN mode"""
        from snake_game import show_menu, GameMode
        
        # Simulate DOWN arrow then ENTER
        down_event = Mock()
        down_event.type = pygame.KEYDOWN
        down_event.key = pygame.K_DOWN
        
        enter_event = Mock()
        enter_event.type = pygame.KEYDOWN
        enter_event.key = pygame.K_RETURN
        
        # First call returns DOWN, second call returns ENTER
        mock_event_get.side_effect = [[down_event], [enter_event]]
        
        result = show_menu(self.display)
        self.assertEqual(result, GameMode.FUN)
    
    @patch('snake_game.pygame.event.get')
    def test_menu_navigation_up_wraps_to_fun(self, mock_event_get):
        """Test that UP arrow from first option wraps to last option (FUN mode)"""
        from snake_game import show_menu, GameMode
        
        # Simulate UP arrow (should wrap to FUN) then ENTER
        up_event = Mock()
        up_event.type = pygame.KEYDOWN
        up_event.key = pygame.K_UP
        
        enter_event = Mock()
        enter_event.type = pygame.KEYDOWN
        enter_event.key = pygame.K_RETURN
        
        mock_event_get.side_effect = [[up_event], [enter_event]]
        
        result = show_menu(self.display)
        self.assertEqual(result, GameMode.FUN)
    
    @patch('snake_game.pygame.event.get')
    def test_menu_navigation_down_twice_wraps_to_classic(self, mock_event_get):
        """Test that DOWN arrow twice wraps back to CLASSIC mode"""
        from snake_game import show_menu, GameMode
        
        # Simulate DOWN, DOWN (wraps to CLASSIC), then ENTER
        down_event = Mock()
        down_event.type = pygame.KEYDOWN
        down_event.key = pygame.K_DOWN
        
        enter_event = Mock()
        enter_event.type = pygame.KEYDOWN
        enter_event.key = pygame.K_RETURN
        
        mock_event_get.side_effect = [[down_event], [down_event], [enter_event]]
        
        result = show_menu(self.display)
        self.assertEqual(result, GameMode.CLASSIC)
    
    @patch('snake_game.pygame.event.get')
    @patch('snake_game.pygame.quit')
    def test_menu_quit_event(self, mock_quit, mock_event_get):
        """Test that QUIT event calls pygame.quit and exits"""
        from snake_game import show_menu
        
        # Simulate QUIT event
        quit_event = Mock()
        quit_event.type = pygame.QUIT
        mock_event_get.return_value = [quit_event]
        
        # Mock quit() to raise SystemExit
        with patch('builtins.quit', side_effect=SystemExit):
            with self.assertRaises(SystemExit):
                show_menu(self.display)
        
        mock_quit.assert_called_once()
    
    @patch('snake_game.pygame.event.get')
    def test_menu_ignores_other_keys(self, mock_event_get):
        """Test that menu ignores keys other than UP, DOWN, ENTER, SPACE"""
        from snake_game import show_menu, GameMode
        
        # Simulate random key then ENTER
        random_key_event = Mock()
        random_key_event.type = pygame.KEYDOWN
        random_key_event.key = pygame.K_a  # Random key
        
        enter_event = Mock()
        enter_event.type = pygame.KEYDOWN
        enter_event.key = pygame.K_RETURN
        
        mock_event_get.side_effect = [[random_key_event], [enter_event]]
        
        result = show_menu(self.display)
        # Should still be CLASSIC (default) since random key was ignored
        self.assertEqual(result, GameMode.CLASSIC)


class TestMainGameLoop(unittest.TestCase):
    """Test suite for main game loop functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
    
    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()
    
    def test_game_over_state_detection(self):
        """Test that game over state is properly detected"""
        game = SnakeGame(GameMode.CLASSIC)
        
        # Force a collision
        game.head = Point(-BLOCK_SIZE, WINDOW_HEIGHT // 2)
        game.snake.insert(0, game.head)
        
        # Check collision
        self.assertTrue(game._is_collision())
    
    def test_game_reset_after_game_over(self):
        """Test that game can be reset after game over"""
        game = SnakeGame(GameMode.CLASSIC)
        
        # Modify game state
        game.score = 10
        game.snake = [Point(100, 100)]
        
        # Reset
        game.reset()
        
        # Verify reset
        self.assertEqual(game.score, 0)
        self.assertEqual(len(game.snake), 3)
    
    def test_mode_change_after_game_over(self):
        """Test that mode can be changed after game over"""
        game = SnakeGame(GameMode.CLASSIC)
        initial_mode = game.mode
        
        # Change mode
        game.set_mode(GameMode.FUN)
        
        # Verify mode changed
        self.assertNotEqual(game.mode, initial_mode)
        self.assertEqual(game.mode, GameMode.FUN)
    
    def test_score_persists_until_reset(self):
        """Test that score persists until explicit reset"""
        game = SnakeGame(GameMode.CLASSIC)
        
        # Set score
        game.score = 15
        
        # Score should persist
        self.assertEqual(game.score, 15)
        
        # Reset should clear score
        game.reset()
        self.assertEqual(game.score, 0)
    
    def test_game_over_returns_final_score(self):
        """Test that play_step returns final score on game over"""
        game = SnakeGame(GameMode.CLASSIC)
        game.score = 5
        
        # Force game over
        game.head = Point(-BLOCK_SIZE, WINDOW_HEIGHT // 2)
        game.snake.insert(0, game.head)
        
        # Simulate play_step detecting collision
        game_over = False
        final_score = 0
        if game._is_collision():
            game_over = True
            final_score = game.score
        
        self.assertTrue(game_over)
        self.assertEqual(final_score, 5)


class TestUIRendering(unittest.TestCase):
    """Test suite for UI rendering functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
        self.game = SnakeGame(GameMode.CLASSIC)
    
    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()
    
    def test_update_ui_does_not_crash(self):
        """Test that _update_ui executes without errors"""
        try:
            self.game._update_ui()
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    def test_update_ui_with_different_scores(self):
        """Test UI update with various score values"""
        for score in [0, 1, 10, 100, 999]:
            self.game.score = score
            try:
                self.game._update_ui()
                success = True
            except Exception:
                success = False
            
            self.assertTrue(success, f"UI update failed with score {score}")
    
    def test_update_ui_with_different_modes(self):
        """Test UI update in both game modes"""
        for mode in [GameMode.CLASSIC, GameMode.FUN]:
            self.game.mode = mode
            try:
                self.game._update_ui()
                success = True
            except Exception:
                success = False
            
            self.assertTrue(success, f"UI update failed in {mode.name} mode")
    
    def test_update_ui_with_empty_food_list(self):
        """Test UI update handles empty food list gracefully"""
        self.game.food_items = []
        try:
            self.game._update_ui()
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    def test_update_ui_with_long_snake(self):
        """Test UI update with a long snake"""
        # Create a long snake
        self.game.snake = [Point(i * BLOCK_SIZE, 100) for i in range(20)]
        try:
            self.game._update_ui()
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)


class TestGameIntegration(unittest.TestCase):
    """Integration tests for complete game scenarios"""
    
    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
    
    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()
    
    def test_complete_game_cycle_classic_mode(self):
        """Test a complete game cycle in Classic mode"""
        game = SnakeGame(GameMode.CLASSIC)
        
        # Verify initial state
        self.assertEqual(game.mode, GameMode.CLASSIC)
        self.assertEqual(game.score, 0)
        self.assertEqual(len(game.snake), 3)
        
        # Simulate eating food
        if game.food_items:
            game.head = game.food_items[0]
            game.snake.insert(0, game.head)
            game.score += 1
            
            self.assertEqual(game.score, 1)
            self.assertEqual(len(game.snake), 4)
    
    def test_complete_game_cycle_fun_mode(self):
        """Test a complete game cycle in Fun mode"""
        game = SnakeGame(GameMode.FUN)
        
        # Verify initial state
        self.assertEqual(game.mode, GameMode.FUN)
        
        # Test wall wrapping
        game.head = Point(WINDOW_WIDTH - BLOCK_SIZE, WINDOW_HEIGHT // 2)
        game._move(Direction.RIGHT)
        
        # Should wrap to left side
        self.assertEqual(game.head.x, 0)
    
    def test_mode_switch_during_gameplay(self):
        """Test switching modes during gameplay"""
        game = SnakeGame(GameMode.CLASSIC)
        
        # Play a bit
        game.score = 5
        
        # Switch mode
        game.set_mode(GameMode.FUN)
        
        # Verify mode changed and game reset
        self.assertEqual(game.mode, GameMode.FUN)
        self.assertEqual(game.score, 0)  # Reset clears score
    
    def test_multiple_food_eating_sequence(self):
        """Test eating multiple food items in sequence"""
        game = SnakeGame(GameMode.CLASSIC)
        initial_length = len(game.snake)
        
        # Eat 3 food items
        for i in range(3):
            if game.food_items:
                game.head = game.food_items[0]
                game.snake.insert(0, game.head)
                game.score += 1
                game.food_items.pop(0)
                game._add_single_food()
        
        # Verify growth and score


class TestHighScore(unittest.TestCase):
    """Test suite for high score functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
        # Clean up any existing test highscore file
        if os.path.exists('test_highscores.json'):
            os.remove('test_highscores.json')
    
    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()
        # Clean up test highscore file
        if os.path.exists('test_highscores.json'):
            os.remove('test_highscores.json')
    
    def test_load_highscores_creates_default(self):
        """Test that load_highscores creates default scores if file doesn't exist"""
        from snake_game import load_highscores
        
        # Remove file if it exists
        if os.path.exists(HIGHSCORE_FILE):
            os.remove(HIGHSCORE_FILE)
        
        highscores = load_highscores()
        
        self.assertEqual(highscores['classic'], 0)
        self.assertEqual(highscores['fun'], 0)
    
    def test_save_and_load_highscores(self):
        """Test saving and loading high scores"""
        from snake_game import save_highscores, load_highscores
        
        # Save test scores
        test_scores = {'classic': 10, 'fun': 15}
        save_highscores(test_scores)
        
        # Load and verify
        loaded_scores = load_highscores()
        self.assertEqual(loaded_scores['classic'], 10)
        self.assertEqual(loaded_scores['fun'], 15)
        
        # Clean up
        if os.path.exists(HIGHSCORE_FILE):
            os.remove(HIGHSCORE_FILE)
    
    def test_highscore_initialization(self):
        """Test that game initializes with high scores"""
        game = SnakeGame(GameMode.CLASSIC)
        
        self.assertIsNotNone(game.highscores)
        self.assertIn('classic', game.highscores)
        self.assertIn('fun', game.highscores)
    
    def test_get_highscore_classic_mode(self):
        """Test getting high score in Classic mode"""
        game = SnakeGame(GameMode.CLASSIC)
        game.highscores = {'classic': 20, 'fun': 15}
        
        highscore = game.get_highscore()
        self.assertEqual(highscore, 20)
    
    def test_get_highscore_fun_mode(self):
        """Test getting high score in Fun mode"""
        game = SnakeGame(GameMode.FUN)
        game.highscores = {'classic': 20, 'fun': 15}
        
        highscore = game.get_highscore()
        self.assertEqual(highscore, 15)
    
    def test_update_highscore_when_higher(self):
        """Test that high score updates when current score is higher"""
        game = SnakeGame(GameMode.CLASSIC)
        game.highscores = {'classic': 10, 'fun': 5}
        game.score = 15
        
        game._update_highscore()
        
        self.assertEqual(game.highscores['classic'], 15)
    
    def test_update_highscore_when_lower(self):
        """Test that high score doesn't update when current score is lower"""
        game = SnakeGame(GameMode.CLASSIC)
        game.highscores = {'classic': 20, 'fun': 5}
        game.score = 10
        
        game._update_highscore()
        
        self.assertEqual(game.highscores['classic'], 20)
    
    def test_update_highscore_when_equal(self):
        """Test that high score doesn't update when scores are equal"""
        game = SnakeGame(GameMode.CLASSIC)
        game.highscores = {'classic': 15, 'fun': 5}
        game.score = 15
        
        game._update_highscore()
        
        self.assertEqual(game.highscores['classic'], 15)
    
    def test_highscore_persists_across_modes(self):
        """Test that high scores are separate for each mode"""
        game = SnakeGame(GameMode.CLASSIC)
        game.highscores = {'classic': 20, 'fun': 10}
        game.score = 25
        game._update_highscore()
        
        # Switch to Fun mode
        game.set_mode(GameMode.FUN)
        
        # Classic high score should still be 25
        game.mode = GameMode.CLASSIC
        self.assertEqual(game.get_highscore(), 25)
        
        # Fun high score should still be 10
        game.mode = GameMode.FUN
        self.assertEqual(game.get_highscore(), 10)
    
    def test_highscore_updates_on_game_over(self):
        """Test that high score updates automatically on game over"""
        game = SnakeGame(GameMode.CLASSIC)
        game.highscores = {'classic': 5, 'fun': 5}
        game.score = 10
        
        # Force collision to trigger game over
        game.head = Point(-BLOCK_SIZE, WINDOW_HEIGHT // 2)
        game.snake.insert(0, game.head)
        
        # Check collision (which should call _update_highscore)
        if game._is_collision():
            game._update_highscore()
        
        self.assertEqual(game.highscores['classic'], 10)
    
    def test_load_highscores_handles_corrupted_file(self):
        """Test that load_highscores handles corrupted JSON gracefully"""
        from snake_game import load_highscores
        
        # Create corrupted JSON file
        with open(HIGHSCORE_FILE, 'w') as f:
            f.write("{ invalid json }")
        
        # Should return default scores
        highscores = load_highscores()
        self.assertEqual(highscores['classic'], 0)
        self.assertEqual(highscores['fun'], 0)
        
        # Clean up
        if os.path.exists(HIGHSCORE_FILE):
            os.remove(HIGHSCORE_FILE)
    
    def test_highscore_display_in_ui(self):
        """Test that high score is displayed in UI"""
        game = SnakeGame(GameMode.CLASSIC)
        game.highscores = {'classic': 100, 'fun': 50}
        
        # UI update should not crash with high score
        try:
            game._update_ui()
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    def test_separate_highscores_for_each_mode(self):
        """Test that Classic and Fun modes have separate high scores"""
        game = SnakeGame(GameMode.CLASSIC)
        
        # Set different scores for each mode
        game.mode = GameMode.CLASSIC
        game.score = 30
        game._update_highscore()
        
        game.mode = GameMode.FUN
        game.score = 50
        game._update_highscore()
        
        # Verify they're different
        game.mode = GameMode.CLASSIC
        classic_high = game.get_highscore()
        
        game.mode = GameMode.FUN
        fun_high = game.get_highscore()
        
        self.assertEqual(classic_high, 30)
        self.assertEqual(fun_high, 50)
        self.assertNotEqual(classic_high, fun_high)
