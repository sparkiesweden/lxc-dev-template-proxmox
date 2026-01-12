#!/bin/bash

# Container Management Script for LXC Development Templates
# Usage: ./manage-containers.sh [action] [options]

set -e

TEMPLATE_ID="9000"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    printf "${1}${2}${NC}\n"
}

# Function to show help
show_help() {
    echo "LXC Development Container Management"
    echo "================================="
    echo ""
    echo "Usage: $0 <action> [options]"
    echo ""
    echo "Actions:"
    echo "  list                          List all development containers"
    echo "  create <name> [vmid]         Create new development container"
    echo "  start <vmid>                  Start container"
    echo "  stop <vmid>                   Stop container"
    echo "  restart <vmid>                Restart container"
    echo "  status <vmid>                 Show container status"
    echo "  console <vmid>                Open container console"
    echo "  ssh <vmid>                    SSH into container"
    echo "  backup <vmid>                 Backup container"
    echo "  delete <vmid>                 Delete container"
    echo "  info <vmid>                  Show detailed container info"
    echo "  update <vmid>                 Update packages in container"
    echo "  resources <vmid>              Show resource usage"
    echo "  help                          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 list                       List all containers"
    echo "  $0 create web-app 1001         Create container 'web-app' with VMID 1001"
    echo "  $0 start 1001                 Start container 1001"
    echo "  $0 ssh 1001                   SSH into container 1001"
    echo "  $0 backup 1001                 Backup container 1001"
}

# Function to list containers
list_containers() {
    print_color $BLUE "Development Containers List"
    echo "=============================="
    echo ""
    printf "%-6s %-20s %-12s %-15s %-10s\n" "VMID" "Hostname" "Status" "IP Address" "Template"
    echo "------------------------------------------------------------------"
    
    while IFS= read -r line; do
        if [[ $line =~ ^[0-9]+ ]]; then
            vmid=$(echo $line | awk '{print $1}')
            status=$(echo $line | awk '{print $2}')
            name=$(echo $line | awk '{print $3}')
            
            # Skip template itself
            if [ "$vmid" = "$TEMPLATE_ID" ]; then
                continue
            fi
            
            # Get IP if container is running
            ip=""
            if [ "$status" = "running" ]; then
                ip=$(pct exec $vmid -- ip addr show eth0 2>/dev/null | grep 'inet ' | awk '{print $2}' | cut -d/ -f1 || echo "")
                # Wait a bit more for IP if not found
                if [ -z "$ip" ]; then
                    sleep 3
                    ip=$(pct exec $vmid -- ip addr show eth0 2>/dev/null | grep 'inet ' | awk '{print $2}' | cut -d/ -f1 || echo "")
                fi
            fi
            
            # Check if from our template
            is_template="no"
            if pct config $vmid 2>/dev/null | grep -q "hostname.*dev-template"; then
                is_template="yes"
            elif [ "$name" != "" ] && [ "$name" != "dev-template" ]; then
                is_template="yes"
            fi
            
            if [ "$is_template" = "yes" ]; then
                printf "%-6s %-20s %-12s %-15s %-10s\n" "$vmid" "$name" "$status" "$ip" "✓"
            fi
        fi
    done <<< "$(pct list)"
    echo ""
}

