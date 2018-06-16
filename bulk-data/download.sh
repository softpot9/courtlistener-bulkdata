#/bin/bash
echo "Downloading Bulk Data --- Start ---"

#echo "----------- dockets/all.tar download & extracting ---------"
#wget https://www.courtlistener.com/api/bulk-data/dockets/all.tar -O dockets.all.tar
#mkdir dockets
#tar -xf dockets.all.tar -C ./dockets/
#rm dockets.all.tar
#for f in ./dockets/*.tar.gz; do
#  echo "------- extracting $f"
#  gunzip -c $f | tar xopf - -C ./dockets/
#done
#rm ./dockets/*.tar.gz

#echo "------------- courts/all.tar.gz download & extracting ..."
#wget https://www.courtlistener.com/api/bulk-data/courts/all.tar.gz -O courts.all.tar.gz
#mkdir courts
#tar -xzf courts.all.tar.gz -C ./courts/
#rm courts.all.tar.gz

#echo "------------- citations/all.csv.gz download & extracting ..."
#wget https://www.courtlistener.com/api/bulk-data/citations/all.csv.gz -O citations.all.csv.gz
#mkdir citations
#gunzip -c citations.all.csv.gz > ./citations/citations.all.csv
#rm citations.all.csv.gz

#echo "-------------- people/all.tar.gz download & extracting ..."
#wget https://www.courtlistener.com/api/bulk-data/people/all.tar.gz -O people.all.tar.gz
#mkdir people
#tar -xvzf people.all.tar.gz -C ./people/ > log.txt
#rm people.all.tar.gz

#echo "--------------- clusters/all.tar download & extracting ..."
#wget https://www.courtlistener.com/api/bulk-data/clusters/all.tar -O clusters.all.tar
#mkdir clusters
#tar -xf clusters.all.tar -C ./clusters/
#rm clusters.all.tar
#for f in ./clusters/*.tar.gz; do
#  echo "------- extracting $f"
#  gunzip -c $f | tar xopf - -C ./clusters/
#done
#rm ./clusters/*.tar.gz

echo "----------- opinions/all.tar download & extracting ---------"
wget https://www.courtlistener.com/api/bulk-data/opinions/all.tar -O opinions.all.tar
mkdir opinions
tar -xf opinions.all.tar -C ./opinions/
rm opinions.all.tar
for f in ./opinions/*.tar.gz; do
  echo "------- extracting $f"
  gunzip -c $f | tar xopf - -C ./opinions/
done
rm ./opinions/*.tar.gz
