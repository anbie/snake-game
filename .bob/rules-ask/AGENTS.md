# Ask Mode Rules (Non-Obvious Only)

## Project Structure (Counterintuitive)
- **Single-file architecture**: All game logic in `snake_game.py` (no separate modules despite 600+ lines)
- **Test file naming**: `test_snake_game.py` uses unittest framework but runs with pytest too
- **Highscore persistence**: Stored in root directory as `highscores.json`, NOT in a data/ or config/ folder
- **GitHub Pages deployment**: Uses `index.html` in root (not docs/ folder) for web version

## Documentation Context
- **Two game modes**: Classic (walls kill) vs Fun (walls wrap) - not obvious from file structure
- **Environment variable override**: `SNAKE_HIGHSCORE_FILE` used for test isolation (documented in test file, not main code)
- **CI/CD quirk**: Tests run on Python 3.11-3.14 with xvfb for headless pygame rendering
- **Dual testing**: Both pytest and unittest frameworks must pass (unusual pattern)

## Hidden Configuration
- **Runtime food configuration**: Menu allows 1-99 food items despite `MAX_FOOD_ITEMS = 50` constant in code
- **Module-level validation**: Window dimensions validated at import time (not runtime) via assertions