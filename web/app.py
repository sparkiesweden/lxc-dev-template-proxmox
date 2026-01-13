#!/usr/bin/env python3
"""
DevContainer Monitor - Mobile Responsive Web Dashboard
Simple Flask application for monitoring LXC development containers.
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import subprocess
import json
import time
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'devcontainer-monitor-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

def run_agent_command(cmd_args):
    """Execute DevContainer manager command and return JSON result."""
    try:
        cmd = ['/opt/lxc-dev-template/subagents/devcontainer-manager.py'] + cmd_args
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {'success': False, 'error': result.stderr}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/')
def dashboard():
    """Main dashboard - mobile responsive container monitoring."""
    return render_template('dashboard.html')

@app.route('/api/containers')
def get_containers():
    """API endpoint to get all containers."""
    try:
        return jsonify(run_agent_command(['list']))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/containers/<vmid>')
def get_container_info(vmid):
    """API endpoint to get specific container info."""
    try:
        return jsonify(run_agent_command(['info', vmid]))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/container/<vmid>/start', methods=['POST'])
def start_container(vmid):
    """API endpoint to start a container."""
    try:
        return jsonify(run_agent_command(['start', vmid]))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/container/<vmid>/stop', methods=['POST'])
def stop_container(vmid):
    """API endpoint to stop a container."""
    try:
        return jsonify(run_agent_command(['stop', vmid]))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/container/<vmid>/restart', methods=['POST'])
def restart_container(vmid):
    """API endpoint to restart a container."""
    try:
        return jsonify(run_agent_command(['restart', vmid]))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/container/<vmid>/monitor')
def monitor_container(vmid):
    """API endpoint to get container resources."""
    try:
        return jsonify(run_agent_command(['monitor', vmid]))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/container/<vmid>/configure-opencode', methods=['POST'])
def configure_opencode(vmid):
    """API endpoint to configure OpenCode."""
    try:
        data = request.get_json()
        providers = data.get('providers', ['anthropic'])
        return jsonify(run_agent_command(['configure-opencode', vmid] + providers))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/health')
def health_check():
    """API health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection."""
    print(f'Client connected: {request.sid}')
    # Send current containers immediately
    try:
        containers = run_agent_command(['list'])
        if containers.get('containers'):
            emit('containers_update', containers.get('containers'))
    except Exception as e:
        print(f'Error sending initial data: {e}')

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection."""
    print(f'Client disconnected: {request.sid}')

@socketio.on('request_containers')
def handle_request_containers():
    """Handle request for container list via WebSocket."""
    try:
        containers = run_agent_command(['list'])
        if containers.get('containers'):
            emit('containers_update', containers.get('containers'))
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('refresh_containers')
def handle_refresh_containers():
    """Handle manual refresh request."""
    try:
        containers = run_agent_command(['list'])
        if containers.get('containers'):
            emit('containers_update', containers.get('containers'))
            emit('notification', {'message': 'Container list refreshed', 'type': 'success'})
    except Exception as e:
        emit('error', {'message': str(e), 'type': 'error'})

if __name__ == '__main__':
    # Create logs directory
    os.makedirs('/opt/lxc-dev-template/web/logs', exist_ok=True)
    
    print("🚀 Starting DevContainer Monitor Web Dashboard")
    print("📱 Mobile-responsive interface")
    print("🔄 Real-time container monitoring")
    print("🌐 WebSocket connectivity enabled")
    print("📊 Open http://localhost:8080 to access")
    
    socketio.run(app, host='0.0.0.0', port=8080, debug=False, allow_unsafe_werkzeug=True)