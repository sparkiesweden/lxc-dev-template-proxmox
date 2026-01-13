#!/bin/bash

# DevContainer Monitor - Start Web Dashboard
# Mobile-responsive LXC container monitoring interface

set -e

# Configuration
APP_DIR="/opt/lxc-dev-template/web"
PYTHON_APP="$APP_DIR/app.py"
HOST="0.0.0.0"
PORT="8080"
LOG_FILE="/var/log/devcontainer/web-dashboard.log"
PID_FILE="/var/run/devcontainer-dashboard.pid"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_color() {
    printf "${1}${2}${NC}\n"
}

# Help function
show_help() {
    echo "DevContainer Monitor - Start Web Dashboard"
    echo "======================================="
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -d, --debug    Enable debug mode"
    echo "  -p, --port     Set custom port (default: 8080)"
    echo "  -H, --host     Set host address (default: 0.0.0.0)"
    echo "  -f, --force     Force restart if already running"
    echo "  -s, --stop      Stop the dashboard"
    echo ""
    echo "Examples:"
    echo "  $0                          # Start with defaults"
    echo "  $0 -p 9000                 # Start on port 9000"
    echo "  $0 -d                         # Start in debug mode"
    echo "  $0 --stop                     # Stop the dashboard"
    echo ""
    echo "Features:"
    echo "  📱 Mobile-responsive interface"
    echo "  🔄 Real-time container monitoring"
    echo "  🌐 WebSocket connectivity"
    echo "  🎛️ Direct integration with DevContainer agent"
    echo "  📊 Resource usage visualization"
}

# Check if dashboard is already running
check_running() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            echo "Dashboard is already running (PID: $pid)"
            echo "Use '$0 --force' to restart or '$0 --stop' to stop"
            return 0
        else
            echo "Removing stale PID file..."
            rm -f "$PID_FILE"
        fi
    fi
    return 1
}

# Stop the dashboard
stop_dashboard() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        echo "Stopping DevContainer Monitor (PID: $pid)..."
        
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            sleep 2
        else
            echo "Process $pid not found"
        fi
        
        rm -f "$PID_FILE"
        echo "Dashboard stopped."
    else
        echo "Dashboard is not running."
    fi
}

# Check dependencies
check_dependencies() {
    # Check if Python 3 is available
    if ! command -v python3 &> /dev/null; then
        print_color $RED "Error: Python 3 is required but not installed"
        echo "Install with: apt install python3"
        exit 1
    fi
    
    # Check if required Python packages are available
    python3 -c "
import sys
try:
    import flask
    import flask_socketio
except ImportError as e:
    print(f'Missing Python package: {e}')
    sys.exit(1)
" 2>/dev/null || {
        print_color $RED "Error: Missing required Python packages"
        echo "Install with: pip install flask flask-socketio"
        exit 1
    }
    
    # Check if DevContainer manager exists
    if [ ! -f "/opt/lxc-dev-template/subagents/devcontainer-manager.py" ]; then
        print_color $RED "Error: DevContainer manager not found"
        echo "Please ensure the LXC dev template is properly installed"
        exit 1
    fi
}

# Create log directory
setup_logging() {
    mkdir -p "$(dirname "$LOG_FILE")"
    mkdir -p "$(dirname "$PID_FILE")"
    
    # Set up log rotation
    cat > "/etc/logrotate.d/devcontainer-dashboard" << EOF
$LOG_FILE {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
    postrotate
        systemctl reload devcontainer-dashboard >/dev/null 2>&1 || true
}
EOF
}

# Start the dashboard
start_dashboard() {
    local debug_flag=""
    local force_restart=""
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -d|--debug)
                debug_flag="--debug"
                shift
                ;;
            -f|--force)
                force_restart="true"
                shift
                ;;
            -p|--port)
                PORT="$2"
                shift 2
                ;;
            -H|--host)
                HOST="$2"
                shift 2
                ;;
            -s|--stop)
                stop_dashboard
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                echo "Use --help for available options"
                exit 1
                ;;
        esac
    done
    
    # Check if running and not forcing restart
    if [ "$force_restart" != "true" ]; then
        if ! check_running; then
            return 0
        fi
    fi
    
    print_color $BLUE "🚀 Starting DevContainer Monitor Web Dashboard"
    print_color $GREEN "📱 Mobile-Responsive Interface"
    print_color $GREEN "🔄 Real-Time Container Monitoring"
    print_color $GREEN "🌐 WebSocket Connectivity Enabled"
    echo ""
    
    # Setup environment
    setup_logging
    
    # Change to app directory
    cd "$APP_DIR" || {
        print_color $RED "Error: Cannot change to application directory $APP_DIR"
        exit 1
    }
    
    # Start the application
    echo "Starting dashboard on http://$HOST:$PORT"
    echo "Logging to: $LOG_FILE"
    echo "PID file: $PID_FILE"
    echo ""
    
    # Use nohup for background execution
    if [ "$debug_flag" = "--debug" ]; then
        echo "Debug mode enabled"
        python3 "$PYTHON_APP" --host="$HOST" --port="$PORT" --debug \
            2>&1 | tee "$LOG_FILE" &
    else
        nohup python3 "$PYTHON_APP" --host="$HOST" --port="$PORT" \
            >> "$LOG_FILE" 2>&1 &
    fi
    
    local pid=$!
    echo "$pid" > "$PID_FILE"
    
    # Wait a moment and check if it started successfully
    sleep 2
    if kill -0 "$pid" 2>/dev/null; then
        print_color $GREEN "✅ Dashboard started successfully!"
        print_color $BLUE "📱 Access at: http://$HOST:$PORT"
        print_color $BLUE "📱 Mobile-optimized interface"
        print_color $BLUE "🔄 Real-time container monitoring"
        print_color $BLUE "🌐 WebSocket connectivity"
        echo ""
        print_color $YELLOW "💡 Tips:"
        print_color $YELLOW "  • Refresh: Pull down on mobile devices"
        print_color $YELLOW "  • Navigate: Use arrow keys and gestures"
        print_color $YELLOW "  • Fullscreen: Tap container cards"
        echo ""
    else
        print_color $RED "❌ Failed to start dashboard"
        print_color $RED "Check logs: tail -f $LOG_FILE"
        rm -f "$PID_FILE"
        exit 1
    fi
}

# Show status
show_status() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            print_color $GREEN "✅ Dashboard is running (PID: $pid)"
            echo "Access at: http://$HOST:$PORT"
        else
            print_color $RED "❌ Dashboard process not found"
            rm -f "$PID_FILE"
        fi
    else
        print_color $YELLOW "📱 Dashboard is not running"
        echo "Start with: $0"
    fi
}

# Main execution
main() {
    case "${1:-}" in
        -h|--help|"")
            show_help
            ;;
        -s|--stop|"stop")
            stop_dashboard
            ;;
        --status|"status")
            show_status
            ;;
        *)
            check_dependencies
            start_dashboard
            ;;
    esac
}

# Execute main function
main "$@"