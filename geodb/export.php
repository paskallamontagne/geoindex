<?php

    $report_name = $_GET["report"];

    $servername = "";
    $username = "";
    $password = "";

    // Create connection
    $conn = new mysqli($servername, $username, $password);
    $conn->set_charset("utf8");

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    } 
    #echo "Connected successfully<BR>";
    #SHOULD RETURN ONLY ONE RECORD
    $sqlCommande = "SELECT  LATITUDE,LONGITUDE,DISTANCE FROM contaminated_geoindex_xyz.COMMANDES WHERE contaminated_geoindex_xyz.COMMANDES.NOM LIKE '$report_name'";
    $resultCommande = $conn->query($sqlCommande);

    $sqlRapport = "SELECT  \"default\" as type, distance,SOURCE, AFFICH, idSites,X(COORD) as lat, Y(COORD) as lng FROM contaminated_geoindex_xyz.RAPPORTS WHERE contaminated_geoindex_xyz.RAPPORTS.NOM LIKE '$report_name' ORDER BY distance";
    #echo $sqlRapport . "<br><BR>";

    $resultRapport = $conn->query($sqlRapport);
    // Creates the Document.
    $dom = new DOMDocument('1.0', 'UTF-8');

    // Creates the root KML element and appends it to the root document.
    $node = $dom->createElementNS('http://earth.google.com/kml/2.1', 'kml');
    $parNode = $dom->appendChild($node);

    // Creates a KML Document element and append it to the KML element.
    $dnode = $dom->createElement('Document');
    $docNode = $parNode->appendChild($dnode);

    // Creates the two Style elements, one for restaurant and one for bar, and append the elements to the Document element.
    $restStyleNode = $dom->createElement('Style');
    $restStyleNode->setAttribute('id', 'defaultStyle');
    $restIconstyleNode = $dom->createElement('IconStyle');
    $restLabelstyleNode = $dom->createElement('LabelStyle');
    $restBalloonstyleNode = $dom->createElement('BalloonStyle');
    
    #$restBallonBgcolor = $dom->createElement('bgColor', 'FFFFFFFF');
    $restTextNode = $dom->createElement('text', '<b>$[name]</b><br><br>$[description]');
    
    $restIconstyleNode->setAttribute('id', 'defaultIcon');
    $restIconNode = $dom->createElement('Icon');
    $restIconColor = $dom->createElement('color', 'ff10ff22');
    $restIconScale = $dom->createElement('scale', '0.9');
    $restHref = $dom->createElement('href', 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png');

    $restLabelColorNode = $dom->createElement('color', 'ff10ff22');
    
    $restIconNode->appendChild($restHref);
    
    $restIconstyleNode->appendChild($restIconColor);
    $restIconstyleNode->appendChild($restIconScale);
    $restIconstyleNode->appendChild($restIconNode);
    
    $restLabelstyleNode->appendChild($restLabelColorNode);

    #$restBalloonstyleNode->appendChild($restBallonBgcolor);
    $restBalloonstyleNode->appendChild($restTextNode);
    
    $restStyleNode->appendChild($restIconstyleNode);
    $restStyleNode->appendChild($restLabelstyleNode);
    $restStyleNode->appendChild($restBalloonstyleNode);
    $docNode->appendChild($restStyleNode);


    //Query location style 
    $queryStyleNode = $dom->createElement('Style');
    $queryStyleNode->setAttribute('id', 'queryStyle');
    $queryIconstyleNode = $dom->createElement('IconStyle');
    $queryLabelstyleNode = $dom->createElement('LabelStyle');
    $queryBalloonstyleNode = $dom->createElement('BalloonStyle');
    
    #$restBallonBgcolor = $dom->createElement('bgColor', 'FFFFFFFF');
    $queryTextNode = $dom->createElement('text', '<b>$[name]</b><br><br>$[description]');
    
    $queryIconstyleNode->setAttribute('id', 'queryIcon');
    $queryIconNode = $dom->createElement('Icon');
    $queryIconColor = $dom->createElement('color', 'ff0afffa');
    $queryIconScale = $dom->createElement('scale', '0.9');
    $queryHref = $dom->createElement('href', 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png');

    $queryLabelColorNode = $dom->createElement('color', 'ff0afffa');
    
    $queryIconNode->appendChild($queryHref);
    
    $queryIconstyleNode->appendChild($queryIconColor);
    $queryIconstyleNode->appendChild($queryIconScale);
    $queryIconstyleNode->appendChild($queryIconNode);
    
    $queryLabelstyleNode->appendChild($queryLabelColorNode);

    #$restBalloonstyleNode->appendChild($restBallonBgcolor);
    $queryBalloonstyleNode->appendChild($queryTextNode);
    
    $queryStyleNode->appendChild($queryIconstyleNode);
    $queryStyleNode->appendChild($queryLabelstyleNode);
    $queryStyleNode->appendChild($queryBalloonstyleNode);
    $docNode->appendChild($queryStyleNode);

    while($row = $resultCommande->fetch_assoc()) {
        // Creates a Placemark and append it to the Document.
        $node = $dom->createElement('Placemark');
        $sitePlaceNode = $docNode->appendChild($node);
        // Creates an id attribute and assign it the value of id column.
        $sitePlaceNode->setAttribute('id', 'placemark');

        $siteNameNode = $dom->createElement('name', 'Site');
        $sitePlaceNode->appendChild($siteNameNode);
        $description = "<b>" . " Rayon " . $row['DISTANCE'] . " km <br>";
        $descNode = $dom->createElement('description', $description);
        $sitePlaceNode->appendChild($descNode);
        $styleUrl = $dom->createElement('styleUrl', '#queryStyle');
        $sitePlaceNode->appendChild($styleUrl);


        $sitePointNode = $dom->createElement('Point');
        $sitePlaceNode->appendChild($sitePointNode);
        $siteCoorStr = $row['LONGITUDE'] . ','  . $row['LATITUDE'];
        $siteCoorNode = $dom->createElement('coordinates', $siteCoorStr);
        $sitePointNode->appendChild($siteCoorNode);
    }

    $counter = 1;
    while($row = $resultRapport->fetch_assoc()) {
    #echo $row["SOURCE"] . ": " . $row["AFFICH"] . "<br>";

        // Creates a Placemark and append it to the Document.
        $node = $dom->createElement('Placemark');
        $placeNode = $docNode->appendChild($node);

        // Creates an id attribute and assign it the value of id column.
        $placeNode->setAttribute('id', 'placemark' . $row['idSites']);
        // Create name, and description elements and assigns them the values of the name and address columns from the results.
        $nameNode = $dom->createElement('name', htmlentities($counter));
        $placeNode->appendChild($nameNode);
        $description = "<b>" . $row['SOURCE'] . '</b><BR>' . $row['AFFICH'];
        $descNode = $dom->createElement('description', $description);
        $placeNode->appendChild($descNode);
        $styleUrl = $dom->createElement('styleUrl', '#' . $row['type'] . 'Style');
        $placeNode->appendChild($styleUrl);
        
        


        // Creates a Point element.
        $pointNode = $dom->createElement('Point');
        $placeNode->appendChild($pointNode);

        // Creates a coordinates element and gives it the value of the lng and lat columns from the results.
        $coorStr = $row['lng'] . ','  . $row['lat'];
        $coorNode = $dom->createElement('coordinates', $coorStr);
        $pointNode->appendChild($coorNode);
        $counter++;
    }
    $conn->close();

    $kmlOutput = $dom->saveXML();
    header('Content-type: application/vnd.google-earth.kml+xml');
    echo $kmlOutput;
?>
