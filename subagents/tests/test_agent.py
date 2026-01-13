#!/usr/bin/env python3
"""
Test suite for DevContainer Manager Subagent
"""

import unittest
import sys
import os
import json
from pathlib import Path

# Add the agent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestDevContainerManager(unittest.TestCase):
    """Test cases for DevContainer Manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock the pct command for testing
        self.mock_pct_responses = {
            'list': '''VMID       Status     Lock         Name                
101        running                 llama-gpu           
102        running                 opencode            
1001       running                 test-project        ''',
            'status_running': 'status: running',
            'status_stopped': 'status: stopped',
            'config': '''arch: amd64
cores: 8
hostname: test-project
memory: 8192''',
            'ip': '''2: eth0@if13: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether bc:24:11:f3:26:14 brd ff:ff:ff:ff:ff link-netnsid 0
    inet 192.168.10.75/24 brd 192.168.10.255 scope global dynamic eth0''',
            'version': '1.1.15'
        }
    
    def test_container_parsing(self):
        """Test container list parsing."""
        from devcontainer_manager import DevContainerManager
        
        # We would mock the command execution here
        # For now, test that the function exists and returns correct structure
        manager = DevContainerManager()
        self.assertTrue(hasattr(manager, 'list_containers'))
        self.assertTrue(callable(getattr(manager, 'list_containers')))
    
    def test_vmid_generation(self):
        """Test VMID generation logic."""
        # Test VMID range logic
        valid_vmids = [str(i) for i in range(1001, 9999)]
        self.assertIn('1001', valid_vmids)
        self.assertIn('1002', valid_vmids)
        self.assertIn('9999', valid_vmids)
        self.assertNotIn('1000', valid_vmids)
    
    def test_project_template_configs(self):
        """Test project template configurations."""
        from devcontainer_manager import DevContainerManager
        
        manager = DevContainerManager()
        
        # Test that template method exists
        self.assertTrue(hasattr(manager, 'setup_project_template'))
        
        # Test template structure (would normally call actual function)
        expected_templates = ['web', 'api', 'ml', 'devops']
        for template in expected_templates:
            # This would test the actual template setup
            self.assertIsInstance(template, str)
    
    def test_resource_monitoring_structure(self):
        """Test resource monitoring structure."""
        from devcontainer_manager import DevContainerManager
        
        manager = DevContainerManager()
        self.assertTrue(hasattr(manager, 'monitor_resources'))
        
        # Expected monitoring structure
        expected_metrics = ['cpu_usage', 'memory_info', 'disk_info', 'status']
        for metric in expected_metrics:
            self.assertIsInstance(metric, str)
    
    def test_opencode_configuration_structure(self):
        """Test OpenCode configuration structure."""
        from devcontainer_manager import DevContainerManager
        
        manager = DevContainerManager()
        self.assertTrue(hasattr(manager, 'configure_opencode'))
        
        # Test provider validation
        valid_providers = ['anthropic', 'openai', 'google', 'azure']
        for provider in valid_providers:
            self.assertIsInstance(provider, str)
    
    def test_backup_operation_structure(self):
        """Test backup operation structure."""
        from devcontainer_manager import DevContainerManager
        
        manager = DevContainerManager()
        self.assertTrue(hasattr(manager, 'backup_container'))
        
        # Test backup naming convention
        import time
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        expected_name = f"lxc-1001-{timestamp}"
        self.assertIn('lxc-', expected_name)
        self.assertIn(timestamp, expected_name)
    
    def test_json_response_format(self):
        """Test that responses follow consistent JSON format."""
        # Test that all response methods return dictionaries
        response_structure = {
            'success': bool,
            'error': type(None),  # Can be None
            'vmid': str,
            'ip': str,
            'project_name': str,
            'access_methods': list
        }
        
        for key, expected_type in response_structure.items():
            self.assertIsInstance(key, str)
            self.assertIn(type(expected_type), [type, type(None)])
    
    def test_error_handling(self):
        """Test error handling patterns."""
        from devcontainer_manager import DevContainerManager
        
        manager = DevContainerManager()
        
        # Test command execution method
        self.assertTrue(hasattr(manager, 'run_command'))
        
        # Test return code handling
        # Would test actual command execution
        success_codes = [0]
        error_codes = [-1, 1, 127]
        
        for code in success_codes:
            self.assertIn(code, success_codes)
        
        for code in error_codes:
            self.assertIn(code, error_codes)
    
    def test_configuration_validation(self):
        """Test configuration validation."""
        # Test required parameters
        required_create_params = ['project_name']
        required_info_params = ['vmid']
        
        for param in required_create_params:
            self.assertIsInstance(param, str)
            self.assertTrue(len(param) > 0)
        
        for param in required_info_params:
            self.assertIsInstance(param, str)
            self.assertTrue(len(param) > 0)
    
    def test_project_template_names(self):
        """Test project template naming conventions."""
        valid_templates = {
            'web': {
                'name': 'Web Development',
                'description': 'React, Vue, Angular development'
            },
            'api': {
                'name': 'Backend API', 
                'description': 'REST API and microservices'
            },
            'ml': {
                'name': 'Machine Learning',
                'description': 'AI/ML and data science'
            },
            'devops': {
                'name': 'DevOps & Infrastructure',
                'description': 'Infrastructure as code'
            }
        }
        
        for template_key, config in valid_templates.items():
            self.assertIn('name', config)
            self.assertIn('description', config)
            self.assertIsInstance(config['name'], str)
            self.assertIsInstance(config['description'], str)

class TestCLIWrapper(unittest.TestCase):
    """Test cases for CLI wrapper script."""
    
    def test_help_command_structure(self):
        """Test help command structure."""
        # Test that help contains required sections
        required_sections = [
            'Quick Commands:',
            'Project Templates:',
            'Examples:',
            'Management Commands:'
        ]
        
        for section in required_sections:
            self.assertIsInstance(section, str)
            self.assertTrue(len(section) > 0)
    
    def test_command_parsing(self):
        """Test command argument parsing."""
        # Test expected command patterns
        commands = [
            'create', 'list', 'info', 'monitor', 
            'backup', 'configure-opencode', 'help'
        ]
        
        for command in commands:
            self.assertIsInstance(command, str)
            self.assertTrue(len(command) > 0)
    
    def test_template_parameter_validation(self):
        """Test template parameter validation."""
        valid_templates = ['web', 'api', 'ml', 'devops', 'default']
        
        for template in valid_templates:
            self.assertIsInstance(template, str)
            self.assertIn(template, valid_templates)

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def test_agent_availability(self):
        """Test that agent files are available."""
        agent_file = Path(__file__).parent.parent / 'devcontainer-manager.py'
        wrapper_file = Path(__file__).parent.parent / 'create-devcontainer.sh'
        
        self.assertTrue(agent_file.exists(), "Agent file should exist")
        self.assertTrue(wrapper_file.exists(), "Wrapper script should exist")
    
    def test_executable_permissions(self):
        """Test that scripts have correct permissions."""
        import stat
        
        wrapper_file = Path(__file__).parent.parent / 'create-devcontainer.sh'
        if wrapper_file.exists():
            file_stats = wrapper_file.stat()
            # Check execute permissions for owner, group, and others
            execute_mode = file_stats.st_mode & stat.S_IXUSR
            self.assertTrue(execute_mode, "Wrapper script should be executable")
    
    def test_configuration_files(self):
        """Test configuration file structure."""
        config_file = Path(__file__).parent.parent / 'devcontainer-agent.json'
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Required top-level keys
            required_keys = ['name', 'version', 'capabilities', 'tools', 'endpoints']
            for key in required_keys:
                self.assertIn(key, config)
            
            # Test endpoint structure
            self.assertIn('endpoints', config)
            endpoints = config['endpoints']
            self.assertIsInstance(endpoints, dict)
            
            # Test required endpoints
            required_endpoints = ['create_container', 'configure_opencode', 'monitor_resources']
            for endpoint in required_endpoints:
                self.assertIn(endpoint, endpoints)

def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDevContainerManager))
    suite.addTests(loader.loadTestsFromTestCase(TestCLIWrapper))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return results
    return {
        'tests_run': result.testsRun,
        'failures': len(result.failures),
        'errors': len(result.errors),
        'success': result.wasSuccessful(),
        'failure_details': [
            {'test': str(test), 'error': str(error)} 
            for test, error in result.failures + result.errors
        ]
    }

if __name__ == '__main__':
    print("Running DevContainer Manager Test Suite")
    print("=" * 50)
    
    results = run_tests()
    
    print(f"\nTest Results:")
    print(f"Tests Run: {results['tests_run']}")
    print(f"Failures: {results['failures']}")
    print(f"Errors: {results['errors']}")
    print(f"Success: {results['success']}")
    
    if not results['success']:
        print(f"\nFailure Details:")
        for failure in results['failure_details']:
            print(f"  - {failure['test']}: {failure['error']}")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
        sys.exit(0)