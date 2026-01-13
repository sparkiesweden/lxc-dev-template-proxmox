#!/bin/bash

# DevContainer Creation Script
# Quick wrapper for the devcontainer-manager.py subagent

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_AGENT="$SCRIPT_DIR/devcontainer-manager.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_color() {
    printf "${1}${2}${NC}\n"
}

show_help() {
    echo "DevContainer Manager - LXC Development Container Creator"
    echo "================================================="
    echo ""
    echo "Quick Commands:"
    echo "  $0 <project_name>                    Create container with default template"
    echo "  $0 <project_name> <vmid>           Create with specific VMID"
    echo "  $0 <project_name> <vmid> <type>    Create with project template"
    echo ""
    echo "Project Templates:"
    echo "  web         - React, Vue, Angular development"
    echo "  api         - Backend API and microservices"
    echo "  ml          - Machine learning and data science"
    echo "  devops      - DevOps and infrastructure tools"
    echo ""
    echo "Examples:"
    echo "  $0 my-web-app 1001 web           # Web dev container with VMID 1001"
    echo "  $0 my-api-project                    # API container with auto-VMID"
    echo "  $0 ml-project 1003 ml               # ML container with VMID 1003"
    echo ""
    echo "Management Commands:"
    echo "  $0 list <vmid>                      List containers"
    echo "  $0 info <vmid>                      Container information"
    echo "  $0 monitor <vmid>                   Resource monitoring"
    echo "  $0 backup <vmid>                    Create backup"
    echo "  $0 configure-opencode <vmid>         Setup OpenCode"
    echo ""
    echo "Full Agent Mode:"
    echo "  $0 agent <command> [options]         Access full agent capabilities"
    echo ""
    echo "Templates Created:"
    echo "  - Complete development environment"
    echo "  - OpenCode AI assistant configured"
    echo "  - Docker and development tools ready"
    echo "  - Project-specific packages installed"
    echo "  - Network ports configured"
    echo "  - SSH access enabled"
}

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    print_color $RED "Error: python3 is required but not installed"
    exit 1
fi

# Check if agent file exists
if [ ! -f "$PYTHON_AGENT" ]; then
    print_color $RED "Error: DevContainer agent not found at $PYTHON_AGENT"
    exit 1
fi

# Parse arguments
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

COMMAND="$1"
shift

case "$COMMAND" in
    "list"|"ls")
        python3 "$PYTHON_AGENT" list
        ;;
    "create"|"new")
        if [ $# -eq 0 ]; then
            print_color $RED "Error: Project name required"
            echo "Usage: $0 create <project_name> [vmid] [template_type]"
            exit 1
        fi
        PROJECT_NAME="$1"
        VMID="${2:-}"
        TEMPLATE_TYPE="${3:-default}"
        
        print_color $BLUE "Creating development container..."
        python3 "$PYTHON_AGENT" create "$PROJECT_NAME" "$VMID" "$TEMPLATE_TYPE"
        ;;
    "info"|"details")
        if [ $# -eq 0 ]; then
            print_color $RED "Error: VMID required"
            echo "Usage: $0 info <vmid>"
            exit 1
        fi
        python3 "$PYTHON_AGENT" info "$1"
        ;;
    "monitor"|"stats")
        if [ $# -eq 0 ]; then
            print_color $RED "Error: VMID required"
            echo "Usage: $0 monitor <vmid>"
            exit 1
        fi
        python3 "$PYTHON_AGENT" monitor "$1"
        ;;
    "backup"|"save")
        if [ $# -eq 0 ]; then
            print_color $RED "Error: VMID required"
            echo "Usage: $0 backup <vmid>"
            exit 1
        fi
        python3 "$PYTHON_AGENT" backup "$1"
        ;;
    "configure-opencode"|"opencode")
        if [ $# -eq 0 ]; then
            print_color $RED "Error: VMID required"
            echo "Usage: $0 configure-opencode <vmid> [providers]"
            exit 1
        fi
        PROVIDERS="${2:-anthropic}"
        python3 "$PYTHON_AGENT" configure-opencode "$1" "$PROVIDERS"
        ;;
    "agent"|"full")
        if [ $# -eq 0 ]; then
            print_color $RED "Error: Command required for agent mode"
            echo "Available agent commands: list, create, info, monitor, backup, configure-opencode, setup-template"
            exit 1
        fi
        python3 "$PYTHON_AGENT" "$@"
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    *)
        # Default behavior: create container
        PROJECT_NAME="$COMMAND"
        VMID="${1:-}"
        TEMPLATE_TYPE="${2:-default}"
        
        if [ -z "$PROJECT_NAME" ]; then
            print_color $RED "Error: Project name required"
            show_help
            exit 1
        fi
        
        print_color $BLUE "Creating development container '$PROJECT_NAME'..."
        RESULT=$(python3 "$PYTHON_AGENT" create "$PROJECT_NAME" "$VMID" "$TEMPLATE_TYPE")
        
        if echo "$RESULT" | grep -q '"success": true'; then
            VMID=$(echo "$RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('vmid', 'unknown'))")
            IP=$(echo "$RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('ip', 'pending'))")
            
            print_color $GREEN "✅ Container created successfully!"
            echo ""
            print_color $BLUE "Container Details:"
            echo "   VMID: $VMID"
            echo "   Project: $PROJECT_NAME"
            echo "   IP: $IP"
            echo ""
            print_color $BLUE "Access Methods:"
            echo "   Console: pct enter $VMID"
            echo "   SSH: ssh developer@$IP"
            echo ""
            print_color $BLUE "Next Steps:"
            echo "   1. Configure OpenCode: $0 configure-opencode $VMID"
            echo "   2. Start developing: pct enter $VMID"
            echo "   3. Use OpenCode: su - developer -c 'opencode'"
            
            # Offer to setup OpenCode
            read -p "Do you want to configure OpenCode now? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                print_color $BLUE "Configuring OpenCode..."
                python3 "$PYTHON_AGENT" configure-opencode "$VMID" "anthropic"
                if [ $? -eq 0 ]; then
                    print_color $GREEN "✅ OpenCode configured successfully!"
                else
                    print_color $YELLOW "⚠️  OpenCode configuration may need manual setup"
                fi
            fi
        else
            print_color $RED "❌ Container creation failed"
            echo "$RESULT"
            exit 1
        fi
        ;;
esac