# LXC Development Template with OpenCode

A comprehensive Proxmox LXC template for development environments with OpenCode AI assistant, Docker, and modern development tools.

## 🚀 Quick Start

### Clone Template
```bash
# Create new development container
pct clone 9000 <NEW_VMID> --hostname <project-name>

# Start container
pct start <NEW_VMID>

# Get IP address
pct exec <NEW_VMID> -- ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1
```

### Access Container
```bash
# Via Proxmox console
pct enter <NEW_VMID>

# Via SSH
ssh developer@<container-ip>
# Password: devpass123

# Switch to developer user
su - developer
```

## 🛠️ What's Included

### Core Development Tools
- **Build Essentials**: gcc, g++, make, cmake, autoconf, automake
- **Version Control**: git
- **Utilities**: curl, wget, unzip, zip, htop, tree, ripgrep, fd-find
- **Editor**: vim-tiny

### Node.js Ecosystem
- **Node.js**: 20.19.6 LTS
- **Package Managers**: npm, yarn, pnpm
- **Ready for**: React, Vue, Angular, Express, etc.

### Docker Platform
- **Docker Engine**: 29.1.4
- **Docker Compose**: v5.0.1
- **Docker Buildx**: For multi-arch builds
- **User Permissions**: Pre-configured

### OpenCode AI Assistant
- **Version**: 1.1.15
- **Global Installation**: Ready to use
- **TUI & CLI**: Terminal-based AI coding assistant

### Additional Tools
- **Python**: 3.13 with pip
- **Shell**: Zsh + Bash
- **GitHub CLI**: gh v2.83.2
- **Development User**: developer with sudo/docker access

## 🎯 Usage Examples

### OpenCode AI Assistant
```bash
# Start TUI interface
opencode

# Run single command
opencode run "Explain this code structure"

# Authenticate with providers
opencode auth login

# List available models
opencode models

# Initialize for project
cd your-project
opencode
# In TUI: /init
```

### Docker Development
```bash
# Check installation
docker --version
docker compose version

# Test with hello-world
docker run hello-world

# Create docker-compose.yml
cat > docker-compose.yml << EOF
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
EOF

# Start services
docker compose up -d
```

### Node.js Projects
```bash
# Create new project
npm create vite@latest my-project
cd my-project

# Install dependencies
npm install

# Start development
npm run dev

# Using alternative package managers
yarn install && yarn dev
pnpm install && pnpm dev
```

### Python Development
```bash
# Check Python version
python3 --version
pip --version

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install fastapi uvicorn
```

### GitHub Integration
```bash
# Authenticate with GitHub
gh auth login

# Clone repository
gh repo clone username/repo

# Create issues, PRs
gh issue create -t "Bug" -b "Description"
gh pr create --title "New Feature"
```

## 📁 Template Specifications

### System Requirements
- **Proxmox VE**: 7.x or later
- **Storage**: LVM recommended
- **Network**: Bridge (vmbr0)
- **Resources**: 8 cores, 8GB RAM, 32GB disk per instance

### Template Details
- **Template ID**: 9000
- **Name**: dev-template
- **Base OS**: Debian 13 (Trixie)
- **Features**: nesting=1, keyctl=1

### User Configuration
- **Developer User**: developer
- **Groups**: sudo, docker
- **Default Password**: devpass123
- **Shell**: /bin/bash
- **Home**: /home/developer

## 🔧 Project Setup Guides

### Web Application
```bash
# React app
npm create vite@latest my-react-app --template react
cd my-react-app
npm install
npm run dev

# Access at http://localhost:3000
```

### Backend API
```bash
# Express.js server
mkdir my-api && cd my-api
npm init -y
npm install express cors

# Create index.js
cat > index.js << EOF
const express = require('express');
const app = express();
app.use(cors());
app.get('/', (req, res) => res.json({message: 'Hello World'}));
app.listen(3000, () => console.log('Server on port 3000'));
EOF

# Start server
npm install -D nodemon
node index.js
```

### Container Project
```bash
# Create Dockerfile
cat > Dockerfile << EOF
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
EOF

# Build and run
docker build -t my-app .
docker run -p 3000:3000 my-app
```

