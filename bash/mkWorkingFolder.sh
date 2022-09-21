#!/bin/bash

folder_name=''
force=0

while test $# -gt 0
do
    case "$1" in
        -n) folder_name=$2
            ;;
        -f) force=1
            ;;
        #--*) echo "bad option $1"
        #    ;;
        #*) echo "argument $1"
        #    ;;
    esac
    shift
done

if [ $folder_name == '' ]; then
	echo "[\!] Missing parameter: -n <name>"
	exit 1
fi


if [[ ( -d $folder_name )  &&  ( $force -eq 0 ) ]]; then
	echo "[!] Directory $folder_name already exists, aborting."
	echo "[?] If you want to create it anyways, use -f parameter (it will erase previous folders)."
	echo "[!] Exit program..."
	exit 1
fi

if [[ ( -d $folder_name )  &&  ( $force -eq 1 ) ]];then
	echo "[!] Removing previous version of ./$folder_name folder..."
	rm -r $folder_name
	echo "[!] Previous version removed successfully..."
fi

echo "[+] Making work tree under ./$folder_name ..."
mkdir $folder_name
mkdir $folder_name/content
mkdir $folder_name/enum
mkdir $folder_name/transfer
echo "[+] Directory tree created successfully!"

exit 0
