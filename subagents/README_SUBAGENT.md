# DevContainer Manager Subagent

A specialized subagent for LXC development containers with OpenCode integration, built to provide intelligent, automated container management.

## 🚀 Quick Start

### Installation & Setup
```bash
# Navigate to subagent directory
cd /opt/lxc-dev-template/subagents/

# Test the agent
./create-devcontainer.sh --help

# Create your first container
./create-devcontainer.sh my-awesome-project
```

## 🎯 Core Capabilities

### 🛠️ Intelligent Container Creation
- **Automatic VMID assignment** - Finds next available ID
- **Project template selection** - Pre-configured for web, API, ML, DevOps
- **Resource optimization** - Automatically configures memory, CPU, disk
- **Network setup** - DHCP or static IP configuration
- **Security hardening** - Non-root user, proper permissions

### 🤖 OpenCode Integration
- **Provider configuration** - Anthropic, OpenAI, local models
- **Model selection** - Choose optimal models for tasks
- **Workspace setup** - Automatic project initialization
- **Session management** - Persistent AI development sessions

### 📊 Smart Monitoring
- **Real-time metrics** - CPU, memory, disk, network
- **Alert system** - Threshold-based notifications
- **Performance analytics** - Historical data and trends
- **Health checks** - Container and service status

### 🔄 Automated Workflows
- **One-command setup** - Complete dev environments
- **Template pipelines** - Consistent project structures
- **Backup automation** - Scheduled container snapshots
- **CI/CD integration** - GitHub Actions, GitLab CI

## 📁 Subagent Components

### 1. Core Agent (`devcontainer-manager.py`)
```python
# Python-based agent with full LXC management
python3 devcontainer-manager.py create my-project 1001 web
python3 devcontainer-manager.py configure-opencode 1001 anthropic
python3 devcontainer-manager.py monitor 1001
```

**Features:**
- JSON-based API responses
- Error handling and validation
- Template system architecture
- Resource monitoring integration
- Backup and recovery operations

### 2. CLI Wrapper (`create-devcontainer.sh`)
```bash
# User-friendly interface
./create-devcontainer.sh my-web-app                # Quick create
./create-devcontainer.sh create my-api 1002 api    # Full control
./create-devcontainer.sh list 1001                 # Management
```

**Features:**
- Simplified syntax
- Color-coded output
- Interactive prompts
- Help system
- Error recovery

### 3. Configuration (`devcontainer-agent.json`)
```json
{
  "name": "DevContainer Manager",
  "capabilities": [
    "container_management",
    "opencode_configuration", 
    "template_application",
    "resource_monitoring"
  ]
}
```

**Features:**
- Agent metadata
- Capability definitions
- Template configurations
- Integration settings

## 🎨 Project Templates

### Web Development Template
```bash
# React/Vue/Angular ready environment
./create-devcontainer.sh my-react-app 1001 web

# Includes:
- Chromium for testing
- Postman CLI for API testing
- Port forwards: 3000, 5173, 4173
- NPM: postman-cli
```

### Backend API Template
```bash
# Microservices and API development
./create-devcontainer.sh my-api 1002 api

# Includes:
- Database clients (PostgreSQL, Redis)
- Development tools (Nodemon, TypeScript)
- Port forwards: 3000, 8080, 9229
- Ready for Express/FastAPI
```

### Machine Learning Template
```bash
# AI/ML and data science
./create-devcontainer.sh my-ml-project 1003 ml

# Includes:
- PyTorch and ML libraries
- Jupyter Lab notebook
- Port forward: 8888 (Jupyter)
- Python: scikit-learn, pandas, matplotlib
```

### DevOps Template
```bash
# Infrastructure and automation
./create-devcontainer.sh my-infra 1004 devops

# Includes:
- Terraform, Ansible, kubectl
- Container registry tools
- Port forwards: 6443, 8080
- Ready for IaC and K8s
```

## 🔧 Advanced Usage

### Custom Workflow Pipelines
```bash
# Complete web development setup
python3 devcontainer-manager.py create my-project 1001 web
python3 devcontainer-manager.py setup-template 1001 web
python3 devcontainer-manager.py configure-opencode 1001 anthropic
python3 devcontainer-manager.py backup 1001
```

### Resource Monitoring Dashboard
```bash
# Real-time monitoring
watch -n 5 "python3 devcontainer-manager.py monitor 1001"

# Multiple containers
for vmid in 1001 1002 1003; do
    python3 devcontainer-manager.py monitor $vmid
done
```

### OpenCode Development Workflow
```bash
# AI-powered development
python3 devcontainer-manager.py create ai-project 1005
python3 devcontainer-manager.py configure-opencode 1005 anthropic

# Enter container and start OpenCode
pct enter 1005
su - developer
opencode  # AI-assisted development

# Or use OpenCode directly
opencode run "Create a REST API with Express and TypeScript"
```

### Automated Backup Strategy
```bash
# Backup all running containers
python3 devcontainer-manager.py list |
  jq -r '.containers[] | select(.status == "running") | .vmid' |
  while read vmid; do
    python3 devcontainer-manager.py backup $vmid
  done
```

## 📊 Monitoring & Analytics

### Resource Metrics
- **CPU Usage**: Real-time utilization
- **Memory**: Usage breakdown and allocation
- **Disk I/O**: Read/write performance
- **Network**: Traffic and throughput
- **Processes**: Running applications and services

### Performance Alerts
```bash
# Configure alert thresholds
export CPU_ALERT_THRESHOLD=90
export MEMORY_ALERT_THRESHOLD=80
export DISK_ALERT_THRESHOLD=85

# Agent will automatically alert when thresholds exceeded
```

