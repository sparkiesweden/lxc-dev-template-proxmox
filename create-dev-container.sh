#!/bin/bash

# Create Development Container from Template Script
# Usage: ./create-dev-container.sh <project-name> [vmid]

set -e

TEMPLATE_ID="9000"

# Check arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <project-name> [vmid]"
    echo "Example: $0 my-web-project 1001"
    exit 1
fi

PROJECT_NAME="$1"
VMID="${2:-}"

# Generate VMID if not provided
if [ -z "$VMID" ]; then
    # Find next available VMID starting from 1001
    for i in {1001..9999}; do
        if ! pct list | grep -q "^$i"; then
            VMID="$i"
            break
        fi
    done
fi

# Check if VMID is already in use
if pct list | grep -q "^$VMID"; then
    echo "❌ VMID $VMID is already in use!"
    echo "Please choose a different VMID or specify one manually."
    exit 1
fi

echo "🚀 Creating Development Container"
echo "================================="
echo "Project Name: $PROJECT_NAME"
echo "VMID: $VMID"
echo "Template: $TEMPLATE_ID"
echo ""

# Clone template
echo "📦 Cloning template $TEMPLATE_ID to container $VMID..."
pct clone $TEMPLATE_ID $VMID --hostname "$PROJECT_NAME"

# Start container
echo "🔧 Starting container..."
pct start $VMID

# Wait for container to be ready
echo "⏳ Waiting for container to be ready..."
sleep 10

# Get IP address
echo "🌐 Getting network configuration..."
sleep 5
IP=$(pct exec $VMID -- ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)

if [ -z "$IP" ]; then
    echo "⚠️  Could not get IP address automatically"
    echo "You can get it manually with:"
    echo "pct exec $VMID -- ip addr show eth0"
else
    echo "✅ Container created successfully!"
    echo ""
    echo "📋 Container Details:"
    echo "   VMID: $VMID"
    echo "   Hostname: $PROJECT_NAME"
    echo "   IP Address: $IP"
    echo ""
    echo "🔑 Access Methods:"
    echo "   Console: pct enter $VMID"
    echo "   SSH: ssh developer@$IP"
    echo "   Password: devpass123"
    echo ""
    echo "🤖 OpenCode Setup:"
    echo "   pct exec $VMID -- su - developer -c 'opencode auth login'"
    echo "   pct exec $VMID -- su - developer -c 'opencode'"
    echo ""
    echo "🐳 Docker is ready:"
    echo "   pct exec $VMID -- su - developer -c 'docker --version'"
    echo ""
    echo "📝 Quick Commands:"
    echo "   Switch to developer: su - developer"
    echo "   Check tools: node --version, docker --version, opencode --version"
    echo "   Start dev: npm create vite@latest"
fi

# Optional: Open SSH connection
read -p "Do you want to SSH into the container now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]] && [ ! -z "$IP" ]; then
    echo "🔗 Connecting to container..."
    ssh developer@$IP
fi

echo ""
echo "🎉 Done! Your development container '$PROJECT_NAME' is ready to use."