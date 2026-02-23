# 🐍 Classic Snake Game

This is the outcome from my first playdate with my new friend Bob (https://www.ibm.com/products/bob). Done while killing some time at the airport. Really impressive!


A classic snake game implementation in Python using Pygame. Control the snake to eat food, grow longer, and avoid hitting the walls or yourself!

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)
![Tests](https://github.com/anbie/snake-game/workflows/Run%20Tests/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎮 Game Features

- **Two Game Modes:**
  - 🏛️ **Classic Mode**: Game ends when snake hits walls
  - 🎪 **Fun Mode**: Snake wraps around walls (appears on opposite side)
- **Interactive startup menu** to select game mode and configure settings
- **Configurable food items** (1-50 items, default 4) with colorful variety (Red, Orange, Yellow, Blue)
- **Pause functionality** - Press 'P' to pause/resume the game
- **High Score System:**
  - 🏆 Separate high scores for each game mode
  - 💾 Automatically saved and persisted across sessions
  - 📊 Displayed during gameplay and in menu
- Smooth controls using arrow keys
- Score tracking with real-time display
- Game over detection with restart option
- Return to menu option after game over
- Clean and simple graphics with improved UI
- Comprehensive unit tests with CI/CD integration
- Type hints for better code quality

## 🎯 How to Play

### Starting the Game
1. Run the game and you'll see a menu with game mode options
2. Use **UP/DOWN** arrow keys to select a mode (Classic or Fun)
3. Use **LEFT/RIGHT** arrow keys to adjust the number of food items (1-50)
4. Press **ENTER** or **SPACE** to start the game

### Game Modes

#### 🏛️ Classic Mode
- Traditional snake gameplay
- Game ends when you hit a wall
- More challenging!

#### 🎪 Fun Mode
- Snake wraps around walls
- Hit the right wall → appear on the left
- Hit the top wall → appear at the bottom
- Endless fun!

### Controls
- Use **Arrow Keys** to control the snake's direction:
  - ⬆️ **UP** - Move up
  - ⬇️ **DOWN** - Move down
  - ⬅️ **LEFT** - Move left
  - ➡️ **RIGHT** - Move right
- Press **P** to pause/resume the game
- Eat the colorful food items (red, orange, yellow, blue) to grow longer and increase your score
- Avoid hitting your own body (in both modes)
- Press **SPACE** to restart after game over
- Press **ESC** to return to menu after game over or during gameplay (press twice to confirm quit)

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/anbie/snake-game.git
cd snake-game
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## 🎮 Running the Game

Simply run the main Python file:

```bash
python snake_game.py
```

## 📦 Dependencies

### Runtime Dependencies
- **pygame**: Game development library for Python

### Development Dependencies
- **pytest**: Testing framework
- **pytest-cov**: Code coverage plugin for pytest
- **coverage**: Code coverage measurement

See `requirements.txt` for specific version requirements.

## 🎨 Game Configuration

You can modify the following constants in `snake_game.py` to customize the game:

- `WINDOW_WIDTH`: Width of the game window (default: 640)
- `WINDOW_HEIGHT`: Height of the game window (default: 480)
- `BLOCK_SIZE`: Size of each snake segment (default: 20)
- `SPEED`: Game speed/FPS (default: 10)
- `DEFAULT_NUM_FOOD_ITEMS`: Default number of food items (default: 4)
- `MIN_FOOD_ITEMS`: Minimum food items allowed (default: 1)
- `MAX_FOOD_ITEMS`: Maximum food items allowed (default: 50)
- Colors: `WHITE`, `BLACK`, `RED`, `GREEN`, `BLUE`, `ORANGE`, `YELLOW`
- `FOOD_COLORS`: Array of colors for food items
- `SNAKE_INNER_OFFSET`: Offset for snake inner detail (default: 4)
- `SNAKE_INNER_SIZE`: Size of snake inner detail (default: 12)

**Note:** Food items can now be configured at runtime through the menu (1-50 items).

## 🏗️ Project Structure

```
snake-game/
├── .github/
│   └── workflows/
│       └── tests.yml       # GitHub Actions CI/CD workflow
├── snake_game.py           # Main game file
├── test_snake_game.py      # Comprehensive unit tests
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore             # Git ignore file
```

## 🎓 Game Mechanics

### Common to Both Modes
- The snake starts with 3 segments
- **Configurable food items** (1-50, default 4) are present on the board with different colors (Red, Orange, Yellow, Blue)
- Each food eaten adds 1 point to the score and 1 segment to the snake
- When a food is eaten, a new one spawns to maintain the configured number of food items
- Food spawns randomly on the grid, avoiding the snake's body and other food
- Hitting your own body ends the game in both modes
- Press 'P' to pause/resume at any time

### Classic Mode Specific
- Game ends when snake hits any wall
- More challenging and traditional gameplay

### Fun Mode Specific
- Snake wraps around when hitting walls:
  - Hit right wall → appear on left side
  - Hit left wall → appear on right side
  - Hit top wall → appear at bottom
  - Hit bottom wall → appear at top
- Only hitting yourself ends the game
- Allows for longer gameplay sessions

## 🧪 Testing

This project includes comprehensive unit tests covering all game functions.

### Running Tests Locally

1. Install test dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests with pytest:
```bash
pytest test_snake_game.py -v
```

3. Run tests with coverage:
```bash
pytest test_snake_game.py -v --cov=snake_game --cov-report=term-missing
```

4. Run tests with unittest:
```bash
python -m unittest test_snake_game.py -v
```

### Test Coverage

The test suite includes:
- **100+ unit tests** covering all game functions in both modes
- Initialization and reset tests for both Classic and Fun modes
- Movement and collision detection tests
- Wall collision tests (Classic mode)
- Wall wrapping tests (Fun mode)
- Food placement and eating mechanics tests
- Game state and scoring tests
- Mode switching tests
- **High score functionality tests:**
  - High score persistence and loading
  - Separate high scores for each mode
  - High score updates on game over
  - Corrupted file handling
- UI rendering tests
- Menu navigation tests
- Integration tests for complete game scenarios
- Boundary and edge case tests

### Continuous Integration

Tests run automatically on every commit via GitHub Actions:
- Tests run on Python 3.11, 3.12, 3.13, and 3.14
- Automatic code coverage reporting
- Tests run on both push and pull requests
- Coverage reports uploaded as artifacts

View test results in the [Actions tab](https://github.com/anbie/snake-game/actions) of the repository.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**anbie**
- GitHub: [@anbie](https://github.com/anbie)

## 🌟 Show your support

Give a ⭐️ if you enjoyed this project!

---

Made with ❤️ and Python
