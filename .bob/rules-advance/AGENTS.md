# Advance Mode Rules (Non-Obvious Only)

## Project-Specific Coding Patterns
- **Collision detection timing**: Use `body_to_check = snake[1:] if food_eaten else snake[1:-1]` to avoid false collision with tail segment that's about to move away
- **Wall wrapping implementation**: Fun mode wrapping happens in `_move()` method using modulo arithmetic, NOT in collision detection
- **Food spawn retry mechanism**: `MAX_FOOD_PLACEMENT_ATTEMPTS = 100` prevents infinite loops when board is nearly full
- **Highscore persistence**: Use `SNAKE_HIGHSCORE_FILE` env var for file location (test isolation requires this)
- **Mode-specific data structure**: Highscores stored as `{'classic': int, 'fun': int}` dict in JSON

## Testing Requirements (Non-Standard)
- **X server dependency**: Pygame tests need `xvfb-run -a` prefix in headless environments (CI/CD)
- **Test isolation**: Must set `SNAKE_HIGHSCORE_FILE=test_highscores.json` before importing game module
- **Dual test frameworks**: Both pytest AND unittest must pass (CI runs both)

## Constants Validation (Hidden Requirements)
- Window dimensions MUST be divisible by `BLOCK_SIZE` - enforced by module-level assertions
- Food items range 1-99 configurable at runtime (not just via `DEFAULT_NUM_FOOD_ITEMS` constant)

## Tool Access
- Has access to MCP and Browser tools (unlike Code mode)