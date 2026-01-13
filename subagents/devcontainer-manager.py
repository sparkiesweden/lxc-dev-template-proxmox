#!/usr/bin/env python3
"""
LXC DevContainer Manager Subagent
A specialized agent for managing LXC development containers with OpenCode integration.

This agent handles:
- Container creation and management
- Project template application
- Development environment setup
- OpenCode configuration
- Resource monitoring
- Automated workflows
"""

import os
import sys
import json
import subprocess
import re
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class DevContainerManager:
    """Manages LXC development containers with OpenCode."""
    
    def __init__(self):
        self.base_dir = Path("/opt/lxc-dev-template")
        self.template_id = "9000"
        
    def run_command(self, command: str, capture_output: bool = True) -> Tuple[int, str, str]:
        """Execute shell command and return result."""
        try:
            if capture_output:
                result = subprocess.run(
                    command, 
                    shell=True, 
                    capture_output=True, 
                    text=True,
                    timeout=30
                )
                return result.returncode, result.stdout, result.stderr
            else:
                process = subprocess.Popen(command, shell=True)
                return process.wait(), "", ""
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)
    
    def list_containers(self) -> List[Dict]:
        """List all development containers."""
        returncode, stdout, stderr = self.run_command("pct list")
        if returncode != 0:
            return []
        
        containers = []
        for line in stdout.strip().split('\n'):
            if re.match(r'^\d+', line):
                parts = line.split()
                if len(parts) >= 3:
                    vmid = parts[0]
                    status = parts[1]
                    name = parts[2] if len(parts) > 2 else ""
                    
                    # Skip template itself
                    if vmid == self.template_id:
                        continue
                    
                    # Get IP if running
                    ip = ""
                    if status == "running":
                        ip_cmd = f"pct exec {vmid} -- ip addr show eth0 2>/dev/null | grep 'inet ' | awk '{{print $2}}' | cut -d/ -f1"
                        _, ip_out, _ = self.run_command(ip_cmd)
                        ip = ip_out.strip()
                    
                    containers.append({
                        'vmid': vmid,
                        'name': name,
                        'status': status,
                        'ip': ip
                    })
        
        return containers
    
    def create_container(self, project_name: str, vmid: Optional[str] = None, 
                     template_type: str = "default") -> Dict:
        """Create new development container."""
        # Generate VMID if not provided
        if not vmid:
            for i in range(1001, 9999):
                check_cmd = f"pct list | grep -q '^{i}'"
                if self.run_command(check_cmd)[0] != 0:
                    vmid = str(i)
                    break
        
        if not vmid:
            return {'success': False, 'error': 'No available VMID found'}
        
        # Clone template
        clone_cmd = f"pct clone {self.template_id} {vmid} --hostname {project_name}"
        returncode, stdout, stderr = self.run_command(clone_cmd)
        
        if returncode != 0:
            return {'success': False, 'error': stderr}
        
        # Start container
        start_cmd = f"pct start {vmid}"
        returncode, _, stderr = self.run_command(start_cmd)
        
        if returncode != 0:
            return {'success': False, 'error': stderr}
        
        # Wait for IP
        time.sleep(10)
        ip_cmd = f"pct exec {vmid} -- ip addr show eth0 2>/dev/null | grep 'inet ' | awk '{{print $2}}' | cut -d/ -f1"
        _, ip_out, _ = self.run_command(ip_cmd)
        ip = ip_out.strip() or "pending"
        
        return {
            'success': True,
            'vmid': vmid,
            'project_name': project_name,
            'ip': ip,
            'access_methods': [
                f"pct enter {vmid}",
                f"ssh developer@{ip}" if ip != "pending" else f"ssh developer@<ip>"
            ]
        }
    
    def configure_opencode(self, vmid: str, providers: List[str] = None) -> Dict:
        """Configure OpenCode in container."""
        if providers:
            # Configure providers
            for provider in providers:
                auth_cmd = f"pct exec {vmid} -- su - developer -c 'opencode auth login --provider {provider}'"
                returncode, _, stderr = self.run_command(auth_cmd)
                if returncode != 0:
                    return {'success': False, 'error': f'Failed to configure {provider}: {stderr}'}
        
        # Test OpenCode
        test_cmd = f"pct exec {vmid} -- su - developer -c 'opencode --version'"
        returncode, version_out, stderr = self.run_command(test_cmd)
        
        return {
            'success': returncode == 0,
            'version': version_out.strip(),
            'error': stderr if returncode != 0 else None
        }
    
    def get_container_info(self, vmid: str) -> Dict:
        """Get detailed container information."""
        # Status and IP
        status_cmd = f"pct status {vmid}"
        _, status_out, _ = self.run_command(status_cmd)
        status = status_out.strip().split('\n')[0].split()[-1] if status_out else "unknown"
        
        ip = ""
        if status == "running":
            ip_cmd = f"pct exec {vmid} -- ip addr show eth0 2>/dev/null | grep 'inet ' | awk '{{print $2}}' | cut -d/ -f1"
            _, ip_out, _ = self.run_command(ip_cmd)
            ip = ip_out.strip()
        
        # Configuration
        config_cmd = f"pct config {vmid}"
        _, config_out, _ = self.run_command(config_cmd)
        
        # Resource usage if running
        resources = {}
        if status == "running":
            mem_cmd = f"pct exec {vmid} -- free -h | grep '^Mem:' | awk '{{print \$3 \"/\" \$2}}'"
            _, mem_out, _ = self.run_command(mem_cmd)
            resources['memory'] = mem_out.strip() if mem_out else "N/A"
            
            disk_cmd = f"pct exec {vmid} -- df -h / | tail -1 | awk '{{print \$3 \"/\" \$2 \" (\" \$5 \" used)\"}}'"
            _, disk_out, _ = self.run_command(disk_cmd)
            resources['disk'] = disk_out.strip() if disk_out else "N/A"
        
        return {
            'vmid': vmid,
            'status': status,
            'ip': ip,
            'config': config_out.strip() if config_out else "",
            'resources': resources
        }
    
    def setup_project_template(self, vmid: str, template_type: str) -> Dict:
        """Apply project template to container."""
        template_configs = {
            'web': {
                'packages': ['chromium', 'lighttpd'],
                'npm_packages': ['postman-cli'],
                'ports': [3000, 5173, 4173]
            },
            'api': {
                'packages': ['postgresql-client', 'redis-tools'],
                'npm_packages': ['nodemon', 'typescript'],
                'services': ['postgres', 'redis'],
                'ports': [3000, 8080, 9229]
            },
            'ml': {
                'packages': ['python3-torch', 'python3-jupyter'],
                'python_packages': ['scikit-learn', 'pandas', 'matplotlib'],
                'ports': [8888],
                'setup_script': 'jupyter_setup.sh'
            },
            'devops': {
                'packages': ['terraform', 'ansible', 'kubectl'],
                'services': ['docker-registry'],
                'ports': [6443, 8080]
            }
        }
        
        config = template_configs.get(template_type, {})
        
        # Install packages
        if 'packages' in config:
            pkg_list = ' '.join(config['packages'])
            install_cmd = f"pct exec {vmid} -- apt install -y {pkg_list}"
            returncode, _, stderr = self.run_command(install_cmd)
            if returncode != 0:
                return {'success': False, 'error': f'Package install failed: {stderr}'}
        
        # Install npm packages
        if 'npm_packages' in config:
            for pkg in config['npm_packages']:
                npm_cmd = f"pct exec {vmid} -- su - developer -c 'npm install -g {pkg}'"
                returncode, _, stderr = self.run_command(npm_cmd)
                if returncode != 0:
                    return {'success': False, 'error': f'NPM install failed: {stderr}'}
        
        # Install Python packages
        if 'python_packages' in config:
            pkg_list = ' '.join(config['python_packages'])
            pip_cmd = f"pct exec {vmid} -- su - developer -c 'pip install {pkg_list}'"
            returncode, _, stderr = self.run_command(pip_cmd)
            if returncode != 0:
                return {'success': False, 'error': f'Pip install failed: {stderr}'}
        
        return {
            'success': True,
            'template': template_type,
            'installed': config
        }
    
    def monitor_resources(self, vmid: str) -> Dict:
        """Get current resource usage."""
        status_cmd = f"pct status {vmid}"
        _, status_out, _ = self.run_command(status_cmd)
        status = status_out.strip().split('\n')[0].split()[-1] if status_out else "unknown"
        
        if status != "running":
            return {'status': status, 'message': 'Container not running'}
        
        # CPU and Memory
        top_cmd = f"pct exec {vmid} -- top -bn1 | head -5"
        _, top_out, _ = self.run_command(top_cmd)
        
        # Memory details
        mem_cmd = f"pct exec {vmid} -- free -h"
        _, mem_out, _ = self.run_command(mem_cmd)
        
        # Disk usage
        disk_cmd = f"pct exec {vmid} -- df -h"
        _, disk_out, _ = self.run_command(disk_cmd)
        
        return {
            'status': status,
            'cpu_usage': top_out.strip() if top_out else "N/A",
            'memory_info': mem_out.strip() if mem_out else "N/A",
            'disk_info': disk_out.strip() if disk_out else "N/A"
        }
    
    def backup_container(self, vmid: str) -> Dict:
        """Create container backup."""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_name = f"lxc-{vmid}-{timestamp}"
        
        backup_cmd = f"vzdump {vmid} --compress zstd --storage local-lvm --mode snapshot"
        returncode, stdout, stderr = self.run_command(backup_cmd, capture_output=False)
        
        return {
            'success': returncode == 0,
            'backup_name': backup_name,
            'error': stderr if returncode != 0 else None,
            'location': '/var/lib/vz/dump/'
        }

