#!/usr/bin/env python3
"""
Standalone Security Fix Validation Tests
Tests the security fixes by extracting just the validation logic.
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# Extract the security validation function
def get_safe_highscore_path() -> str:
    """
    Get validated highscore file path to prevent path traversal attacks.
    
    Security measures:
    - Resolves to absolute path
    - Ensures path is within allowed directories (cwd or user home)
    - Validates .json extension
    - Falls back to safe default if validation fails
    
    Returns:
        str: Safe, validated path to highscore file
    """
    default_file = 'highscores.json'
    env_file = os.environ.get('SNAKE_HIGHSCORE_FILE', default_file)
    
    try:
        # Resolve to absolute path
        file_path = Path(env_file).resolve()
        
        # Ensure it's within allowed directories (current working directory or user home)
        allowed_dirs = [Path.cwd(), Path.home()]
        
        # Check if path starts with any allowed directory
        is_allowed = any(
            str(file_path).startswith(str(allowed_dir)) 
            for allowed_dir in allowed_dirs
        )
        
        if not is_allowed:
            print(f"WARNING: Highscore path outside allowed directories: {file_path}")
            return str(Path.cwd() / default_file)
        
        # Ensure filename ends with .json
        if file_path.suffix != '.json':
            print(f"WARNING: Highscore file must have .json extension: {file_path}")
            return str(Path.cwd() / default_file)
        
        return str(file_path)
        
    except (ValueError, OSError) as e:
        print(f"WARNING: Invalid highscore path: {e}")
        return str(Path.cwd() / default_file)


def load_highscores(highscore_file: str) -> dict:
    """
    Load high scores from JSON file with validation.
    
    Security measures:
    - Validates JSON structure (must be dict)
    - Validates data types (must be integers)
    - Clamps values to reasonable range (0-999999)
    - Returns safe defaults on any error
    
    Returns:
        dict: Validated highscores with keys 'classic' and 'fun'
    """
    default_scores = {'classic': 0, 'fun': 0}
    
    if not os.path.exists(highscore_file):
        return default_scores
    
    try:
        with open(highscore_file, 'r') as f:
            data = json.load(f)
        
        # Validate structure - must be a dictionary
        if not isinstance(data, dict):
            print(f"WARNING: Invalid highscore format: expected dict, got {type(data).__name__}")
            return default_scores
        
        # Validate and sanitize each mode
        validated = {}
        for mode in ['classic', 'fun']:
            score = data.get(mode, 0)
            
            # Ensure it's a numeric type
            if not isinstance(score, (int, float)):
                print(f"WARNING: Invalid score type for {mode}: {type(score).__name__}, using 0")
                validated[mode] = 0
            else:
                # Convert to int and clamp to reasonable range
                validated[mode] = max(0, min(int(score), 999999))
        
        return validated
        
    except (json.JSONDecodeError, IOError) as e:
        print(f"WARNING: Failed to load highscores: {type(e).__name__}")
        return default_scores


def test_path_traversal_protection():
    """Test that path traversal attacks are blocked."""
    print("=" * 70)
    print("TEST 1: Path Traversal Protection")
    print("=" * 70)
    
    test_cases = [
        ("/etc/passwd", "Absolute path outside allowed dirs", False),
        ("../../../etc/passwd", "Relative path traversal", False),
        ("/tmp/malicious.json", "Absolute path to /tmp", False),
        ("malicious.txt", "Non-JSON extension", False),
        ("valid_scores.json", "Valid path in CWD", True),
        (str(Path.home() / "my_scores.json"), "Valid path in home", True),
    ]
    
    passed = 0
    failed = 0
    
    for test_path, description, should_be_valid in test_cases:
        os.environ['SNAKE_HIGHSCORE_FILE'] = test_path
        safe_path = get_safe_highscore_path()
        
        # Check if path is safe
        is_safe = (
            safe_path.endswith('.json') and
            (str(Path.cwd()) in safe_path or str(Path.home()) in safe_path) and
            '/etc/' not in safe_path
        )
        
        # For valid inputs, check they weren't changed unnecessarily
        if should_be_valid:
            is_correct = test_path in safe_path or Path(test_path).name in safe_path
        else:
            is_correct = safe_path == str(Path.cwd() / 'highscores.json')
        
        if is_safe and is_correct:
            status = "✅ PASS"
            passed += 1
        else:
            status = "❌ FAIL"
            failed += 1
            
        print(f"\n{status}: {description}")
        print(f"  Input:    {test_path}")
        print(f"  Output:   {safe_path}")
        print(f"  Expected: {'Valid path' if should_be_valid else 'Default fallback'}")
    
    print(f"\n{'=' * 70}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'=' * 70}\n")
    
    return failed == 0


def test_json_validation():
    """Test that malicious JSON is rejected."""
    print("=" * 70)
    print("TEST 2: JSON Validation & Sanitization")
    print("=" * 70)
    
    test_cases = [
        ('{"classic": 100, "fun": 200}', "Valid JSON", {'classic': 100, 'fun': 200}),
        ('{"classic": "not_a_number", "fun": 50}', "String instead of number", {'classic': 0, 'fun': 50}),
        ('{"classic": 999999999999999999, "fun": 50}', "Extremely large number", {'classic': 999999, 'fun': 50}),
        ('{"classic": -100, "fun": 50}', "Negative number", {'classic': 0, 'fun': 50}),
        ('["not", "a", "dict"]', "Array instead of dict", {'classic': 0, 'fun': 0}),
        ('{"malicious": "data", "classic": 50}', "Extra keys", {'classic': 50, 'fun': 0}),
        ('not valid json', "Invalid JSON syntax", {'classic': 0, 'fun': 0}),
    ]
    
    passed = 0
    failed = 0
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for json_content, description, expected in test_cases:
            test_file = Path(tmpdir) / "test_scores.json"
            
            # Write test JSON
            with open(test_file, 'w') as f:
                f.write(json_content)
            
            try:
                scores = load_highscores(str(test_file))
                
                # Validate returned structure
                is_valid = (
                    isinstance(scores, dict) and
                    'classic' in scores and
                    'fun' in scores and
                    isinstance(scores['classic'], int) and
                    isinstance(scores['fun'], int) and
                    0 <= scores['classic'] <= 999999 and
                    0 <= scores['fun'] <= 999999 and
                    scores == expected
                )
                
                status = "✅ PASS" if is_valid else "❌ FAIL"
                if is_valid:
                    passed += 1
                else:
                    failed += 1
                    
                print(f"\n{status}: {description}")
                print(f"  Input:    {json_content[:50]}...")
                print(f"  Output:   {scores}")
                print(f"  Expected: {expected}")
                
            except Exception as e:
                print(f"\n❌ FAIL: {description}")
                print(f"  Unexpected exception: {e}")
                failed += 1
    
    print(f"\n{'=' * 70}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'=' * 70}\n")
    
    return failed == 0


def main():
    """Run all security tests."""
    print("\n" + "=" * 70)
    print("SECURITY FIX VALIDATION TEST SUITE (Standalone)")
    print("=" * 70 + "\n")
    
    results = []
    
    try:
        results.append(("Path Traversal Protection", test_path_traversal_protection()))
    except Exception as e:
        print(f"❌ Path Traversal test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Path Traversal Protection", False))
    
    try:
        results.append(("JSON Validation", test_json_validation()))
    except Exception as e:
        print(f"❌ JSON Validation test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        results.append(("JSON Validation", False))
    
    # Summary
    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("=" * 70)
    
    if all_passed:
        print("\n🎉 All security fixes validated successfully!")
        print("\nSummary of fixes:")
        print("  ✅ Path traversal vulnerability fixed")
        print("  ✅ JSON validation and sanitization implemented")
        print("  ✅ Input clamping to prevent integer overflow")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the fixes.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