### AI-Powered Development
```bash
# Navigate to your project
cd your-project

# Start OpenCode
opencode

# In OpenCode TUI:
# /init - Initialize project understanding
# Ask: "Create a REST API with Express.js"
# Ask: "Review my code and suggest improvements"
# Ask: "Add authentication to this app"
```

## 🔒 Security

### Password Management
```bash
# Change default password
passwd developer

# Or as root:
passwd developer
```

### SSH Keys
```bash
# Add SSH keys for passwordless access
mkdir -p ~/.ssh
echo "your-public-key" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### Container Security
- Unprivileged LXC mode
- Non-root development user
- Docker permissions limited to developer user
- Firewall can be configured per container

## 🛠️ Container Management

### Daily Operations
```bash
# List containers
pct list

# Start/Stop/Restart
pct start <VMID>
pct stop <VMID>
pct restart <VMID>

# Check status
pct status <VMID>

# View console
pct enter <VMID>
```

### Resource Management
```bash
# Edit container resources
pct set <VMID> --cores 4 --memory 4096

# Add network interface
pct set <VMID> --net1 name=eth1,bridge=vmbr0

# Mount volume from host
pct set <VMID> --mp0 /path/on/host,mp=/path/in/container
```

### Backup & Recovery
```bash
# Create backup
vzdump <VMID> --compress zstd --storage local-lvm

# Restore from backup
qmrestore <backup-file> <NEW_VMID>

# Snapshot before changes
pct snapshot <VMID> before-update
pct rollback <VMID> before-update
```

## 🚀 Advanced Usage

### Multiple Development Environments
```bash
# Web development container
pct clone 9000 1001 --hostname web-dev

# API development container  
pct clone 9000 1002 --hostname api-dev

# ML/AI development container
pct clone 9000 1003 --hostname ml-dev
```

### Customization
```bash
# Install additional packages
pct exec <VMID> -- apt install -y <package>

# Add users
pct exec <VMID> -- useradd -m -s /bin/bash <username>

# Configure services
pct exec <VMID> -- systemctl enable <service>
```

### Performance Optimization
```bash
# Adjust container resources for workload
pct set <VMID> --cores 8 --memory 8192 --swap 4096

# Enable CPU limits
pct set <VMID> --cpuunits 1024 --cpulimit 4

# Configure I/O limits
pct set <VMID> --iops 1000
```

## 🐛 Troubleshooting

### Common Issues

#### Docker Permission Denied
```bash
# Add user to docker group
usermod -aG docker developer

# Restart container or relogin
su - developer
```

#### Network Issues
```bash
# Check network interface
pct exec <VMID> -- ip addr show

# Restart networking
pct exec <VMID> -- systemctl restart networking

# Check DNS
pct exec <VMID> -- nslookup google.com
```

#### OpenCode Issues
```bash
# Reinstall OpenCode
npm install -g opencode-ai

# Check installation
which opencode
opencode --version

# Check authentication
opencode auth list
```

#### Performance Issues
```bash
# Check resource usage
pct exec <VMID> -- htop
pct exec <VMID> -- df -h
pct exec <VMID> -- free -h

# Clear package cache
pct exec <VMID> -- apt autoremove -y && apt autoclean
```

### Getting Help
- OpenCode: `opencode --help`
- Container: `pct --help`
- System: Check `/var/log/syslog`
- Docker: `docker logs <container>`

## 📚 Additional Resources

### Documentation
- [OpenCode Documentation](https://opencode.ai/docs/)
- [Proxmox VE Documentation](https://pve.proxmox.com/pve-docs/)
- [Docker Documentation](https://docs.docker.com/)

### Community
- [OpenCode Discord](https://opencode.ai/discord/)
- [Proxmox Forums](https://forum.proxmox.com/)
- [GitHub Issues](https://github.com/anomalyco/opencode/issues)

## 🔄 Updates

### Updating OpenCode
```bash
# Update OpenCode to latest version
opencode upgrade

# Or via npm
npm update -g opencode-ai
```

### Updating System
```bash
# Update system packages
apt update && apt upgrade -y

# Update Node.js packages
npm update -g

# Clean up
apt autoremove -y
```

---

## 📄 License

This template is provided as-is for development purposes. Please ensure compliance with all software licenses and terms of service for included tools.

## 🤝 Contributing

Feel free to modify and adapt this template for your specific development needs. Contributions and suggestions are welcome!