#! /bin/bash

# Usage: Given an RFC name and a commit, retrieve all the files of the RFC into the AIP RFC at the right commit.
# Example: code/cpAIP.sh concepts/0003-protocols c3b0e2120ad24810598375663b6922b980f85d00
# Designed to fetch files in subdirectories, although it is not clear how to add them to the documentatioon

PROTOCOL=$1
COMMIT=$2
AIP2=aip2

# echo Getting AIP docs for RFC $PROTOCOL, Commit $COMMIT
cd docs
for i in $(find $PROTOCOL -type f); do
    AIPFile=$(echo $i | sed -r "s#(features|concepts)/#${AIP2}/#")
    # echo $i $AIPFile
    mkdir -p $(dirname $AIPFile)
    curl -s https://raw.githubusercontent.com/hyperledger/aries-rfcs/${COMMIT}/$i -o $AIPFile
done
cd ..