def main():
    """Main agent interface."""
    if len(sys.argv) < 2:
        print(json.dumps({
            'error': 'Usage: python3 devcontainer-manager.py <action> [options]'
        }))
        sys.exit(1)
    
    action = sys.argv[1]
    manager = DevContainerManager()
    
    try:
        if action == "list":
            result = manager.list_containers()
        
        elif action == "create":
            if len(sys.argv) < 3:
                result = {'error': 'Usage: create <project_name> [vmid] [template_type]'}
            else:
                project_name = sys.argv[2]
                vmid = sys.argv[3] if len(sys.argv) > 3 else None
                template_type = sys.argv[4] if len(sys.argv) > 4 else "default"
                result = manager.create_container(project_name, vmid, template_type)
        
        elif action == "info":
            if len(sys.argv) < 3:
                result = {'error': 'Usage: info <vmid>'}
            else:
                result = manager.get_container_info(sys.argv[2])
        
        elif action == "configure-opencode":
            if len(sys.argv) < 3:
                result = {'error': 'Usage: configure-opencode <vmid> [provider1,provider2,...]'}
            else:
                vmid = sys.argv[2]
                providers = sys.argv[3].split(',') if len(sys.argv) > 3 else None
                result = manager.configure_opencode(vmid, providers)
        
        elif action == "setup-template":
            if len(sys.argv) < 4:
                result = {'error': 'Usage: setup-template <vmid> <template_type>'}
            else:
                result = manager.setup_project_template(sys.argv[2], sys.argv[3])
        
        elif action == "monitor":
            if len(sys.argv) < 3:
                result = {'error': 'Usage: monitor <vmid>'}
            else:
                result = manager.monitor_resources(sys.argv[2])
        
        elif action == "backup":
            if len(sys.argv) < 3:
                result = {'error': 'Usage: backup <vmid>'}
            else:
                result = manager.backup_container(sys.argv[2])
        
        else:
            result = {
                'error': f'Unknown action: {action}',
                'available_actions': [
                    'list', 'create', 'info', 'configure-opencode', 
                    'setup-template', 'monitor', 'backup'
                ]
            }
    
    except Exception as e:
        result = {'error': str(e)}
    
    print(json.dumps(result, indent=2, default=str))

if __name__ == "__main__":
    main()