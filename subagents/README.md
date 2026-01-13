# DevContainer Manager Subagent

A specialized subagent for managing LXC development containers with OpenCode integration.

## Overview

The DevContainer Manager is designed to handle all aspects of LXC development container lifecycle, from creation to monitoring and backup. It integrates seamlessly with OpenCode for AI-powered development assistance.

## Features

### 🛠️ Container Management
- **Create containers** from development templates
- **List containers** with status and IP information  
- **Monitor resources** (CPU, memory, disk usage)
- **Container information** and configuration display
- **Backup operations** for data safety

### 🎯 Project Templates
- **Web Development**: React, Vue, Angular with modern tooling
- **Backend API**: Express, microservices with database support
- **Machine Learning**: Python, Jupyter, ML libraries
- **DevOps**: Terraform, Ansible, Kubernetes tools

### 🤖 OpenCode Integration
- **Automatic configuration** with multiple providers
- **Model selection** and management
- **Workspace setup** for AI-assisted development
- **Session management** and sharing

### 📊 Monitoring & Analytics
- **Real-time resource monitoring**
- **Performance alerts** and thresholds
- **Historical data** collection
- **Health checks** and diagnostics

## Installation

### Prerequisites
- Proxmox VE with LXC support
- Python 3.8+ in host system
- Access to `pct` and `vzdump` commands
- Development template (VMID 9000) created

### Setup
```bash
# Make the agent executable
chmod +x /opt/lxc-dev-template/subagents/devcontainer-manager.py

# Add to PATH (optional)
echo 'export PATH=$PATH:/opt/lxc-dev-template/subagents' >> ~/.bashrc

# Test installation
python3 /opt/lxc-dev-template/subagents/devcontainer-manager.py list
```

## Usage

### Basic Operations

#### List All Containers
```bash
python3 devcontainer-manager.py list
```

#### Create New Container
```bash
# Basic container
python3 devcontainer-manager.py create my-project

# With specific VMID and template
python3 devcontainer-manager.py create web-app 1001 web

# API project with automatic VMID
python3 devcontainer-manager.py create my-api "" api
```

#### Get Container Information
```bash
python3 devcontainer-manager.py info 1001
```

#### Monitor Resources
```bash
python3 devcontainer-manager.py monitor 1001
```

#### Create Backup
```bash
python3 devcontainer-manager.py backup 1001
```

### OpenCode Configuration

#### Configure with Providers
```bash
# Configure Anthropic and OpenAI
python3 devcontainer-manager.py configure-opencode 1001 anthropic,openai

# Just Anthropic
python3 devcontainer-manager.py configure-opencode 1001 anthropic
```

#### Quick OpenCode Setup
```bash
# Create container and configure OpenCode
python3 devcontainer-manager.py create ai-project 1001
python3 devcontainer-manager.py configure-opencode 1001 anthropic
```

### Project Templates

#### Web Development Template
```bash
# Create web development container
python3 devcontainer-manager.py create react-app 1001 web
python3 devcontainer-manager.py setup-template 1001 web

# This installs:
# - Chromium for testing
# - Postman CLI for API testing  
# - Port forwards: 3000, 5173, 4173
# - NPM packages: postman-cli
```

#### API Development Template
```bash
# Create API development container
python3 devcontainer-manager.py create my-api 1002 api
python3 devcontainer-manager.py setup-template 1002 api

# This installs:
# - Database clients (PostgreSQL, Redis)
# - Development tools (Nodemon, TypeScript)
# - Port forwards: 3000, 8080, 9229
# - Ready for microservices development
```

#### Machine Learning Template
```bash
# Create ML development container  
python3 devcontainer-manager.py create ml-project 1003 ml
python3 devcontainer-manager.py setup-template 1003 ml

# This installs:
# - PyTorch and ML libraries
# - Jupyter Lab
# - Data science packages
# - Port forward: 8888 (Jupyter)
```

