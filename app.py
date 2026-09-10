<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Management System</title>
    <style>
        :root {
            --primary-color: #2575fc;
            --secondary-color: #6a11cb;
            --bg-color: #f4f7f6;
            --card-bg: #ffffff;
            --text-color: #333333;
            --danger-color: #ff4b5c;
            --success-color: #28a745;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 900px;
            margin: 40px auto;
            background: var(--card-bg);
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        h2, h3 {
            color: var(--secondary-color);
            text-align: center;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
        }

        input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 6px;
            box-sizing: border-box;
            font-size: 16px;
        }

        button {
            background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            font-weight: bold;
            transition: opacity 0.3s;
        }

        button:hover {
            opacity: 0.9;
        }

        .hidden {
            display: none !important;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th, td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: center;
        }

        th {
            background-color: var(--primary-color);
            color: white;
        }

        tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        .action-btns button {
            padding: 6px 12px;
            margin: 0 2px;
            font-size: 14px;
            width: auto;
        }

        .delete-btn {
            background: var(--danger-color);
        }

        .edit-btn {
            background: var(--success-color);
        }

        .logout-btn {
            background: #6c757d;
            width: auto;
            float: right;
            margin-bottom: 20px;
        }

        .error-msg {
            color: var(--danger-color);
            text-align: center;
            margin-top: 10px;
            font-weight: bold;
        }
    </style>
</head>
<body>

<div class="container">
    <!-- Login Section -->
    <div id="loginSection">
        <h2>లాగిన్ అవ్వండి (Login)</h2>
        <div class="form-group">
            <label>యూజర్‌నేమ్ (Username):</label>
            <input type="text" id="loginUser" placeholder="యూజర్‌నేమ్ నమోదు చేయండి">
        </div>
        <div class="form-group">
            <label>పాస్‌వర్డ్ (Password):</label>
            <input type="password" id="loginPass" placeholder="పాస్‌వర్డ్ నమోదు చేయండి">
        </div>
        <button onclick="handleLogin()">లాగిన్</button>
        <div id="loginError" class="error-msg"></div>
    </div>

    <!-- Dashboard Section -->
    <div id="dashboardSection" class="hidden">
        <button class="logout-btn" onclick="handleLogout()">లాగౌట్</button>
        <h3>స్టాక్ మేనేజ్‌మెంట్ డాష్‌బోర్డ్</h3>

        <!-- Add Stock Form -->
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 25px;">
            <h4 id="formTitle" style="margin-top: 0;">కొత్త స్టాక్ జోడించండి</h4>
            <input type="hidden" id="editIndex" value="">
            <div class="form-group">
                <label>వస్తువు పేరు (Item Name):</label>
                <input type="text" id="itemName" placeholder="ఉదా: రైస్ బ్యాగ్">
            </div>
            <div class="form-group">
                <label>పరిమాణం (Quantity):</label>
                <input type="number" id="itemQty" placeholder="ఉదా: 50">
            </div>
            <div class="form-group">
                <label>ధర (Price):</label>
                <input type="number" id="itemPrice" placeholder="ఉదా: 1200">
            </div>
            <!-- Stock Adding Security Password Field -->
            <div class="form-group">
                <label>స్టాక్ యాడ్ చేయడానికి సెక్యూరిటీ కోడ్ (samsri25285):</label>
                <input type="password" id="stockSecurityPass" placeholder="samsri25285 నమోదు చేయండి">
            </div>
            <button onclick="saveStock()">స్టాక్ భద్రపరచండి (Save Stock)</button>
            <div id="stockError" class="error-msg"></div>
        </div>

        <!-- Stock Table -->
        <h3>ఉన్న స్టాక్ జాబితా (Stock List)</h3>
        <table>
            <thead>
                <tr>
                    <th>క్రమ సంఖ్య</th>
                    <th>వస్తువు పేరు</th>
                    <th>పరిమాణం</th>
                    <th>ధర (₹)</th>
                    <th>చర్యలు (Actions)</th>
                </tr>
            </thead>
            <tbody id="stockTableBody">
                <!-- Data dynamically inserted here -->
            </tbody>
        </table>
    </div>
</div>

