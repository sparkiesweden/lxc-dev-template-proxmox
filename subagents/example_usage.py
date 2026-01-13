#!/usr/bin/env python3
"""
Example usage of DevContainer Manager Subagent
Demonstrates how to integrate the agent into automated workflows.
"""

import sys
import json
import time
from pathlib import Path

# Add agent to path
sys.path.insert(0, str(Path(__file__).parent))

def example_basic_container_creation():
    """Example: Create a basic development container."""
    print("=== Basic Container Creation Example ===")
    
    from devcontainer_manager import DevContainerManager
    manager = DevContainerManager()
    
    # Create a web development container
    result = manager.create_container(
        project_name="example-web-app",
        template_type="web"
    )
    
    if result['success']:
        print(f"✅ Container created with VMID: {result['vmid']}")
        print(f"   IP Address: {result['ip']}")
        print(f"   Access: ssh developer@{result['ip']}")
    else:
        print(f"❌ Creation failed: {result['error']}")
    
    return result

def example_opencode_setup():
    """Example: Configure OpenCode with multiple providers."""
    print("\n=== OpenCode Configuration Example ===")
    
    from devcontainer_manager import DevContainerManager
    manager = DevContainerManager()
    
    # Configure with Anthropic and OpenAI
    vmid = "1001"  # Assuming container exists
    result = manager.configure_opencode(
        vmid=vmid,
        providers=["anthropic", "openai"]
    )
    
    if result['success']:
        print(f"✅ OpenCode configured: {result['version']}")
        print("   Providers: anthropic, openai")
    else:
        print(f"❌ Configuration failed: {result['error']}")
    
    return result

def example_project_template_application():
    """Example: Apply machine learning template."""
    print("\n=== ML Template Application Example ===")
    
    from devcontainer_manager import DevContainerManager
    manager = DevContainerManager()
    
    # Apply ML template
    vmid = "1001"
    result = manager.setup_project_template(
        vmid=vmid,
        template_type="ml"
    )
    
    if result['success']:
        installed = result['installed']
        print(f"✅ ML template applied to container {vmid}")
        print(f"   Packages: {installed.get('packages', [])}")
        print(f"   Python packages: {installed.get('python_packages', [])}")
        print(f"   Ports: {installed.get('ports', [])}")
    else:
        print(f"❌ Template application failed: {result['error']}")
    
    return result

def example_resource_monitoring():
    """Example: Continuous resource monitoring."""
    print("\n=== Resource Monitoring Example ===")
    
    from devcontainer_manager import DevContainerManager
    manager = DevContainerManager()
    
    vmid = "1001"
    print(f"Monitoring container {vmid} for 10 seconds...")
    
    for i in range(5):
        result = manager.monitor_resources(vmid)
        
        if 'error' not in result:
            print(f"\n--- Check {i+1} ---")
            print(f"Status: {result['status']}")
            print(f"Memory: {result.get('memory_info', 'N/A')}")
            print(f"Disk: {result.get('disk_info', 'N/A')}")
        else:
            print(f"❌ Monitoring failed: {result['error']}")
            break
        
        if i < 4:
            time.sleep(2)
    
    return result

