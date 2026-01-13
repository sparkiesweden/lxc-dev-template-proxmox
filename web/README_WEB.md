# DevContainer Monitor Web Dashboard

A mobile-responsive web interface for monitoring LXC development containers with real-time updates and AI integration.

## 🚀 Quick Start

```bash
# Start the monitoring dashboard
cd /opt/lxc-dev-template/web
./start-dashboard.sh

# Access on any device
# Mobile: http://your-host:8080
# Desktop: http://your-host:8080
```

## 📱 Features

### Mobile-First Design
- **Responsive Layout**: Works on phones (320px+), tablets, and desktop
- **Touch-Friendly**: 44px minimum touch targets, swipe gestures
- **Performance Optimized**: <2s load time, <500ms WebSocket latency
- **Progressive Enhancement**: Core functionality works without JavaScript

### Real-Time Monitoring
- **Live Container Status**: Running/stopped states with color indicators
- **Resource Metrics**: CPU, memory, disk usage with visual bars
- **Instant Updates**: WebSocket-based real-time data streaming
- **Auto-Refresh**: Automatic status updates every 5 seconds

### Container Management
- **Create Containers**: One-click container creation with templates
- **Quick Actions**: Start/stop/restart/backup operations
- **Access Methods**: Direct command copying and SSH access info
- **Details View**: Comprehensive container information and configuration

### Integration Features
- **DevContainer Agent API**: Direct integration with Python backend
- **OpenCode Configuration**: AI assistant setup with provider management
- **Template Support**: Pre-configured project environments
- **Error Handling**: Graceful error display with user-friendly messages

## 🛠️ Technical Architecture

### Backend (Python Flask)
```python
# Core Components
app.py                    # Main Flask application
/api/                     # API endpoints
  - containers.py          # Container management
  - monitoring.py          # Resource monitoring
static/                   # Static web assets
templates/                # HTML templates
```

### Frontend (Vanilla JS)
```javascript
// Core Components
app.js                    # Main application logic
WebSocket Client            # Real-time communication
API Integration            # Backend communication
Mobile Touch Support       # Gesture handling
```

### Responsive Design
```css
/* Mobile-First CSS */
.container-grid          # 1 column (mobile) -> 2 columns (tablet) -> 3+ columns (desktop)
.touch-action          # Enable horizontal swipes
.min-height: 44px       # iOS touch targets
.responsive-breakpoints   # Optimized for all screen sizes
```

## 📊 API Endpoints

### Container Management
```bash
GET  /api/containers              # List all containers
POST /api/containers              # Create new container
GET  /api/containers/{id}           # Get container details
POST /api/containers/{id}/start   # Start container
POST /api/containers/{id}/stop    # Stop container
POST /api/containers/{id}/restart # Restart container
```

### Configuration
```bash
POST /api/containers/{id}/configure-opencode  # Configure OpenCode
POST /api/containers/{id}/backup           # Create backup
```

### Monitoring
```bash
GET  /api/container/{id}/monitor          # Get resource usage
GET  /api/health                        # Health check
```

## 🎯 Usage Examples

### Basic Container Creation
```javascript
// Via Web UI
// 1. Click "Create Container" button
// 2. Fill form: Project name, VMID, template type
// 3. Submit to create container with chosen template
```

### Programmatic Access
```bash
# Create web development container
curl -X POST http://localhost:8080/api/containers \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "my-web-app",
    "template_type": "web"
  }'

# Get all containers
curl http://localhost:8080/api/containers
```

### WebSocket Integration
```javascript
// Real-time updates
socket.on('containers_update', function(data) {
    console.log('Containers updated:', data.containers);
});

// Request manual refresh
socket.emit('refresh_containers');

// Error handling
socket.on('error', function(error) {
    console.error('Socket error:', error);
});
```

## 📱 Mobile Features

### Touch Interactions
- **Swipe Navigation**: Horizontal swipes for quick actions
- **Touch Targets**: 44px minimum button height
- **Pull to Refresh**: Pull down gesture to refresh container list
- **Tap Actions**: Single tap for container operations
- **Long Press**: Context menus for additional options

### Responsive Design
- **Mobile (320px-480px)**: Single column, large touch targets
- **Phablet (481px-768px)**: Single column, optimized for one-handed use
- **Tablet (769px-1024px)**: Multi-column layout, larger touch areas
- **Desktop (1025px+)**: Multi-column grid, hover states

### Performance Optimizations
- **Lazy Loading**: Load data as needed for mobile
- **Minified Assets**: Optimized CSS and JavaScript
- **Caching**: Browser caching for faster subsequent loads
- **Compression**: Gzip compression for reduced bandwidth

## 🔧 Configuration

### Environment Variables
```bash
# Server Configuration
HOST=0.0.0.0                    # Server bind address
PORT=8080                          # Server port
DEBUG=false                         # Debug mode flag

# DevContainer Integration
DEVCONTAINER_AGENT=/opt/lxc-dev-template/subagents/devcontainer-manager.py  # Agent path
API_TIMEOUT=30                     # API request timeout
WS_HEARTBEAT=25                   # WebSocket heartbeat interval
```

