#!/usr/bin/env bash

curl --request GET -L \
     --url 'http://data.gdeltproject.org/events/GDELT.MASTERREDUCEDV2.1979-2013.zip'\
     --output 'data.zip'

unzip data.zip -d data
rm data.zip
./csv-parquet.py
aws s3 cp data/gdelt.masterreducedv2 s3://athena-showcase/gdelt.masterreducedv2 --recursive --profile Athena