def example_automated_workflow():
    """Example: Complete automated workflow setup."""
    print("\n=== Automated Workflow Example ===")
    
    from devcontainer_manager import DevContainerManager
    manager = DevContainerManager()
    
    # Step 1: Create container
    print("Step 1: Creating API development container...")
    create_result = manager.create_container(
        project_name="automated-api",
        template_type="api"
    )
    
    if not create_result['success']:
        print(f"❌ Container creation failed: {create_result['error']}")
        return create_result
    
    vmid = create_result['vmid']
    print(f"✅ Container {vmid} created")
    
    # Step 2: Wait for container to be ready
    print("Step 2: Waiting for container to be ready...")
    time.sleep(10)
    
    # Step 3: Apply project template
    print("Step 3: Applying API template...")
    template_result = manager.setup_project_template(
        vmid=vmid,
        template_type="api"
    )
    
    if not template_result['success']:
        print(f"❌ Template application failed: {template_result['error']}")
        return template_result
    
    print("✅ API template applied")
    
    # Step 4: Configure OpenCode
    print("Step 4: Configuring OpenCode...")
    opencode_result = manager.configure_opencode(
        vmid=vmid,
        providers=["anthropic"]
    )
    
    if not opencode_result['success']:
        print(f"❌ OpenCode configuration failed: {opencode_result['error']}")
        return opencode_result
    
    print("✅ OpenCode configured")
    
    # Step 5: Generate summary
    summary = {
        'project_name': 'automated-api',
        'vmid': vmid,
        'ip': create_result.get('ip'),
        'template': 'api',
        'opencode_version': opencode_result.get('version'),
        'setup_time': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    print("\n🎉 Automated setup completed!")
    print(json.dumps(summary, indent=2))
    
    return summary

def example_container_list_and_analysis():
    """Example: List containers and analyze status."""
    print("\n=== Container Analysis Example ===")
    
    from devcontainer_manager import DevContainerManager
    manager = DevContainerManager()
    
    # Get all containers
    result = manager.list_containers()
    
    if not result:
        print("❌ Failed to list containers")
        return
    
    containers = result['containers']
    
    # Analysis
    total_containers = len(containers)
    running_containers = len([c for c in containers if c['status'] == 'running'])
    stopped_containers = total_containers - running_containers
    containers_with_ip = len([c for c in containers if c.get('ip')])
    
    print(f"Total containers: {total_containers}")
    print(f"Running: {running_containers}")
    print(f"Stopped: {stopped_containers}")
    print(f"Containers with IP: {containers_with_ip}")
    
    # Detailed breakdown
    print("\nContainer Details:")
    for container in containers:
        status_icon = "🟢" if container['status'] == 'running' else "🔴"
        ip_info = f"({container['ip']})" if container.get('ip') else "(no IP)"
        
        print(f"  {status_icon} {container['vmid']}: {container['name']} {ip_info}")
    
    return {
        'total': total_containers,
        'running': running_containers,
        'stopped': stopped_containers,
        'containers': containers
    }

def example_backup_management():
    """Example: Automated backup workflow."""
    print("\n=== Backup Management Example ===")
    
    from devcontainer_manager import DevContainerManager
    manager = DevContainerManager()
    
    # Get running containers
    containers_result = manager.list_containers()
    containers = containers_result.get('containers', [])
    running_containers = [c for c in containers if c['status'] == 'running']
    
    if not running_containers:
        print("No running containers to backup")
        return
    
    print(f"Creating backups for {len(running_containers)} running containers...")
    
    backups_created = []
    for container in running_containers:
        vmid = container['vmid']
        print(f"  Backing up container {vmid} ({container['name']})...")
        
        backup_result = manager.backup_container(vmid)
        
        if backup_result['success']:
            backups_created.append({
                'vmid': vmid,
                'name': container['name'],
                'backup_file': backup_result['backup_name'],
                'location': backup_result['location']
            })
            print(f"    ✅ Backup created: {backup_result['backup_name']}")
        else:
            print(f"    ❌ Backup failed: {backup_result['error']}")
    
    print(f"\nBackup Summary:")
    print(f"  Total containers: {len(running_containers)}")
    print(f"  Successful backups: {len(backups_created)}")
    print(f"  Failed backups: {len(running_containers) - len(backups_created)}")
    
    return backups_created

def main():
    """Run all examples."""
    print("DevContainer Manager - Example Usage")
    print("=" * 50)
    
    examples = [
        ("Basic Container Creation", example_basic_container_creation),
        ("OpenCode Setup", example_opencode_setup),
        ("Project Template Application", example_project_template_application),
        ("Resource Monitoring", example_resource_monitoring),
        ("Container Analysis", example_container_list_and_analysis),
        ("Automated Workflow", example_automated_workflow),
        ("Backup Management", example_backup_management)
    ]
    
    results = {}
    
    for name, example_func in examples:
        try:
            print(f"\n{'='*20} {name} {'='*20}")
            result = example_func()
            results[name] = result
        except Exception as e:
            print(f"❌ Example '{name}' failed: {str(e)}")
            results[name] = {'error': str(e)}
    
    # Final summary
    print("\n" + "=" * 50)
    print("EXAMPLE EXECUTION SUMMARY")
    print("=" * 50)
    
    for name, result in results.items():
        status = "✅ Success" if 'error' not in result else "❌ Failed"
        print(f"{name}: {status}")
    
    return results

if __name__ == "__main__":
    # Check if we're being called with specific examples
    if len(sys.argv) > 1:
        example_name = sys.argv[1]
        
        examples = {
            'create': example_basic_container_creation,
            'opencode': example_opencode_setup,
            'template': example_project_template_application,
            'monitor': example_resource_monitoring,
            'analyze': example_container_list_and_analysis,
            'workflow': example_automated_workflow,
            'backup': example_backup_management
        }
        
        if example_name in examples:
            examples[example_name]()
        else:
            print(f"Unknown example: {example_name}")
            print(f"Available examples: {', '.join(examples.keys())}")
    else:
        # Run all examples
        main()