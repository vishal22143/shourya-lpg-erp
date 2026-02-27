<?php
// test_password.php - Use this to test password verification
// Put this in C:\xampp\htdocs\erp\test_password.php
// Then open: http://localhost/erp/test_password.php

// The hash we're using in the database
$stored_hash = '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi';

// The password we're trying
$password_to_test = '1234';

echo "<h2>Password Test</h2>";
echo "<p><strong>Testing password:</strong> " . htmlspecialchars($password_to_test) . "</p>";
echo "<p><strong>Against hash:</strong> " . htmlspecialchars($stored_hash) . "</p>";

// Test verification
$result = password_verify($password_to_test, $stored_hash);

if ($result) {
    echo "<p style='color:green;font-weight:bold;font-size:20px'>✅ PASSWORD VERIFIED! It should work!</p>";
} else {
    echo "<p style='color:red;font-weight:bold;font-size:20px'>❌ PASSWORD DOES NOT MATCH!</p>";
    
    // Generate a new hash
    echo "<h3>Solution: Use this new hash instead</h3>";
    $new_hash = password_hash('1234', PASSWORD_DEFAULT);
    echo "<p><strong>New hash for '1234':</strong></p>";
    echo "<textarea style='width:100%;height:60px;font-family:monospace'>" . $new_hash . "</textarea>";
    
    echo "<h3>SQL Command to fix:</h3>";
    echo "<textarea style='width:100%;height:100px;font-family:monospace'>";
    echo "UPDATE users SET password = '$new_hash' WHERE 1=1;";
    echo "</textarea>";
    
    // Test the new hash
    echo "<h3>Testing new hash:</h3>";
    if (password_verify('1234', $new_hash)) {
        echo "<p style='color:green'>✅ New hash works!</p>";
    }
}

// Also test database connection
echo "<hr><h3>Database Connection Test</h3>";
try {
    require_once 'config.php';
    $db = getDB();
    echo "<p style='color:green'>✅ Database connection works!</p>";
    
    // Try to fetch a user
    $stmt = $db->prepare("SELECT username, name, password FROM users WHERE username = 'owner' LIMIT 1");
    $stmt->execute();
    $user = $stmt->fetch();
    
    if ($user) {
        echo "<p style='color:green'>✅ Found user: " . htmlspecialchars($user['name']) . "</p>";
        echo "<p><strong>Stored password hash:</strong></p>";
        echo "<textarea style='width:100%;height:60px;font-family:monospace'>" . $user['password'] . "</textarea>";
        
        // Test if the stored password matches
        if (password_verify('1234', $user['password'])) {
            echo "<p style='color:green;font-weight:bold'>✅ Database password hash works with '1234'</p>";
        } else {
            echo "<p style='color:red;font-weight:bold'>❌ Database password hash does NOT match '1234'</p>";
        }
    } else {
        echo "<p style='color:red'>❌ User 'owner' not found in database</p>";
    }
    
} catch (Exception $e) {
    echo "<p style='color:red'>❌ Database error: " . htmlspecialchars($e->getMessage()) . "</p>";
}
?>
