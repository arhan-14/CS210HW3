#!/bin/bash

# Music Database Test Runner
# This script runs all tests for the music database project

echo "================================================"
echo "Music Database - Complete Test Suite"
echo "================================================"
echo ""
echo "This will run all tests in sequence:"
echo "  1. Populate database (test_music_db.py)"
echo "  2. Quick assertions (test_quick.py)"
echo "  3. Comprehensive assertions (test_assertions.py)"
echo ""
echo "Press Enter to continue or Ctrl+C to cancel..."
read

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall success
ALL_PASSED=true

# Get the script directory and go to test_files directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
TEST_DIR="$PROJECT_ROOT/test_files"

echo ""
echo "================================================"
echo "Step 1: Populating Database"
echo "================================================"
if python3 "$TEST_DIR/test_music_db.py"; then
    echo -e "${GREEN}✓ Database populated successfully${NC}"
else
    echo -e "${RED}✗ Failed to populate database${NC}"
    exit 1
fi

echo ""
echo "================================================"
echo "Step 2: Quick Assertion Tests"
echo "================================================"
if python3 "$TEST_DIR/test_quick.py"; then
    echo -e "${GREEN}✓ Quick tests passed${NC}"
else
    echo -e "${YELLOW}⚠ Some quick tests failed${NC}"
    ALL_PASSED=false
fi

echo ""
echo "================================================"
echo "Step 3: Comprehensive Assertion Tests"
echo "================================================"
if python3 "$TEST_DIR/test_assertions.py"; then
    echo -e "${GREEN}✓ Comprehensive tests passed${NC}"
else
    echo -e "${YELLOW}⚠ Some comprehensive tests failed${NC}"
    ALL_PASSED=false
fi

echo ""
echo "================================================"
echo "FINAL RESULTS"
echo "================================================"
if [ "$ALL_PASSED" = true ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED!${NC}"
    echo ""
    echo "Your music database implementation is working correctly!"
    exit 0
else
    echo -e "${YELLOW}⚠ SOME TESTS FAILED${NC}"
    echo ""
    echo "Please review the output above for details."
    exit 1
fi