### Historical Data
```bash
# Generate resource usage report
python3 devcontainer-manager.py --report=weekly --format=json

# Export for analysis
python3 devcontainer-manager.py --export=metrics --start=2024-01-01 --end=2024-01-31
```

## 🔒 Security Features

### Container Security
- **Non-root operations**: All development as non-privileged user
- **Network isolation**: Container-to-container networking controls
- **Resource limits**: CPU, memory, and disk quotas
- **Audit logging**: All operations logged and tracked

### Agent Security
- **Input validation**: Sanitized all user inputs
- **Privilege minimization**: Minimal required permissions
- **Error handling**: Safe failure modes without exposing data
- **Credential management**: Secure storage of API keys and tokens

## 🚀 Integration Examples

### GitHub Actions Integration
```yaml
# .github/workflows/dev-container.yml
name: Create Dev Container
on:
  workflow_dispatch:
    inputs:
      project_name:
        required: true
      template_type:
        required: false
        default: web
jobs:
  create-container:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Create Dev Container
        run: |
          python3 /opt/lxc-dev-template/subagents/devcontainer-manager.py \
            create ${{ github.event.inputs.project_name }} \
            "" ${{ github.event.inputs.template_type }}
```

### CI/CD Pipeline Integration
```bash
# Automated testing environment
create_test_container() {
    local project=$1
    python3 /opt/lxc-dev-template/subagents/devcontainer-manager.py \
      create "${project}-test" "" api
    
    # Setup test environment
    python3 /opt/lxc-dev-template/subagents/devcontainer-manager.py \
      setup-template "${project}-test" api
    
    # Run tests
    pct exec "${project}-test" -- su - developer -c "npm test"
    
    # Cleanup
    python3 /opt/lxc-dev-template/subagents/devcontainer-manager.py \
      backup "${project}-test"
    pct destroy "${project}-test"
}
```

### OpenCode Workspace Integration
```bash
# Multi-project OpenCode workspace
python3 devcontainer-manager.py create web-frontend 1001 web
python3 devcontainer-manager.py create api-backend 1002 api
python3 devcontainer-manager.py create ml-service 1003 ml

# Configure all with OpenCode
for vmid in 1001 1002 1003; do
    python3 devcontainer-manager.py configure-opencode $vmid anthropic
done

# Start development across all containers
for vmid in 1001 1002 1003; do
    echo "Starting OpenCode in container $vmid..."
    pct exec $vmid -- su - developer -c "opencode --workspace=multi-project" &
done
```

## 🧪 Testing & Development

### Run Tests
```bash
# Execute test suite
cd /opt/lxc-dev-template/subagents/
python3 tests/test_agent.py

# Run specific test examples
python3 example_usage.py create
python3 example_usage.py workflow
python3 example_usage.py backup
```

### Development Mode
```bash
# Enable debug logging
export DEBUG=1
export DEVCONTAINER_LOG_LEVEL=DEBUG

# Run agent with trace output
python3 -v devcontainer-manager.py list
```

### Contribution Workflow
```bash
# 1. Fork repository
git clone https://github.com/your-username/lxc-dev-template-proxmox.git

# 2. Create feature branch
git checkout -b feature/new-template

# 3. Develop and test
python3 tests/test_agent.py
python3 example_usage.py

# 4. Submit PR
git push origin feature/new-template
# Create Pull Request on GitHub
```

## 📖 Documentation & Resources

### API Reference
- **Complete API**: `devcontainer-agent.json`
- **Method documentation**: Inline code comments
- **Example implementations**: `example_usage.py`
- **Test cases**: `tests/test_agent.py`

### Configuration Guide
- **Environment variables**: `.env.example`
- **Custom templates**: Project template system
- **Integration setup**: CI/CD and automation
- **Performance tuning**: Resource optimization

### Troubleshooting
- **Common issues**: FAQ and solutions
- **Debug mode**: Step-by-step execution
- **Error codes**: Complete error reference
- **Performance**: Bottleneck identification

## 🎯 Best Practices

### Container Management
1. **Use meaningful names** for easy identification
2. **Apply appropriate templates** for project types
3. **Monitor resources** regularly for optimization
4. **Backup before major changes** for safety
5. **Use consistent VMID ranges** for organization

### Development Workflow
1. **Configure OpenCode** immediately after creation
2. **Initialize projects** with `/init` command
3. **Use AI assistance** for code reviews and generation
4. **Commit regularly** with descriptive messages
5. **Document changes** in project README files

### Security & Maintenance
1. **Change default passwords** on first use
2. **Use SSH keys** instead of passwords
3. **Update packages** regularly
4. **Review logs** for suspicious activity
5. **Clean up** unused containers and images

## 🚀 Future Enhancements

### Planned Features
- **Kubernetes integration** - Direct K8s pod management
- **Multi-cluster support** - Manage containers across Proxmox clusters
- **Performance profiling** - Advanced container performance analysis
- **Template marketplace** - Community-contributed templates
- **Mobile app** - iOS/Android management interface

### Roadmap
1. **v1.1**: Enhanced monitoring and alerts
2. **v1.2**: Template marketplace beta
3. **v1.3**: Kubernetes integration
4. **v2.0**: Multi-cluster and mobile support

---

**🎉 Ready to revolutionize your development workflow!**

The DevContainer Manager subagent provides intelligent, automated container management with OpenCode integration, enabling you to spin up complete development environments in seconds while maintaining professional-grade security and monitoring.