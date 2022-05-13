# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import string
from urllib import request
from azure.storage.blob import BlobClient
import json
import os


def generate_file_name(company_id, document_description, document_date):

    # write file to %HOME%\data

    document_name = document_description
    document_name = document_name.translate(str.maketrans('', '', string.punctuation))
    document_name = document_name.replace("\n","").replace(" ","")
    return company_id + "_" + document_name + "_" + document_date + ".pdf" 

def write_file_to_blob_store(file_path, file_name, blob_connection_string, blob_container_name):
 
    #blob = BlobClient.from_connection_string(conn_str="<connection_string>", container_name="my_container", blob_name="my_blob")
    blob = BlobClient.from_connection_string(conn_str=blob_connection_string, container_name=blob_container_name, blob_name=file_name)

    with open(file_path, "rb") as data:
        blob.upload_blob(data)

def main(filedetails) -> str:
    
    """
    file_details = {
                    "company_id" : company_id,
                    "document_date" : document_date,
                    "document_description" : document_description, 
                    "url" : remote_url
                }
    """

    for file in filedetails:

        file_details = json.loads(file)
        
        local_file = generate_file_name(file_details["company_id"], file_details["document_description"], file_details["document_date"])
                    
        request.urlretrieve(file_details["url"], local_file)
        
        write_file_to_blob_store(local_file, local_file, 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;', 'companies-house-files')

        os.remove(local_file)

    return ""