#### DevOps Template
```bash
# Create DevOps container
python3 devcontainer-manager.py create infra-project 1004 devops
python3 devcontainer-manager.py setup-template 1004 devops

# This installs:
# - Terraform for IaC
# - Ansible for automation
# - kubectl for Kubernetes
# - Container registry tools
```

## API Reference

### Methods

#### `list()`
Lists all development containers with their status and network information.

**Returns:**
```json
{
  "containers": [
    {
      "vmid": "1001",
      "name": "web-project",
      "status": "running", 
      "ip": "192.168.1.100"
    }
  ]
}
```

#### `create(project_name, vmid?, template_type?)`
Creates a new development container from the base template.

**Parameters:**
- `project_name` (string, required): Project/container name
- `vmid` (string, optional): Specific VMID to use
- `template_type` (string, optional): Project template type

**Returns:**
```json
{
  "success": true,
  "vmid": "1001",
  "project_name": "web-project",
  "ip": "192.168.1.100",
  "access_methods": [
    "pct enter 1001",
    "ssh developer@192.168.1.100"
  ]
}
```

#### `info(vmid)`
Gets detailed information about a specific container.

**Parameters:**
- `vmid` (string, required): Container VMID

**Returns:**
```json
{
  "vmid": "1001",
  "status": "running",
  "ip": "192.168.1.100",
  "config": "Configuration details...",
  "resources": {
    "memory": "2.1Gi/8.0Gi",
    "disk": "5.2G/32G (16% used)"
  }
}
```

#### `configure_opencode(vmid, providers?)`
Configures OpenCode with specified providers.

**Parameters:**
- `vmid` (string, required): Container VMID  
- `providers` (array, optional): List of providers to configure

**Returns:**
```json
{
  "success": true,
  "version": "1.1.15",
  "error": null
}
```

#### `setup_template(vmid, template_type)`
Applies a project-specific template to the container.

**Parameters:**
- `vmid` (string, required): Container VMID
- `template_type` (string, required): Template type (web, api, ml, devops)

**Returns:**
```json
{
  "success": true,
  "template": "web",
  "installed": {
    "packages": ["chromium", "lighttpd"],
    "npm_packages": ["postman-cli"],
    "ports": [3000, 5173, 4173]
  }
}
```

#### `monitor(vmid)`
Gets real-time resource usage for the container.

**Parameters:**
- `vmid` (string, required): Container VMID

**Returns:**
```json
{
  "status": "running",
  "cpu_usage": "CPU usage details...",
  "memory_info": "Memory usage details...",
  "disk_info": "Disk usage details..."
}
```

#### `backup(vmid)`
Creates a backup snapshot of the container.

**Parameters:**
- `vmid` (string, required): Container VMID

**Returns:**
```json
{
  "success": true,
  "backup_name": "lxc-1001-20240113-143022",
  "location": "/var/lib/vz/dump/",
  "error": null
}
```

## Workflows

### Quick Web Project Setup
```bash
# Complete web development environment in 3 commands
python3 devcontainer-manager.py create my-react-app 1001 web
python3 devcontainer-manager.py setup-template 1001 web  
python3 devcontainer-manager.py configure-opencode 1001 anthropic

# Now you have:
# - Running container with web development tools
# - IP address for access
# - OpenCode configured and ready
# - Development ports forwarded
```

### API Development with Database
```bash
# Setup API development environment
python3 devcontainer-manager.py create my-api 1002 api
python3 devcontainer-manager.py setup-template 1002 api

# Start database services
pct exec 1002 -- su - developer -c "docker compose up -d postgres redis"

# Configure OpenCode for API assistance
python3 devcontainer-manager.py configure-opencode 1002 anthropic,openai
```

### Machine Learning Environment
```bash
# Setup ML development with Jupyter
python3 devcontainer-manager.py create ml-project 1003 ml
python3 devcontainer-manager.py setup-template 1003 ml

# Access Jupyter Lab
# http://<container-ip>:8888

# Start development with OpenCode
python3 devcontainer-manager.py configure-opencode 1003 anthropic
```

## Configuration

