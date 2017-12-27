#!/bin/bash
python3 ~/devel/logger.py -p "LOGGER" -e "Starting"
python3 ~/devel/logger.py -p "LOGGER" -e "Stamping DB start time"
python3 ~/devel/updatestart.py
# MDDELCC
# Archive files
python3 ~/devel/logger.py -p "LOGGER.MDDELCC" -e "Starting MDDELCC script"
python3 ~/devel/logger.py -p "LOGGER.MDDELCC" -e "Verifying for files to archive"
if [ ! -f ~/geoindex.xyz/files/mddelcc_region01.html ]; then
    python3 ~/devel/logger.py -p "LOGGER.MDDELCC" -e "Directory is empty, no files to archive"
else
    python3 ~/devel/logger.py -p "LOGGER.MDDELCC" -e "Archiving previously downloaded files"
    ts=$(date "+%Y.%m.%d-%H.%M.%S")
    tar -czf mddelcc-$ts.tar.gz ~/geoindex.xyz/files/mddelcc_region*
    rm -f ~/geoindex.xyz/files/mddelcc_region*
    mv mddelcc-*.tar.gz ~/prod/archives/mddelcc/
fi

# Download files
python3 ~/devel/logger.py -p "LOGGER.MDDELCC" -e "Downloading new files"
i=1
while [ $i -lt 18 ]; do
   python3 ~/devel/logger.py -p "LOGGER.MDDELCC" -e "Downloading file $i of 17"
   if [ $i -lt 10 ]; then
       curl "http://www.mddelcc.gouv.qc.ca/sol/terrains/terrains-contamines/formatExcel.asp?nom_dossier=&adresse=&municipalite=&mrc=&nom_region=0${i}&contaminant=&eau_contaminant=&sol_contaminant=&debut=&fin=&sens=&type_tri=" --output ~/geoindex.xyz/files/mddelcc_region0${i}.html;
   else
       curl "http://www.mddelcc.gouv.qc.ca/sol/terrains/terrains-contamines/formatExcel.asp?nom_dossier=&adresse=&municipalite=&mrc=&nom_region=${i}&contaminant=&eau_contaminant=&sol_contaminant=&debut=&fin=&sens=&type_tri=" --output ~/geoindex.xyz/files/mddelcc_region${i}.html;
   fi
let i=i+1
done
ts=$(date "+%Y.%m.%d-%H.%M.%S")
python3 ~/devel/logger.py -p "LOGGER.MDDELCC" -e "Downloading files complete"

python3 ~/devel/logger.py -p "LOGGER.MDDELCC" -e "Calling MDDELCC parser"
python3 ~/devel/mddelcc_parser.py
python3 ~/devel/logger.py -p "LOGGER.MDDELCC" -e "MDDELCC parser completed with exit status $?"
python3 ~/devel/logger.py -p "LOGGER.MDDELCC" -e "Starting SQL script"
python3 ~/devel/mddelcc_sql.py
python3 ~/devel/logger.py -p "LOGGER.MDDELCC" -e "SQL script completed with exit status $?"

# MDDELCCRI
# Archive files
python3 ~/devel/logger.py -p "LOGGER.MDDELCC_RI" -e "Starting MDDELCC_RI script"
python3 ~/devel/logger.py -p "LOGGER.MDDELCC_RI" -e "Verifying for files to archive"
if [ ! -f ~/geoindex.xyz/files/mddelcc_ri_region01.html ]; then
    python3 ~/devel/logger.py -p "LOGGER.MDDELCC_RI" -e "Directory is empty, no files to archive"
else
    python3 ~/devel/logger.py -p "LOGGER.MDDELCC_RI" -e "Archiving previously downloaded files"
    ts=$(date "+%Y.%m.%d-%H.%M.%S")
    tar -czf mddelcc_ri-$ts.tar.gz ~/geoindex.xyz/files/mddelcc_ri_region*
    rm -f ~/geoindex.xyz/files/mddelcc_ri_region*
    mv mddelcc_ri-*.tar.gz ~/prod/archives/mddelccri/
fi

