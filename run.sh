#!/bin/bash

# Function to run linting
lint() {
    echo "Running linting..."
    pre-commit run --all-files
    echo "Linting done! ✨ 🍰 ✨"
}

# Function to start the Django application
start() {
    echo "Starting Django Server 🚀"
    python manage.py runserver
}

help() {
    printf "%s <task> [args]\n\nTasks:\n" "${0}"
    compgen -A function | grep -v "^_" | cat -n
}


"${@:-help}"