### Environment Variables
```bash
# Template configuration
export DEV_TEMPLATE_ID="9000"
export DEV_BASE_DIR="/opt/lxc-dev-template"

# Default settings
export DEFAULT_CORES="4"
export DEFAULT_MEMORY="4096"
export DEFAULT_DISK="16"

# OpenCode settings
export OPENCODE_DEFAULT_PROVIDERS="anthropic,openai"
export OPENCODE_DEFAULT_MODEL="anthropic/claude-3-5-sonnet-20241022"
```

### Agent Configuration
Edit `devcontainer-agent.json` to customize:
- Available project templates
- Default packages and versions
- Resource monitoring thresholds
- Backup settings
- Provider configurations

## Monitoring

### Resource Alerts
The agent monitors resources and can trigger alerts:
- **Memory usage > 80%**
- **CPU usage > 90%**  
- **Disk usage > 85%**
- **Container downtime**

### Logging
```bash
# Monitor agent logs
tail -f /var/log/devcontainer-agent.log

# Check specific container logs
pct exec 1001 -- journalctl -u devcontainer-agent -f
```

## Integration

### OpenCode Integration
```bash
# Start OpenCode with agent context
pct exec 1001 -- su - developer -c "opencode --context devcontainer"

# Use agent for project setup
pct exec 1001 -- su - developer -c 'opencode run "Setup a React project with TypeScript and Tailwind"'
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Setup Dev Container
  run: |
    python3 /opt/lxc-dev-template/subagents/devcontainer-manager.py create ${{ env.PROJECT_NAME }}
    python3 /opt/lxc-dev-template/subagents/devcontainer-manager.py configure-opencode ${{ env.VMID }} anthropic
```

### Docker Integration
```bash
# Container uses Docker for services
python3 devcontainer-manager.py setup-template 1001 web

# Docker Compose file created
pct exec 1001 -- su - developer -c "docker compose up -d"

# Monitor Docker services
pct exec 1001 -- su - developer -c "docker ps"
```

## Troubleshooting

### Common Issues

#### Container Creation Fails
```bash
# Check template exists
pct list | grep 9000

# Verify storage space
df -h /var/lib/vz

# Check permissions
ls -la /opt/lxc-dev-template/
```

#### OpenCode Configuration Fails
```bash
# Verify OpenCode installation
pct exec 1001 -- su - developer -c "opencode --version"

# Check authentication
pct exec 1001 -- su - developer -c "opencode auth list"

# Reset OpenCode config
pct exec 1001 -- su - developer -c "rm -rf ~/.local/share/opencode"
```

#### Resource Monitoring Issues
```bash
# Check container status
pct status 1001

# Verify commands work
pct exec 1001 -- free -h
pct exec 1001 -- df -h
pct exec 1001 -- top -bn1
```

### Debug Mode
```bash
# Enable debug logging
export DEBUG=true
python3 devcontainer-manager.py list 2>&1 | tee debug.log
```

### Performance Optimization
```bash
# Optimize for SSD storage
export IO_SCHEDULE="noop"

# Optimize memory usage
export SWAPPINESS="10"

# Network optimization
export TCP_CONGESTION_CONTROL="bbr"
```

## Development

### Extending the Agent
```python
# Add custom project template
def setup_custom_template(self, vmid: str) -> Dict:
    # Custom setup logic
    return {'success': True, 'template': 'custom'}

# Add new monitoring metrics
def advanced_monitoring(self, vmid: str) -> Dict:
    # Advanced monitoring logic
    return {'custom_metrics': 'data'}
```

### Testing
```bash
# Run tests
python3 -m pytest tests/

# Integration tests
python3 tests/integration.py

# Performance benchmarks
python3 tests/benchmarks.py
```

## Security

### Container Security
- Non-root development user
- SSH key authentication support
- Docker permissions limited to developer user
- Network isolation between containers

### Agent Security
- Minimal privilege requirements
- Audit logging of all operations
- Input validation and sanitization
- Secure credential handling

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes and add tests
4. Submit pull request
5. Follow code review process