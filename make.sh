#!/bin/env bash

# Default settings
N_JOBS="8"

# Parse command line args
for arg in $*; do
    case "$arg" in
        mode=*)
            MODE=${arg:5};;
        nekbuild=*)
            NEK_BUILD=${arg:9}
            ;;
        *)
            echo "Unrecognised argument: $arg"
            echo "usage:"
            echo " $0 <mode=DEBUG|RELEASE>  (default is RELEASE) |<nekbuild=PATH_TO_NEKTAR_BUILD_DIR>"
            exit 1
    esac
done
if [ -n "$NEK_BUILD" ]; then
    if [ -n "$MODE" ] && [ "${MODE^^}" != "CUSTOM" ]; then
        echo "WARNING: 'nekbuild' arg was passed, so 'mode' arg will be ignored"
    fi
    MODE="CUSTOM"
fi
if [ -z "$MODE" ]; then
    MODE="RELEASE"
fi


# Set mode-dependent options
BUILD_DIR="build"
case "${MODE^^}" in
    CUSTOM)
        BUILD_DIR+="Custom"
        ;;
    DEBUG)
        BUILD_DIR+="Debug"
        NEK_BUILD="$NEKDEBUGBUILD_FOR_SOLVERS";;
    RELEASE)
        NEK_BUILD="$NEKBUILD_FOR_SOLVERS";;
    *)
        echo "'$MODE' is not a valid mode, choose 'DEBUG' or 'RELEASE' (case insensitive)"
        exit 2;;
esac
BUILD_TYPE=${MODE,,}
BUILD_TYPE=${BUILD_TYPE^}

# Look for Nektar library CMake config
echo "Looking for Nektar library in [$NEK_BUILD]"
NEK_CMAKE_CONFIG="$NEK_BUILD/Nektar++Config.cmake"
if [ -f "$NEK_CMAKE_CONFIG" ]; then
    echo "Found Nektar CMake config at $NEK_CMAKE_CONFIG"
else
    echo "No CMake config at $NEK_CMAKE_CONFIG (might need to 'make install' Nektar?)"
    exit 3
fi

# Create build directory, run CMake and compile
echo "Building in '$BUILD_DIR'"
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"
cmake -DNektar++_DIR=$NEK_BUILD -DCMAKE_BUILD_TYPE="$BUILD_TYPE" ..
make -j $N_JOBS install
cd -