# Download files
python3 ~/devel/logger.py -p "LOGGER.MDDELCC_RI" -e "Downloading new files"
i=1
while [ $i -lt 18 ]; do
    python3 ~/devel/logger.py -p "LOGGER.MDDELCC_RI" -e "Downloading file $i of 17"
    if [ $i -lt 10 ]; then
        curl "http://www.mddelcc.gouv.qc.ca/sol/residus_ind/resultats.asp?nom_dossier=&adresse=&municipalite=&mrc=&nom_region=0${i}&contaminant=&etat_dossier=" --output ~/geoindex.xyz/files/mddelcc_ri_region0${i}.html;
        sed -i -e 's/<br>/, /g' ~/geoindex.xyz/files/mddelcc_ri_region0${i}.html
    else
        curl "http://www.mddelcc.gouv.qc.ca/sol/residus_ind/resultats.asp?nom_dossier=&adresse=&municipalite=&mrc=&nom_region=${i}&contaminant=&etat_dossier=" --output ~/geoindex.xyz/files/mddelcc_ri_region${i}.html;
        sed -i -e 's/<br>/, /g' ~/geoindex.xyz/files/mddelcc_ri_region${i}.html
    fi
let i=i+1
done
ts=$(date "+%Y.%m.%d-%H.%M.%S")
python3 ~/devel/logger.py -p "LOGGER.MDDELCC_RI" -e "Downloading files complete"

python3 ~/devel/logger.py -p "LOGGER.MDDELCC_RI" -e "Calling MDDELCC_RI parser"
python3 ~/devel/mddelcc_ri_parser.py
python3 ~/devel/logger.py -p "LOGGER.MDDELCC_RI" -e "MDDELCC_RI parser completed with exit status $?"
python3 ~/devel/logger.py -p "LOGGER.MDDELCC_RI" -e "Starting SQL script"
python3 ~/devel/mddelcc_ri_sql.py
python3 ~/devel/logger.py -p "LOGGER.MDDELCC_RI" -e "SQL script completed with exit status $?"

#RBQ Sites
python3 ~/devel/logger.py -p "LOGGER.RBQ" -e "Starting RBQ script"
file1=sites-equipements-petroliers-region-01-a-06.xls
file2=sites-equipements-petroliers-region-07-a-17.xls

python3 ~/devel/logger.py -p "LOGGER.RBQ" -e "Starting RBQ script"
python3 ~/devel/logger.py -p "LOGGER.RBQ" -e "Verifying for files to archive"
# Archive files
if [ ! -f ~/geoindex.xyz/files/sites-equipements-petroliers-region-01-a-06.xls ]; then
    python3 ~/devel/logger.py -p "LOGGER.RBQ" -e "Directory is empty, no files to archive"
else
    python3 ~/devel/logger.py -p "LOGGER.RBQ" -e "Archiving RBQ Sites files"
    ts=$(date "+%Y.%m.%d-%H.%M.%S")
    tar -czf rbqsites-$ts.tar.gz ~/geoindex.xyz/files/sites-equipements*
    rm -f ~/geoindex.xyz/files/sites-equipements*
    mv rbqsites-*.tar.gz ~/prod/archives/rbqsites/
fi

# Download files
python3 ~/devel/logger.py -p "LOGGER.RBQ" -e "Downloading RBQ Sites files"
wget --no-check-certificate https://www.rbq.gouv.qc.ca/fileadmin/medias/pdf/equipements-petroliers/sites-equipements-petroliers-region-01-a-06.xls -O ~/geoindex.xyz/files/sites-equipements-petroliers-region-01-a-06.xls
python3 ~/devel/logger.py -p "LOGGER.RBQ" -e "$file1 downloaded with exit status $?"
wget --no-check-certificate https://www.rbq.gouv.qc.ca/fileadmin/medias/pdf/equipements-petroliers/sites-equipements-petroliers-region-07-a-17.xls -O ~/geoindex.xyz/files/sites-equipements-petroliers-region-07-a-17.xls
python3 ~/devel/logger.py -p "LOGGER.RBQ" -e "$file2 downloaded with exit status $?"
python3 ~/devel/logger.py -p "LOGGER.RBQ" -e "RBQ Sites Done"

python3 ~/devel/updateend.py
python3 ~/devel/logger.py -p "LOGGER" -e "Stamping DB end time"
python3 ~/devel/logger.py -p "LOGGER" -e "Done"

exit