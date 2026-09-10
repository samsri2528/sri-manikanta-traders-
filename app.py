<?php
session_start();

// సింపుల్ డేటాబేస్ కనెక్షన్ (మీ వివరాల ప్రకారం మార్చుకోండి)
$host = "localhost";
$user = "root";
$password = "";
$dbname = "stock_db";

$conn = new mysqli($host, $user, $password, $dbname);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// టేబుల్ లేకపోతే ఆటోమేటిక్‌గా క్రియేట్ అవ్వడానికి
$conn->query("CREATE TABLE IF NOT EXISTS stock_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL
)");

$msg = "";
$error = "";

// లాగిన్ హ్యాండ్లింగ్
if (isset($_POST['login_btn'])) {
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);

    if ($username === 'admin' && $password === 'manikanta123') {
        $_SESSION['user'] = 'admin';
        $_SESSION['role'] = 'admin';
    } elseif ($username === 'manikanta' && $password === 'samsri2528') {
        $_SESSION['user'] = 'manikanta';
        $_SESSION['role'] = 'staff';
    } else {
        $error = "యూజర్‌నేమ్ లేదా పాస్‌వర్డ్ తప్పుగా ఉంది!";
    }
}

// స్టాక్ యాడ్ హ్యాండ్లింగ్
if (isset($_POST['add_stock_btn'])) {
    $auth_code = trim($_POST['auth_code']);
    
    if ($auth_code === 'samsri25285') {
        $item_name = $conn->real_escape_string($_POST['item_name']);
        $quantity = intval($_POST['quantity']);
        $price = floatval($_POST['price']);

        $sql = "INSERT INTO stock_items (item_name, quantity, price) VALUES ('$item_name', $quantity, $price)";
        
        if ($conn->query($sql) === TRUE) {
            $msg = "కొత్త స్టాక్ విజయవంతంగా యాడ్ చేయబడింది!";
        } else {
            $error = "సమస్య ఏర్పడింది: " . $conn->error;
        }
    } else {
        $error = "స్టాక్ యాడ్ చేయడానికి తప్పు సీక్రెట్ కోడ్ ('samsri25285') ఎంటర్ చేసారు!";
    }
}

// లాగౌట్
if (isset($_GET['logout'])) {
    session_destroy();
    header("Location: " . $_SERVER['PHP_SELF']);
    exit();
}
?>

<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <title>స్టాక్ మేనేజ్‌మెంట్ సిస్టమ్</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: white; padding: 30px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); width: 350px; }
        h2 { text-align: center; margin-bottom: 20px; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; }
        .form-group input { width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
        .btn { width: 100%; background: #007BFF; color: white; border: none; padding: 10px; border-radius: 4px; cursor: pointer; }
        .btn:hover { background: #0056b3; }
        .btn-green { background: #28a745; }
        .btn-green:hover { background: #218838; }
        .error { color: red; text-align: center; margin-bottom: 10px; font-size: 14px; }
        .msg { color: green; text-align: center; margin-bottom: 10px; font-size: 14px; font-weight: bold; }
        .logout-link { text-align: right; margin-bottom: 10px; }
        .logout-link a { color: red; text-decoration: none; font-size: 14px; }
    </style>
</head>
<body>

<div class="box">
    <?php if (!isset($_SESSION['user'])): ?>
        <!-- 1. లాగిన్ ఫారం -->
        <h2>లాగిన్ అవ్వండి</h2>
        <?php if($error != "") { echo "<div class='error'>$error</div>"; } ?>
        <form method="POST" action="">
            <div class="form-group">
                <label>యూజర్‌నేమ్:</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>పాస్‌వర్డ్:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit" name="login_btn" class="btn">లాగిన్</button>
        </form>

    <?php else: ?>
        <!-- 2. కొత్త స్టాక్ యాడ్ చేసే ఫారం -->
        <div class="logout-link"><a href="?logout=true">లాగౌట్ (Logout)</a></div>
        <h2>కొత్త స్టాక్ యాడ్ చేయండి</h2>
        <?php if($error != "") { echo "<div class='error'>$error</div>"; } ?>
        <?php if($msg != "") { echo "<div class='msg'>$msg</div>"; } ?>
        
        <form method="POST" action="">
            <div class="form-group">
                <label>వస్తువు పేరు (Item Name):</label>
                <input type="text" name="item_name" required>
            </div>
            <div class="form-group">
                <label>పరిమాణం (Quantity):</label>
                <input type="number" name="quantity" required>
            </div>
            <div class="form-group">
                <label>ధర (Price):</label>
                <input type="text" name="price" required>
            </div>
            <div class="form-group">
                <label>స్టాక్ కోడ్ (samsri25285):</label>
                <input type="password" name="auth_code" required placeholder="samsri25285 ఎంటర్ చేయండి">
            </div>
            <button type="submit" name="add_stock_btn" class="btn btn-green">స్టాక్ సేవ్ చేయి</button>
        </form>
    <?php endif; ?>
</div>

</body>
</html>
