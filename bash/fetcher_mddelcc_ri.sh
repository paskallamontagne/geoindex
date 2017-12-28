#!/bin/bash
ts=$(date "+%Y.%m.%d-%H.%M.%S")

# Archive files
if [ ! -f ~/geoindex.xyz/files/mddelcc_ri_region01.html ]; then
    echo "No files to archive"
else
    tar -czf mddelcc_ri-$ts.tar.gz ~/geoindex.xyz/files/mddelcc_ri_region*
    rm -f ~/geoindex.xyz/files/mddelcc_ri_region*
    mv mddelcc_ri-$ts.tar.gz ~/prod/archive/mddelccri/
fi

# Download files
echo "Downloading..."
i=1
while [ $i -lt 18 ]; do
    echo "$i"
    if [ $i -lt 10 ]; then
        curl "http://www.mddelcc.gouv.qc.ca/sol/residus_ind/resultats.asp?nom_dossier=&adresse=&municipalite=&mrc=&nom_region=0${i}&contaminant=&etat_dossier=" --output ~/geoindex.xyz/files/mddelcc_ri_region0${i}.html;
        sed -i -e 's/<br>/, /g' ~/geoindex.xyz/files/mddelcc_ri_region0${i}.html
    else
        curl "http://www.mddelcc.gouv.qc.ca/sol/residus_ind/resultats.asp?nom_dossier=&adresse=&municipalite=&mrc=&nom_region=${i}&contaminant=&etat_dossier=" --output ~/geoindex.xyz/files/mddelcc_ri_region${i}.html;
        sed -i -e 's/<br>/, /g' ~/geoindex.xyz/files/mddelcc_ri_region${i}.html
    fi
let i=i+1
done
echo "Done"

exit

