#!/bin/sh

if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

if [ -z "$BLENDER" ]; then
    echo "Please set the Blender path in the .env file"
    exit 1
fi

echo "Blender path: $BLENDER"


build() {
    "$BLENDER" --command extension build --source-dir ./src --output-dir ./
}

build_dev() {
    "$BLENDER" --command extension build --source-dir ./src --output-filepath ./modifier_stack_manager.zip
    "$BLENDER" --command extension install-file -r user_default ./modifier_stack_manager.zip
}


case "$1" in
    b)
        build
        ;;
    bd)
        build_dev
        ;;
    *)
esac