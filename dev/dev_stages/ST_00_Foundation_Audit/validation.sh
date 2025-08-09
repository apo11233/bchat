#!/bin/bash

# ST_00 Foundation Validation Suite
# Tests all currently working functionality to establish baseline

echo "🔍 ST_00 Foundation Validation Suite"
echo "===================================="
echo "Testing Date: $(date)"
echo ""

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run test and track results
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_result="$3"  # 0 for success, 1 for failure
    
    echo -n "Testing $test_name... "
    TESTS_RUN=$((TESTS_RUN + 1))
    
    if eval "$test_command" &>/dev/null; then
        if [ "$expected_result" = "0" ]; then
            echo "✅ PASS"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo "❌ FAIL (unexpected success)"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    else
        if [ "$expected_result" = "1" ]; then
            echo "✅ PASS (expected failure)"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo "❌ FAIL"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    fi
}

echo "📋 BASELINE FUNCTIONALITY TESTS"
echo "--------------------------------"

# File Structure Tests
run_test "Config file exists" "[ -f config/config.json ]" 0
run_test "Chats directory exists" "[ -d data/chats ]" 0
run_test "Logs directory exists" "[ -d data/logs ]" 0
run_test "Core source exists" "[ -f core/src/bchat.py ]" 0
run_test "Auto-detect exists" "[ -f core/src/auto_detect.py ]" 0

echo ""
echo "🔧 COMMAND FUNCTIONALITY TESTS"
echo "------------------------------"

# Working Commands (should pass)
run_test "bchat --status command" "./bchat --status" 0

# Broken Commands (should fail - this validates our audit)
run_test "bchat without venv (should fail)" "./bchat" 1

# Virtual Environment Tests
if [ -d "dev/venv" ]; then
    run_test "bchat with venv" "source dev/venv/bin/activate && ./bchat" 0
    run_test "Auto-detect with venv" "source dev/venv/bin/activate && python3 core/src/auto_detect.py" 0
else
    echo "⚠️  Warning: dev/venv not found, skipping venv tests"
fi

echo ""
echo "📄 JSON PROCESSING TESTS"
echo "-----------------------"

# Check if JSON files are being generated and are valid
run_test "Chat index exists" "[ -f data/chats/chat_index.json ]" 0
run_test "Context summary exists" "[ -f data/chats/context_summary.json ]" 0
run_test "Chat index is valid JSON" "python3 -m json.tool data/chats/chat_index.json > /dev/null" 0
run_test "Context summary is valid JSON" "python3 -m json.tool data/chats/context_summary.json > /dev/null" 0

# Test if recent sessions show proper structure
if [ -f "data/chats/chat_index.json" ]; then
    RECENT_ENTRIES=$(python3 -c "import json; data=json.load(open('data/chats/chat_index.json')); print(len(data))")
    if [ "$RECENT_ENTRIES" -gt 0 ]; then
        echo "✅ PASS: Chat index contains $RECENT_ENTRIES entries"
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo "❌ FAIL: Chat index is empty"
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
fi

echo ""
echo "🔑 API CONFIGURATION TESTS"
echo "-------------------------"

# Check configuration validity
run_test "Config is valid JSON" "python3 -m json.tool config/config.json > /dev/null" 0

# Test environment setup
if [ -f ".env" ]; then
    run_test ".env file exists" "[ -f .env ]" 0
    # Check if API keys are configured (don't expose values)
    if grep -q "GOOGLE_API_KEY=" .env 2>/dev/null; then
        echo "✅ PASS: GOOGLE_API_KEY configured"
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo "⚠️  WARNING: GOOGLE_API_KEY not found in .env"
    fi
else
    echo "⚠️  WARNING: .env file not found"
fi

echo ""
echo "📊 VALIDATION RESULTS"
echo "===================="
echo "Tests Run: $TESTS_RUN"
echo "Tests Passed: $TESTS_PASSED"
echo "Tests Failed: $TESTS_FAILED"

if [ $TESTS_FAILED -eq 0 ]; then
    echo "🎉 ALL TESTS PASSED - Baseline validated successfully!"
    exit 0
else
    echo "⚠️  $TESTS_FAILED tests failed - Check audit report for known issues"
    exit 1
fi