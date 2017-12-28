#!/bin/bash
ts=$(date "+%Y.%m.%d-%H.%M.%S")

# Archive files
if [ ! -f ~/geoindex.xyz/files/mddelcc_region01.html ]; then
    echo "No files to archive"
else
    tar -czf mddelcc-$ts.tar.gz ~/geoindex.xyz/files/mddelcc_region*
    rm -f ~/geoindex.xyz/files/mddelcc_region*
    mv mddelcc-$ts.tar.gz ~/prod/archive/mddelcc/
fi

# Download files
echo "Downloading files..."
i=1
while [ $i -lt 18 ]; do
   echo "$i"
   if [ $i -lt 10 ]; then
       curl "http://www.mddelcc.gouv.qc.ca/sol/terrains/terrains-contamines/formatExcel.asp?nom_dossier=&adresse=&municipalite=&mrc=&nom_region=0${i}&contaminant=&eau_contaminant=&sol_contaminant=&debut=&fin=&sens=&type_tri=" --output ~/geoindex.xyz/files/mddelcc_region0${i}.html;
   else
       curl "http://www.mddelcc.gouv.qc.ca/sol/terrains/terrains-contamines/formatExcel.asp?nom_dossier=&adresse=&municipalite=&mrc=&nom_region=${i}&contaminant=&eau_contaminant=&sol_contaminant=&debut=&fin=&sens=&type_tri=" --output ~/geoindex.xyz/files/mddelcc_region${i}.html;
   fi
let i=i+1
done
echo "Done"

exit
