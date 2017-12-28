<html> 

<head> 
<meta http-equiv="Content-Type" content="text/html;charset=UTF8">
<title>Résultats de la recherche</title> 



</head>
<body> 

<?php   



$lon = $_POST["lon"];
$lat = $_POST["lat"];
$dist = 1; //km

echo "<font color=\"yellow\"";
echo "Résulats de la recherche : ";
echo $lon;
echo " ";
echo $lat;
echo "<BR><BR>";

/* 
    DO NOT LEAVE CREDENTIALS IN FILE 
*/

$servername = "mysql.geoindex.xyz";
$username = "geoindex_sqladm";
$password = "6aTF5i4NR3nxuqJ95";

// Create connection
$conn = new mysqli($servername, $username, $password);
$conn->set_charset("utf8");

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
#echo "Connected successfully<BR>";



/*
$sql = "SELECT 6371 * 2 * ASIN(SQRT(" .
    "POWER(SIN((" . $lat . "- abs(X(COORD))) * pi()/180 / 2)," .
    "2) + COS(" . $lat . "* pi()/180 ) * COS(abs(X(COORD)) *" .
    "pi()/180) * POWER(SIN((" . $lon . "- Y(COORD)) *" .
    "pi()/180 / 2), 2) )) as distance," .
    "SOURCE, AFFICH, idSites " .
    "FROM SITES" .
    " HAVING distance < " . $dist .
    " ORDER BY distance";
*/
//$sql = "SELECT SOURCE,AFFICH FROM SITES LIMIT 10";

//$sql = "SELECT 6371 * 2 * ASIN(SQRT(POWER(SIN((" . $lat . " - abs(X(COORD))) * pi()/180 / 2),2) + COS(" . $lat . " * pi()/180 ) * COS(abs(X(COORD)) * pi()/180) * POWER(SIN((" . $lon . " - Y(COORD)) * pi()/180 / 2), 2) )) as distance,SOURCE, AFFICH, idSites FROM SITES HAVING distance < " . $dist . " ORDER BY distance";

//$sql = "SELECT 6371 * 2 * ASIN(SQRT(POWER(SIN(($lat - abs(X(COORD))) * pi()/180 / 2),2) + COS($lat * pi()/180 ) * COS(abs(X(COORD)) * pi()/180) * POWER(SIN(($lon  - Y(COORD)) * pi()/180 / 2), 2) )) as distance,SOURCE, AFFICH, idSites,COUNT(SELECT 6371 * 2 * ASIN(SQRT(POWER(SIN(($lat - abs(X(COORD))) * pi()/180 / 2),2) + COS($lat * pi()/180 ) * COS(abs(X(COORD)) * pi()/180) * POWER(SIN(($lon  - Y(COORD)) * pi()/180 / 2), 2) )) as distance,SOURCE, AFFICH, idSites FROM contaminated_geoindex_xyz.SITES HAVING distance < $dist) AS RCOUNT FROM contaminated_geoindex_xyz.SITES GROUP BY SOURCE HAVING distance < $dist ORDER BY distance";

/* FIRST QUERY TO DETERMINE IF RECORDS ARE PRESENT - DEBUG WITH MORE SOURCES IN DATABASE */
$sqlGroup = "SELECT 6371 * 2 * ASIN(SQRT(POWER(SIN(($lat - abs(X(COORD))) * pi()/180 / 2),2) + COS($lat * pi()/180 ) * COS(abs(X(COORD)) * pi()/180) * POWER(SIN(($lon  - Y(COORD)) * pi()/180 / 2), 2) )) as distance,SOURCE, AFFICH, idSites FROM contaminated_geoindex_xyz.SITES HAVING distance < $dist ORDER BY distance";
#echo $sqlGroup . "<BR><BR>";
$resultGroup = $conn->query($sqlGroup);



