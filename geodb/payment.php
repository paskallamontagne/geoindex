<html> 

<head> 
<meta http-equiv="Content-Type" content="text/html;charset=UTF8">
<title>Process Payment</title> 



</head>
<body> 

<?php 
use Omnipay\Omnipay;
echo "Paiement : <BR>";  

$number = $_POST["number"];

echo $number;



// Setup payment gateway
$gateway = Omnipay::create('Stripe');
$gateway->setApiKey('abc123');

// Example form data
$formData = [
    'number' => '4242424242424242',
    'expiryMonth' => '6',
    'expiryYear' => '2016',
    'cvv' => '123'
];

// Send purchase request
$response = $gateway->purchase(
    [
        'amount' => '10.00',
        'currency' => 'USD',
        'card' => $formData
    ]
)->send();

// Process response
if ($response->isSuccessful()) {
    
    // Payment was successful
    print_r($response);

} elseif ($response->isRedirect()) {
    
    // Redirect to offsite payment gateway
    $response->redirect();

} else {

    // Payment failed
    echo $response->getMessage();
}

?>




</body> 

</html>