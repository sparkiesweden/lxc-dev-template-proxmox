// DevContainer Monitor - JavaScript for mobile-responsive container monitoring

let socket;
let containers = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeWebSocket();
    refreshContainers();
});

// WebSocket initialization
function initializeWebSocket() {
    socket = io();
    
    socket.on('connect', function() {
        updateConnectionStatus('online');
        showToast('Connected to DevContainer Manager', 'success');
    });
    
    socket.on('disconnect', function() {
        updateConnectionStatus('offline');
        showToast('Disconnected from DevContainer Manager', 'error');
    });
    
    socket.on('containers_update', function(data) {
        if (data.success) {
            containers = data.containers || [];
            renderContainers();
        }
    });
    
    socket.on('error', function(data) {
        showToast(data.message, 'error');
    });
    
    socket.on('notification', function(data) {
        showToast(data.message, data.type);
    });
}

// Connection status update
function updateConnectionStatus(status) {
    const indicator = document.getElementById('connection-status').querySelector('.status-indicator');
    const text = document.getElementById('connection-status').querySelector('.status-text');
    
    indicator.className = `status-indicator ${status}`;
    
    switch(status) {
        case 'online':
            text.textContent = 'Connected';
            break;
        case 'connecting':
            indicator.className = 'status-indicator connecting';
            text.textContent = 'Connecting...';
            break;
        case 'offline':
            text.textContent = 'Offline';
            break;
    }
}

// Container rendering
function renderContainers() {
    const grid = document.getElementById('containers-grid');
    const count = document.getElementById('container-count').querySelector('.status-number');
    
    count.textContent = containers.length;
    
    if (containers.length === 0) {
        grid.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📦</div>
                <h3>No Containers Found</h3>
                <p>Create your first development container to get started.</p>
                <button class="btn btn-primary" onclick="showCreateModal()">Create Container</button>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = containers.map(container => createContainerCard(container)).join('');
}

function createContainerCard(container) {
    const statusClass = container.status === 'running' ? 'running' : 'stopped';
    const statusText = container.status === 'running' ? 'Running' : 'Stopped';
    const statusIcon = container.status === 'running' ? '🟢' : '🔴';
    const ipDisplay = container.ip || 'No IP';
    const accessMethods = getAccessMethods(container);
    
    return `
        <div class="container-card ${statusClass}" onclick="showContainerDetails('${container.vmid}')">
            <div class="container-header">
                <div class="container-name">${container.name}</div>
                <div class="container-status ${statusClass}">${statusText}</div>
            </div>
            <div class="container-info">
                <div class="info-item">
                    <span class="info-label">VMID:</span>
                    <span class="info-value">${container.vmid}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">IP:</span>
                    <span class="info-value">${ipDisplay}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Status:</span>
                    <span class="info-value">${statusIcon} ${statusText}</span>
                </div>
            </div>
            <div class="container-actions">
                ${container.status === 'running' ? `
                    <button class="action-btn" onclick="event.stopPropagation(); startContainer('${container.vmid}')">
                        <span class="action-icon">🔄</span>
                        <span class="action-label">Restart</span>
                    </button>
                    <button class="action-btn" onclick="event.stopPropagation(); stopContainer('${container.vmid}')">
                        <span class="action-icon">⏹</span>
                        <span class="action-label">Stop</span>
                    </button>
                    <button class="action-btn" onclick="event.stopPropagation(); configureOpenCode('${container.vmid}')">
                        <span class="action-icon">🤖</span>
                        <span class="action-label">OpenCode</span>
                    </button>
                ` : `
                    <button class="action-btn" onclick="event.stopPropagation(); startContainer('${container.vmid}')">
                        <span class="action-icon">▶️</span>
                        <span class="action-label">Start</span>
                    </button>
                `}
                <button class="action-btn" onclick="event.stopPropagation(); backupContainer('${container.vmid}')">
                    <span class="action-icon">💾</span>
                    <span class="action-label">Backup</span>
                </button>
            </div>
        </div>
    `;
}

function getAccessMethods(container) {
    if (!container.ip || container.ip === 'No IP') {
        return [];
    }
    
    return [
        `pct enter ${container.vmid}`,
        `ssh developer@${container.ip}`,
        `http://${container.ip}:8080` // If web services are running
    ];
}

// API calls
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(`/api/${endpoint}`, options);
        const result = await response.json();
        
        if (result.success) {
            return result;
        } else {
            showToast(result.error || 'Operation failed', 'error');
            return null;
        }
    } catch (error) {
        showToast(`Network error: ${error.message}`, 'error');
        return null;
    }
}

// Container operations
async function refreshContainers() {
    const containers = await apiCall('containers');
    if (containers) {
        renderContainers();
    }
}

async function startContainer(vmid) {
    showToast(`Starting container ${vmid}...`, 'warning');
    const result = await apiCall(`container/${vmid}/start`, 'POST');
    if (result && result.success) {
        showToast(`Container ${vmid} started successfully`, 'success');
        setTimeout(refreshContainers, 2000);
    }
}

async function stopContainer(vmid) {
    if (confirm(`Are you sure you want to stop container ${vmid}?`)) {
        showToast(`Stopping container ${vmid}...`, 'warning');
        const result = await apiCall(`container/${vmid}/stop`, 'POST');
        if (result && result.success) {
            showToast(`Container ${vmid} stopped successfully`, 'success');
            setTimeout(refreshContainers, 2000);
        }
    }
}

async function restartContainer(vmid) {
    showToast(`Restarting container ${vmid}...`, 'warning');
    const result = await apiCall(`container/${vmid}/restart`, 'POST');
    if (result && result.success) {
        showToast(`Container ${vmid} restarted successfully`, 'success');
        setTimeout(refreshContainers, 3000);
    }
}

