#!/usr/bin/env python3
"""
Manual test script for the menu functionality.
Run this to test that LEFT/RIGHT arrows adjust food items.
"""

import pygame
from snake_game import show_menu

def main():
    pygame.init()
    display = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Menu Test')
    
    print("Testing menu...")
    print("Use LEFT/RIGHT arrows to adjust food items")
    print("Use UP/DOWN to select mode")
    print("Press ENTER to confirm")
    
    mode, num_food = show_menu(display)
    
    print(f"\nSelected:")
    print(f"  Mode: {mode.name}")
    print(f"  Food Items: {num_food}")
    
    pygame.quit()

if __name__ == '__main__':
    main()

# Made with Bob
