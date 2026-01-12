# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-13

### Added
- Complete LXC development template with OpenCode integration
- Automated template creation script (`create-template.sh`)
- Quick container creation script (`create-dev-container.sh`)
- Comprehensive container management script (`manage-containers.sh`)
- Environment configuration template (`.env.example`)
- Advanced project templates documentation
- Detailed README with usage examples
- MIT License

### Features
- **Base System**: Debian 13 (Trixie) with latest updates
- **Development Tools**: Build essentials, git, curl, wget, htop, tree, ripgrep, fd-find
- **Node.js**: 20.x LTS with npm, yarn, pnpm
- **Docker**: Engine 29.1.4 + Docker Compose v5.0.1 + buildx
- **OpenCode**: v1.1.15 AI coding assistant
- **Python**: 3.13 with pip
- **Shell**: Zsh + Bash with enhanced environment
- **GitHub CLI**: gh v2.83.2
- **User Management**: developer user with sudo and docker access

### Security
- Non-root development user
- Configurable password
- SSH key authentication support
- Docker permissions limited to developer user

### Performance
- 8 cores, 8GB RAM, 32GB disk allocation
- Optimized container configuration
- Clean package cache for smaller template size

### Documentation
- Comprehensive README with examples
- Project templates guide
- Troubleshooting section
- Advanced usage scenarios
- Container management commands

### Templates Included
- Web development template
- Backend API template
- Machine learning template
- DevOps and infrastructure template
- Mobile development template
- Go development template
- Rust development template
- Database development template

## [Unreleased]

### Planned
- Container auto-update functionality
- GPU support templates
- Kubernetes integration
- CI/CD pipeline templates
- Performance monitoring dashboard
- Container health checks