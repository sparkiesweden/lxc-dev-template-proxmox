# Project Templates

This document contains pre-configured project templates that can be automatically applied to new development containers.

## Available Templates

### 1. Web Development (web)
**Perfect for**: React, Vue, Angular, and modern web applications

**Pre-installed**: Everything from base template + web-specific tools
```bash
# Create web development container
./create-dev-container.sh my-web-app 1001

# After container creation:
npm create vite@latest latest-project --template react
# or
npm create vue@latest latest-project
# or
npm create svelte@latest latest-project
```

**Additional Tools**:
- Postman CLI (`npm install -g postman-cli`)
- Browser automation tools
- Web development VS Code extensions (if using VS Code)

### 2. Backend API (api)
**Perfect for**: REST APIs, GraphQL, microservices

**Pre-installed**: Everything from base template + API tools
```bash
# Create API development container
./create-dev-container.sh my-api 1002

# Quick project setup:
npm init -y
npm install express cors helmet morgan
npm install -D nodemon typescript @types/node @types/express
```

**Additional Tools**:
- Postman CLI
- API documentation generators
- Database clients (PostgreSQL, MongoDB, Redis)

### 3. Machine Learning (ml)
**Perfect for**: AI/ML projects, data science, neural networks

**Pre-installed**: Everything from base template + ML tools
```bash
# Create ML development container
./create-dev-container.sh my-ml-project 1003

# Python ML environment:
pip install torch torchvision torchaudio
pip install scikit-learn pandas numpy matplotlib
pip install jupyterlab
```

**Additional Tools**:
- Jupyter Lab
- CUDA support (if GPU available)
- Popular ML libraries
- Data visualization tools

### 4. DevOps & Infrastructure (devops)
**Perfect for**: CI/CD, infrastructure as code, automation

**Pre-installed**: Everything from base template + DevOps tools
```bash
# Create DevOps container
./create-dev-container.sh my-infra 1004

# Terraform project:
terraform init
terraform plan
terraform apply
```

**Additional Tools**:
- Terraform
- Ansible
- kubectl
- Helm
- Docker Compose with multi-stage builds

### 5. Mobile Development (mobile)
**Perfect for**: React Native, Flutter, mobile app development

**Pre-installed**: Everything from base template + mobile tools
```bash
# Create mobile development container
./create-dev-container.sh my-mobile-app 1005

# React Native project:
npx react-native init MyMobileApp
cd MyMobileApp
npm start
```

**Additional Tools**:
- React Native CLI
- Flutter SDK
- Android Studio tools
- iOS development tools (limited in container)

### 6. Go Development (go)
**Perfect for**: Go applications, microservices, CLI tools

**Pre-installed**: Everything from base template + Go tools
```bash
# Create Go development container
./create-dev-container.sh my-go-app 1006

# Go project setup:
go mod init github.com/username/my-project
go get github.com/gin-gonic/gin
```

**Additional Tools**:
- Go 1.21+
- Popular Go frameworks
- Go testing tools
- Performance profiling tools

### 7. Rust Development (rust)
**Perfect for**: Systems programming, performance-critical applications

**Pre-installed**: Everything from base template + Rust tools
```bash
# Create Rust development container
./create-dev-container.sh my-rust-app 1007

# Rust project setup:
cargo new my-project
cd my-project
cargo run
```

**Additional Tools**:
- Rust toolchain (stable)
- Cargo crates for web development
- Rust formatting and linting tools

### 8. Database Development (database)
**Perfect for**: Database management, migrations, data engineering

**Pre-installed**: Everything from base template + database tools
```bash
# Create database development container
./create-dev-container.sh my-db-project 1008

# Start PostgreSQL with Docker:
docker run --name postgres-dev -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15
```

**Additional Tools**:
- Database clients (psql, mysql, mongosh)
- Migration tools
- Database GUI tools (DBeaver alternatives)
- Redis CLI

## Using Project Templates

### Method 1: Specify Template During Creation
```bash
# Create container with specific template
./create-dev-container.sh my-project 1001 --template web
./create-dev-container.sh my-api 1002 --template api
./create-dev-container.sh my-ml-project 1003 --template ml
```

### Method 2: Apply Template After Creation
```bash
# Create base container
./create-dev-container.sh my-project 1001

# Apply template
./apply-template.sh 1001 web
```

### Method 3: Interactive Template Selection
```bash
# Interactive template selection
./create-dev-container.sh my-project 1001 --interactive
```

## Template-Specific Configurations