/* SOMETHING IS FOUND */
if ($resultGroup->num_rows > 0) {
    
    $sqlSource = "SELECT contaminated_geoindex_xyz.SOURCES.NAME,contaminated_geoindex_xyz.SOURCES.FNAME FROM contaminated_geoindex_xyz.SOURCES";
    echo "Votre requête a retourné un total de " . $resultGroup->num_rows . " enregistrement(s) au sein des répertoires suivants: <BR><BR>";
    $resultSource = $conn->query($sqlSource);

    /* GENERATE REPORT IN TABLE RAPPORT_RANDOM_DATETIME */

    /* GENERATE RANDOM NUMBER BETWEEN 100 000 and 999 999 TIMESTAMP AND NAME */
    $r = rand (100000,999999);
    $REPORT_TIMESTAMP = date("Y-m-d-H-i-s");
    $REPORT_NAME = "RAPPORT_" . $r . "_" . $REPORT_TIMESTAMP;

    //$sqlCreate = "CREATE TABLE contaminated_geoindex_xyz.$REPORT_NAME (idSITES int(11) NOT NULL AUTO_INCREMENT,AFFICH varchar(1000) DEFAULT NULL,COORD point DEFAULT NULL,SOURCE varchar(45) DEFAULT NULL,DISTANCE double DEFAULT NULL,PRIMARY KEY (idSITES)) ENGINE=InnoDB AUTO_INCREMENT=3070 DEFAULT CHARSET=utf8";

    /*
    $sqlCreate = "CREATE TABLE contaminated_geoindex_xyz.`$REPORT_NAME` (
        `idSITES` int(11) NOT NULL AUTO_INCREMENT,
        `AFFICH` varchar(1000) DEFAULT NULL,
        `COORD` point DEFAULT NULL,
        `SOURCE` varchar(45) DEFAULT NULL,
        `DISTANCE` double DEFAULT NULL,
        PRIMARY KEY (`idSITES`)
      ) ENGINE=InnoDB AUTO_INCREMENT=3070 DEFAULT CHARSET=utf8";

    //echo $sqlCreate . "<br><BR>";
    //$resultCreate = $conn->query($sqlCreate);
    */

    $sqlSelectInsert = "INSERT INTO contaminated_geoindex_xyz.`RAPPORTS` (COORD,NOM,DISTANCE,SOURCE, AFFICH, idSites) SELECT COORD,'$REPORT_NAME', 6371 * 2 * ASIN(SQRT(POWER(SIN((" . $lat . " - abs(X(COORD))) * pi()/180 / 2),2) + COS(" . $lat . " * pi()/180 ) * COS(abs(X(COORD)) * pi()/180) * POWER(SIN((" . $lon . " - Y(COORD)) * pi()/180 / 2), 2) )) as distance,SOURCE, AFFICH, idSites FROM contaminated_geoindex_xyz.SITES HAVING distance < " . $dist . " ORDER BY distance";
    #echo $sqlSelectInsert . "<BR><BR>";
    $resultReport = $conn->query($sqlSelectInsert);
    

    $sqlInsertCommande = "INSERT INTO contaminated_geoindex_xyz.`COMMANDES` (NOM,DATE_PRODUCTION,LATITUDE,LONGITUDE,DISTANCE) VALUES (\"$REPORT_NAME\",\"$REPORT_TIMESTAMP\",\"$lat\",\"$lon\",\"$dist\")";
    #echo $sqlInsertCommande . "<BR><BR>";
    $resultInsertCommande = $conn->query($sqlInsertCommande);

   /* DISPLAY SEARCH RESULTS */ 
    while($row = $resultSource->fetch_assoc()) {
        $source = $row["NAME"];
        $sqlSitesBySource = "SELECT 6371 * 2 * ASIN(SQRT(POWER(SIN(($lat - abs(X(COORD))) * pi()/180 / 2),2) + COS($lat * pi()/180 ) * COS(abs(X(COORD)) * pi()/180) * POWER(SIN(($lon  - Y(COORD)) * pi()/180 / 2), 2) )) as distance,SOURCE, AFFICH, idSites FROM contaminated_geoindex_xyz.SITES WHERE contaminated_geoindex_xyz.SITES.SOURCE LIKE '$source' HAVING distance < $dist ORDER BY distance";
        
        #echo $sqlSitesBySource . "<br><BR>";
        
        $resultSitesBySource = $conn->query($sqlSitesBySource);
        
        //$rowSource = $resultSource->fetch_assoc();
        echo $row["FNAME"] . ": " . $resultSitesBySource->num_rows . " enregistrement(s)<BR>";
        //echo $row["SOURCE"] . ": " . $row["AFFICH"]. "<br>";
    }
    echo "<BR>Pour commander les résultats veuillez suivre sur le lien suivant: <BR><BR>";
    echo "</font>";
    /* PAYMENT FORM - 
        TODO PASS REPORT ID IN HIDDEN FIELD FOR FUTURE DISPLAY 
    */ 
    echo "<form action=\"charge.php\" method=\"POST\">";
    echo "<script ";
    echo "src=\"https://checkout.stripe.com/checkout.js\" class=\"stripe-button\"";
    echo " data-key=\"pk_test_IN1UijO86nrvEQwQZm1LxZSP\""; // your publishable keys
    echo " data-image=\"logo.png\""; // your company Logo
    echo " data-name=\"WALRUS\"";
    echo " data-description=\"Download Script (5.00$)\"";
    echo " data-amount=\"500\">";
    echo "</script>";
    echo " <input id=\"reportname\" name=\"reportname\" type=\"hidden\" value=\"$REPORT_NAME\">";
    echo "</form>";

} else {
    echo "Aucun résultat. Effectué une <a href='http://geoindex.xyz/geodb/' target='_parent' style='color: rgb(0,255,255)'><font color=\"yellow\">nouvelle recherche</font></a></a>";
}
$conn->close();





?>




</body> 

</html>