### Logging
```bash
# Application Logs
/var/log/devcontainer/web-dashboard.log          # Main application log
/var/log/devcontainer/error.log                # Error log
/var/log/devcontainer/api.log                  # API request log

# Log Rotation
/etc/logrotate.d/devcontainer-dashboard          # Log rotation config
```

### Security
```bash
# CORS Settings
ALLOWED_ORIGINS=["http://localhost:8080", "http://your-host:8080"]

# Rate Limiting
REQUEST_LIMIT=100                     # Requests per minute
Burst_LIMIT=20                        # Burst capacity

# Authentication (optional)
ENABLE_AUTH=false                     # Basic auth toggle
SECRET_KEY="devcontainer-monitor-secret"  # Session secret
```

## 🚀 Deployment

### Development Mode
```bash
# Start with debug and auto-reload
cd /opt/lxc-dev-template/web
python3 app.py --debug --reload

# Watch for file changes
python3 app.py --debug --reload --watch
```

### Production Mode
```bash
# Start with production WSGI server
cd /opt/lxc-dev-template/web
gunicorn --workers 4 --bind 0.0.0.0:8080 app:app

# Or with systemd service
systemctl start devcontainer-dashboard
systemctl enable devcontainer-dashboard
```

### Systemd Service
```ini
# /etc/systemd/system/devcontainer-dashboard.service
[Unit]
Description=DevContainer Monitor Web Dashboard
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/lxc-dev-template/web
ExecStart=/usr/local/bin/start-dashboard.sh --production
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## 🔍 Testing

### Mobile Testing
```bash
# Chrome DevTools Device Mode
# 1. Open http://localhost:8080
# 2. F12 -> Device Toolbar -> Mobile devices
# 3. Test on iPhone (320px), iPad (768px), Android (360px)

# Responsive Testing
curl -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1" \
  http://localhost:8080/api/containers
```

### Performance Testing
```bash
# Load testing
ab -n 100 -c 10 http://localhost:8080/api/containers

# WebSocket stress test
node websocket-stress-test.js ws://localhost:8080
```

### API Testing
```bash
# Health check
curl http://localhost:8080/api/health

# Container operations
curl -X POST http://localhost:8080/api/containers/1001/start
curl -X GET http://localhost:8080/api/containers/1001

# Error simulation
curl -X POST http://localhost:8080/api/containers/9999/start
```

## 📊 Monitoring

### Metrics Collection
```javascript
// Real-time monitoring
setInterval(() => {
    socket.emit('request_containers');
}, 5000); // Every 5 seconds

// Performance monitoring
performance.mark('api-call-start');
fetch('/api/containers').then(() => {
    performance.mark('api-call-end');
    const duration = performance.getEntriesByName('api-call')[0].duration;
    console.log(`API call took: ${duration}ms`);
});
```

### Resource Visualization
```css
/* Animated resource bars */
.metric-fill {
    transition: width 0.5s ease;
    background: linear-gradient(90deg, #28a745, #1e88e5);
}

/* Pulse animation for status indicators */
.status-indicator.online {
    animation: pulse 2s infinite;
}
```

## 🔄 Troubleshooting

### Common Issues

#### WebSocket Connection Failed
```bash
# Check if WebSocket server is running
curl -I http://localhost:8080/socket.io/

# Check network connectivity
telnet localhost 8080

# Debug WebSocket connection
# In browser console: socket.connected === false
```

#### API Requests Fail
```bash
# Check if Flask app is running
curl -I http://localhost:8080/api/health

# Test DevContainer agent
python3 /opt/lxc-dev-template/subagents/devcontainer-manager.py list

# Check permissions
ls -la /opt/lxc-dev-template/subagents/devcontainer-manager.py
```

#### Mobile Performance Issues
```bash
# Minimize JavaScript bundle size
python3 -m jsmin static/js/app.js > static/js/app.min.js

# Enable compression
# In Flask app: app.config['COMPRESSOR_STATIC_FILTER'] = True

# Optimize images
# Use WebP format and proper sizing
```

### Debug Mode
```bash
# Enable detailed logging
./start-dashboard.sh --debug

# Monitor all requests
tail -f /var/log/devcontainer/api.log

# Check WebSocket messages
# In browser: socket.emit('test', 'message')
```

## 🎯 Best Practices

### Mobile Optimization
- **Minimize HTTP Requests**: Batch API calls when possible
- **Use Efficient Animations**: CSS transitions instead of JavaScript
- **Optimize Images**: Proper sizing and WebP format
- **Enable Caching**: Leverage browser caching effectively
- **Test Real Devices**: Not just emulators

### Security Considerations
- **HTTPS in Production**: Use SSL certificates
- **CORS Configuration**: Proper origin handling
- **Rate Limiting**: Prevent abuse and DoS attacks
- **Input Validation**: Sanitize all user inputs
- **Secure Headers**: Proper security headers

### Performance Optimization
- **WebSocket Optimization**: Binary messages, compression
- **Database Efficiency**: Proper indexing and queries
- **Asset Optimization**: Minified, compressed static files
- **Monitoring**: Track performance metrics and bottlenecks

---

## 🎉 Ready for Production

The web dashboard provides a complete, mobile-first interface for monitoring LXC development containers with real-time updates, responsive design, and seamless integration with the DevContainer manager agent. It's optimized for performance on both mobile and desktop devices and provides comprehensive container management capabilities.