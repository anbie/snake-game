# Plan Mode Rules (Non-Obvious Only)

## Architecture Constraints (Hidden)
- **Monolithic design**: Single 600+ line file by design (not accidental - keeps game simple)
- **Pygame initialization timing**: Must happen at module level, not in class `__init__` (pygame requirement)
- **State management**: No external state library - all state in SnakeGame class attributes
- **Collision detection split**: Wall collision in `_is_collision()` for Classic mode, but wrapping in `_move()` for Fun mode (not centralized)

## Performance Considerations
- **Food placement algorithm**: Retry-based with `MAX_FOOD_PLACEMENT_ATTEMPTS = 100` limit (can fail silently if board nearly full)
- **Tail collision optimization**: Checks `snake[1:]` or `snake[1:-1]` depending on whether food was eaten (avoids false positive with moving tail)

## Testing Architecture
- **Dual framework requirement**: Both pytest and unittest must pass (intentional redundancy for compatibility)
- **Headless rendering**: CI requires xvfb wrapper for pygame display (not mocked)
- **Test isolation pattern**: Uses environment variable override for highscore file (not dependency injection)

## Data Persistence
- **Highscore structure**: JSON dict with mode keys `{'classic': int, 'fun': int}` - not array of objects
- **No database**: Simple JSON file in root directory (intentionally simple, not scalable)