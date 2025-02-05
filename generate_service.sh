#!/bin/bash
set -e
LOG_FILE="service.log"

function print_success { printf "\033[32m✔️  %s\033[0m\n" "$1"; }
function print_warning { printf "\033[33m⚠️  %s\033[0m\n" "$1"; }
function print_error { printf "\033[31m❌  %s\033[0m\n" "$1"; }
function log { echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"; }

service() {
    local service_name="Feather_API_Backend"
    local service_file="/etc/systemd/system/${service_name}.service"
    local current_user
    local script_directory
    local project_root

    current_user=$(whoami)
    script_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    project_root="$(cd "$script_directory/.." && pwd)"

    if [ -f "$service_file" ]; then
        print_warning "Existing service file found. Replacing..."
        sudo rm -f "$service_file"
    fi

    cat << EOF | sudo tee "$service_file" > /dev/null
[Unit]
Description=${service_name}
After=network.target

[Service]
User=${current_user}
ExecStart=${script_directory}/gunicorn --workers 1 --bind 127.0.0.1:1234 endpoint:backend
WorkingDirectory=${project_root}
Restart=always
RestartSec=5
TasksMax=10000

[Install]
WantedBy=multi-user.target
EOF

    print_warning "Starting the service..."
    if sudo systemctl daemon-reload && sudo systemctl enable "${service_name}.service" && sudo systemctl start "${service_name}.service" | tee -a "$LOG_FILE" 2>&1; then
        sleep 10
        if sudo systemctl is-active --quiet "${service_name}.service"; then
            print_success "Service is active."
        else
            print_error "The service is not running. Please check the logs."
        fi
    else
        print_error "Oops! Something went wrong while starting the service. Check '$LOG_FILE' for details."
    fi
}
