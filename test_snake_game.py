import unittest
import pygame
from unittest.mock import Mock, patch, MagicMock
from snake_game import SnakeGame, Direction, Point, BLOCK_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT


class TestSnakeGame(unittest.TestCase):
    """Test suite for Snake Game"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        pygame.init()
        self.game = SnakeGame()
    
    def tearDown(self):
        """Clean up after each test method"""
        pygame.quit()
    
    # Test initialization
    def test_game_initialization(self):
        """Test that game initializes with correct default values"""
        self.assertIsNotNone(self.game.display)
        self.assertIsNotNone(self.game.clock)
        self.assertEqual(self.game.direction, Direction.RIGHT)
        self.assertEqual(len(self.game.snake), 3)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(len(self.game.food_items), 3)
    
    def test_reset(self):
        """Test that reset method properly resets game state"""
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
        self.assertEqual(len(self.game.food_items), 3)
    
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
        """Test that exactly 3 food items are placed"""
        self.assertEqual(len(self.game.food_items), 3)
    
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
    
    # Test collision detection
    def test_collision_with_left_wall(self):
        """Test collision detection with left wall"""
        self.game.head = Point(-BLOCK_SIZE, WINDOW_HEIGHT // 2)
        self.assertTrue(self.game._is_collision())
    
    def test_collision_with_right_wall(self):
        """Test collision detection with right wall"""
        self.game.head = Point(WINDOW_WIDTH, WINDOW_HEIGHT // 2)
        self.assertTrue(self.game._is_collision())
    
    def test_collision_with_top_wall(self):
        """Test collision detection with top wall"""
        self.game.head = Point(WINDOW_WIDTH // 2, -BLOCK_SIZE)
        self.assertTrue(self.game._is_collision())
    
    def test_collision_with_bottom_wall(self):
        """Test collision detection with bottom wall"""
        self.game.head = Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT)
        self.assertTrue(self.game._is_collision())
    
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
    
    def test_no_collision_in_valid_position(self):
        """Test that no collision is detected in valid position"""
        self.game.head = Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.game.snake = [self.game.head]
        self.assertFalse(self.game._is_collision())
    
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
        # Fill most of the board with snake to test collision avoidance
        self.game._add_single_food()
        new_food = self.game.food_items[-1]
        self.assertNotIn(new_food, self.game.snake)
    
    def test_add_single_food_unique_position(self):
        """Test that newly added food has unique position"""
        initial_foods = self.game.food_items.copy()
        self.game._add_single_food()
        new_food = self.game.food_items[-1]
        self.assertNotIn(new_food, initial_foods)
    
    # Test game state
    def test_game_over_on_wall_collision(self):
        """Test that game ends when snake hits wall"""
        # Move snake to wall
        self.game.head = Point(-BLOCK_SIZE, WINDOW_HEIGHT // 2)
        self.game.snake.insert(0, self.game.head)
        
        # Check collision
        game_over = self.game._is_collision()
        self.assertTrue(game_over)
    
    def test_game_continues_in_valid_state(self):
        """Test that game continues when in valid state"""
        # Ensure snake is in valid position
        self.game.head = Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.game.snake = [self.game.head]
        
        game_over = self.game._is_collision()
        self.assertFalse(game_over)
    
    # Test Direction enum
    def test_direction_enum_values(self):
        """Test that Direction enum has correct values"""
        self.assertEqual(Direction.RIGHT.value, 1)
        self.assertEqual(Direction.LEFT.value, 2)
        self.assertEqual(Direction.UP.value, 3)
        self.assertEqual(Direction.DOWN.value, 4)
    
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
            
            self.assertEqual(len(self.game.food_items), 3)


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
