#!/bin/bash

# ACTIONS

action_run_tests_and_linting=tests
action_run_ptw=ptw

# MESSAGES

msg_no_params=$"Usage:

    ./go.sh <command>

    ptw     Launch PyTest Watch
    tests   Run Tests and Linting (flake8)
"

announce_action_docker_image_tests=$"Run app tests and linting..."
announce_action_run_ptw=$"Run PyTest Watch..."

# PARAMETERS PROCESSING

if [[ $1 == $action_run_tests_and_linting ]]; then

    echo "$announce_action_docker_image_tests"
    echo "Starting linting check..."
    eval "python3 -m flake8 ."
    echo "Starting unittests..."
    eval "python3 -m unittest discover -p test_*.py"

elif [[ $1 == $action_run_ptw ]]; then

    echo "$announce_action_run_ptw"
    eval "ptw $2 $3"

else
    echo "$msg_no_params"
fi
