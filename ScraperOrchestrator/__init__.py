# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json
from unittest.mock import NonCallableMock

import azure.functions as func
import azure.durable_functions as df


def orchestrator_function(context: df.DurableOrchestrationContext):
    work_batch = yield context.call_activity('CompaniesList', None)

    parallel_tasks = [ context.call_activity('ScrapeCompanyFiles', b) for b in work_batch ]
    
    outputs = yield context.task_all(parallel_tasks)

    #result3 = yield context.call_activity('CompaniesList', "London")

    #Get Company List
    #For each company in Company List, find files to download
    #For each file to download, download
    #For each downloaded file, OCR

    return ['', '']#[result1, result2, result3]

    #https://docs.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview?tabs=python#fan-in-out

main = df.Orchestrator.create(orchestrator_function)