<script>
    // Credentials definition as requested
    const VALID_USER = "manikanta";
    const VALID_PASS = "samsri2528";
    const STOCK_ADD_PASS = "samsri25285";

    let stocks = JSON.parse(localStorage.getItem('stocks_data')) || [];

    // Check if already logged in during session
    window.onload = function() {
        if(sessionStorage.getItem('isLoggedIn') === 'true') {
            showDashboard();
        }
    }

    function handleLogin() {
        const user = document.getElementById('loginUser').value.trim();
        const pass = document.getElementById('loginPass').value.trim();
        const errorDiv = document.getElementById('loginError');

        if(user === VALID_USER && pass === VALID_PASS) {
            sessionStorage.setItem('isLoggedIn', 'true');
            errorDiv.textContent = "";
            showDashboard();
        } else {
            errorDiv.textContent = "తప్పు యూజర్‌నేమ్ లేదా పాస్‌వర్డ్!";
        }
    }

    function showDashboard() {
        document.getElementById('loginSection').classList.add('hidden');
        document.getElementById('dashboardSection').classList.remove('hidden');
        renderTable();
    }

    function handleLogout() {
        sessionStorage.removeItem('isLoggedIn');
        document.getElementById('dashboardSection').classList.add('hidden');
        document.getElementById('loginSection').classList.remove('hidden');
        document.getElementById('loginUser').value = "";
        document.getElementById('loginPass').value = "";
    }

    function saveStock() {
        const name = document.getElementById('itemName').value.trim();
        const qty = document.getElementById('itemQty').value.trim();
        const price = document.getElementById('itemPrice').value.trim();
        const secPass = document.getElementById('stockSecurityPass').value.trim();
        const editIdx = document.getElementById('editIndex').value;
        const errorDiv = document.getElementById('stockError');

        // Validation for security password to add/edit stock
        if(secPass !== STOCK_ADD_PASS) {
            errorDiv.textContent = "స్టాక్ మార్చడానికి సరైన సెక్యూరిటీ కోడ్ (samsri25285) అవసరం!";
            return;
        }

        if(!name || !qty || !price) {
            errorDiv.textContent = "దయచేసి అన్ని వివరాలను నింపండి!";
            return;
        }

        errorDiv.textContent = "";

        if(editIdx === "") {
            // Add new
            stocks.push({ name, qty, price });
        } else {
            // Update existing
            stocks[editIdx] = { name, qty, price };
            document.getElementById('editIndex').value = "";
            document.getElementById('formTitle').textContent = "కొత్త స్టాక్ జోడించండి";
        }

        localStorage.setItem('stocks_data', JSON.stringify(stocks));
        clearForm();
        renderTable();
    }

    function clearForm() {
        document.getElementById('itemName').value = "";
        document.getElementById('itemQty').value = "";
        document.getElementById('itemPrice').value = "";
        document.getElementById('stockSecurityPass').value = "";
    }

    function renderTable() {
        const tbody = document.getElementById('stockTableBody');
        tbody.innerHTML = "";

        if(stocks.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5">ఎటువంటి స్టాక్ అందుబాటులో లేదు</td></tr>`;
            return;
        }

        stocks.forEach((item, index) => {
            let tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${index + 1}</td>
                <td>${item.name}</td>
                <td>${item.qty}</td>
                <td>₹${item.price}</td>
                <td class="action-btns">
                    <button class="edit-btn" onclick="editStock(${index})">మార్చు</button>
                    <button class="delete-btn" onclick="deleteStock(${index})">తొలగించు</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }

    function editStock(index) {
        const sec = prompt("స్టాక్ ఎడిట్ చేయడానికి సెక్యూరిటీ కోడ్ (samsri25285) ఎంటర్ చేయండి:");
        if(sec !== STOCK_ADD_PASS) {
            alert("తప్పు కోడ్! అనుమతి నిరాకరించబడింది.");
            return;
        }

        const item = stocks[index];
        document.getElementById('itemName').value = item.name;
        document.getElementById('itemQty').value = item.qty;
        document.getElementById('itemPrice').value = item.price;
        document.getElementById('editIndex').value = index;
        document.getElementById('formTitle').textContent = "స్టాక్ వివరాలను సవరించండి";
    }

    function deleteStock(index) {
        const sec = prompt("స్టాక్ తొలగించడానికి సెక్యూరిటీ కోడ్ (samsri25285) ఎంటర్ చేయండి:");
        if(sec !== STOCK_ADD_PASS) {
            alert("తప్పు కోడ్! అనుమతి నిరాకరించబడింది.");
            return;
        }

        if(confirm("మీరు నిజంగా ఈ స్టాక్‌ను తొలగించాలనుకుంటున్నారా?")) {
            stocks.splice(index, 1);
            localStorage.setItem('stocks_data', JSON.stringify(stocks));
            renderTable();
        }
    }
</script>

</body>
</html>
