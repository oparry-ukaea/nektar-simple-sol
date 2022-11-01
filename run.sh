#!/bin/env bash

# Defaults - run in debug and output to a subdirectory tagged with the current date and time
MODE="RELEASE"
TEMPLATE_SUBDIR="2DSOL"
# Parse command line args
for arg in $*; do
    case "$arg" in
        mode=*)
            MODE=${arg:5};;
        subdir=*)
            RUN_SUBDIR=${arg:7};;
        template=*)
            TEMPLATE_SUBDIR=${arg:9};;
        *)
            echo "Unrecognised argument: $arg"
            echo "Usage:"
            echo " $0 <mode=mode_str> <subdir=label> <template=template_name>"
            echo "    mode_str      : 'DEBUG' or 'RELEASE' (default='RELEASE'; case insensitive)"
            echo "    label         : name of the subdirectory in ./runs/ in which to execute solver (default is <template_name>)"
            echo "    template_name : name of a subdirectory in runs/templates on which to base this run"
            exit 1
    esac
done
if [ -z "$RUN_SUBDIR" ]; then 
    RUN_SUBDIR="$TEMPLATE_SUBDIR"
fi
# Set mode-dependent options
case "${MODE^^}" in
    DEBUG)
        BUILD_SUBDIR="buildDebug";;
    RELEASE)
        BUILD_SUBDIR="build";;
    *)
        echo "'$MODE' is not a valid mode, choose 'DEBUG' or 'RELEASE' (case insensitive)"
        exit 2;;
esac

REPO_ROOT=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
BIN_DIR="$REPO_ROOT/$BUILD_SUBDIR/dist"
RUNS_DIR="$REPO_ROOT/runs"
RUN_TEMPLATE="$RUNS_DIR/templates/$TEMPLATE_SUBDIR"

# Check template exists
if [ ! -d "$RUN_TEMPLATE" ]; then
    echo "No run template at $RUN_TEMPLATE"
    exit 3
fi

# Set run directory and confirm overwrite if it exists
run_dir="$RUNS_DIR/$RUN_SUBDIR"
if [ -e "$run_dir" ]; then
    read -p "Overwrite existing run directory at $run_dir? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1
    \rm -rf "$run_dir"
fi

# Copy template
cp -r "$RUN_TEMPLATE" "$run_dir"

# Set command line from file
cmd_line_file="$run_dir/cmd_line.txt"
if [ -f "$cmd_line_file" ]; then
    cmd_line=$(sed -e 's|<BIN_DIR>|'"$BIN_DIR"'|g' < "$cmd_line_file")
    \rm "$cmd_line_file"
else
    echo "Can't read run command for template; no file found at $cmd_line_file."
    exit 5
fi

# cd to run directory and run cmd_line
cd "$run_dir" 
eval "$cmd_line"
cd -