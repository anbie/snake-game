# 🐍 Classic Snake Game

A classic snake game implementation in Python using Pygame. Control the snake to eat food, grow longer, and avoid hitting the walls or yourself!

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎮 Game Features

- Classic snake gameplay mechanics
- Smooth controls using arrow keys
- Score tracking
- Game over detection with restart option
- Clean and simple graphics

## 🎯 How to Play

- Use **Arrow Keys** to control the snake's direction:
  - ⬆️ **UP** - Move up
  - ⬇️ **DOWN** - Move down
  - ⬅️ **LEFT** - Move left
  - ➡️ **RIGHT** - Move right
- Eat the red food to grow longer and increase your score
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

- **pygame**: Game development library for Python

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
├── snake_game.py      # Main game file
├── requirements.txt   # Python dependencies
├── README.md         # This file
└── .gitignore        # Git ignore file
```

## 🎓 Game Mechanics

- The snake starts with 3 segments
- Each food eaten adds 1 point to the score and 1 segment to the snake
- The game ends when the snake hits a wall or itself
- Food spawns randomly on the grid

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