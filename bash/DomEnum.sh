#!/bin/bash

url=$1

if [ ! -d "$url" ];then
	mkdir $url
fi

if [ ! -d "$url/recon" ];then
	mkdir $url/recon
fi

echo "[+] Haversting subdomains with assetfinder..."
assetfinder $url >> $url/recon/assets.txt
cat $url/recon/assets.txt | grep $url >> $url/recon/final.txt
rm $url/recon/assets.txt

#echo "[+] Harvesting subdomains with Amass..."
#amass enum -d $url >> $url/recon/.txt
#sort -u $url/recon/f.txt >> $url/recon/final.txt
#rm $url/recon/f.txt


echo "[+] Probing alive domains..."
cat $url/recon/final.txt | sort -u | httprobe -s -p https:443 | sed 's/https\?:\/\///' | tr -d ':443' >> $url/recon/alive.txt