### Web Development Container
```yaml
# Additional packages:
# - chromium (for testing)
# - lighttpd (local server)
# - imagemagick (image processing)

# Environment variables:
# NODE_ENV=development
# CHROME_BIN=/usr/bin/chromium

# Port forwards (via Proxmox):
# 3000 -> Development servers
# 5173 -> Vite dev server
# 4173 -> Vite preview
```

### API Development Container
```yaml
# Additional packages:
# - postgresql-client
# - redis-tools
# - mongodb-clients

# Database services via Docker:
# - PostgreSQL 15
# - Redis 7
# - MongoDB 7

# Development ports:
# 3000 -> API server
# 8080 -> Alternative API port
# 9229 -> Node.js debugging
```

### ML Development Container
```yaml
# Additional packages:
# - python3-torch
# - python3-tensorflow
# - jupyterlab

# GPU support (if available):
# - NVIDIA CUDA toolkit
# - cuDNN libraries

# Jupyter configuration:
# - Auto-start on container boot
# - Token authentication
# - Port 8888 exposed
```

## Custom Templates

### Creating Custom Templates

1. **Create template directory**:
```bash
mkdir project-templates/my-template
```

2. **Create template definition** (`template.yaml`):
```yaml
name: "My Custom Template"
description: "Custom development environment"
version: "1.0.0"

# Packages to install
packages:
  - htop
  - git
  - custom-package

# Node.js packages (global)
npm_packages:
  - "@mycompany/cli-tool"

# Python packages (global)
python_packages:
  - my-company-utils

# Docker services to start
docker_services:
  - name: redis
    image: redis:7
    ports: ["6379:6379"]

# Environment variables
environment:
  CUSTOM_VAR: "value"
  NODE_ENV: "development"

# Scripts to run after setup
post_install_scripts:
  - setup-custom-tool.sh
  - configure-dev.sh
```

3. **Create setup scripts**:
```bash
# setup-custom-tool.sh
#!/bin/bash
echo "Setting up custom tools..."
# Custom installation commands
```

4. **Test template**:
```bash
./test-template.sh my-template
```

### Template Best Practices

1. **Keep it minimal**: Only install what's essential for the project type
2. **Use Docker**: For databases and services, prefer Docker over system packages
3. **Document everything**: Include README with usage examples
4. **Version control**: Track template definitions in Git
5. **Test regularly**: Ensure templates work with latest package versions

## Advanced Template Features

### Multi-Stage Templates
Templates can define stages for different development phases:

```yaml
stages:
  development:
    packages: ["nodemon", "typescript"]
    environment:
      NODE_ENV: "development"
  
  testing:
    packages: ["jest", "cypress"]
    environment:
      NODE_ENV: "test"
  
  production:
    packages: ["pm2", "nginx"]
    environment:
      NODE_ENV: "production"
```

### Conditional Features
Install features based on availability or user preference:

```yaml
conditional_features:
  - condition: "has_gpu"
    packages: ["nvidia-cuda-toolkit"]
    environment:
      CUDA_VISIBLE_DEVICES: "all"
  
  - condition: "large_memory"
    packages: ["redis-tools", "postgresql-client"]
```

### Integration Hooks
Hook into container lifecycle events:

```yaml
hooks:
  pre_create: "scripts/pre-create.sh"
  post_create: "scripts/post-create.sh"
  pre_start: "scripts/pre-start.sh"
  post_start: "scripts/post-start.sh"
  pre_stop: "scripts/pre-stop.sh"
  post_stop: "scripts/post-stop.sh"
```

## Troubleshooting Templates

### Common Issues

1. **Package Installation Fails**
   - Check package availability in Debian repositories
   - Verify correct package names
   - Check network connectivity

2. **Docker Services Won't Start**
   - Verify Docker is running in container
   - Check port conflicts
   - Review Docker logs

3. **Node.js Global Packages Missing**
   - Verify npm global path
   - Check permissions
   - Reinstall global packages

4. **Environment Variables Not Set**
   - Check shell initialization files
   - Verify profile scripts are executed
   - Test with `env | grep VAR_NAME`

### Debug Mode

Run template creation with debug output:

```bash
DEBUG=true ./create-dev-container.sh my-project 1001 --template web
```

This will show detailed logs of the template application process.

## Contributing Templates

To contribute new templates:

1. Fork the repository
2. Create a new template directory
3. Follow the template structure
4. Test thoroughly
5. Submit a pull request

Include:
- Template definition (`template.yaml`)
- Setup scripts
- Documentation (README.md in template directory)
- Example usage
- Test cases