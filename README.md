# Papiprints 🖨️

A printing services backend built with FastAPI for campus printing management.

## Overview
Papiprints provides a fast API for students to submit print orders, with automatic cost calculation and order management for staff. The system eliminates long queues and manual calculations.

## Features

✅ Submit print orders (black & white, colored, photo paper)  
✅ Automatic cost calculation based on document properties  
✅ View all orders (admin dashboard)  
✅ Track individual orders by ID  
✅ Update order status (pending → completed)  
✅ View student order history  

## Installation & Setup

### Backend Setup (FastAPI)

1. **Create virtual environment:**
   ```bash
   cd d:\prints
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

The API will be running at: **http://127.0.0.1:8000**

View interactive API docs: **http://127.0.0.1:8000/docs**

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/orders` | Create a new print order |
| **GET** | `/orders` | List all orders (admin) |
| **GET** | `/orders/{order_id}` | Get specific order details |
| **PATCH** | `/orders/{order_id}/status` | Update order status |
| **GET** | `/users/{user_id}/orders` | Get student's orders |

### Example Request - Create Order
```bash
POST http://127.0.0.1:8000/orders
Content-Type: application/json

{
  "user_id": "student_001",
  "pages": 10,
  "print_type": "black_white",
  "filename": "assignment.pdf"
}
```

### Example Response
```json
{
  "user_id": "student_001",
  "pages": 10,
  "print_type": "black_white",
  "filename": "assignment.pdf",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "cost": 20.0,
  "created_at": "2026-03-03T12:00:00"
}
```

---

## Pricing

| Print Type | Price |
|-----------|-------|
| 🖤 Black & White | PHP 2.00/page |
| 🌈 Colored | PHP 5.00/page |
| 📸 Photo Paper | PHP 20.00/page |

---

## Frontend Integration (HTML + CSS + JavaScript)

### Step 1: Create the Frontend Files

