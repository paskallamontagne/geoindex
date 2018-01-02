
<html>
  <head>
    <title>Geocoding service</title>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <style>
      /* Always set the map height explicitly to define the size of the div
       * element that contains the map. */
      #map {
        height: 100%;
      }
      /* Optional: Makes the sample page fill the window. */
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      
      #logo {
        position: absolute;
        top: 5px;
        left: 1%;
        z-index: 5;
        background-color: #fff;
        padding: 5px;
        border: 1px solid #999;
        text-align: center;
        font-family: 'Roboto','sans-serif';
        line-height: 30px;
        padding-left: 10px;
      }
      #floating-panel {
        position: absolute;
        top: 1%;
        left: 1%;
        right: 1%;
        z-index: 5;
        background-color: transparent;
        padding: 5px;
        border: 1px solid #999;
        text-align: center;
        font-family: 'Roboto','sans-serif';
        line-height: 30px;
        padding-left: 10px;
        text-align: left;
      }
      #submit-form {
        position: absolute;
        top: 1%;
        right: 1%;
        width: 600px;
        z-index: 5;
        background-color: #fff;
        padding: 5px;
        border: 1px solid #999;
        text-align: center;
        font-family: 'Roboto','sans-serif';
        line-height: 30px;
        padding-left: 10px;
        text-align: left;
      }
      #console {
        position: absolute;
        top: 150px;
        left: 1%;
        z-index: 5;
        background-color: transparent;
        padding: 5px;
        border: 0px solid #999;
        text-align: left;
        font-family: 'Roboto','sans-serif';
        font-size: '8px';
        line-height: 30px;
        padding-left: 10px;
      }
      #stats-panel {
        position: absolute;
        right: 1%;
        bottom: 1%;
        z-index: 5;
        background-color: transparent;
        padding: 5px;
        border: 0px solid #999;
        text-align: left;
        font-family: 'Roboto','sans-serif';
        font-size: '8px';
        line-height: 30px;
        padding-left: 10px;
      }

      

    </style>
  </head>
  <body>
  <iframe name="console" id="console" height="600" width="600">
      
  </iframe>

    
    <div id="floating-panel">
      <table border=0 width="100%">
      <tr>
      <td colspan="3" align="center"><font color="yellow">---------------------------</font></td>
      </tr>
      <tr>
      <td colspan="3" align="center"><font color="yellow">GEODB</font></td>
      </tr>
      <tr>
      <td colspan="3" align="center"><font color="yellow">---------------------------</font></td>
      </tr>
      <tr>
      <td><font color="yellow">1. Centrer la carte</font></td>
      <td><font color="yellow">2. Choisir un point</font></td>
      <td align="right"><font color="yellow">3. Rechercher</font></td>
      </tr>
      <tr>
        <td align="left">
        <input id="address" type="textbox" value="Québec" size="75">
        <input id="submit" type="button" value="Centrer la carte">
        </td>
        
        <form action="search.php" target="console" method="post">
        <td></td>
        <td align="right"><input type="text" name="lon" id='lon' value='<?php echo $_GET['lon'];?>'>
        <input type="text" name="lat" id='lat' value='<?php echo $_GET['lat'];?>'>
        <input type="submit" value="Recherche"></td>
        </form>
        </td>
      </tr>
      </table>

      
      
    </div>
    

      <?php

      echo "<div id=\"stats-panel\" >";
      

      $servername = "";
      $username = "";
      $password = "";

      // Create connection
      $conn = new mysqli($servername, $username, $password);

      // Check connection
      if ($conn->connect_error) {
          die("Connection failed: " . $conn->connect_error);
      } 
      //echo "Connected successfully<BR>";

      //$sqlselect = "SELECT LAST_UPDATE_END FROM contaminated_geoindex_xyz.UPDATES ORDER BY contaminated_geoindex_xyz.UPDATES.idUpdates DESC LIMIT 1";
      //$sqlSelect = "SELECT NAME,URL,LAST_UPDATE,RECORD_COUNT,SOURCE_RECORD_COUNT FROM contaminated_geoindex_xyz.SOURCES";
      $sqlSelect = "SELECT LAST_UPDATE_START,LAST_UPDATE_END FROM contaminated_geoindex_xyz.UPDATES ORDER BY idUpdates DESC LIMIT 1";
      #echo $sqlSelect . "<BR>";
      $resultSelect = $conn->query($sqlSelect);
      if ($resultSelect->num_rows > 0) {
        while($row = $resultSelect->fetch_assoc()) {
          $last_update_start = $row["LAST_UPDATE_START"];
          $last_update_end = $row["LAST_UPDATE_END"];
          
          echo "<font color=\"yellow\">Dernière mise à jour: </font><a href=\"dbStats.php\"><font color=\"yellow\">" . $last_update_start . " / " . $last_update_end  . "</font></a>";
        }
      }

      /*
       * $sqlSelect = "SELECT NAME,URL,LAST_UPDATE,RECORD_COUNT,SOURCE_RECORD_COUNT FROM contaminated_geoindex_xyz.SOURCES";
       * //echo $sqlSelect . "<BR><BR>";
       * $resultSelect = $conn->query($sqlSelect);
      
      
      /* SOMETHING IS FOUND */
      /*
      if ($resultSelect->num_rows > 0) {
        while($row = $resultSelect->fetch_assoc()) {
          $name = $row["NAME"];
          $url = $row["URL"];
          $last_update = $row["LAST_UPDATE"];
          $record_count = $row["RECORD_COUNT"];
          $source_record_count = $row["SOURCE_RECORD_COUNT"];
          echo $row["NAME"] .  " maj " . $last_update . " " . $record_count . " / " . $source_record_count . " enregistrements<BR>";
        }
      }
      */
      
      echo "</div>";
      $conn->close();
      ?>



    </div>
    <div id="map"></div>
    <script>
      function initMap() {
        var map = new google.maps.Map(document.getElementById('map'), {
            mapTypeId: 'hybrid',
            zoom: 6,
            center: {lat: 47.413220330169025, lng: -74.42138671875},
            disableDefaultUI: true

        });

        google.maps.event.addListener(map, 'click', function(event) {
            //alert("Latitude: " + event.latLng.lat() + " " + ", longitude: " + event.latLng.lng());

            document.getElementById('lon').value = event.latLng.lng();
            document.getElementById('lat').value = event.latLng.lat();

        });

        //map.addListener('click', function() {
          //alert("Click");
          //map.setZoom(8);
          //map.setCenter(marker.getPosition());
        //});

        var geocoder = new google.maps.Geocoder();

        document.getElementById('submit').addEventListener('click', function() {
          geocodeAddress(geocoder, map);
        });
      }

      function geocodeAddress(geocoder, resultsMap) {
        var address = document.getElementById('address').value;
        geocoder.geocode({'address': address}, function(results, status) {
          if (status === 'OK') {
            resultsMap.setCenter(results[0].geometry.location);
            resultsMap.setZoom(12)
            var marker = new google.maps.Marker({
              map: resultsMap,
              position: results[0].geometry.location
            });
          } else {
            alert('Geocode was not successful for the following reason: ' + status);
          }
        });
      }
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDeco3PdOJgF342P5Bg8r1M5zX33TZzlg8&callback=initMap">
    </script>
  </body>
</html>
