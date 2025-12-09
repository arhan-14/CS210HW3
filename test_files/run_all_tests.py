#!/usr/bin/env python3
"""
Run all tests in sequence: populate database, then run assertions.
This is a convenience script to run the full test suite.
"""

import subprocess
import sys


def run_command(command, description):
    """Run a command and print status"""
    print("\n" + "=" * 70)
    print(f"{description}")
    print("=" * 70)

    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=False, text=True
        )
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed with exit code {e.returncode}")
        return False


def main():
    """Run all test suites"""
    print("\n" + "=" * 70)
    print("MUSIC DATABASE - COMPLETE TEST SUITE")
    print("=" * 70)
    print("\nThis will run:")
    print("1. test_music_db.py - Populate database with test data")
    print("2. test_quick.py - Quick assertion tests")
    print("3. test_assertions.py - Comprehensive assertion tests")
    print("\nMake sure:")
    print("- MySQL is running")
    print("- Database credentials are configured in DB_CONFIG")
    print("- Database schema has been created (schema.sql)")

    response = input("\nPress Enter to continue or Ctrl+C to cancel... ")

    all_passed = True

    # Get the directory where this script is located (test_files/)
    import os

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Step 1: Populate database
    if not run_command(
        f"{sys.executable} {os.path.join(script_dir, 'test_music_db.py')}",
        "Step 1: Populating database",
    ):
        print("\n✗ Failed to populate database. Please check your configuration.")
        return False

    # Step 2: Quick tests
    if not run_command(
        f"{sys.executable} {os.path.join(script_dir, 'test_quick.py')}",
        "Step 2: Quick assertion tests",
    ):
        print("\n⚠ Quick tests had failures")
        all_passed = False

    # Step 3: Comprehensive tests
    if not run_command(
        f"{sys.executable} {os.path.join(script_dir, 'test_assertions.py')}",
        "Step 3: Comprehensive assertion tests",
    ):
        print("\n⚠ Comprehensive tests had failures")
        all_passed = False

    # Summary
    print("\n" + "=" * 70)
    print("COMPLETE TEST SUITE SUMMARY")
    print("=" * 70)

    if all_passed:
        print("✓ ALL TEST SUITES PASSED!")
        print("\nYour music database implementation is working correctly.")
        return True
    else:
        print("⚠ SOME TESTS FAILED")
        print("\nPlease review the output above for details.")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest suite cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Error running test suite: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