# Function to create container
create_container() {
    if [ $# -lt 1 ]; then
        print_color $RED "Error: Project name required"
        echo "Usage: $0 create <project-name> [vmid]"
        exit 1
    fi
    
    ./create-dev-container.sh "$1" "$2"
}

# Function to get IP address
get_ip() {
    local vmid=$1
    if [ "$(pct status $vmid | grep status | awk '{print $2}')" = "running" ]; then
        pct exec $vmid -- ip addr show eth0 2>/dev/null | grep 'inet ' | awk '{print $2}' | cut -d/ -f1
    fi
}

# Function to SSH into container
ssh_container() {
    if [ $# -lt 1 ]; then
        print_color $RED "Error: VMID required"
        exit 1
    fi
    
    local vmid=$1
    local ip=$(get_ip $vmid)
    
    if [ -z "$ip" ]; then
        print_color $RED "Container $vmid is not running or has no IP address"
        print_color $YELLOW "Try: $0 start $vmid"
        exit 1
    fi
    
    print_color $GREEN "Connecting to container $vmid ($ip)..."
    ssh developer@$ip
}

# Function to show container info
show_info() {
    if [ $# -lt 1 ]; then
        print_color $RED "Error: VMID required"
        exit 1
    fi
    
    local vmid=$1
    local ip=$(get_ip $vmid)
    
    print_color $BLUE "Container Information"
    echo "====================="
    echo "VMID: $vmid"
    echo "Status: $(pct status $vmid | grep status | awk '{print $2}')"
    echo "Hostname: $(pct config $vmid | grep hostname | cut -d' ' -f2)"
    echo "IP Address: ${ip:-N/A}"
    echo ""
    
    print_color $BLUE "Configuration"
    echo "============"
    pct config $vmid
    echo ""
    
    if [ "$(pct status $vmid | grep status | awk '{print $2}')" = "running" ]; then
        print_color $BLUE "Resource Usage"
        echo "==============="
        pct exec $vmid -- bash -c "echo 'Memory: '; free -h | grep '^Mem:' | awk '{print \$3 \"/\" \$2}'; echo 'Disk: '; df -h / | tail -1 | awk '{print \$3 \"/\" \$2 \" (\" \$5 \" used)\"}'"
        echo ""
        
        print_color $BLUE "Installed Versions"
        echo "=================="
        pct exec $vmid -- su - developer -c "echo 'Node.js: '; node --version; echo 'Docker: '; docker --version; echo 'OpenCode: '; opencode --version" 2>/dev/null || print_color $YELLOW "Developer user tools not accessible"
    fi
}

# Function to backup container
backup_container() {
    if [ $# -lt 1 ]; then
        print_color $RED "Error: VMID required"
        exit 1
    fi
    
    local vmid=$1
    local backup_name="lxc-$vmid-$(date +%Y%m%d-%H%M%S)"
    
    print_color $BLUE "Creating backup of container $vmid..."
    vzdump $vmid --compress zstd --storage local-lvm --mode snapshot --dumpdir /var/lib/vz/dump
    
    if [ $? -eq 0 ]; then
        print_color $GREEN "Backup completed successfully!"
        print_color $YELLOW "Backup location: /var/lib/vz/dump/"
    else
        print_color $RED "Backup failed!"
        exit 1
    fi
}

# Function to update packages in container
update_container() {
    if [ $# -lt 1 ]; then
        print_color $RED "Error: VMID required"
        exit 1
    fi
    
    local vmid=$1
    
    if [ "$(pct status $vmid | grep status | awk '{print $2}')" != "running" ]; then
        print_color $RED "Container $vmid must be running to update packages"
        exit 1
    fi
    
    print_color $BLUE "Updating packages in container $vmid..."
    pct exec $vmid -- bash -c "apt update && apt upgrade -y && apt autoremove -y"
    
    print_color $GREEN "Package update completed!"
    
    # Update Node.js packages
    print_color $BLUE "Updating global Node.js packages..."
    pct exec $vmid -- npm update -g
    
    # Update OpenCode
    print_color $BLUE "Updating OpenCode..."
    pct exec $vmid -- su - developer -c "opencode upgrade" 2>/dev/null || print_color $YELLOW "OpenCode update failed or not configured"
    
    print_color $GREEN "All updates completed!"
}

# Main script logic
case "$1" in
    "list")
        list_containers
        ;;
    "create")
        create_container "$2" "$3"
        ;;
    "start")
        pct start "$2" && print_color $GREEN "Container $2 started"
        ;;
    "stop")
        pct stop "$2" && print_color $GREEN "Container $2 stopped"
        ;;
    "restart")
        pct restart "$2" && print_color $GREEN "Container $2 restarted"
        ;;
    "status")
        if [ -z "$2" ]; then
            list_containers
        else
            pct status "$2"
        fi
        ;;
    "console")
        pct enter "$2"
        ;;
    "ssh")
        ssh_container "$2"
        ;;
    "backup")
        backup_container "$2"
        ;;
    "delete")
        read -p "Are you sure you want to delete container $2? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            pct destroy "$2" && print_color $GREEN "Container $2 deleted"
        fi
        ;;
    "info")
        show_info "$2"
        ;;
    "update")
        update_container "$2"
        ;;
    "resources")
        if [ -z "$2" ]; then
            print_color $RED "Error: VMID required"
            exit 1
        fi
        pct exec "$2" -- bash -c "echo '=== Memory ==='; free -h; echo '=== Disk ==='; df -h; echo '=== CPU ==='; top -bn1 | head -5"
        ;;
    "help"|"--help"|"-h"|"")
        show_help
        ;;
    *)
        print_color $RED "Unknown action: $1"
        echo ""
        show_help
        exit 1
        ;;
esac