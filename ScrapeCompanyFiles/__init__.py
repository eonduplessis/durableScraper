# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib import request
import string






# sending request and parsing
base_url = 'https://find-and-update.company-information.service.gov.uk'

#website = requests.get('https://find-and-update.company-information.service.gov.uk/company/01888425/filing-history?page=1', verify=False).text

company_id = '01888425'
page_count = 5
last_document_date = datetime(2019,3,1)

file_list = []
file_count = 1 #Needs to go and be replaced by a file name


def generate_file_name(company_id, document_description, document_date):
    document_name = document_description
    document_name = document_name.translate(str.maketrans('', '', string.punctuation))
    document_name = document_name.replace("\n","").replace(" ","")
    return company_id + "_" + document_name + "_" + document_date.strftime('%d%m%Y') + ".pdf" 



def main(name: str):

    company_id = name

    for page_number in range(1,page_count + 1):
        website_url = 'https://find-and-update.company-information.service.gov.uk/company/%s/filing-history?page=%d'%(company_id, page_number)
        website = requests.get(website_url, verify=False).text
        soup = BeautifulSoup(website, 'html.parser')

        # extracting data
        headlines = soup.find_all('span', class_='class-example')
        data = [headline.text for headline in headlines]

        table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="fhTable")
        rows = soup.find_all("tr")

        for row in rows[1:]:
            valid_row = False

            columns = list(row.children)

            document_description_raw = columns[5]
            document_description = columns[5].text

            if 'full accounts' in document_description:
                valid_row = True
            elif 'roup of compa' in document_description:
                valid_row = True
            elif 'accounts for a' in document_description and '<strong>' in document_description_raw:
                valid_row = True
            elif 'accounts' in document_description and '<strong>' in document_description_raw:
                valid_row = True

            document_date = datetime.strptime(columns[1].text.strip(), '%d %b %Y') #Date

            if (valid_row) and document_date > last_document_date: #Check if file is newer than last file date
                    
                print(columns[7].find_all("a")) #Href
                remote_url = base_url + columns[7].find("a").get('href')
            
                local_file = generate_file_name(company_id, document_description, document_date)
                
                request.urlretrieve(remote_url, local_file)
                file_list.append(local_file)
