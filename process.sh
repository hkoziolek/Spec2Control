#!/bin/bash
# Spec2Control CLI Wrapper Script
# Runs the CLI tool from the root directory with argument passthrough

cd "$(dirname "$0")/src"
python spec2control_cli.py "$@"