Create two files in a folder (e.g., `D:\prints\frontend\`):

```html
<!DOCTYPE html>
<html>
<head>
    <title>Papiprints Student Portal</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        .form-group { margin-bottom: 15px; }
        label { font-weight: bold; }
        input, select { padding: 5px; width: 200px; }
        button { padding: 8px 15px; background: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background: #45a049; transform: brightness(0.9); }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: white; 
            padding: 30px; 
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        .success { background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
        .error { background-color: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
        .info { background-color: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; }
        .message { 
            margin-top: 20px; 
            padding: 15px; 
            border-radius: 5px; 
            display: none;
        }
        .message.show { display: block; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        table th, table td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        table th { background-color: #4CAF50; color: white; }
        .tab-buttons { display: flex; gap: 10px; margin-bottom: 20px; }
        .tab-button { padding: 10px 20px; background: #ddd; border: none; cursor: pointer; border-radius: 5px; }
        .tab-button.active { background: #4CAF50; color: white; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖨️ Papiprints - Student Portal</h1>
        
        <!-- Tab Navigation -->
        <div class="tab-buttons">
            <button class="tab-button active" onclick="switchTab('submit')">📝 Submit Order</button>
            <button class="tab-button" onclick="switchTab('history')">📋 My Orders</button>
            <button class="tab-button" onclick="switchTab('admin')">⚙️ Admin View</button>
        </div>

        <!-- TAB 1: Submit Order -->
        <div id="submit" class="tab-content active">
            <h2>Submit New Print Order</h2>
            
            <div class="form-group">
                <label>Student ID:</label>
                <input type="text" id="userId" placeholder="e.g. student_001" />
            </div>
            
            <div class="form-group">
                <label>Number of Pages:</label>
                <input type="number" id="pages" placeholder="e.g. 10" min="1" />
            </div>
            
            <div class="form-group">
                <label>Print Type:</label>
                <select id="printType" onchange="calculateCost()">
                    <option value="black_white">🖤 Black & White (PHP 2.00/page)</option>
                    <option value="colored">🌈 Colored (PHP 5.00/page)</option>
                    <option value="photo">📸 Photo Paper (PHP 20.00/page)</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Filename (optional):</label>
                <input type="text" id="filename" placeholder="e.g. assignment.pdf" />
            </div>

            <div class="form-group">
                <label><strong>Estimated Cost:</strong> <span id="costDisplay">PHP 0.00</span></label>
            </div>
            
            <button onclick="submitOrder()">🚀 Submit Order</button>
            
            <div id="submitResult" class="message"></div>
        </div>

        <!-- TAB 2: My Orders (History) -->
        <div id="history" class="tab-content">
            <h2>My Print Orders</h2>
            
            <div class="form-group">
                <label>Enter Student ID:</label>
                <input type="text" id="studentIdForHistory" placeholder="e.g. student_001" />
                <button onclick="fetchStudentOrders()">Search Orders</button>
            </div>
            
            <div id="ordersTable"></div>
            <div id="historyResult" class="message"></div>
        </div>

        <!-- TAB 3: Admin View -->
        <div id="admin" class="tab-content">
            <h2>Admin - All Orders</h2>
            <button onclick="fetchAllOrders()">🔄 Refresh Orders</button>
            <div id="adminTable"></div>
            <div id="adminResult" class="message"></div>
        </div>
    </div>

    <script>
        const API_URL = 'http://127.0.0.1:8000';
        const PRICES = {
            'black_white': 2.0,
            'colored': 5.0,
            'photo': 20.0
        };

        // Tab Switching
        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remove active class from all buttons
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            
            // Highlight button
            event.target.classList.add('active');
        }

        // Calculate cost in real-time
        function calculateCost() {
            const pages = parseInt(document.getElementById('pages').value) || 0;
            const printType = document.getElementById('printType').value;
            const price = PRICES[printType];
            const totalCost = pages * price;
            document.getElementById('costDisplay').innerText = `PHP ${totalCost.toFixed(2)}`;
        }

        // Add listener for pages input
        document.getElementById('pages').addEventListener('input', calculateCost);

        // Submit New Order
        async function submitOrder() {
            const userId = document.getElementById('userId').value.trim();
            const pages = parseInt(document.getElementById('pages').value);
            const printType = document.getElementById('printType').value;
            const filename = document.getElementById('filename').value.trim();

            if (!userId || !pages) {
                showMessage('submitResult', 'error', '❌ Please fill in Student ID and Pages');
                return;
            }

            try {
                const response = await fetch(`${API_URL}/orders`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        user_id: userId,
                        pages: pages,
                        print_type: printType,
                        filename: filename || null
                    })
                });

                const data = await response.json();
                
                if (response.ok) {
                    showMessage('submitResult', 'success', `
                        <h3>✅ Order Created Successfully!</h3>
                        <p><strong>Order ID:</strong> ${data.id}</p>
                        <p><strong>Student:</strong> ${data.user_id}</p>
                        <p><strong>Pages:</strong> ${data.pages}</p>
                        <p><strong>Type:</strong> ${data.print_type}</p>
                        <p><strong>Total Cost:</strong> PHP ${data.cost.toFixed(2)}</p>
                        <p><strong>Status:</strong> ${data.status}</p>
                        <p><strong>Created:</strong> ${new Date(data.created_at).toLocaleString()}</p>
                    `);
                    // Clear form
                    document.getElementById('userId').value = '';
                    document.getElementById('pages').value = '';
                    document.getElementById('filename').value = '';
                } else {
                    showMessage('submitResult', 'error', `❌ Error: ${data.detail || 'Unknown error'}`);
                }
            } catch (error) {
                showMessage('submitResult', 'error', `❌ Connection Error: ${error.message}`);
            }
        }

        // Fetch Student Orders
        async function fetchStudentOrders() {
            const studentId = document.getElementById('studentIdForHistory').value.trim();
            if (!studentId) {
                showMessage('historyResult', 'error', '❌ Please enter a Student ID');
                return;
            }

            try {
                const response = await fetch(`${API_URL}/users/${studentId}/orders`);
                const orders = await response.json();

                if (Array.isArray(orders) && orders.length > 0) {
                    let tableHTML = '<table><tr><th>Order ID</th><th>Pages</th><th>Type</th><th>Cost (PHP)</th><th>Status</th><th>Created</th></tr>';
                    orders.forEach(order => {
                        tableHTML += `<tr>
                            <td>${order.id.substring(0, 8)}...</td>
                            <td>${order.pages}</td>
                            <td>${order.print_type}</td>
                            <td>${order.cost.toFixed(2)}</td>
                            <td><strong>${order.status}</strong></td>
                            <td>${new Date(order.created_at).toLocaleDateString()}</td>
                        </tr>`;
                    });
                    tableHTML += '</table>';
                    document.getElementById('ordersTable').innerHTML = tableHTML;
                    showMessage('historyResult', 'success', `✅ Found ${orders.length} order(s)`);
                } else {
                    document.getElementById('ordersTable').innerHTML = '';
                    showMessage('historyResult', 'info', 'ℹ️ No orders found for this student');
                }
            } catch (error) {
                showMessage('historyResult', 'error', `❌ Error: ${error.message}`);
            }
        }

        // Fetch All Orders (Admin)
        async function fetchAllOrders() {
            try {
                const response = await fetch(`${API_URL}/orders`);
                const orders = await response.json();

                if (Array.isArray(orders) && orders.length > 0) {
                    let tableHTML = '<table><tr><th>Student</th><th>Order ID</th><th>Pages</th><th>Type</th><th>Cost (PHP)</th><th>Status</th><th>Action</th></tr>';
                    orders.forEach(order => {
                        tableHTML += `<tr>
                            <td>${order.user_id}</td>
                            <td>${order.id.substring(0, 8)}...</td>
                            <td>${order.pages}</td>
                            <td>${order.print_type}</td>
                            <td>${order.cost.toFixed(2)}</td>
                            <td>${order.status}</td>
                            <td><button onclick="updateOrderStatus('${order.id}')">Mark Done</button></td>
                        </tr>`;
                    });
                    tableHTML += '</table>';
                    document.getElementById('adminTable').innerHTML = tableHTML;
                    showMessage('adminResult', 'success', `✅ Total orders: ${orders.length}`);
                } else {
                    document.getElementById('adminTable').innerHTML = '<p>No orders found</p>';
                }
            } catch (error) {
                showMessage('adminResult', 'error', `❌ Error: ${error.message}`);
            }
        }

        // Update Order Status (Admin)
        async function updateOrderStatus(orderId) {
            try {
                const response = await fetch(`${API_URL}/orders/${orderId}/status`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ status: 'completed' })
                });

                if (response.ok) {
                    showMessage('adminResult', 'success', '✅ Order marked as completed!');
                    fetchAllOrders();
                } else {
                    showMessage('adminResult', 'error', '❌ Failed to update order');
                }
            } catch (error) {
                showMessage('adminResult', 'error', `❌ Error: ${error.message}`);
            }
        }

        // Helper function to show messages
        function showMessage(elementId, type, message) {
            const messageEl = document.getElementById(elementId);
            messageEl.className = `message show ${type}`;
            messageEl.innerHTML = message;
        }
    </script>
</body>
</html>
```

### Step 2: Save this as `index.html`

Save the HTML code above as a file named **`index.html`** in a folder like `D:\prints\frontend\`

### Step 3: Open in Browser

Simply **double-click the HTML file** or open it in your browser:
```
File → Open → d:\prints\frontend\index.html
```

Or use **Live Server** in VS Code:
1. Right-click the HTML file
2. Select "Open with Live Server"
3. Browser opens at `http://127.0.0.1:5500` (or similar)

---

## ✅ Final Verification

**Terminal 1 - Run Backend:**
```powershell
cd d:\prints
.\.venv\Scripts\activate
uvicorn main:app --reload
```

**Result:** Backend running at `http://127.0.0.1:8000`

**Terminal 2 (or separately):**
- Open your HTML file in the browser
- Or use Live Server extension in VS Code

**Now you can:**
1. ✏️ **Submit orders** from the form
2. 📋 **View your orders** by student ID
3. ⚙️ **Admin view** to see all orders and update status

---

## Frontend Features

🎯 **Three Tabs:**
- **Submit Order** - Create new print jobs with live cost calculation
- **My Orders** - Search orders by student ID
- **Admin View** - See all orders and mark them as complete

💡 **Real-time:**
- Cost updates automatically as you change pages/type
- Instant feedback after submitting
- Live order status updates

---

## Troubleshooting

**"API connection failed"**
- Make sure backend is running: `uvicorn main:app --reload`
- Check that API URL is `http://127.0.0.1:8000` in the HTML

**"CORS error"**
- Already enabled in `main.py` - refresh your browser

**"Can't find order"**
- Make sure you use the exact student ID you submitted with
