#!/usr/bin/env python3.7
from pyspark.sql import SQLContext, SparkSession
import os
import re


SS = SparkSession.builder.appName('CSV to Parquet').getOrCreate()
data_dir = os.getcwd() + '/data/'
files = [data_dir + file for file in os.listdir(data_dir)]

for file in files:
    print(file)
    ctx = SQLContext(SS)
    # .setConf("spark.driver.memory", "8GB")
    if not ctx:
        import sys
        sys.exit(1)
    df = ctx.read.csv(file, inferSchema=True, header=True, sep='\t')
    df.show(n=10)
    df.printSchema()
    columns = ', \n'.join([f'{col[0].lower()}' + f' {col[1]}' for col in df.dtypes])
    table_name = os.path.basename(file).replace('.TXT', '').lower()
    re.sub('[\s,.]+', '_', table_name)
    # re.sub('[,.?!\t\n ]+|.txt', '_', table_name)
    hive_ddl = f'CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (\n{columns})' \
               ' \nSTORED AS PARQUET ' \
               f'\nLOCATION \'s3://athena-showcase/{table_name}/\';'
    open(file=os.getcwd() + '/queries/' + table_name + '.ddl.sql', mode='w').write(hive_ddl)
    df.write.parquet(path=data_dir + table_name, compression='snappy')
    #os.remove(file)
