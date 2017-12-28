<html> 

<head>
<meta http-equiv="Content-Language" content="fr"/>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Paiement</title> 
</head>
<body> 

<?php
#mb_internal_encoding("ISO-8859-1");
mb_internal_encoding("UTF-8");
#echo mb_internal_encoding();
require_once('Stripe/init.php');
#require('phpsqlajax_dbinfo.php');

/* Stripe variables */
$stripe = [
    'publishable' => 'hidden',
    'private' => 'sk_test_WF9fkU6leAIwl19PXNVDuzQU'
];
  
\Stripe\Stripe::setApiKey($stripe['private']);
  
if(isset($_POST['stripeToken'])) {
  
  $token = $_POST['stripeToken'];
  $email = $_POST['stripeEmail'];
  
  try {
    
    $charge = \Stripe\Charge::create(array(
    "amount" => 500,
    "currency" => "cad",
    "source" => $token,
    "description" => "Charge for ".$email

  ));
  
  //send the file, this line will be reached if no error was thrown above
  

  $report_name = $_POST["reportname"];
  #echo "<h1>Your payment has been completed. See you space cowboy...$report_name</h1>";
  
  $servername = "mysql.geoindex.xyz";
  $username = "geoindex_sqladm";
  $password = "6aTF5i4NR3nxuqJ95";
  
  
  

  setlocale(LC_ALL, 'fr_fr');
  // Create connection
  $conn = new mysqli($servername, $username, $password);
  $conn->set_charset("utf8");

  // Check connection
  if ($conn->connect_error) {
      die("Connection failed: " . $conn->connect_error);
  } 
  #echo "Connected successfully<BR>";

  $sqlRapport = "SELECT  distance,SOURCE, AFFICH, idSites FROM contaminated_geoindex_xyz.RAPPORTS WHERE contaminated_geoindex_xyz.RAPPORTS.NOM LIKE '$report_name' ORDER BY distance";
  #echo $sqlRapport . "<br><BR>";
  
  echo "<a href=\"export.php?report=$report_name\" style=\"color: rgb(0,255,255)\"><font color=\"yellow\">Télécharger le rapport</font></a>. <font color=\"yellow\">Effectué une </font><a href='http://geoindex.xyz/geodb/' target='_parent' style='color: rgb(0,255,255)'><font color=\"yellow\">nouvelle recherche</font></a><BR><BR>";

  $resultRapport = $conn->query($sqlRapport);
  
  while($row = $resultRapport->fetch_assoc()) {
    $utf8_str = utf8_encode($row["AFFICH"]);
    #echo utf8_decode($row["SOURCE"]) . ": " . utf8_decode($utf8_str) . "<br>";
  }
  $conn->close();

  

  //you can send the file to this email:
  //echo $_POST[$email];
    


  // echo $charge->id;
  } catch(\Stripe\Error\Card $e) {
    // Since it's a decline, \Stripe\Error\Card will be caught
    $body = $e->getJsonBody();
    $err  = $body['error'];
  
    print('Status is:' . $e->getHttpStatus() . "\n");
    print('Type is:' . $err['type'] . "\n");
    print('Code is:' . $err['code'] . "\n");
    // param is '' in this case
    print('Param is:' . $err['param'] . "\n");
    print('Message is:' . $err['message'] . "\n");
  } catch (\Stripe\Error\RateLimit $e) {
    // Too many requests made to the API too quickly
  } catch (\Stripe\Error\InvalidRequest $e) {
    // Invalid parameters were supplied to Stripe's API
  } catch (\Stripe\Error\Authentication $e) {
    // Authentication with Stripe's API failed
    // (maybe you changed API keys recently)
  } catch (\Stripe\Error\ApiConnection $e) {
    // Network communication with Stripe failed
  } catch (\Stripe\Error\Base $e) {
    // Display a very generic error to the user, and maybe send
    // yourself an email
  } catch (Exception $e) {
    // Something else happened, completely unrelated to Stripe
  }
}
?>
</body>
</html>