#!/usr/bin/env python3.7
import json
import os
from boto3 import Session


def run_query(file, db, workgroup):
    session = Session(profile_name='Athena')
    client = session.client('athena')
    query = open(file).read()
    response = client.get_work_group(WorkGroup=workgroup)
    output_loc = response['WorkGroup']['Configuration']['ResultConfiguration']['OutputLocation']
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': db},
        ResultConfiguration={'OutputLocation': output_loc}
    )
    print(json.dumps(response, indent=2))


ddl_dir = os.getcwd() + '/queries/'
ddl_files = [ddl_dir + file for file in os.listdir(ddl_dir)]
db = 'test_db'
workgroup = 'athena_test'
for query in ddl_files:
    run_query(query, db, workgroup)
