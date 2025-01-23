// Initialize Bootstrap modal
let messageModal;
document.addEventListener('DOMContentLoaded', function() {
    messageModal = new bootstrap.Modal(document.getElementById('messageModal'));
});

// Show message in modal
function showMessage(message) {
    document.getElementById('modalMessage').textContent = message;
    messageModal.show();
}

// Fetch and display network state
async function updateNetworkState() {
    try {
        const response = await fetch('/api/network-state');
        const data = await response.json();
        
        const stateDiv = document.getElementById('networkState');
        stateDiv.innerHTML = '';
        
        data.servers.forEach(server => {
            const serverBox = document.createElement('div');
            serverBox.className = 'server-box';
            serverBox.id = `server-${server}`;
            
            const dataItems = data.data[server].map(item => 
                `<span class="data-item" id="data-${item}">${item}</span>`
            ).join('');
            
            serverBox.innerHTML = `
                <h5>Server ${server}</h5>
                <div class="server-data">${dataItems}</div>
            `;
            stateDiv.appendChild(serverBox);
        });
    } catch (error) {
        showMessage('Error updating network state: ' + error.message);
    }
}

// Animate data movement
async function animateDataMovement(dataMovements, deletedServer) {
    const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
    
    // Highlight the server being deleted
    const deletedServerBox = document.getElementById(`server-${deletedServer}`);
    if (deletedServerBox) {
        deletedServerBox.classList.add('deleted');
    }
    
    // Animate each data movement
    for (const movement of dataMovements) {
        const dataElement = document.getElementById(`data-${movement.data}`);
        const targetServer = document.getElementById(`server-${movement.to_server}`);
        
        if (dataElement && targetServer) {
            // Highlight the data being moved
            dataElement.classList.add('moving');
            targetServer.classList.add('highlight');
            
            await delay(500); // Wait for animation
            
            // Move the data to the new server
            const targetDataContainer = targetServer.querySelector('.server-data');
            targetDataContainer.appendChild(dataElement);
            
            dataElement.classList.remove('moving');
            targetServer.classList.remove('highlight');
            
            await delay(300); // Wait between movements
        }
    }
    
    // Remove the deleted server
    if (deletedServerBox) {
        deletedServerBox.style.opacity = '0';
        await delay(300);
        deletedServerBox.remove();
    }
}

// Add data
async function addData() {
    const input = document.getElementById('addDataInput');
    const data = input.value;
    
    try {
        const response = await fetch('/api/add-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: data }),
        });
        
        const result = await response.json();
        showMessage(result.message);
        if (result.success) {
            input.value = '';
            updateNetworkState();
        }
    } catch (error) {
        showMessage('Error adding data: ' + error.message);
    }
}

// Find data
async function findData() {
    const input = document.getElementById('findDataInput');
    const data = input.value;
    
    try {
        const response = await fetch('/api/find-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: data }),
        });
        
        const result = await response.json();
        if (result.success) {
            showMessage(result.found ? 
                `Data found in server ${result.server}` : 
                'Data not found in any server');
        } else {
            showMessage(result.message);
        }
    } catch (error) {
        showMessage('Error finding data: ' + error.message);
    }
}

// Remove data
async function removeData() {
    const input = document.getElementById('removeDataInput');
    const data = input.value;
    
    try {
        const response = await fetch('/api/remove-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: data }),
        });
        
        const result = await response.json();
        showMessage(result.message);
        if (result.success) {
            input.value = '';
            updateNetworkState();
        }
    } catch (error) {
        showMessage('Error removing data: ' + error.message);
    }
}

// Add server
async function addServer() {
    try {
        const response = await fetch('/api/add-server', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
        const result = await response.json();
        showMessage(result.message);
        if (result.success) {
            updateNetworkState();
        }
    } catch (error) {
        showMessage('Error adding server: ' + error.message);
    }
}

// Remove server
async function removeServer() {
    const input = document.getElementById('removeServerInput');
    const serverIndex = parseInt(input.value);
    
    try {
        const response = await fetch('/api/remove-server', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ serverIndex: serverIndex }),
        });
        
        const result = await response.json();
        if (result.success) {
            // Animate the data movement
            await animateDataMovement(result.data_movement, result.deleted_server);
            input.value = '';
            showMessage('Server removed successfully');
        } else {
            showMessage(result.message);
        }
    } catch (error) {
        showMessage('Error removing server: ' + error.message);
    }
}

// Update network state on page load
updateNetworkState(); 