async function backupContainer(vmid) {
    showToast(`Creating backup of container ${vmid}...`, 'warning');
    const result = await apiCall(`container/${vmid}/backup`, 'POST');
    if (result && result.success) {
        showToast(`Backup created: ${result.backup_name}`, 'success');
    }
}

async function configureOpenCode(vmid) {
    if (confirm(`Configure OpenCode for container ${vmid}?`)) {
        showToast(`Configuring OpenCode for container ${vmid}...`, 'warning');
        const result = await apiCall(`container/${vmid}/configure-opencode`, 'POST', {
            providers: ['anthropic']
        });
        if (result && result.success) {
            showToast(`OpenCode configured successfully`, 'success');
        }
    }
}

async function createContainer(formData) {
    const result = await apiCall('containers', 'POST', formData);
    if (result && result.success) {
        showToast(`Container created: ${result.vmid}`, 'success');
        closeModal('create-modal');
        document.getElementById('create-form').reset();
        setTimeout(refreshContainers, 3000);
        
        // Show access methods
        const accessMethods = result.access_methods || [];
        if (accessMethods.length > 0) {
            showToast(`Access: ${accessMethods[0]}`, 'success');
        }
    }
}

async function showContainerDetails(vmid) {
    const result = await apiCall(`containers/${vmid}`);
    if (result && result.success) {
        displayContainerDetails(result);
    }
}

function displayContainerDetails(container) {
    const modal = document.getElementById('container-modal');
    const info = document.getElementById('modal-container-info');
    
    const statusClass = container.status === 'running' ? 'running' : 'stopped';
    const statusText = container.status === 'running' ? 'Running' : 'Stopped';
    
    info.innerHTML = `
        <div class="container-details">
            <div class="details-section">
                <h4>Basic Information</h4>
                <div class="info-grid">
                    <div class="info-item">
                        <span class="info-label">VMID:</span>
                        <span class="info-value">${container.vmid}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Name:</span>
                        <span class="info-value">${container.name}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Status:</span>
                        <span class="info-value"><span class="container-status ${statusClass}">${statusText}</span></span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">IP Address:</span>
                        <span class="info-value">${container.ip || 'N/A'}</span>
                    </div>
                </div>
            </div>
            
            <div class="details-section">
                <h4>Configuration</h4>
                <div class="config-display">
                    <pre>${container.config || 'Configuration not available'}</pre>
                </div>
            </div>
            
            ${container.resources ? `
                <div class="details-section">
                    <h4>Resource Usage</h4>
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="info-label">Memory:</span>
                            <span class="info-value">${container.resources.memory || 'N/A'}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Disk:</span>
                            <span class="info-value">${container.resources.disk || 'N/A'}</span>
                        </div>
                    </div>
                </div>
            ` : ''}
            
            <div class="details-section">
                <h4>Access Methods</h4>
                <div class="access-methods">
                    ${getAccessMethods(container).map(method => `
                        <div class="access-method">
                            <code>${method}</code>
                            <button class="copy-btn" onclick="copyToClipboard('${method}')">📋</button>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
    
    showModal('container-modal');
}

// Modal management
function showModal(modalId) {
    document.getElementById(modalId).classList.add('show');
    document.body.style.overflow = 'hidden';
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
    document.body.style.overflow = '';
}

// Create modal
function showCreateModal() {
    showModal('create-modal');
}

function showBackupModal() {
    if (confirm('Create backup of all running containers?')) {
        backupAllContainers();
    }
}

async function backupAllContainers() {
    const runningContainers = containers.filter(c => c.status === 'running');
    
    for (const container of runningContainers) {
        showToast(`Creating backup: ${container.vmid}...`, 'warning');
        await backupContainer(container.vmid);
    }
}

// Form submission
function createContainer(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = {
        project_name: formData.get('project_name'),
        vmid: formData.get('vmid') || '',
        template_type: formData.get('template_type')
    };
    
    createContainer(data);
}

// Utility functions
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copied to clipboard', 'success');
        }).catch(err => {
            console.error('Failed to copy: ', err);
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            document.execCommand('copy');
            showToast('Copied to clipboard', 'success');
        } catch (err) {
            console.error('Failed to copy: ', err);
        }
        
        document.body.removeChild(textArea);
    }
}

function showToast(message, type = 'info', duration = 3000) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    toast.innerHTML = `
        <span class="toast-message">${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    container.appendChild(toast);
    
    // Auto remove after duration
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, duration);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // ESC to close modals
    if (event.key === 'Escape') {
        document.querySelectorAll('.modal.show').forEach(modal => {
            modal.classList.remove('show');
        });
        document.body.style.overflow = '';
    }
    
    // Ctrl/Cmd + R to refresh
    if ((event.ctrlKey || event.metaKey) && event.key === 'r') {
        event.preventDefault();
        refreshContainers();
    }
    
    // Ctrl/Cmd + N to create new container
    if ((event.ctrlKey || event.metaKey) && event.key === 'n') {
        event.preventDefault();
        showCreateModal();
    }
});

// Pull-to-refresh support
let startY = 0;
let isPulling = false;

document.addEventListener('touchstart', function(e) {
    startY = e.touches[0].clientY;
    isPulling = false;
});

document.addEventListener('touchmove', function(e) {
    if (!isPulling) return;
    
    const currentY = e.touches[0].clientY;
    const diff = startY - currentY;
    
    // Pull down to refresh (pull threshold)
    if (diff > 100) {
        isPulling = true;
        refreshContainers();
    }
});

document.addEventListener('touchend', function() {
    setTimeout(() => {
        isPulling = false;
    }, 1000);
});

// Service Worker registration for offline support (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(registration => console.log('SW registered'))
            .catch(error => console.log('SW registration failed:', error));
    });
}