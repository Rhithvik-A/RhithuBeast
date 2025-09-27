<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Collect and sanitize form data
    $name    = htmlspecialchars($_POST['name']);
    $email   = filter_var($_POST['email'], FILTER_SANITIZE_EMAIL);
    $subject = htmlspecialchars($_POST['subject']);
    $message = htmlspecialchars($_POST['message']);

    // Email address where messages will be sent
    $to = "youraddress@example.com"; // <-- replace with your email

    // Email headers
    $headers  = "From: $name <$email>\r\n";
    $headers .= "Reply-To: $email\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

    // Send the email
    if (mail($to, $subject, $message, $headers)) {
        echo "<h3>Email sent successfully!</h3>";
    } else {
        echo "<h3>Failed to send email. Check server mail configuration.</h3>";
    }
} else {
    echo "<h3>Invalid request method.</h3>";
}
?>

