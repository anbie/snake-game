# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Environment Setup (Non-Standard)
- **CRITICAL**: macOS uses `python3` not `python` - always use `python3` command
- **Virtual environment required**: System blocks global pip installs - must use venv:
  ```bash
  python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
  ```
- Run game: `python3 snake_game.py` (or `python` inside activated venv)

## Testing (Non-Obvious Requirements)
- **Tests require X server**: CI uses `xvfb-run -a` prefix for headless pygame tests
- **Environment variable for test isolation**: Tests set `SNAKE_HIGHSCORE_FILE=test_highscores.json` to avoid touching real highscores
- Run single test: `pytest test_snake_game.py::TestClassName::test_method_name -v`
- Both pytest AND unittest are used (CI runs both frameworks)

## Code Patterns (Project-Specific)
- **Highscore file location**: Configurable via `SNAKE_HIGHSCORE_FILE` env var (defaults to `highscores.json`)
- **Mode-specific highscores**: Stored as dict with keys `'classic'` and `'fun'` in JSON file
- **Collision detection quirk**: Uses `body_to_check = snake[1:] if food_eaten else snake[1:-1]` to avoid false collision with tail that's about to move
- **Wall wrapping in Fun mode**: Implemented in `_move()` method, not in collision detection
- **Food placement**: Uses `MAX_FOOD_PLACEMENT_ATTEMPTS = 100` retry limit to prevent infinite loops

## Constants (Non-Standard Validation)
- Window dimensions MUST be divisible by BLOCK_SIZE (enforced by assertions at module level)
- Food items configurable 1-99 at runtime (not just via constants)