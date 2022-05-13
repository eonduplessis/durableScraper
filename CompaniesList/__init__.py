# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging

#Return companies list
def main(name: str) -> list:
    companies_list = []

    with open('CompaniesList\companies_list.txt') as f:
        companies_list = f.read().splitlines()
    
    return companies_list #['01888425', '03633621', '09446231', '00041424', '02723534', '03196209','00617987', '03888792', '00023307', '03407696', '00102498']
