# 🐍 Classic Snake Game

This is my first playdate with my new friend Bob (https://www.ibm.com/products/bob). Done while killing some time at the airport. Really impressive!


A classic snake game implementation in Python using Pygame. Control the snake to eat food, grow longer, and avoid hitting the walls or yourself!

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)
![Tests](https://github.com/anbie/snake-game/workflows/Run%20Tests/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎮 Game Features

- Classic snake gameplay mechanics with **3 colorful food items** (Red, Orange, Yellow)
- Smooth controls using arrow keys
- Score tracking
- Game over detection with restart option
- Clean and simple graphics
- Comprehensive unit tests with CI/CD integration

## 🎯 How to Play

- Use **Arrow Keys** to control the snake's direction:
  - ⬆️ **UP** - Move up
  - ⬇️ **DOWN** - Move down
  - ⬅️ **LEFT** - Move left
  - ➡️ **RIGHT** - Move right
- Eat the colorful food items (red, orange, yellow) to grow longer and increase your score
- Avoid hitting the walls or your own body
- Press **SPACE** to restart after game over

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
- Colors: `WHITE`, `BLACK`, `RED`, `GREEN`, `BLUE`

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

- The snake starts with 3 segments
- **3 food items** are always present on the board with different colors
- Each food eaten adds 1 point to the score and 1 segment to the snake
- When a food is eaten, a new one spawns to maintain 3 food items
- The game ends when the snake hits a wall or itself
- Food spawns randomly on the grid, avoiding the snake's body

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
- **50+ unit tests** covering all game functions
- Initialization and reset tests
- Movement and collision detection tests
- Food placement and eating mechanics tests
- Game state and scoring tests
- Boundary and edge case tests

### Continuous Integration

Tests run automatically on every commit via GitHub Actions:
- Tests run on Python 3.8, 3.9, 3.10, and 3.11
- Automatic code coverage reporting
- Tests run on both push and pull requests

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
