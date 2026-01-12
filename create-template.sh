#!/bin/bash

# LXC Development Template Creation Script
# This script recreates the development template from scratch

set -e

# Configuration
TEMPLATE_ID="9000"
TEMPLATE_NAME="dev-template"
CORES="8"
MEMORY="8192"
DISK_SIZE="32"
DEBIAN_TEMPLATE="debian-13-standard_13.1-2_amd64.tar.zst"

echo "🚀 Creating LXC Development Template with OpenCode"
echo "================================================="

# Check if template already exists
if pct list | grep -q "^$TEMPLATE_ID"; then
    echo "⚠️  Template $TEMPLATE_ID already exists!"
    read -p "Do you want to destroy and recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Destroying existing template..."
        pct destroy $TEMPLATE_ID
    else
        echo "❌ Template creation cancelled."
        exit 1
    fi
fi

echo "📦 Creating base container from Debian 13 template..."
pct create $TEMPLATE_ID local:vztmpl/$DEBIAN_TEMPLATE \
    --hostname $TEMPLATE_NAME \
    --cores $CORES \
    --memory $MEMORY \
    --swap 4096 \
    --rootfs local-lvm:$DISK_SIZE \
    --net0 name=eth0,bridge=vmbr0,ip=dhcp \
    --features nesting=1,keyctl=1

echo "🔧 Starting container for package installation..."
pct start $TEMPLATE_ID

echo "⏳ Waiting for container to be ready..."
sleep 10

echo "🔄 Updating system packages..."
pct exec $TEMPLATE_ID -- bash -c "apt update && apt upgrade -y"

echo "🛠️ Installing build essentials and core utilities..."
pct exec $TEMPLATE_ID -- apt install -y \
    build-essential cmake make gcc g++ pkg-config autoconf automake \
    git curl wget unzip zip ca-certificates gnupg lsb-release \
    htop tree ripgrep fd-find vim-tiny

echo "📦 Installing Node.js 20.x LTS..."
pct exec $TEMPLATE_ID -- bash -c "curl -fsSL https://deb.nodesource.com/setup_20.x | bash -"
pct exec $TEMPLATE_ID -- apt install -y nodejs
pct exec $TEMPLATE_ID -- npm install -g yarn pnpm

echo "🐳 Installing Docker Engine..."
pct exec $TEMPLATE_ID -- bash -c "curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh"

echo "🤖 Installing OpenCode CLI..."
pct exec $TEMPLATE_ID -- npm install -g opencode-ai

echo "🐍 Installing additional utilities..."
pct exec $TEMPLATE_ID -- apt install -y zsh python3 python3-pip
pct exec $TEMPLATE_ID -- bash -c "curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && echo 'deb [arch=\$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main' | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && apt update && apt install -y gh"

echo "👤 Creating development user..."
pct exec $TEMPLATE_ID -- useradd -m -s /bin/bash -G sudo,docker developer
pct exec $TEMPLATE_ID -- bash -c "echo 'developer:devpass123' | chpasswd"

echo "🧹 Cleaning up and optimizing container..."
pct exec $TEMPLATE_ID -- bash -c "apt autoremove -y && apt autoclean && apt clean"
pct exec $TEMPLATE_ID -- bash -c "rm -f get-docker.sh && rm -rf /tmp/* && rm -rf /var/tmp/* && echo '' > /etc/machine-id"

echo "⚙️ Configuring environment..."
pct exec $TEMPLATE_ID -- bash -c "echo 'export PATH=\$PATH:/usr/local/bin' >> /etc/bash.bashrc && echo 'export EDITOR=vim' >> /etc/bash.bashrc"

echo "🛑 Stopping container before template conversion..."
pct stop $TEMPLATE_ID

echo "📄 Converting to template..."
pct template $TEMPLATE_ID

echo "✅ Template creation completed successfully!"
echo ""
echo "📋 Template Details:"
echo "   ID: $TEMPLATE_ID"
echo "   Name: $TEMPLATE_NAME"
echo "   Resources: ${CORES} cores, ${MEMORY}MB RAM, ${DISK_SIZE}GB disk"
echo "   Features: nesting=1, keyctl=1"
echo ""
echo "🎯 Usage:"
echo "   pct clone $TEMPLATE_ID <NEW_VMID> --hostname <project-name>"
echo "   pct start <NEW_VMID>"
echo "   pct exec <NEW_VMID> -- ip addr show eth0 | grep 'inet ' | awk '{print \$2}' | cut -d/ -f1"
echo ""
echo "🔐 Default Credentials:"
echo "   User: developer"
echo "   Password: devpass123"
echo "   (Please change password in production!)"
echo ""
echo "🤖 OpenCode Commands:"
echo "   opencode                      # Start TUI"
echo "   opencode run \"command\"        # Run single command"
echo "   opencode auth login           # Configure providers"
echo ""
echo "🐳 Docker is ready to use:"
echo "   docker --version"
echo "   docker compose version"